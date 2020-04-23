#! /bin/bash

if [[ $# -gt 0 ]]; then
    frp=-$1
fi

. ./openrc.sh; ansible-playbook -i inventory/hosts$frp.ini install-dependency.yaml
