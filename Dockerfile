FROM alpine:3

ENV HTTPD_BASE="/etc/httpd"

# install main packages
RUN set -ex; apk add apache2 apache2-ssl apache2-http2

# install suppliment packages
RUN set -ex; \
    apk add binutils file; \
    apk add perl; \
    apk add python3

# copy configuration files
COPY etc/httpd ${HTTPD_BASE}
RUN set -ex; \
    ln -s /usr/lib/apache2 ${HTTPD_BASE}/modules; \
    ln -s /var/log ${HTTPD_BASE}/logs; \
    ln -s /run/apache2 ${HTTPD_BASE}/run; \
    cp /etc/apache2/mime.types /etc; \
    ln -s ${HTTPD_BASE} /etc/apache2

# expose main port
EXPOSE 80 443

# expose test port
EXPOSE 8080 8443

# run httpd foregound
COPY bin/httpd-foreground /usr/local/sbin/
CMD ["httpd-foreground"]
