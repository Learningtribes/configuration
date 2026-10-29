# When install MySQL-python library, the python:2.7 image get a issue. Temporarily modify the file to resolve the issue.
#
# As no syslogd in container, SysLogHandler(/dev/log) fails at LMS startup with:
#   ValueError: Unable to configure handler 'local': [Errno 2] No such file or directory
# Patch get_logger_config() to use RotatingFileHandler under LOG_DIR instead.
# (Passing dev_env=True no longer works — platform removed that argument.)
#
# As install mysql-python==1.2.5 failed, app fails at startup with:
#   ImportError: No module named _mysql
# Patch MySQLdb._mysql as default _mysql under manage.py file
#
# asset.py files do not merged. Temporarily add the files to resolve the compile theme issue.
#
# As lms.env.json / lms.auth.json are not stored in image, please mount them into
# container when using this image.
#
# docker run --rm -d -t --mount type=bind,src=/edx/app/edxapp/lms.env.json,dst=/edx/app/edxapp/lms.env.json,readonly --mount type=bind,src=/edx/app/edxapp/lms.auth.json,dst=/edx/app/edxapp/lms.auth.json,readonly --name lms lms:test


FROM alpine/git:2.54.0 AS builder
ARG GITHUB_TOKEN
RUN git clone -b master https://oauth2:${GITHUB_TOKEN}@github.com/Learningtribes/platform.git /platform
RUN rm -rf /platform/.git
RUN git clone -b hawthorn https://oauth2:${GITHUB_TOKEN}@github.com/Learningtribes/triboo-theme.git /theme
RUN rm -rf /theme/.git




FROM python:2.7

RUN useradd -G www-data -m lms
RUN sed -i "s/http/https/g" /etc/apt/sources.list && sed -i "s/deb.debian/archive.debian/g" /etc/apt/sources.list && sed -i "s/security.debian/archive.debian/g" /etc/apt/sources.list
RUN apt-get update && apt-get install -y build-essential default-libmysqlclient-dev gfortran graphviz graphviz-dev liblapack-dev libxml2-dev libgeos-dev libxslt1-dev gettext libjpeg62-turbo libpng-dev libxmlsec1-dev libsasl2-dev libldap2-dev libssl-dev xmlsec1 swig && rm -rf /var/lib/apt/lists/*
RUN pip install pip==20.3.4
RUN mkdir -p /var/log/lms /edx/app/edxapp /edx/app/edxapp/themes /edx/var/edxapp/staticfiles /edx/var/edxapp/data /edx/var/log/edx/lms /edx/var/log/tracking
COPY lms_env /edx/app/edxapp/lms_env
COPY lms_gunicorn.py /edx/app/edxapp/lms_gunicorn.py
COPY lms-entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh
COPY --from=builder /platform /edx/app/edxapp/edx-platform
COPY --from=builder /theme /edx/app/edxapp/themes/hawthorn
COPY patch_logsettings.py /tmp/patch_logsettings.py
COPY patch_mysqlclient_manage.sh /tmp/patch_mysqlclient_manage.sh
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
RUN sed -i "s/mysql-python==1.2.5/mysqlclient==1.4.6/g" requirements/edx/base.txt
RUN python /tmp/patch_logsettings.py
RUN bash /tmp/patch_mysqlclient_manage.sh
RUN pip install -r requirements/edx/base.txt
RUN pip install -r requirements/edx/third-party.txt
RUN pip install -e git+https://github.com/oppia/xblock.git@9f6b95b7eb7dbabb96b77198a3202604f96adf65#egg=oppia-xblock \
    -e git+https://github.com/OfficeDev/xblock-officemix.git@3f876b5f0267b017812620239533a29c7d562d24#egg=officemix \
    -e git+https://github.com/schoolyourself/schoolyourself-xblock.git@5e4d37716e3e72640e832e961f7cc0d38d4ec47b#egg=schoolyourself-xblock \
    -e git+https://github.com/edx/ConceptXBlock.git@2376fde9ebdd83684b78dde77ef96361c3bd1aa0#egg=concept-xblock \
    -e git+https://github.com/edx/AudioXBlock.git@1fbf19cc21613aead62799469e1593adb037fdd9#egg=audio-xblock \
    -e git+https://github.com/edx/AnimationXBlock.git@d2b551bb8f49a138088e10298576102164145b87#egg=animation-xblock \
    -e git+https://github.com/open-craft/xblock-vectordraw.git@c57df9d98119fd2ca4cb31b9d16c27333cdc65ca#egg=xblock-vectordraw==0.2.1 \
    -e git+https://github.com/open-craft/xblock-activetable.git@e933d41bb86a8d50fb878787ca680165a092a6d5#egg=xblock-activetable
RUN pip install xblock-problem-builder==3.1.3 ubcpi-xblock==0.6.4 pyOpenSSL==19.1.0 cffi==1.11.5 cryptography==2.2.2 raven==6.8.0 beautifulsoup4==4.6.0 fs==2.4.16 django-cookies-samesite==0.9.0
RUN npm install
RUN python -m compileall -q -x '.claude/.*|node_modules/.*' /edx/app/edxapp/edx-platform
RUN python scripts/trans.py --all --settings=asset
RUN paver update_assets lms --settings=asset
EXPOSE 8000
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
