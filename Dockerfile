FROM python:alpine


ENV JOB_DIR="/jobs"

COPY requirements.txt /requirements.txt

RUN pip install -r /requirements.txt \
&& mkdir /jobs

COPY app /app


CMD /app/scheduled_toots.py

