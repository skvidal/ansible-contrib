This is a port of a script I wrote originally for func.


It lets you specify hosts to reboot - either altogether or
one-at-a-time. It checks for the host to return to functionality before
exiting. 

uses:
 - reboot-a-thon for outages for new kernels - where you want to do them
   all but not be tied down by watching them all.

 - rebooting a class of hosts that provide the same service so not all
   of them will be down at once (--one-at-a-time)


ans-host-reboot.py [options] host1 host2 host3 ...

