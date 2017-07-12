FROM python:2.7

COPY . /app
WORKDIR /app

RUN pip install -r requeriments.txt
EXPOSE 8000
CMD ["./entrypoint.sh"]