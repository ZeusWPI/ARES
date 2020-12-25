FROM python:3.9.1-buster
WORKDIR /app
COPY . /app
RUN pip3 install -r requirements.txt
RUN mkdir -p /app/shared
RUN apt-get update -qq && apt-get install --no-install-recommends -y inotify-tools sox
CMD ./entry.sh