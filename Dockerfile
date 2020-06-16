FROM alpine:3

ENV HTDOCS="/var/www/devel.keys.jp"

# install main packages
RUN set -ex; apk add apache2 apache2-ssl apache2-http2

# install suppliment packages
RUN set -ex; \
    apk add binutils file; \
    apk add perl; \
    apk add python3; \
    ;

# copy configuration files
COPY etc/httpd/conf/httpd.conf /etc/apache2
COPY etc/httpd/conf/conf.d /etc/apache2

# make htdocs volume share point
# add "-v local_htdocs_dir:${HTDOCS}" in arguments when run container
RUN mkdir -p ${HTDOCS}

# expose main port
EXPOSE 80 443

# expose test port
EXPOSE 8080 8443

# run httpd foregound
COPY bin/httpd-foreground /usr/local/sbin
RUN chmod u+x /usr/local/sbin/httpd-foreground
CMD ["/usr/local/sbin/httpd-foreground"]
