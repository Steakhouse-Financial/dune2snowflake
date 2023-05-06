# dune2snowflake
![GitHub all releases](https://img.shields.io/github/downloads/Steakhouse-Financial/dune2snowflake/total?style=for-the-badge)![GitHub pull requests](https://img.shields.io/github/issues-pr/Steakhouse-Financial/dune2snowflake?style=for-the-badge)![GitHub forks](https://img.shields.io/github/forks/Steakhouse-Financial/dune2snowflake?style=for-the-badge)![GitHub Repo stars](https://img.shields.io/github/stars/Steakhouse-Financial/dune2snowflake?style=for-the-badge)![GitHub last commit](https://img.shields.io/github/last-commit/Steakhouse-Financial/dune2snowflake?style=for-the-badge)

A Python script to load data from Dune query to Postgresql/Snowflake

### How to use

- Install docker and docker compose 
- Run the docker command below with variables updated

```other
  docker run \
  --name dune2snow \
  --network steakhouse \
  --detach \
  -e CONNECTION_STRING=postgresql://postgres:passwsord@postgres:5432/db \
  -e SCHEMA=<DB Schema> \
  -e DUNE_API_KEY=<API Key> \
  -e TABLE_NAME=<Table name to load the data> \
  -e DUNE_QUERY_ID=<Dune Query ID> \
  -e SMTP_PASSWORD=<SMTP Password to send notifications> \
  -e SMTP_SENDER="<sender email>" \
  -e UPTIME_URL="<Uptime-kuma URL>" \
   bloodyburger/dune2snow:latest
```

