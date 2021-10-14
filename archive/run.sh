nohup bash measure.sh & echo $! > cmd.pid

python src_node_rsync.py

kill -9 `cat cmd.pid`

