FROM python:3.9.1

RUN pip install pandas

WORKDIR /app
COPY pipeline.py pipeline.py

ENTRYPOINT [ "python", "pipeline.py" ]

# services:
#     postgres:
#         image: postgres:13
#         environment:
#             POSTGRES USER: airflow
#             POSTGRES PASSWORD: airflow
#             POSTGRES DB: airflow
#         volumes:
#             - postgres-db-volume:/var/lib/postgresq1/data # for mapping folder in local with the folder in container 
#         healthcheck:
#             test: ["CMD", "pg_isready", "-U", "airflow"]
#             interval: 5s
#             retries: 5
#         restart: always

# docker run -it \
#   -e POSTGRES_USER="root" \
#   -e POSTGRES_PASSWORD="root" \
#   -e POSTGRES_DB="ny_taxi" \
#   -v $(pwd)/ny_taxi_postgres_data:/var/lib/postgresql/data \
#   -p 5432:5432 \
#   postgres:13





