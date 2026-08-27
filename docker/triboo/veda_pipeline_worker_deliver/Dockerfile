# When install MySQL-python library, the python:2.7 image get a issue. Temporarily modify the file to resolve the issue.
#
# As no syslogd in container, a issue raised by logging settings in the production environment. Temporarily modify the file to resolve the issue.
# Ensure dev_env is True in the get_logger_config()




FROM python:2.7 AS builder
ARG GITHUB_TOKEN
RUN git clone -b hawthorn https://oauth2:${GITHUB_TOKEN}@github.com/Learningtribes/edx-video-pipeline.git /src
RUN rm -rf /src/.git




FROM python:2.7

RUN useradd -m veda_pipeline_worker_deliver
RUN mkdir -p /edx/etc /edx/app/veda_pipeline_worker/veda_pipeline_worker /edx/var/veda_pipeline_worker/DELIVER_WORK_DIR
COPY veda_pipeline_worker_env /edx/app/veda_pipeline_worker/veda_pipeline_worker_env
COPY veda_pipeline_worker_deliver-entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh
COPY --from=builder /src /edx/app/veda_pipeline_worker/veda_pipeline_worker
RUN chown -R veda_pipeline_worker_deliver:veda_pipeline_worker_deliver /edx/etc /edx/app/veda_pipeline_worker/veda_pipeline_worker_env /edx/app/veda_pipeline_worker/veda_pipeline_worker /edx/var/veda_pipeline_worker

USER veda_pipeline_worker_deliver
ENV PATH="/home/veda_pipeline_worker_deliver/.local/bin:$PATH"
WORKDIR /edx/app/veda_pipeline_worker/veda_pipeline_worker
RUN sed -i "s/MySQL-python==1.2.5/mysqlclient==1.4.6/g" requirements.txt
RUN sed -i "s/LOGGING = get_logger_config(service_variant=CONFIG_DATA.get('SERVICE_VARIANT_NAME', DEFATULT_SERVICE_VARIANT_NAME))/LOGGING = get_logger_config(dev_env=True, service_variant=CONFIG_DATA.get('SERVICE_VARIANT_NAME', DEFATULT_SERVICE_VARIANT_NAME))/g" VEDA/settings/production.py
RUN pip install -r requirements.txt
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
