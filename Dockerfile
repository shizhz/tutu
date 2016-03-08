FROM python:2.7.11

MAINTAINER Shizhz <messi.shizz@gmail.com>

RUN mkdir /opt/tutu/
ADD tutu.tar.gz /opt/tutu/

# Please prepare the id_rsa.pub and put it under directory config/
ADD config/id_rsa.pub /opt/tutu/config/
RUN pip install -r /opt/tutu/requirements.txt \
    && chmod a+x /opt/tutu/entrypoint.sh

WORKDIR /opt/tutu
EXPOSE 8888

ENTRYPOINT ["/opt/tutu/entrypoint.sh"]


