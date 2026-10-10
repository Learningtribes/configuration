# As env.json and auth.json config file are not stored in image, please mount them into container when using this image.
#
# docker run  --rm --mount type=bind,src=/edx/app/certs/env.json,dst=/edx/app/certs/env.json,readonly --mount type=bind,src=/edx/app/certs/auth.json,dst=/edx/app/certs/auth.json,readonly -d -t --name certificate certificate:test


FROM alpine/git:2.54.0 AS builder
ARG GITHUB_TOKEN
RUN git clone -b open-release/hawthorn.master https://oauth2:${GITHUB_TOKEN}@github.com/Learningtribes/edx-certificates.git /src
RUN rm -rf /src/.git




FROM python:2.7

RUN useradd -G www-data -m certificate
RUN mkdir -p /edx/app/certs /edx/app/certs/gnupg /edx/app/certs/certificates /edx/var/certs /edx/var/certs/www-data
COPY example-private-key.txt /edx/app/certs/example-private-key.txt
COPY trust.export /edx/app/certs/trust.export
RUN /usr/bin/gpg --homedir /edx/app/certs/gnupg --import /edx/app/certs/example-private-key.txt
RUN /usr/bin/gpg --homedir /edx/app/certs/gnupg --import-ownertrust /edx/app/certs/trust.export
COPY certificate-entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh
COPY --from=builder /src /edx/app/certs/certificates
RUN chown -R certificate:certificate /edx/app/certs /edx/var/certs 

USER certificate
ENV PATH="/home/certificate/.local/bin:$PATH"
ENV SERVICE_VARIANT="certs"
WORKDIR /edx/app/certs/certificates
RUN pip install -r requirements.txt
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]