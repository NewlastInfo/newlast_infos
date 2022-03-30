
### 以python:3.7来作为基础镜像
FROM python:3.7

RUN apt-get update
RUN apt-get install vim
# RUN apt-get -y install zip
RUN apt-get -y install unzip

### 创建工作目录
RUN mkdir /spiders
### 将python项目复制到 /spider工作目录下
COPY ke_info.py  /spiders/ke_info.py

COPY settings.py  /spiders/settings.py
COPY dingTalk_ke.py  /spiders/dingTalk_ke.py

COPY requirements.txt /spiders/requirements.txt
### 设置 /spider 为工作目录
### 下载 python 项目的依赖库
RUN pip3 install -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com -r /spiders/requirements.txt
### 最后一步，运行docker镜像时运行自己的python项目
### 可以多个参数： CMD ["python3","a","main.py"]
CMD ["python3" ,"/spiders/ke_info.py"]
