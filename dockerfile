FROM python:3.9.13-slim
ENV PYTHONUNBUFFERED 1
WORKDIR /app
RUN apt update &&\
    apt install -y netcat
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt
COPY . /app
EXPOSE 8000
RUN chmod u+x entrypoint.sh
CMD ["sh", "entrypoint.sh"]