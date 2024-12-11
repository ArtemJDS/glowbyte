FROM python:3.10.16
EXPOSE 8085
WORKDIR /code
COPY . .
ENV SERVER_PORT="8080"
ENV MODEL_PORT="8081"
RUN pip install --no-cache-dir -r /code/requirements.txt
RUN pip install "uvicorn"
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8085"]

