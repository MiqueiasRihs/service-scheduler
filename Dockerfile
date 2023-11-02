FROM ubuntu
RUN addgroup --gid 1024 shared

RUN apt-get update && apt-get install -y locales
RUN locale-gen pt_BR.UTF-8
ENV LANG pt_BR.UTF-8
ENV LANGUAGE pt_BR:pt
ENV LC_ALL pt_BR.UTF-8

WORKDIR /home/app

COPY . .

RUN apt-get update && \
	apt-get install postgresql-client -y && \
	apt-get install sudo git nano curl gnupg build-essential libpq-dev \
	libjpeg8-dev zlib1g-dev libtiff-dev libfreetype6 libfreetype6-dev \
	libwebp-dev libopenjp2-7-dev -y python3-pip \
	&& pip install --no-cache-dir -r requirements.txt \
    && chmod +x setup_dev.sh
