FROM ubuntu:16.04
RUN apt-get update \
 && apt-get install -y --no-install-recommends \
      gcc \
      libc6-dev \
      gcovr

WORKDIR /experiment
COPY . .
ARG PROGRAM
RUN gcc -o "${PROGRAM}" "${PROGRAM}.c"
