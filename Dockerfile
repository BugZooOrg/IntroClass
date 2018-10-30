# FIXME switch to Alpine
FROM ubuntu:16.04
RUN apt-get update \
 && apt-get install -y --no-install-recommends \
      gcc \
      libc6-dev \
      gcovr \
      python3 \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

# install genprog test harness
COPY bin/genprog_tests.py /usr/bin/gpth
RUN chmod +x /usr/bin/gpth

WORKDIR /experiment

# build an oracle for the program
ARG PROGRAM
COPY "${PROGRAM}/tests/whitebox" whitebox
COPY "${PROGRAM}/tests/blackbox" blackbox
COPY "${PROGRAM}/tests/${PROGRAM}.c" oracle.c
RUN gcc -o oracle oracle.c

# build the subject program
ARG REPO
ARG VERSION
COPY "${PROGRAM}/${REPO}/${VERSION}/${PROGRAM}.c" "${PROGRAM}.c"
RUN gcc -o "${PROGRAM}" "${PROGRAM}.c"

# build the test harness
COPY "${PROGRAM}/${REPO}/${VERSION}/blackbox_test.sh" blackbox_test.sh
COPY "${PROGRAM}/${REPO}/${VERSION}/whitebox_test.sh" whitebox_test.sh
RUN sed -i "s#\$DIR/../../../bin/genprog_tests.py#gpth#g" blackbox_test.sh \
 && sed -i "s#\$DIR/../../../bin/genprog_tests.py#gpth#g" whitebox_test.sh \
 && sed -i "s#\$DIR/../../tests/blackbox#\$DIR/blackbox#g" blackbox_test.sh \
 && sed -i "s#\$DIR/../../tests/whitebox#\$DIR/whitebox#g" whitebox_test.sh \
 && sed -i "s#\$1#\$DIR/${PROGRAM}#g" blackbox_test.sh \
 && sed -i "s#\$1#\$DIR/${PROGRAM}#g" whitebox_test.sh \
 && sed -i "s#\$2#\$1#g" blackbox_test.sh \
 && sed -i "s#\$2#\$1#g" whitebox_test.sh \
 && chmod +x blackbox_test.sh whitebox_test.sh
