# Get error during install codecov library, as the library is for testing, simple to delete it from Gemfile
#
# As the env file saves sensitive data, delete them, then mount the sensitive env file when running the container
#
# docker run  --rm --mount type=bind,src=/root/dockerization/forum/forum_sensitive_env,dst=/edx/app/forum/forum_sensitive_env,readonly -d -t --name forum forum:test

FROM alpine/git:2.54.0 AS builder
ARG GITHUB_TOKEN
RUN git clone --revision=90240509a681575b47f270a0710eda61732d6833 --depth=1 https://oauth2:${GITHUB_TOKEN}@github.com/edx/cs_comments_service.git /src
RUN rm -rf /src/.git




FROM ruby:2.4.1

RUN useradd -G www-data -m forum
RUN mkdir -p /edx/app/forum /edx/var/forum /edx/app/forum/cs_comments_service
COPY forum_env /edx/app/forum/forum_env
COPY forum-entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh
COPY --from=builder /src /edx/app/forum/cs_comments_service
RUN chown -R forum:forum /edx/app/forum /edx/var/forum 

USER forum
WORKDIR /edx/app/forum/cs_comments_service
RUN sed -i -r "s/^(.*)codecov(.*)$//g" Gemfile
RUN sed -i -r "s/^(.*)codecov$//g" Gemfile.lock
RUN bundle install
EXPOSE 4567
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]