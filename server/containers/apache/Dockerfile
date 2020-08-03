FROM alpine:3

ARG HTTPD_BASE="/etc/httpd"

# 1) install packages.
# 2) make conf file comatibility with Amazon Linux 2
RUN set -ex; \
    apk add apache2 apache2-ssl apache2-http2; \
    \
    mkdir -p $HTTPD_BASE; \
    ln -s /usr/lib/apache2 ${HTTPD_BASE}/modules; \
    ln -s /var/log         ${HTTPD_BASE}/logs; \
    ln -s /run/apache2     ${HTTPD_BASE}/run; \
    ln -s /etc/apache2/mime.types /etc; \
    ln -s $HTTPD_BASE /etc/apache2

EXPOSE 80 443

COPY httpd-foreground /usr/local/sbin/
COPY etc $HTTPD_BASE

CMD ["httpd-foreground"]
