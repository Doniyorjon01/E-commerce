# Use an official Python runtime as the base image
FROM python:3.11

WORKDIR /app

ADD ./requirements.txt /app/requirements.txt
RUN apt-get update && apt-get install -y tzdata
RUN pip install --no-cache-dir -r requirements.txt
ENV TZ=Asia/Tashkent
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

ADD .. /app

EXPOSE 8000

#CMD ["python", "run.py"]