FROM ubuntu
RUN apt-get update -y && apt-get upgrade -y
RUN mkdir fastapi-project
WORKDIR fastapi-project
ADD project project
ADD main.py .
ADD myblogs.db .
RUN apt install python3-pip -y && pip3 install -r project/src/requirements.txt
EXPOSE 8000
CMD uvicorn main:app --host 0.0.0.0 --port 8000