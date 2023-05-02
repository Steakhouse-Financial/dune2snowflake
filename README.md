# dune2snowflake

## How to run via docker
```
docker run \
 --name dune2snow \
 --detach \
 -e SNOWFLAKE_USER= \
 -e SNOWFLAKE_PASSWORD= \
 -e SNOWFLAKE_ACCOUNT= \
 -e SNOWFLAKE_WAREHOUSE=XS \
 -e SNOWFLAKE_DATABASE= \
 -e SNOWFLAKE_SCHEMA= \
 -e DUNE_API_KEY= \
 -e TABLE_NAME= \
 -e STAGE_NAME= \
 -e DUNE_QUERY_ID= \
 -e SMTP_PASSWORD= \
 -e SMTP_SENDER="" \
 -e UPTIME_URL="" \
  bloodyburger/dune2snow:latest
  ```