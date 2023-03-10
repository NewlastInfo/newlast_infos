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
##RUN sh -c 'echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list'
##RUN apt-get update
##
##RUN apt-get -y install google-chrome-stable
##
##### 复制浏览器驱动linux版本到docker容器内并且编译安装浏览器驱动
### COPY chromedriver_linux64.zip  /usr/local/python37/bin/
### RUN unzip /usr/local/python37/bin/chromedriver_linux64.zip
##
##RUN wget http://chromedriver.storage.googleapis.com/2.38/chromedriver_linux64.zip
### RUN apt-get -y install zip
#RUN apt-get -y install unzip
##RUN unzip -c  chromedriver_linux64.zip
##RUN unzip   chromedriver_linux64.zip
#RUN ls
##RUN cp chromedriver /home/root/chromedriver
##RUN apt-get -y install vim
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



FROM python:3.8

# 设置镜像源为国内站点
RUN sed -i 's/archive.ubuntu.com/mirrors.tencentyun.com/g' /etc/apt/sources.list \
    && sed -i 's/deb.debian.org/mirrors.tencentyun.com/g' /etc/apt/sources.list \
    && sed -i 's/security.debian.org/mirrors.tencentyun.com/g' /etc/apt/sources.list \
    && sed -i 's/httpredir.debian.org/mirrors.tencentyun.com/g' /etc/apt/sources.list

# 安装必要的依赖
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    unzip \
    libgconf-2-4 \
    libnss3 \
    libgtk-3-0

# 下载安装Chrome浏览器
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] https://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list \
    && apt-get update && apt-get install -y google-chrome-stable

# 下载安装chromedriver
#RUN wget -q https://npm.taobao.org/mirrors/chromedriver/$(curl -s https://npm.taobao.org/mirrors/chromedriver/LATEST_RELEASE)/chromedriver_linux64.zip \
#    && unzip chromedriver_linux64.zip \
#    && rm -rf chromedriver_linux64.zip \
#    && mv chromedriver /usr/local/bin/

RUN wget http://chromedriver.storage.googleapis.com/2.38/chromedriver_linux64.zip
 RUN apt-get -y install zip
RUN apt-get -y install unzip
RUN unzip -c  chromedriver_linux64.zip
RUN unzip   chromedriver_linux64.zip
RUN ls
#RUN cp chromedriver /home/root/chromedriver

# 安装Python依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 设置环境变量
ENV DISPLAY=:99

# 启动Xvfb
RUN Xvfb :99 -screen 0 1024x768x24 > /dev/null 2>&1 &

# 设置工作目录
WORKDIR /app

# 复制应用代码
COPY app.py .

# 运行应用
CMD ["python", "app.py"]