FROM python
COPY ./requirements.txt ./requirements.txt
RUN --mount=type=cache,target=/root/.cache/pip python -m pip install -r requirements.txt
CMD ["/root/github.com/loicbourgois/downtowhat/generator/main.sh"]
