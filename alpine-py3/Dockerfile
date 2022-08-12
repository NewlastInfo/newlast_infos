FROM hsb-tcr.tencentcloudcr.com/hsb/alpine-py3
### 复制依赖包到服务项目目录下
COPY requirements.txt /home/devenv/zjc/hsb_pajia_spider/requirements.txt
### 下载 python 项目的依赖库
RUN pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple  --upgrade pip
RUN pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple -r /home/devenv/zjc/hsb_pajia_spider/requirements.txt



