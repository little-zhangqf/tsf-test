#! /bin/bash

mkdir -p /opt/tsf/app_config/apis 
cp /root/app/shopService/spec.* /opt/tsf/app_config/
cp -r /root/app/shopService/apis /opt/tsf/app_config/
cd /root/app/shopService/
python ./shopService.py 80 1>./logs/shop.log 2>&1
