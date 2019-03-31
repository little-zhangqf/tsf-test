FROM ccr.ccs.tencentyun.com/qcloud/centos

RUN mkdir -p /root/app/shopService

COPY shopService /root/app/shopService

ENTRYPOINT ["bash","/root/app/shopService/start.sh"]
