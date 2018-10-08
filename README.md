# Telegram with QQ


### Requirements
```
sudo pip3 install pipenv
pipenv install

# or with python3.6

sudo pip3 install -r requirements.txt
```

open `qq_client.py`, `telegram_client.py`, change the top variables as you need.

### Usage
0. run server at china VPS

```
python3 server.py &
```

1. set up `cqhttp` in china VPS

```
# https://cqhttp.cc/docs/4.5/#/?id=%E4%BD%BF%E7%94%A8-docker
docker pull richardchien/cqhttp:latest
mkdir coolq  # 用于存储酷 Q 的程序文件
docker run -d -ti --name cqhttp-test \
           -v $(pwd)/coolq:/home/user/coolq \  # 将宿主目录挂载到容器内用于持久化酷 Q 的程序文件
           -p 9000:9000 \  # noVNC 端口，用于从浏览器控制酷 Q (密码:MAX8char)
           -p 5700:5700 \  # HTTP API 插件开放的端口
           -e CQHTTP_POST_URL=http://{your_china_VPS_public_ip_adress}:8080 \  # 事件上报地址, 必须是公网ip地址, Docker_CQhttp_address, for example: 182.294.242.181
           -e CQHTTP_SERVE_DATA_FILES=yes \  # 允许通过 HTTP 接口访问酷 Q 数据文件
           richardchien/cqhttp:latest
```

* go to: `http:{your_china_VPS_public_ip_adress}:9000`. (passwd is `MAX8char`) to login your robot QQ

* run qq client: `python3 qq_client.py &`


2. set up `telegram` at US VPS
```
python3 telegram_client.py &
```
