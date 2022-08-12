FROM hsb-tcr.tencentcloudcr.com/hsb/alpine-py3
### 复制依赖包到服务项目目录下
COPY requirements.txt /home/devenv/zjc/hsb_pajia_spider/requirements.txt
### 下载 python 项目的依赖库
RUN pip3 install -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com -r /home/devenv/zjc/hsb_pajia_spider/requirements.txt



