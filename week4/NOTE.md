# Docker

# Table of content

0. [Install DBT locally](#intro-to-docker)


# Install DBT locally
## step: 
- create docker compose
### compose.yml
~~~ 
version: '3'
services:
  dbt-bq: #name of the service
    build:
      context: . #which docker file to use
      target: dbt-bigquery #which plugin to install in addition to dbt-core
    image: dbt/bigquery
    environment:
      - GOOGLE_APPLICATION_CREDENTIALS=/.google/credentials/google_credentials.json
    volumes:
      - .:/usr/app #persisting dbt data
      - ~/.dbt:/root/.dbt #location of profiles.yml
      - ~/.google/credentials/google_credentials.json:/.google/credentials/google_credentials.json
~~~ 
- target: target ที่เราจะใช้ ดูได้ใน Dockerfile ของ dbt มีหลาย services ของ dbt เราจะใช้ plugin bigq เราก็ใส่เป็น dbt-bigquery แล้วรันออกมาเปน image dbt/bigquery
- volumes: เราจะใช้อะไรใน local ก็ map ไปให้หมด 
- credential: create key จาก service account with access: roles/bigquery.dataEditor, roles/bigquery.jobUser in IAM
- run
~~~ 
docker compose build
~~~ 

~~~ 
docker compose run --workdir="//usr/app/dbt/taxi_ride_ny" dbt-bq init
~~~ 
- จะมี config ของ gcp มาให้ใส่ พวก project, dataset, region etc.
- key file ใส่เปน {{ env_var('GOOGLE_APPLICATION_CREDENTIALS') }}
- dbt จะ gen พวก file ต่างๆมาให้เรา จะมี .dbt, .google มาให้ใน C:\Users\poon มี Dockerfile, profiles.yml, taxi_ride_ny(ชื่อโปรเจคเราตั้งเอง) etc.
- เราสามารถแก้ config docker compose ใหม่ได้เรื่อยๆ โดยดู service ที่จะใช้ใน Dockerfile ของ dbt แล้วลองรันดู ใส่ entry point=bash เพื่อเช็ก path ใน container ก็ได้ buildจริงค่อยเอาออก 

### profiles.yml
~~~ 
taxi_ride_ny:
  outputs:
    dev:
      dataset: stg_poon
      fixed_retries: 1
      keyfile: "{{ env_var('GOOGLE_APPLICATION_CREDENTIALS') }}"
      location: asia-southeast1
      method: service-account
      priority: interactive
      project: de-zoomcamp-376514
      threads: 4
      timeout_seconds: 300
      type: bigquery
    prod:
      dataset: prod_poon
      fixed_retries: 1
      keyfile: "{{ env_var('GOOGLE_APPLICATION_CREDENTIALS') }}"
      location: asia-southeast1
      method: service-account
      priority: interactive
      project: de-zoomcamp-376514
      threads: 4
      timeout_seconds: 300
      type: bigquery
  target: dev
~~~ 
- ตอนแรก dbt gen มาให้แค่ dev (dataset stg_poon มาจากตอนเราใส่ config gcp ตอน dbt init) เราก็เพิ่ม prod เข้าไปได้ เพื่อแยก dev & production แล้วก็ใส่ config ของ prod เข้าไป

- run debug เพื่อ test connection (entry point ใน Dockerfile ของ dbt จะเป็น dbt อยู่แล้ว เราสามารถรัน command dbt ได้เลย)
~~~ 
docker compose run --workdir="//usr/app/dbt/taxi_ride_ny" dbt-bq debug
~~~ 

- run 
~~~ 
docker compose run --workdir="//usr/app/dbt/taxi_ride_ny" dbt-bq run
~~~ 






