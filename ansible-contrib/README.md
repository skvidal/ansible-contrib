Ansible Contrib Repo
====================

This repository contains user-contributed real world examples for ansible playbooks as well as modules that
are not a part of Ansible's core distribution that other users may like to use.  

   * Core project: https://github.com/ansible/ansible
   * Documentation site: http://ansible.github.com

Contrib Modules
===============

Modules may not be included in ansible's core if they:

   * Target a specific software application rather than a basic Unix construct
   * Aren't particularly idempotent
   * Are written in a language other than Python
   * Interact with proprietary software
   * Etc...

Being in contrib is not a reflection on the module's quality in any way.  Code
quality still matters and will be reviewed.

More Playbook Examples
======================

Ansible has a number of playbook/syntax examples in the examples directory
of the main project.  If you're just starting out, also consult these
as they contain various comments about syntax and language features.

How to Contribute
=================

Contributions to this project are very welcome.

Follow the existing structure and include a README.md explaining
their usage and how to get in touch with yourself.

Send a github pull request to add or update content.

Modules that don't follow Ansible best practices may be requested to be upgraded prior
to inclusion, so that new users can learn from reading other modules how to do things.

Licensing
=========

Example modules should be licensed GPLv3 per the rest of Ansible, to encourage modules
to graduate from contrib to core.

Playbook example content and templates, etc, should be full copyleft or
BSD/MIT licensed, up the discretion of the author.


