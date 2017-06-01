#export http_proxy=http://127.0.0.1:1088
#export https_proxy=http://127.0.0.1:1088
#pkill python
python3 server.py &
python3 telegram.py &
