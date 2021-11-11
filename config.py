import time

#************************************
#? ************必修改*****************
is_test = False # True 则运行下面的5个测试的代码， False则为具体game的迁移测试
test = 'mem'  # cpu, io, mem, tar, video
#************************************


# ====================is_test = True=================================

wait_time= 5         # 运行几秒开始迁移
target_ip= '192.168.50.141' #'10.112.149.97',
target_user= 'edge'
target_pass= '****'

podman_dir = '/tmp/podman/'   # 迁移过程的工作目录，#!在checkpoint之后，整个目录会被同步
chkpt_path = podman_dir+'srvMig.tar.gz'  # 保存checkpoint的位置
mount_dir = podman_dir+'test/'  # 挂载的目录
mount_src_dir = mount_dir+'src/' # 预迁移的目录 #! 在checkpoint之前会同步这个目录


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




# ====================is_test = False=================================
game = 'snake' # snake, minecraft

ga_chkpt_path = podman_dir+'GA.tar.gz'
game_chkpt_path = podman_dir+'game.tar.gz'



ga_cmd = 'sudo xhost +local:root && sudo podman run -it --rm --ipc=host --env="DISPLAY=$DISPLAY" --env="QT_X11_NO_MITSHM=1" --volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" -v /dev/shm:/dev/shm -v /var/run/dbus:/var/run/dbus  --device /dev/dri/card0 --device /dev/snd:/dev/snd -v /tmp/podman/test:/tmp/podman  -p 8554:8554 -p 8555:8555  parkhi/gaminganywhere:16.04 bash /tmp/podman/src/run_ga.sh'


# game运行需要的Python代码和jar包都放到  mount_src_dir 里面

game_base_cmd = 'xhost +local:root && podman run -it --rm --env="DISPLAY" --env="QT_X11_NO_MITSHM=1" --volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" -v /tmp/podman/test:/tmp/podman '

snake_cmd = 'snake-edge python /tmp/podman/src/Snakepygame.py -n snake -i 10.112.145.90 -p 5500'

minecraft_cmd = 'platpus/javafx java -jar /tmp/podman/src/HMCL-3.3.188.jar'

if game == 'snake':
    game_cmd = game_base_cmd+snake_cmd
elif game == 'minecraft':
    game_cmd = game_base_cmd+minecraft_cmd
else:
    raise Exception(f'游戏选择错误---> {game}，应该选snake or minecraft')