FROM python:3.12-alpine3.19
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
WORKDIR /code

COPY requirements.txt /code/
RUN pip install --upgrade pip setuptools
RUN pip install -r requirements.txt
COPY . /code/
CMD ["python", "main.py"]