
### 以python:3.7来作为基础镜像
FROM python:3.7
#FROM hsb-tcr.tencentcloudcr.com/hsb/alpine-py3

# 设置时区，避免晚8小时
ENV TZ="Asia/Shanghai"
#RUN sed -i 's#http://archive.ubuntu.com/#http://mirrors.tuna.tsinghua.edu.cn/#' /etc/apt/sources.list
RUN apt-get update
RUN apt-get -y install vim
# RUN apt-get -y install zip
#RUN apt-get -y install unzip

#RUN echo "129.204.136.155 cms.huishoubao.com"  >> /etc/hosts
#RUN cat /etc/hosts
### 创建工作目录
RUN mkdir /spiders
### 将python项目复制到 /spider工作目录下
COPY zz_cookie_update.py /spiders/zz_cookie_update.py


COPY settings.py  /spiders/settings.py
COPY requirements.txt /spiders/requirements.txt
### 设置 /spider 为工作目录
### 下载 python 项目的依赖库
RUN pip3 install -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com -r /spiders/requirements.txt
### 最后一步，运行docker镜像时运行自己的python项目
#CMD ['echo 129.204.136.155 cms.huishoubao.com  >> /etc/hosts']
CMD ["python3" ,"/spiders/zz_cookie_update.py"]
