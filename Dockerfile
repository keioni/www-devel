FROM alpine:3

ENV HTDOCS="/var/www/_default"

# install main packages
RUN set -ex; apk add apache2 apache2-ssl apache2-http2

# install suppliment packages
RUN set -ex; \
    apk add binutils file; \
    apk add perl; \
    apk add python3

# copy configuration files
COPY etc/httpd /etc/httpd
RUN set -ex; \
    ln -s /usr/lib/apache2 /etc/httpd/modules; \
    ln -s /var/log /etc/httpd/logs; \
    ln -s /run/apache2 /etc/httpd/run; \
    cp /etc/apache2/mime.types /etc; \
    ln -s /etc/httpd /etc/apache2

# make htdocs volume share point
# add "-v local_htdocs_dir:${HTDOCS}" in arguments when run container
RUN mkdir -p ${HTDOCS}

# expose main port
EXPOSE 80 443

# expose test port
EXPOSE 8080 8443

# run httpd foregound
COPY bin/httpd-foreground /usr/local/sbin/
CMD ["httpd-foreground"]
