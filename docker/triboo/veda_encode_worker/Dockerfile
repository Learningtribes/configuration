# When install v_videocompile command, the python:2.7 image get a issue about Linux distribution. Temporarily modify the file to resolve the issue.

FROM python:2.7 AS builder
ARG GITHUB_TOKEN
RUN git clone -b hawthorn https://oauth2:${GITHUB_TOKEN}@github.com/Learningtribes/edx-video-worker.git /src




FROM python:2.7

RUN useradd -m veda_encode_worker
RUN mkdir -p /edx/etc /edx/app/veda_encode_worker/veda_encode_worker /edx/var/veda_encode_worker/ENCODE_WORKDIR
COPY veda_encode_worker_env /edx/app/veda_encode_worker/veda_encode_worker_env
COPY veda_encode_worker-entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh
COPY --from=builder /src /edx/app/veda_encode_worker/veda_encode_worker
RUN chown -R veda_encode_worker:veda_encode_worker  /edx/etc /edx/app/veda_encode_worker/veda_encode_worker_env /edx/app/veda_encode_worker/veda_encode_worker /edx/var/veda_encode_worker
RUN git clone -b master https://oauth2:${GITHUB_TOKEN}@github.com/Learningtribes/v_videocompile.git /var/tmp/veda_ffmpeg
WORKDIR /var/tmp/veda_ffmpeg
RUN sed -i 's/deb.debian.org/archive.debian.org/g' /etc/apt/sources.list
RUN sed -i 's/security.debian.org/archive.debian.org/g' /etc/apt/sources.list
RUN sed -i "s/'Ubuntu'/'debian'/g" v_videocompile/__init__.py
RUN sed -i 's/libvpx3/libvpx5/g' v_videocompile/__init__.py
RUN apt-get update && apt-get install -y sudo libvpx5
RUN pip install -r REQUIREMENTS.txt
RUN python setup.py install
RUN v_videocompile

USER veda_encode_worker
ENV PATH="/home/veda_encode_worker/.local/bin:$PATH"
WORKDIR /edx/app/veda_encode_worker/veda_encode_worker
RUN pip install -r requirements.txt
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]