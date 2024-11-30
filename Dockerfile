# docker build -t postgres-init . && docker run -p 5432:5432 postgres-init
FROM postgres:latest

# ENV POSTGRES_USER=dbuser
ENV POSTGRES_PASSWORD=password
#ENV POSTGRES_DB=db

#ENV POSTGRES_HOST_AUTH_METHOD=trust

# This file will be executed during the initialization of the PostgreSQL database
COPY init.sql /docker-entrypoint-initdb.d/

# Expose PostgreSQL port
EXPOSE 5432
