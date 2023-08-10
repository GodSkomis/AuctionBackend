from python:slim-bullseye

RUN pip install --upgrade pip
COPY . .
RUN pip install -r reqs.txt

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000", "--noreload"]