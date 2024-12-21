FROM python:3.9-slim-bullseye
WORKDIR /usr/local/app

COPY hello_world ./hello_world
COPY the_ultimate_poc ./the_ultimate_poc
COPY manage.py ./manage.py
COPY requirements.txt ./requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]