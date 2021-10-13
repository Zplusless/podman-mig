

time= 5,         # 运行几秒开始迁移
target_ip= '127.0.0.1' #'10.112.149.97',
target_user= 'edge',
target_pass= '123456'

checkpoint_path = '/home/edge/chkpt/srvMig.tar.gz'

container_info = {
    # "info":'info',
    'image':'docker.io/borda/docker_python-opencv-ffmpeg',
    'mount_dir':'/home/edge/test',     # dir patt in host, default mount to /tmp/podman
    # 'bash_file':'',     # 容器启动后运行的 .sh 脚本
    'init_cmd': 'ffmpet -i /tmp/podman/test.mp4 /tmp/podman/test.avi',
    'chkpt_path': checkpoint_path
}