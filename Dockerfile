FROM ubuntu:latest
LABEL authors="zhantemir"

ENTRYPOINT ["top", "-b"]