#! /bin/bash

. ./openrc.sh; ansible-playbook -i inventory/hosts.ini install_dependency.yaml