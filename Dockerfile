FROM python
MAINTAINER Alex Standke "xanderstrike@gmail.com"
VOLUME ["/torrents", "/app/config"]
COPY requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt
COPY . /app
WORKDIR /app
ENTRYPOINT ["python"]
CMD ["GazelleUI.py"]
