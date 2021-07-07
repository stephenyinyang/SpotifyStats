FROM registry.access.redhat.com/ubi8

WORKDIR /app

COPY Pipfile* /app/

## NOTE - rhel enforces user container permissions stronger ##
USER root
RUN yum -y install python3
RUN yum -y install python3-pip wget

RUN python3 -m pip install --upgrade pip \
  && python3 -m pip install --upgrade pipenv \
  && pipenv install --system --deploy

USER 1001

COPY . /app
ENV FLASK_APP=server/__init__.py
ENV SPOTIPY_CLIENT_ID = "07babcfeaea747f0967bb1d5145fc21f"
ENV SPOTIPY_CLIENT_SECRET = "45e1dbda55da450b808e50aaf728365b"
ENV SPOTIPY_REDIRECT_URI = "https://spotify-stats.mybluemix.net/"
CMD ["python3", "manage.py", "start", "0.0.0.0:3334"]
