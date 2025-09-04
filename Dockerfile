FROM python
VOLUME ["/torrents", "/app/config"]
COPY requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt
COPY . /app
WORKDIR /app
ENTRYPOINT ["gunicorn"]
CMD ["-b", "0.0.0.0:2020", "--workers", "1", "wsgi:app"]
