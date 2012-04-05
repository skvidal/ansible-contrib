Ansible Contrib Repo
====================

This repository contains user-contributed real world examples for ansible playbooks as well as modules that
are not a part of Ansible's core distribution.

This is designed to be a resource to folks learning Ansible, as well as a way to share useful resources
of all kinds.

If you have just found Ansible, you should start here:

   * [Documentation site](http://ansible.github.com)
   * [Core project](https://github.com/ansible/ansible) -- see the examples directory

Contrib Modules
===============

This repo contains non-core ansible modules.

Modules may not be included in ansible's core if they:

   * Target a specific software application rather than a basic Unix construct
   * Aren't particularly idempotent
   * Are written in a language other than Python
   * Have a fair number of non-standard library dependencies
   * Interact with proprietary software
   * Etc...

Being in contrib is not a reflection on the module's quality in any way.  Code
quality still matters and will be reviewed.

Contrib Playbook Examples
======================

Ansible has a number of playbook/syntax examples in the examples directory
of the main project, that are mostly about learning the language.

Examples here are more involved, and are about performing real world tasks.
They are derived from real playbooks written by Ansible users.

If you're just starting out, also consult the project's examples dir, but reading
these may help you apply lessons learned in context.

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

All playbook content is assumed to be Creative Commons 3.0 Attribution licensed. 
Non-commerical or No-derivatives CC extensions are not acceptable, to encourage
easy use by all users, regardless of purpose.

