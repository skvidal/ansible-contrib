#!/usr/bin/python -tt
# by skvidal
# This is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with This.  If not, see <http://www.gnu.org/licenses/>.
# copyright 2012 Red Hat, Inc.

#take list of hosts
# connect to all and look at output of 'w -h -s -f'
# if any output - then notify users of which hosts have users on them
# wait for confirmation from user to reboot
# if confirmation run rebootcmd
# if --one-at-a-time
#    reboot first host
#    wait for host to return and be available via func
#    next
# reboot hosts
# wait and watch for hosts to return

  

import sys
import ansible
import ansible.runner
from ansible.utils import base_parser, err
import getpass
import time

usercmd = "/usr/bin/w -h -s -f"
rebootcmd = "/sbin/shutdown -r now"
get_uptime = "cut -d' ' -f1 /proc/uptime"
max_reboot_wait = 300 # how long to wait for a host to reboot

def confirm():
    ans = raw_input()
    if ans.lower() != 'yes':
        print "Aborting...."
        sys.exit(1)

def get_host_uptimes(results):
    uptimes = {}
    for hn, resdict in results['contacted'].items():
        if resdict['rc'] != 0:
            uptime = None
        else:
            uptime = float(resdict['stdout'])
        uptimes[hn] = uptime
    
    return uptimes

def reboot_and_check(client, hostspec):
    # create a client for the hostspec
    # send reboot to them
    # wait until all hosts are back up or time out occurs

    # reboot command
    client.pattern = ';'.join(hostspec)
    client.module_args = rebootcmd
    client.run()
    

    print 'Waiting max %ss for host(s) to reboot and come back.' % max_reboot_wait
    reboot_start = time.time()

    unreturned = set(client._match_hosts(client.pattern))
    
    # check for uptime from each
    # if any hosts passes the uptime check = mark it as finished in the dict
    # if time expires and not all are back up
    # return list of hostnames not back up yet.
    
    while unreturned and ((time.time() - reboot_start)  < max_reboot_wait):
        # now switch to the get_uptime command
        client.timeout=5
        client.module_args = get_uptime
        #only contact the unreturned hosts - no need to bug the returned ones again
        client.pattern = ';'.join(unreturned)
        tleft = int(max_reboot_wait - (time.time()-reboot_start))
        if tleft % 2 == 0:
            print 'Time Left: %s ' % tleft
        uptimes = get_host_uptimes(client.run())
        for host,utime in uptimes.items():
            if not utime:
                continue
            if utime <= (time.time() - reboot_start): 
                if host in unreturned:
                    print '%s is back!' % host
                    unreturned.remove(host)

        if unreturned:
            time.sleep(3)
    
    return unreturned

def main(args):
    parser = base_parser(runas_opts=True,
       usage = "ans-host-reboot [options] hostname-or-glob [..]")
       
    parser.add_option('--one-at-a-time', dest='oneatatime', default=False,
        action='store_true', 
        help="Reboot hosts one at a time waiting for each to return before doing the next one")

    opts, args = parser.parse_args(args)
    
    opts.sshpass = None
    if opts.ask_pass:
        opts.sshpass = getpass.getpass(prompt="SSH password: ")

    if len(args) < 1:
        err(parser.format_help())
        return 1

    # each arg is a host
    pattern = ';'.join(args)

    # setup our basic ansible client connection
    client = ansible.runner.Runner(
        module_path=opts.module_path,
        remote_user=opts.remote_user, remote_pass=opts.sshpass,
        host_list=opts.inventory, timeout=opts.timeout, 
        remote_port=opts.remote_port, forks=opts.forks, 
        pattern=pattern, sudo=opts.sudo, verbose=True,
        debug=opts.debug)


    client.module_name = 'shell'
    client.module_args = usercmd

    thesehosts = client._match_hosts(pattern)

    print 'checking for users on hosts:\n' 
    results = client.run()

    # for any hosts which are dark, take them out of the reboot list
    for (hn, resdict) in results['dark'].items():
        msg = '\nError: %s is unavailable, removing from reboot list\n' % hn
        thesehosts.remove(hn)
        print msg
        continue
        
    for (hn, resdict) in results['contacted'].items():
        if resdict['rc'] != 0:
            msg = 'Error: %s: ' % hn
            msg += resdict['stdout'] + resdict['stderr']
            err(msg)
            continue
        res = '%s %s\n' % (resdict['stdout'], resdict['stderr'])
        if res.strip() == '':
            continue
        print 'Users on %s' % hn
        print res

    # wait for confirmation from user
    print "Will be rebooting these hosts:"
    print '\n'.join(sorted(thesehosts))
    print 'Okay to proceed with reboots of guests? ("yes" to continue) ',
    confirm()
    
    # if we are setup to run one-at-a-time - then do the reboot-test cycle on each
    # host
    if opts.oneatatime:
        anyerrs=False
        for hn in thesehosts:
            print hn
            errs = reboot_and_check(client, [hn])
            if errs:
                anyerrs = True
                for h in errs:
                    err("Error rebooting %s" % h)
                print "Continue? (yes or anything else to exit)",
                confirm()

        if anyerrs:
            return 1
    else:
        errs = reboot_and_check(client,thesehosts)
        if errs:
            for h in errs:
                err("Host %s has not come back up." % h)
            return 1
    
    print "All hosts rebooted successfully and back up"
    return 0

    
if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv[1:]))
    except KeyboardInterrupt:
        print "\nExiting on User Cancel\n"
        sys.exit(1)
