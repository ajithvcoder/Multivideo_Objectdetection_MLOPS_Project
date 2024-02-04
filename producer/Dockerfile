FROM python:3.10-slim

# USER ROOT
WORKDIR /usr/app
# RUN apt-get update && \
#   apt-get install -y net-tools

RUN apt-get update -y

# RUN apk add --update ffmpeg libsm6 libxext6  -y
RUN apt install ffmpeg libsm6 libxext6  -y
ADD ./requirements.txt ./

RUN pip3 install  -r requirements.txt
ADD ./ ./
# RUN python create_topic.py

CMD ["python3", "app.py"]