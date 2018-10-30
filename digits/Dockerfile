FROM introclass:base

ENV PROGRAM digits
WORKDIR /experiment
COPY tests/blackbox blackbox
COPY tests/whitebox whitebox
COPY tests/digits.c oracle.c
RUN gcov -o "${PROGRAM}" oracle.c
