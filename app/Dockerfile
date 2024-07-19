FROM python
COPY ./app/requirements.txt /root/github.com/loicbourgois/downtowhat/app/requirements.txt
RUN python -m pip install -r /root/github.com/loicbourgois/downtowhat/app/requirements.txt
COPY ./app /root/github.com/loicbourgois/downtowhat/app
COPY ./utils /root/github.com/loicbourgois/downtowhat/utils
CMD ["/root/github.com/loicbourgois/downtowhat/app/main.sh"]
