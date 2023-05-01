FROM python:3.9

RUN mkdir /lido
RUN rm /bin/sh && ln -s /bin/bash /bin/sh
WORKDIR /lido

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
COPY . /lido
RUN pip install -r requirements.txt

ENV SNOWFLAKE_USER=nothing
ENV SNOWFLAKE_PASSWORD=nothing
ENV SNOWFLAKE_ACCOUNT=nothing
ENV SNOWFLAKE_WAREHOUSE=nothing
ENV SNOWFLAKE_DATABASE=nothing
ENV SNOWFLAKE_SCHEMA=nothing
ENV DJANGO_SECRET=mysecretkey
ENV DUNE_API_KEY=nothing
ENV TABLE_NAME=nothing
ENV STAGE_NAME=nothing
ENV DUNE_QUERY_ID=12345
ENV SMTP_PASSWORD=123ds
ENV SMTP_SENDER=a@b.com
ENV UPTIME_URL="https://uptime.teej.xyz/api/push/l5qfsgDouW?status=up&msg=OK&ping="

RUN apt-get update && apt install nano -y

CMD ["python", "dune_2_snowflake.py"]