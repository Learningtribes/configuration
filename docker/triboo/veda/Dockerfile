# When install MySQL-python library, the python:2.7 image get a issue. Temporarily modify the file to resolve the issue.
#
# As no syslogd in container, a issue raised by logging settings in the production environment. Temporarily modify the file to resolve the issue.
# Ensure dev_env is True in the get_logger_config() 



FROM python:2.7 AS builder
ARG GITHUB_TOKEN
RUN git clone -b hawthorn https://oauth2:${GITHUB_TOKEN}@github.com/Learningtribes/edx-video-pipeline.git /src




FROM python:2.7

RUN useradd -m veda
RUN mkdir -p /var/log/veda /edx/var/veda/staticfiles /edx/etc /edx/app/veda/veda /edx/var/veda/VEDA_WORKING
COPY veda_env /edx/app/veda/veda_env
COPY veda_gunicorn.py /edx/app/veda/veda_gunicorn.py
COPY veda-entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh
COPY --from=builder /src /edx/app/veda/veda
RUN chown -R veda:veda /var/log/veda /edx/etc /edx/app/veda/veda_env /edx/app/veda/veda /edx/app/veda/veda_gunicorn.py /edx/var/veda/staticfiles /edx/var/veda/VEDA_WORKING

USER veda
ENV NVM_DIR="/home/veda/.nvm"
RUN curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.1/install.sh | bash
RUN echo 'export NVM_DIR="$HOME/.nvm"' >> ~/.bashrc \
    && echo '[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"' >> ~/.bashrc
RUN . "$NVM_DIR/nvm.sh" \
    && nvm install 10.24.1
ENV PATH="/home/veda/.local/bin:/home/veda/.nvm/versions/node/v10.24.1/bin:$PATH"
WORKDIR /edx/app/veda/veda
RUN sed -i "s/MySQL-python==1.2.5/mysqlclient==1.4.6/g" requirements.txt
RUN sed -i "s/LOGGING = get_logger_config(service_variant=CONFIG_DATA.get('SERVICE_VARIANT_NAME', DEFATULT_SERVICE_VARIANT_NAME))/LOGGING = get_logger_config(dev_env=True, service_variant=CONFIG_DATA.get('SERVICE_VARIANT_NAME', DEFATULT_SERVICE_VARIANT_NAME))/g" VEDA/settings/production.py
RUN pip install -r requirements.txt
EXPOSE 8555
# As veda.yml config file is not stored in image, please mount it into container when using this image.
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
