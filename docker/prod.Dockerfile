#################
# BookStore production Image
#################
FROM base

ENV DJANGO_SETTINGS_MODULE portal.settings.prod

COPY       . /var/app/bookstore

COPY       scripts/run_prod.sh /var/app/run_prod.sh
COPY       scripts/test_local_backend.sh /var/app/test_local_backend.sh
RUN        chmod +x run_prod.sh

EXPOSE     8001
CMD        ["/var/app/run_prod.sh"]