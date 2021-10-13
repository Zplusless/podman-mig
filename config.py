

time= 5         # 运行几秒开始迁移
target_ip= '192.168.50.141' #'10.112.149.97',
target_user= 'edge'
target_pass= '****'

chkpt_path = '/tmp/podman/srvMig.tar.gz'
mount_dir = '/tmp/podman/test'



container_info = {
    # "info":'info',
    'image':'docker.io/borda/docker_python-opencv-ffmpeg:cpu-py3.8-cv4.5.1',
    'mount_dir':mount_dir,     # dir patt in host, default mount to /tmp/podman
    # 'bash_file':'',     # 容器启动后运行的 .sh 脚本
    'init_cmd': 'ffmpeg -i /tmp/podman/test.mp4 /tmp/podman/test.avi',
    'chkpt_path': chkpt_path
} 