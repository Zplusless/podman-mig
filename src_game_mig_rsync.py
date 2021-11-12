# source node

import config
from call_cmd import cmd_run

import requests as r
from typing import Dict
import time, datetime
from pprint import pprint
import csv


CACHE={'id':None}

def send_info(data:Dict, target:str, function:str):
    # 调用flask端口
    addr = f"http://{target}:8000/{function}/"
    res = r.post(addr, data = data)
    if res.status_code == 200:
        return res.text
    
    raise Exception('target node error') 

def send_file(local_path,target_path, target_ip, is_dir=True):
    # sshpass -p 1423 scp -r ./test_scp/ edge@192.168.50.141:/home/edge
    dir_flag = '-r' if is_dir else ''
    cmd = f'sshpass -p {config.target_pass} rsync {dir_flag} -av {local_path} {config.target_user}@{target_ip}:{target_path}'
    
    # print(f'\nCOMMAND:  {cmd}')
    ans, t = cmd_run(cmd, True)

    # print(f'\nSTDOUT:  {ans}')
    
    return ans, t

def run_container():
    # podman run -d -v /home/edge/XXX:/tmp/podman docker.io/borda/docker_python-opencv-ffmpeg  ffmpeg -i /tmp/podman/test.mp4 /tmp/podman/test.avi
    
    game_base_cmd = 'sudo xhost +local:root && sudo podman run -d --rm --env="DISPLAY" --env="QT_X11_NO_MITSHM=1" --volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" -v /tmp/podman/test:/tmp/podman '
   
    cmd = game_base_cmd + f" {config.container_info['image']} {config.container_info['init_cmd']}"
    # print(f'COMMAND:  {cmd}')
    ans, t = cmd_run(cmd, True)

    CACHE['id'] = ans[:-1]

    # print(f'\nSTDOUT:  {ans}')

    return ans,t

def checkpoint(i):

    cmd = f"sudo podman container checkpoint {CACHE['id']} -e {config.chkpt_path}"

    # print(f'COMMAND:  {cmd}')
    ans, t = cmd_run(cmd, True)

    # print(f'\nSTDOUT:  {ans}')

    return ans,t


def milisecond(t):
    return datetime.datetime.fromtimestamp(t).strftime("%H:%M:%S.%f")


def main(i):

    #* =========  启动容器 ==========
    t1 = time.time()
    run_container()

    time.sleep(config.wait_time)


    #! =========  通知用户连接 ==========
    r.post(f'http://{config.user_ip}:8000/connect/', data={'ip':config.src_ip})

    if config.test == 'minecraft':
        print("请手动开始minecraft游戏")
        time.sleep(20)


    #* =========  发送原始文件 ==========
    t2_ = time.time()
    data_size1, dt1 = send_file(config.mount_src_dir, config.mount_src_dir, config.target_ip, True)

    t2 = time.time()
    ans = send_info(config.container_info, config.target_ip, 'container_info')
    print('send info:', ans)
    t3 = time.time()


    #* =========  checkpoint ==========
    checkpoint(i)
    t4 = time.time()



    #* =========  发送checkpoint ==========
    cmd_run(f"sudo chmod 666 {config.chkpt_path}", True)
    data_size2, dt2 = send_file(config.podman_dir, config.podman_dir, config.target_ip, True)
    
    t5 = time.time()
    # cmd_run(f"sudo chmod 666 {config.chkpt_path}", True)
    # send_file(config.chkpt_path, config.chkpt_path, config.target_ip, is_dir=False)
    # t6 = time.time()

    #* =========  通知dst启动 ==========
    ans = send_info({'info': 'done'}, config.target_ip, 'migrate')
    # print(ans)
    t7 = time.time()


    #! =========  通知用户重连 ==========
    r.post(f'http://{config.user_ip}:8000/connect/', data={'ip':config.dst_ip})
    # 等待一会
    time.sleep(3)



    #* =========  记录数据 ==========
    tt = ans.split(',')
    tt1 = float(tt[0])
    tt2 = float(tt[1])

    mig_data = [["item", "d_t", "time"]]
    
    mig_data.append(['send basic data', t2-t2_, milisecond(t2_)])
    mig_data.append(['send image name', t3-t2, milisecond(t2)])
    mig_data.append(['checkpoint', t4-t3, milisecond(t3)])
    mig_data.append(['send chkpt data', t5-t4, milisecond(t4), milisecond(t5)])
    # mig_data.append(['send chkpt', t6-t5, milisecond(t4)])
    # ['send done', tt1-t6]
    mig_data.append(['restore', tt2-tt1, milisecond(tt1), milisecond(tt2)])

    mig_data.append(['total', t7-t2_, milisecond(t7)])

    mig_data.append([])
    mig_data.append([])

    mig_data.append(['pre data transfer:', data_size1, dt1])
    mig_data.append(['chkpt data transfer:', data_size2, dt2])

    pprint(mig_data)

    with open(config.csv_path.format(i), 'w') as f:
        wtr = csv.writer(f)
        wtr.writerows(mig_data)
    


if __name__ == '__main__':
    # ck, _ = cmd_run('whoami', True)
    # # print(ck, type(ck))
    # if 'root' not in ck:
    #     raise Exception('please run with root')
    if config.is_test or config.test not in ['snake', 'minecraft']:
        print(f'This script is used to test [minecraft, snake], but config.test={config.test}')
        print('exit')
        exit(0)


    #! 启动本地GA
    #nohup bash measure.sh & echo $! > cmd.pid
    cmd_run(f'bash scripts/run_ga.sh', False)
    print('ga started')
    time.sleep(3)

    for i in range(1,9):
      #  清除临时文件
        # cmd_run(f"sudo rm -rf {config.mount_dir}"+"!(src)", True)  # 删除挂载目录下非src路径下的文件
        # cmd_run(f"sudo rm -rf {config.podman_dir}"+"!(test)", True) # 删除podman路径下非挂载路径的文件
        
        # cmd_run(f'll {config.mount_dir}', True)
        # cmd_run(f'll {config.podman_dir}', True)

        # print('delete intermediate files')
        # time.sleep(10)


        #* 源节点和目标节点文件的权限mod也要完全一样
        cmd_run(f"sudo chmod 644 {config.mount_dir}"+"src/* ", True) 
        
        # 让chkpt文件可以发送
        cmd_run(f"sudo rm {config.chkpt_path}", True)
        cmd_run(f'sudo rm {config.mount_dir}'+'*.tar.bz2', True)
        print('delete intermediate files')
        time.sleep(3)


        # target节点 清除临时文件
        r.get(f'http://{config.target_ip}:8000/init/')

        # 启动本地measure程序
        r.get(f'http://127.0.0.1:8000/start/{i}/')
        r.get(f'http://{config.target_ip}:8000/start/{i}/')


        main(i)

        time.sleep(6)

        # 断开user
        r.get(f'http://{config.user_ip}:8000/end/')


        r.get(f'http://127.0.0.1:8000/end/')
        r.get(f'http://{config.target_ip}:8000/end/')

        time.sleep(10)
        mv_srvMig = f'srvMig_{i}.tar.gz'
        cmd_run(f"sudo cp {config.chkpt_path} {config.csv_dir+mv_srvMig}", False)

        time.sleep(3)

        
                        

