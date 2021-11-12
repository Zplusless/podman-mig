# destination node

import time
import threading
from flask import Flask, request
app = Flask(__name__)

from call_cmd import cmd_run
from measure import Measure


data = {'data': Measure()}
INFO = {'info' : None}

@app.route('/container_info/', methods=['POST'])
def recieve_data():

    INFO['info'] = dict(request.form)

    image = request.form.get('image')
 
    cmd_run(f'podman pull {image}', True)


    return 'done'



@app.route('/migrate/', methods=['POST'])
def migrate():
    
    t1 = time.time()
    # image = request.form.get('image')
    
    cmd = f"podman container restore -i {INFO['info']['chkpt_path']}"
    print('CMD:  ', cmd)
    ans, t = cmd_run(cmd, True)
    print('RESTORE:  ', ans)
    t2 = time.time()

    return f'{t1},{t2}'


@app.route('/init/')
def init():
    cmd_run('podman rm -f $(podman ps -aq)', True)
    cmd_run('rm -r /tmp/podman/test/*', False)
    cmd_run('rm -r /tmp/podman/srvMig.tar.gz', True)
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
    

    #! 启动本地GA
    #nohup bash measure.sh & echo $! > cmd.pid
    cmd_run(f'bash scripts/run_ga_server.sh', False)
    print('ga started')
    time.sleep(3)
    
    app.run('0.0.0.0', port=8000)