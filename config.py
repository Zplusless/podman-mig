import time

is_test = False

#************************************
#? ************必修改*****************
test = 'mem'  # cpu, io, mem, tar, video, snake, minecraft
#************************************


src_ip = '10.112.150.12'
dst_ip = '10.112.149.97'
user_ip = '10.112.30.143'   #game client/UE 的ip


wait_time= 5         # 运行几秒开始迁移
target_ip= dst_ip
target_user= 'edge'   # destination节点的账户密码，用于rsync传文件
target_pass= '123456'

podman_dir = '/tmp/podman/'  # 实验临时文件的根目录
chkpt_path = podman_dir+'srvMig.tar.gz'  # checkpoint文件存放地址
mount_dir = podman_dir+'test/'  # 容器启动挂载的目录
mount_src_dir = mount_dir+'src/'    # 容器启动后会使用到的源文件的路径，本路径在容器迁移前会先与destination node同步


# 记录实验数据的log的路径
csv_dir = "/tmp/csv_data/"
csv_path = csv_dir+"time_stamps_{}.csv"


mount_volume = True if test in ['tar', 'video'] else False  # 是否挂载本地目录


test_cmds = {
    'cpu':{
        'image':'docker.io/progrium/stress',
        'init_cmd': '-c 10'
    },
    'io':{
        'image':'docker.io/progrium/stress',
        'init_cmd': '-i 20'
    },
    'mem':{
        'image':'docker.io/progrium/stress',
        'init_cmd': '-m 20'
    },
    'tar':{
        'image':'docker.io/library/ubuntu:20.04',
        'init_cmd': 'tar -jcvf /tmp/podman/examples.tar.bz2 /tmp/podman/src/tarTest'
    },
    'video':{
        'image':'docker.io/borda/docker_python-opencv-ffmpeg:cpu-py3.8-cv4.5.1',
        'init_cmd': 'ffmpeg -i /tmp/podman/src/1015.flv /tmp/podman/1015.mp4'
    },
    'snake':{
        'image':'docker.io/zzdflyz351/snake-edge',
        'init_cmd': '\"python /tmp/podman/src/Snakepygame.py -n podman -i 10.112.145.90 -p 5500\"'
    },
    'minecraft':{
        'image':'docker.io/platpus/javafx',
        'init_cmd': 'java -jar /tmp/podman/src/HMCL-3.3.188.jar'
    }
}



# 只用修改这里
container_info = {
    # "info":'info',
    'image':test_cmds[test]['image'],
    'mount_dir':mount_dir,     # dir patt in host, default mount to /tmp/podman
    # 'bash_file':'',     # 容器启动后运行的 .sh 脚本
    'init_cmd': test_cmds[test]['init_cmd'],
    'chkpt_path': chkpt_path
} 
