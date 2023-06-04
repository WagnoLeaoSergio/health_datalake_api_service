FROM python:3.7-alpine
COPY . /app
WORKDIR /app
RUN pip install .
RUN health_datalake_api_service create-db
RUN health_datalake_api_service populate-db
RUN health_datalake_api_service add-user -u admin -p admin
EXPOSE 5000
CMD ["health_datalake_api_service", "run"]
