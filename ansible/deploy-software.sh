#! /bin/bash

if [[ $# -gt 0 ]]; then
    frp=-$1
fi

ansible-playbook -i inventory/hosts$frp.ini deploy-software.yaml
