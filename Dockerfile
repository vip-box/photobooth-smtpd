
FROM ubuntu:22.04

LABEL org.label-schema.url="https://github.com/runlevel/vipbox-smtp" \
    org.label-schema.summary="vipbox smtp image" \
    org.label-schema.vendor="Romain Gaillegue <romain@runlevel.fr>"

ENV DEBIAN_FRONTEND noninteractive

# Update
RUN apt-get update \
    && apt-get -y install supervisor postfix sasl2-bin opendkim opendkim-tools \
    && apt-get clean

# Add files
ADD assets/filter.py /etc/postfix/filter.py 
ADD assets/install.sh /opt/install.sh

EXPOSE 25/tcp
CMD /opt/install.sh; /usr/bin/supervisord -c /etc/supervisor/supervisord.conf
