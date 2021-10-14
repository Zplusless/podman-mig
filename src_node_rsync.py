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
    
    print(f'\nCOMMAND:  {cmd}')
    ans, t = cmd_run(cmd, True)

    print(f'\nSTDOUT:  {ans}')
    
    return ans, t

def run_container():
    # podman run -d -v /home/edge/XXX:/tmp/podman docker.io/borda/docker_python-opencv-ffmpeg  ffmpeg -i /tmp/podman/test.mp4 /tmp/podman/test.avi
    
    
    
    cmd = f"sudo podman run -d -v {config.mount_dir}:/tmp/podman {config.container_info['image']} {config.container_info['init_cmd']}"
    print(f'COMMAND:  {cmd}')
    ans, t = cmd_run(cmd, True)

    CACHE['id'] = ans[:-1]

    print(f'\nSTDOUT:  {ans}')

    return ans,t

def checkpoint():

    cmd = f"sudo podman container checkpoint {CACHE['id']} -e {config.chkpt_path}"

    print(f'COMMAND:  {cmd}')
    ans, t = cmd_run(cmd, True)

    print(f'\nSTDOUT:  {ans}')

    return ans,t


def milisecond(t):
    return datetime.datetime.fromtimestamp(t).strftime("%H:%M:%S.%f")


def main():
    t1 = time.time()
    run_container()

    time.sleep(config.wait_time)

    t2_ = time.time()
    send_file(config.podman_dir, config.podman_dir, config.target_ip, True)

    t2 = time.time()
    ans = send_info(config.container_info, config.target_ip, 'container_info')
    print('send info:', ans)
    t3 = time.time()

    checkpoint()
    t4 = time.time()

    #* test
    cmd_run(f"sudo chmod 666 {config.chkpt_path}", True)
    send_file(config.podman_dir, config.podman_dir, config.target_ip, True)
    
    t5 = time.time()
    # cmd_run(f"sudo chmod 666 {config.chkpt_path}", True)
    # send_file(config.chkpt_path, config.chkpt_path, config.target_ip, is_dir=False)
    # t6 = time.time()

    
    ans = send_info({'info': 'done'}, config.target_ip, 'migrate')
    # print(ans)
    t7 = time.time()
    
    # 等待一会
    time.sleep(3)


    tt = ans.split(',')
    tt1 = float(ans[0])
    tt2 = float(ans[1])

    mig_data = [["item", "d_t", "time"]]
    
    mig_data.append(['send basic data', t2-t2_, milisecond(t2)])
    mig_data.append(['send image name', t3-t2, milisecond(t2)])
    mig_data.append(['checkpoint', t4-t3, milisecond(t3)])
    mig_data.append(['send mount', t5-t4, milisecond(t4)])
    # mig_data.append(['send chkpt', t6-t5, milisecond(t4)])
    # ['send done', tt1-t6]
    mig_data.append(['restore', tt2-tt1, milisecond(tt1)])

    mig_data.append(['total', t7-t2_, milisecond(t2_)])

    pprint(mig_data)

    with open(config.csv_path, 'w') as f:
        wtr = csv.writer(f)
        wtr.writerows(mig_data)
    


if __name__ == '__main__':
    # ck, _ = cmd_run('whoami', True)
    # # print(ck, type(ck))
    # if 'root' not in ck:
    #     raise Exception('please run with root')

    #  清除临时文件
    cmd_run(f"sudo rm {config.mount_dir}/test.avi ", True)
    
    #* 源节点和目标节点文件的权限mod也要完全一样
    cmd_run(f"sudo chmod 644 {config.mount_dir}/test.mp4 ", True) 
    # 让chkpt文件可以发送
    cmd_run(f"sudo rm {config.chkpt_path}", True)

    # target节点 清除临时文件
    r.get(f'http://{config.target_ip}:8000/init/')


    main()


