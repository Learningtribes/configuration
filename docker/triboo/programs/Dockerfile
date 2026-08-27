# When install cryptography and mysqlclient library, the python:3.5 image get issues. Temporarily modify the file to resolve the issue.
#
# As catalogs application gone. Temporarily modify the file to resolve the issue.



FROM python:3.5 AS builder
ARG GITHUB_TOKEN
RUN git clone -b lt-master https://oauth2:${GITHUB_TOKEN}@github.com/Learningtribes/course-discovery.git /src
RUN rm -rf /src/.git




FROM python:3.5

RUN useradd -m discovery
RUN mkdir -p /edx/app/discovery/discovery /var/log/discovery /edx/etc /edx/var/discovery/media /edx/var/discovery/staticfiles
COPY discovery_env /edx/app/discovery/discovery_env
COPY discovery_gunicorn.py /edx/app/discovery/discovery_gunicorn.py
COPY discovery-entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh
COPY --from=builder /src /edx/app/discovery/discovery
RUN chown -R discovery:discovery /var/log/discovery /edx/etc /edx/app/discovery/discovery_env /edx/app/discovery/discovery /edx/app/discovery/discovery_gunicorn.py /edx/var/discovery/media /edx/var/discovery/staticfiles

USER discovery
ENV NVM_DIR="/home/discovery/.nvm"
RUN curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.1/install.sh | bash
RUN echo 'export NVM_DIR="$HOME/.nvm"' >> ~/.bashrc \
    && echo '[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"' >> ~/.bashrc
RUN . "$NVM_DIR/nvm.sh" \
    && nvm install 10.24.1
ENV PATH="/home/discovery/.local/bin:/home/discovery/.nvm/versions/node/v10.24.1/bin:$PATH"
WORKDIR /edx/app/discovery/discovery
RUN sed -i "s/cryptography==1.7.1/cryptography==3.2.1/g" requirements/base.txt
RUN sed -i "s/mysqlclient==1.3.9/mysqlclient==1.4.6/g" requirements/production.txt
RUN pip install -r requirements.txt
RUN npm install --production
RUN node_modules/.bin/bower install --allow-root --production
RUN sed -i "/'course_discovery.apps.catalogs',/d" course_discovery/settings/base.py
EXPOSE 8381
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]