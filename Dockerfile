FROM ubuntu:latest
MAINTAINER Alex Standke "xanderstrike@gmail.com"
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential
VOLUME ["/torrents", "/app/config"]
COPY requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt
COPY . /app
WORKDIR /app
ENTRYPOINT ["python"]
CMD ["GazelleUI.py"]
