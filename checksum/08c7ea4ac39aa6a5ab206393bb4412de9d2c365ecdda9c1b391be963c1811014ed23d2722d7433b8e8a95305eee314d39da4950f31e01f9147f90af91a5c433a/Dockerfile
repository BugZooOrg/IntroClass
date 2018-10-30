FROM ubuntu:16.04
RUN apt-get update \
 && apt-get install -y --no-install-recommends \
      gcc \
      gcovr

WORKDIR /experiment
COPY . .
ARG PROGRAM
# RUN gcc -o "${PROGRAM}" "${PROGRAM}.c"
