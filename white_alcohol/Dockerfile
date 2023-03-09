#
#
#### 以python:3.7来作为基础镜像
#FROM python:3.7
##FROM hsb-tcr.tencentcloudcr.com/hsb/centos-py3-bi:latest
## 设置时区，避免晚8小时
#ENV TZ="Asia/Shanghai"
#RUN sed -i 's#http://archive.ubuntu.com/#http://mirrors.tuna.tsinghua.edu.cn/#' /etc/apt/sources.list
#RUN apt-get update
#RUN apt-get -y install vim
#
##### 将dockerfile目录下的谷歌浏览器安装包和浏览器驱动安装包复制到docker容器内
##COPY linux_signing_key.pub  /home/root/linux_signing_key.pub
##
##RUN apt-key add /home/root/linux_signing_key.pub
##RUN sh -c 'echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list'
##
##RUN apt-get -y install google-chrome-stable
#RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
#RUN echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list
#RUN apt-get update && apt-get install -y google-chrome-stable
#
#### 复制浏览器驱动linux版本到docker容器内并且编译安装浏览器驱动
## COPY chromedriver_linux64.zip  /usr/local/python37/bin/
## RUN unzip /usr/local/python37/bin/chromedriver_linux64.zip
#
#RUN wget http://chromedriver.storage.googleapis.com/2.38/chromedriver_linux64.zip
## RUN apt-get -y install zip
#RUN apt-get -y install unzip
#RUN unzip -c  chromedriver_linux64.zip
#RUN unzip   chromedriver_linux64.zip
#RUN ls
#RUN cp chromedriver /home/root/chromedriver
#
#
#### 创建工作目录
#RUN mkdir /spiders
#### 将python项目复制到 /spider工作目录下
#COPY white_alcohol.py  /spiders/white_alcohol.py
#
#COPY settings.py  /spiders/settings.py
#COPY dingTalk_white_alchol.py  /spiders/dingTalk_white_alchol.py
#
#COPY requirements.txt /spiders/requirements.txt
#### 设置 /spider 为工作目录
#### 下载 python 项目的依赖库
#RUN pip3 install -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com -r /spiders/requirements.txt
#### 最后一步，运行docker镜像时运行自己的python项目
#### 可以多个参数： CMD ["python3","a","main.py"]
#CMD ["python3" ,"/spiders/white_alcohol.py"]



# 基于python:3.8-slim-buster作为基础镜像
FROM python:3.8-slim-buster

# 安装Chrome浏览器和驱动程序
RUN apt-get update && \
    apt-get install -y wget gnupg && \
    wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list && \
    apt-get update && \
    apt-get install -y google-chrome-stable chromium-driver && \
    rm -rf /var/lib/apt/lists/*

# 创建工作目录
WORKDIR /app

# 复制应用程序代码到工作目录
COPY . .

# 安装Python依赖库
RUN pip install --no-cache-dir -r requirements.txt

# 设置环境变量
ENV CHROME_BIN=/usr/bin/google-chrome
ENV CHROME_DRIVER=/usr/bin/chromedriver

# 启动应用程序
CMD ["python", "app.py"]
