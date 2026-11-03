FROM python:3.13

RUN useradd -u 50000 -g root -m airflow
RUN mkdir /opt/airflow
RUN chown -R airflow:root /opt/airflow
COPY entrypoint /entrypoint
RUN chmod +x /entrypoint
RUN apt-get update && apt-get install -y netcat-openbsd && rm -rf /var/lib/apt/lists/*


USER airflow
WORKDIR /opt/airflow
RUN pip install apache-airflow[celery]==3.3.2
RUN pip install apache-airflow-providers-postgres==7.0.2
ENV PATH="/home/airflow/.local/bin:$PATH"
ENTRYPOINT ["/entrypoint"]
