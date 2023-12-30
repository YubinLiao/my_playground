FROM ubuntu:22.04
RUN apt-get update && \
    apt-get install -y wget && \
    apt-get clean
RUN apt-get install -y python3.10
RUN apt-get install -y python3-pip
COPY requirements.txt .
RUN pip install -r requirements.txt
#upgrade robotframework browser to latest version, due to dependency conflict with tensorflow
RUN pip install robotframework-browser==18.0.0
RUN apt-get install -y curl
RUN curl -fsSL https://deb.nodesource.com/setup_current.x | bash
RUN apt-get install -y nodejs
RUN rfbrowser init
RUN npx playwright install-deps
# Or install playwright dependency with apt-get
# RUN apt-get install libglib2.0-0 libnss3 libnspr4 libdbus-1-3 libatk1.0-0 libatk-bridge2.0-0 libcups2 libdrm2 libxkbcommon0 libatspi2.0-0 libxcomposite1 libxdamage1 libxext6 libxfixes3 libxrandr2 libgbm1 libpango-1.0-0 libcairo2 libasound2
RUN mkdir /home/code
COPY . /home/code
WORKDIR /home/code


