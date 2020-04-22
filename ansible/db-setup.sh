#! /bin/bash

. ./openrc.sh; ansible-playbook -i inventory/hosts.ini db-setup.yaml