import time

wait_time= 5         # 运行几秒开始迁移
target_ip= '192.168.50.141' #'10.112.149.97',
target_user= 'edge'
target_pass= '****'

podman_dir = '/tmp/podman/'
chkpt_path = podman_dir+'srvMig.tar.gz'
mount_dir = podman_dir+'test'

csv_path = f"/tmp/csv_data/time_stamps.csv"


# 只用修改这里
container_info = {
    # "info":'info',
    'image':'docker.io/borda/docker_python-opencv-ffmpeg:cpu-py3.8-cv4.5.1',
    'mount_dir':mount_dir,     # dir patt in host, default mount to /tmp/podman
    # 'bash_file':'',     # 容器启动后运行的 .sh 脚本
    'init_cmd': 'ffmpeg -i /tmp/podman/test.mp4 /tmp/podman/test.avi',
    'chkpt_path': chkpt_path
} 