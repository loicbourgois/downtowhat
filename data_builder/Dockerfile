# syntax = docker/dockerfile:experimental
FROM python:3.10
COPY requirements.txt ./requirements.txt
RUN --mount=type=cache,target=/root/.cache/pip python -m pip install -r ./requirements.txt
