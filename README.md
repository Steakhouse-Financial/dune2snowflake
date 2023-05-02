# dune2snowflake
![GitHub all releases](https://img.shields.io/github/downloads/Steakhouse-Financial/dune2snowflake/total?style=for-the-badge)![GitHub pull requests](https://img.shields.io/github/issues-pr/Steakhouse-Financial/dune2snowflake?style=for-the-badge)![GitHub forks](https://img.shields.io/github/forks/Steakhouse-Financial/dune2snowflake?style=for-the-badge)![GitHub Repo stars](https://img.shields.io/github/stars/Steakhouse-Financial/dune2snowflake?style=for-the-badge)![GitHub last commit](https://img.shields.io/github/last-commit/Steakhouse-Financial/dune2snowflake?style=for-the-badge)

## 🔧 How to Install

### 🐳 Docker
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