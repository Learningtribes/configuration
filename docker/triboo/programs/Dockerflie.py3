# As discovery.yml and discovery.auth.json config file are not stored in image, please mount them into container when using this image.
#
# docker run  --rm --mount type=bind,src=/edx/etc/discovery.yml,dst=/edx/etc/discovery.yml,readonly --mount type=bind,src=/edx/app/discovery/discovery/discovery.auth.json,dst=/edx/app/discovery/discovery/discovery.auth.json,readonly -d -t --name discovery discovery:test



FROM alpine/git:2.54.0 AS builder
ARG GITHUB_TOKEN
RUN git clone -b py3-master https://oauth2:${GITHUB_TOKEN}@github.com/Learningtribes/course-discovery.git /src
RUN rm -rf /src/.git




FROM python:3.13

RUN useradd -G www-data -m discovery
RUN mkdir -p /edx/app/discovery/discovery /var/log/discovery /edx/etc /edx/var/discovery/media /edx/var/discovery/staticfiles
COPY discovery_env.py3 /edx/app/discovery/discovery_env
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
    && nvm install 16.20.2
ENV PATH="/home/discovery/.local/bin:/home/discovery/.nvm/versions/node/v16.20.2/bin:$PATH"
WORKDIR /edx/app/discovery/discovery
RUN sed -i "s|file:///workspace/|file:./|g" requirements/py313/production.txt
RUN pip install -r requirements/py313/production.txt
RUN npm install --production
EXPOSE 8381
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]