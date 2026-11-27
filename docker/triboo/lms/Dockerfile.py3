# As no syslogd in container, SysLogHandler(/dev/log) fails at LMS startup with:
#   ValueError: Unable to configure handler 'local': [Errno 2] No such file or directory
# Patch get_logger_config() to use RotatingFileHandler under LOG_DIR instead.
# (Passing dev_env=True no longer works — platform removed that argument.)
#
# asset.py files do not merged. Temporarily add the files to resolve the compile theme issue.
#
# create /edx/var/log/lms/ilt_xblock.log file to resolve the scripts/trans.py warning log.
#
# As lms.env.json / lms.auth.json are not stored in image, please mount them into
# container when using this image.
#
# use slim docker image, but size still big. Pending to improve it after validate docker image 


FROM alpine/git:2.54.0 AS builder
ARG GITHUB_TOKEN
RUN git clone -b py3-master https://oauth2:${GITHUB_TOKEN}@github.com/Learningtribes/platform.git /platform
RUN rm -rf /platform/.git
RUN git clone -b py3-master https://oauth2:${GITHUB_TOKEN}@github.com/Learningtribes/triboo-theme.git /theme
RUN rm -rf /theme/.git



#FROM python:3.13
FROM python:3.13-slim

RUN useradd -G www-data -m lms
#RUN apt-get update && apt-get install -y libsasl2-dev libldap2-dev libssl-dev gettext libxml2-dev libxmlsec1-dev libxslt1-dev libxmlsec1t64-openssl xmlsec1 libglib2.0-0t64 libx11-6 libxext6 libxrender1 graphviz && rm -rf /var/lib/apt/lists/*
RUN apt-get update && apt-get install -y --no-install-recommends git libsasl2-dev libldap2-dev libssl-dev gettext libxml2-dev libxmlsec1-dev libxslt1-dev libxmlsec1t64-openssl xmlsec1 pkg-config default-libmysqlclient-dev curl build-essential libglib2.0-0t64 libx11-6 libxext6 libxrender1 graphviz && rm -rf /var/lib/apt/lists/*
RUN mkdir -p /var/log/lms /edx/app/edxapp /edx/app/edxapp/themes /edx/var/edxapp/staticfiles /edx/var/edxapp/data /edx/var/log/edx/lms /edx/var/log/tracking
COPY lms_env /edx/app/edxapp/lms_env
COPY lms_gunicorn.py /edx/app/edxapp/lms_gunicorn.py
COPY lms-entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh
COPY --from=builder /platform /edx/app/edxapp/edx-platform
COPY --from=builder /theme /edx/app/edxapp/themes/hawthorn
COPY patch_logsettings.py3 /tmp/patch_logsettings.py
COPY requirements.py3 /edx/app/edxapp/edx-platform/requirements.txt
COPY lms_asset.py /edx/app/edxapp/edx-platform/lms/envs/asset.py
COPY cms_asset.py /edx/app/edxapp/edx-platform/cms/envs/asset.py
RUN chown -R lms:lms /var/log/lms /edx/app/edxapp /edx/var/edxapp /edx/var/log


USER lms
ENV NVM_DIR="/home/lms/.nvm"
RUN curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.1/install.sh | bash
RUN echo 'export NVM_DIR="$HOME/.nvm"' >> ~/.bashrc \
    && echo '[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"' >> ~/.bashrc
RUN . "$NVM_DIR/nvm.sh" \
    && nvm install 16.20.2
ENV PATH="/home/lms/.local/bin:/home/lms/.nvm/versions/node/v16.20.2/bin:/edx/app/edxapp/edx-platform/node_modules/.bin:$PATH"
ENV LANG="en_US.UTF-8"
ENV SKIP_WS_MIGRATIONS="1"
ENV NO_PREREQ_INSTALL="1"
ENV EDX_PLATFORM_SETTINGS="aws"
ENV CONFIG_ROOT="/edx/app/edxapp"
ENV PYTHONPATH="/edx/app/edxapp/edx-platform"
ENV COMPREHENSIVE_THEME_DIRS='["/edx/app/edxapp/themes"]'
ENV DEFAULT_SITE_THEME="hawthorn"
ENV STATIC_ROOT_BASE="/edx/var/edxapp/staticfiles"
WORKDIR /edx/app/edxapp/edx-platform
RUN python /tmp/patch_logsettings.py
RUN pip install --no-cache-dir -r requirements.txt
RUN npm install
RUN mkdir /edx/var/log/lms
RUN touch /edx/var/log/lms/ilt_xblock.log
RUN python scripts/trans.py --all --settings=asset
RUN paver update_assets lms --settings=asset
EXPOSE 8000
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]