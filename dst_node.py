# destination node

import time
import threading
from flask import Flask, request
app = Flask(__name__)

from call_cmd import cmd_run
from measure import Measure

import config


data = {'data': Measure()}
INFO = {'info' : None}

@app.route('/container_info/', methods=['POST'])
def recieve_data():


    #todo 此处暂时使用配置文件，后续应该改成传输数据
    if config.is_test:
        INFO['info'] = dict(request.form)

        image = request.form.get('image')
    
        cmd_run(f'podman pull {image}', True)

    else:
        cmd_run(f'podman pull platpus/javafx', True)

    return 'done'



@app.route('/migrate/', methods=['POST'])
def migrate():
    
    t1 = time.time()
    # image = request.form.get('image')
    if config.is_test:
        cmd = f"podman container restore -i {INFO['info']['chkpt_path']}"
        print('CMD:  ', cmd)
        ans, t = cmd_run(cmd, True)
        print('RESTORE:  ', ans)
    else:
        cmd = f"podman container restore -i {config.game_chkpt_path}"
        ans, t = cmd_run(cmd, True)

        cmd = f"podman container restore -i {config.ga_chkpt_path}"
        ans, t = cmd_run(cmd, True)

    t2 = time.time()

    return f'{t1},{t2}'


@app.route('/init/')
def init():
    cmd_run('podman rm -f $(podman ps -aq)', True)
    cmd_run('rm -r /tmp/podman/test/*', False)
    cmd_run('rm -r /tmp/podman/*.tar.gz', True)
    return 'done'



@app.route('/start/<int:log_id>/')
def start(log_id):
    m = data['data']
    m.init(log_id)

    p = threading.Thread(target=m.task)
    p.start()

    return 'start'



@app.route('/end/')
def end():
    m = data['data']
    m.end()

    m.write_data(node_id='2')

    cmd_run('podman rm -f $(podman ps -aq)', False)

    return 'done'




if __name__ == '__main__':
    ck, _ = cmd_run('whoami', True)
    if 'root' not in ck:
        raise Exception('please run with root')
    
    app.run('0.0.0.0', port=8000)