# source node

import config
from call_cmd import cmd_run

import requests as r
from typing import Dict
import time


def send_info(data:Dict, target:str, function:str):
    # 调用flask端口
    addr = f"http://{target}:8000/{function}/"
    res = r.post(addr, data = data)
    if res.status_code == 200:
        return res.text
    
    raise Exception('target node error') 

def send_file(path, target_ip, is_dir=False):
    # sshpass -p 1423 scp -r ./test_scp/ edge@192.168.50.141:/home/edge
    dir_flag = '-r' if is_dir else ''
    cmd = f'sshpass -p {config.target_pass} scp {dir_flag} {path} {config.target_user}@{target_ip}:path'
    ans, t = cmd_run(cmd, True)
    
    return ans, t

def run_container():
    # podman run -d -v /home/edge/XXX:/tmp/podman docker.io/borda/docker_python-opencv-ffmpeg  ffmpeg -i /tmp/podman/test.mp4 /tmp/podman/test.avi
    cmd = f"podman run -d -v {config.container_info['mount_dir']}:/tmp/podman --name test {config.container_info['image']} {config.container_info['init_cmd']}"
    ans, t = cmd_run(cmd, True)

    return ans,t

def main():
    t1 = time.time()
    run_container()

    time.sleep(config.time)

    t2 = time.time()
    send_file(config.container_info['mount_dir'], config.target_ip, True)
    t3 = time.time()
    send_info(config.container_info, config.target_ip, 'container_info')
    t4 = time.time()
    cmd_run(f'podman container checkpoint test -e {config.checkpoint_path}', True)
    t5 = time.time()
    send_file(config.checkpoint_path, config.target_ip, is_dir=False)
    t6 = time.time()
    ans = send_info({'info': 'done'}, config.target_ip, 'migrate')
    t7 = time.time()
    


if __name__ == '__main__':
    ck, _ = cmd_run('whoami', True)
    # print(ck, type(ck))
    if 'root' not in ck:
        raise Exception('please run with root')
    main()
