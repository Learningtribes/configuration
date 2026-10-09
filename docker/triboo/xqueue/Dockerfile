# When install MySQL-python library, the python:2.7 image get a issue. Temporarily modify the file to resolve the issue.
#
# As no syslogd in container, a issue raised by logging settings in the production environment. Temporarily modify the file to resolve the issue.
# Ensure dev_env is True in the get_logger_config() 



FROM alpine/git:2.54.0 AS builder
ARG GITHUB_TOKEN
RUN git clone -b open-release/hawthorn.master https://oauth2:${GITHUB_TOKEN}@github.com/Learningtribes/xqueue.git /src
RUN rm -rf /src/.git




FROM python:2.7

RUN useradd -m xqueue
RUN mkdir -p /edx/app/xqueue/xqueue /edx/etc /var/log/xqueue /edx/var/logs/xqueue
COPY xqueue_gunicorn.py /edx/app/xqueue/xqueue_gunicorn.py
COPY xqueue_env /edx/app/xqueue/xqueue_env 
COPY xqueue-entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh
COPY --from=builder /src /edx/app/xqueue/xqueue
RUN chown -R xqueue:xqueue /edx/app/xqueue/xqueue /edx/etc /var/log/xqueue /edx/var/logs/xqueue /edx/app/xqueue/xqueue_gunicorn.py /edx/app/xqueue/xqueue_env

USER xqueue
ENV PATH="/home/xqueue/.local/bin:$PATH"
WORKDIR /edx/app/xqueue/xqueue
RUN sed -i "s/mysql-python==1.2.5/mysqlclient==1.4.6/g" requirements.txt
RUN sed -i "s/LOGGING = get_logger_config(LOG_DIR,/LOGGING = get_logger_config(LOG_DIR, dev_env=True,/g" xqueue/production.py
RUN pip install -r requirements.txt
EXPOSE 8040
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]