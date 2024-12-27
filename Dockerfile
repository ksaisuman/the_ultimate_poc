FROM python:3.9-slim-bullseye
WORKDIR /usr/local/app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt
RUN apt update && apt install -y net-tools watch
RUN mkdir prom_multiproc_dir

ENV PROMETHEUS_MULTIPROC_DIR="/usr/local/app/prom_multiproc_dir"

EXPOSE 8000

CMD ["gunicorn", "--log-level",  "debug", "the_ultimate_poc.wsgi:application"]