# CCC-A2 Team 22
## Team Members:
* [Xinglin Qiang - 1153086](https://github.com/qiangxinglin)
* [Shaohua Liu - 1150336](https://github.com/sliu15)
* [Wentao Hao - 1096215](https://github.com/Taylorrrr)
* [Kaixin Chen - 1103908](https://github.com/k229chen)
* [Yichao Xu - 1045184](https://github.com/FlashXu)

## Video links
* Ansible Deployment: https://www.youtube.com/watch?v=_uzXLX3cHwQ
* Frontend Presentation: https://www.youtube.com/watch?v=U7CeZP5M2pg

## PPT
xxx

## How to install
Clone this repository

```bash
cd ansible
./launch-instance.sh
./install-dependency.sh
./deploy-software.sh
```

Then access the webpage through http://172.26.132.92

Backend API can be accessed through http://172.26.132.92:5000


## Instance Arrangement

Instance1: 172.26.131.114
    
    CouchDB/ couchdb:latest
    Harvester/


Instance2: 172.26.130.201
    
    CouchDB/ couchdb:latest
    Harvester/


Instance3: 172.26.133.133
    
    CouchDB/ couchdb:latest
    Harvester/


Instance4: 172.26.132.92

    Frontend/ node:lts-alpine & nginx:stable-alpine
    Backend/ python:3.7-alpine & redis:latest
    Stream_Harvester/
    User_Expansion/
    SA_Classifier/ python:3.7-slim
