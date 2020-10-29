#################
# BookStore development Image
#################
FROM base

ENV DJANGO_SETTINGS_MODULE bookstore.settings.dev

COPY       . /var/app/bookstore
COPY       scripts/run_local.sh /var/app/run_local.sh
COPY       scripts/test_local_backend.sh /var/app/test_local_backend.sh

RUN        chmod +x run_local.sh && chmod +x test_local_backend.sh
EXPOSE     8001
CMD        ["/var/app/run_local.sh"]