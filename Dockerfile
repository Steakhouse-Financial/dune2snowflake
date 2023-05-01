FROM python:3.9

RUN mkdir /lido
RUN rm /bin/sh && ln -s /bin/bash /bin/sh
RUN apt-get update && apt install nano bash dos2unix vim cron -y
WORKDIR /lido

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
COPY . /lido
RUN pip install -r requirements.txt && pip install colorama

# Copy files
COPY jobs/*.* ./jobs/
COPY crontab.* ./
COPY start.sh .

# Fix line endings && execute permissions
RUN dos2unix crontab.* *.sh jobs/*.* \
    && \
    find . -type f -iname "*.sh" -exec chmod +x {} \; \
    && \
    find . -type f -iname "*.py" -exec chmod +x {} \;

# create cron.log file
RUN touch /var/log/cron.log

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



# Run cron on container startup
CMD ["./start.sh"]