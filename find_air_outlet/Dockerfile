
 
### 以python:3.7来作为基础镜像
FROM python:3.7

# 设置时区，避免晚8小时
ENV TZ="Asia/Shanghai"
RUN sed -i 's#http://archive.ubuntu.com/#http://mirrors.tuna.tsinghua.edu.cn/#' /etc/apt/sources.list
RUN apt-get update
RUN apt-get -y install vim

### 将dockerfile目录下的谷歌浏览器安装包和浏览器驱动安装包复制到docker容器内
COPY linux_signing_key.pub  /home/root/linux_signing_key.pub

RUN apt-key add /home/root/linux_signing_key.pub
#RUN sh -c 'echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list'

RUN sh -c 'echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN apt update
RUN apt install google-chrome-stable -y
RUN wget https://chromedriver.storage.googleapis.com/107.0.5304.62/chromedriver_linux64.zip
#RUN unzip chromedriver_linux64.zip -d /usr/bin/


#RUN apt-get -y install google-chrome-stable

### 复制浏览器驱动linux版本到docker容器内并且编译安装浏览器驱动
# COPY chromedriver_linux64.zip  /usr/local/python37/bin/
# RUN unzip /usr/local/python37/bin/chromedriver_linux64.zip

#RUN wget http://chromedriver.storage.googleapis.com/2.38/chromedriver_linux64.zip
# RUN apt-get -y install zip
RUN apt-get -y install unzip
RUN unzip -c  chromedriver_linux64.zip
RUN unzip   chromedriver_linux64.zip
RUN ls
RUN cp chromedriver /home/root/chromedriver


### 创建工作目录
RUN mkdir /spiders
### 将python项目复制到 /spider工作目录下
COPY find_air_outlet.py  /spiders/find_air_outlet.py

COPY settings.py  /spiders/settings.py
COPY dingTalk_find_air_outlet.py  /spiders/dingTalk_find_air_outlet.py

COPY requirements.txt /spiders/requirements.txt
### 设置 /spider 为工作目录
### 下载 python 项目的依赖库
RUN pip3 install -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com -r /spiders/requirements.txt
### 最后一步，运行docker镜像时运行自己的python项目
### 可以多个参数： CMD ["python3","a","main.py"]
CMD ["python3" ,"/spiders/find_air_outlet.py"]
