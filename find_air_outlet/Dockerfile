#
#
#### 以python:3.7来作为基础镜像
#FROM python:3.7
#
## 设置时区，避免晚8小时
#ENV TZ="Asia/Shanghai"
##RUN sed -i 's#http://archive.ubuntu.com/#http://mirrors.tuna.tsinghua.edu.cn/#' /etc/apt/sources.list
#RUN  sed -i s@/archive.ubuntu.com/@/mirrors.aliyun.com/@g /etc/apt/sources.list
#RUN  apt-get clean
#
#RUN apt-get update
#
#### 将dockerfile目录下的谷歌浏览器安装包和浏览器驱动安装包复制到docker容器内
#COPY linux_signing_key.pub  /home/root/linux_signing_key.pub
#
#RUN apt-key add /home/root/linux_signing_key.pub
#RUN sh -c 'echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list'
#RUN apt-get update
#
#RUN apt-get -y install google-chrome-stable
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
#RUN apt-get -y install vim
#
#### 创建工作目录
#RUN mkdir /spiders
#### 将python项目复制到 /spider工作目录下
#COPY find_air_outlet.py  /spiders/find_air_outlet.py
#
#COPY settings.py  /spiders/settings.py
#COPY dingTalk_find_air_outlet.py  /spiders/dingTalk_find_air_outlet.py
#
#COPY requirements.txt /spiders/requirements.txt
#### 设置 /spider 为工作目录
#### 下载 python 项目的依赖库
#RUN pip3 install -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com -r /spiders/requirements.txt
#### 最后一步，运行docker镜像时运行自己的python项目
#### 可以多个参数： CMD ["python3","a","main.py"]
#CMD ["python3" ,"/spiders/find_air_outlet.py"]


FROM python:3.8-slim-buster

# 安装必要的软件包
#RUN apt-get update && \
#    apt-get -yq --no-install-recommends install \
#    wget \
#    curl \
#    gnupg2 \
#    unzip \
#    xvfb \
#    libxi6 \
#    libgconf-2-4 \
#    libnss3 \
#    libasound2 \
#    libxtst6 \
#    libgtk-3-0 \
#    libatk-bridge2.0-0 \
#    fonts-liberation \
#    && apt-get clean

RUN  sed -i s@/archive.ubuntu.com/@/mirrors.aliyun.com/@g /etc/apt/sources.list
RUN  apt-get clean

RUN apt-get update

# 下载并安装Chrome浏览器和驱动程序
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
    dpkg -i google-chrome-stable_current_amd64.deb && \
    rm google-chrome-stable_current_amd64.deb

RUN LATEST=$(wget -q -O - http://chromedriver.storage.googleapis.com/LATEST_RELEASE) && \
    wget http://chromedriver.storage.googleapis.com/$LATEST/chromedriver_linux64.zip && \
    unzip chromedriver_linux64.zip && \
    mv chromedriver /usr/local/bin/ && \
    rm chromedriver_linux64.zip

# 设置虚拟显示
ENV DISPLAY=:99

# 设置入口点脚本
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# 安装Selenium和其他Python依赖项
RUN pip install selenium

ENTRYPOINT ["/entrypoint.sh"]
