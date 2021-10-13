# destination node

import time
from flask import Flask, request
app = Flask(__name__)

from call_cmd import cmd_run

INFO = {'info' : None}

@app.route('container_info', methods=['POST'])
def recieve_data():

    INFO['info'] = dict(request.form)

    image = request.form.get('image')
 
    cmd_run(f'podman pull {image}', True)


    return 'done'



@app.route('migrate', methods=['POST'])
def recieve_data():
    
    t1 = time.time()
    image = request.form.get('image')
 
    cmd_run(f"podman container restore -i {INFO['info']['chkpt_path']}", True)
    t2 = time.time()

    return f'{t1},{t2}'



if __name__ == '__main__':
    ck, _ = cmd_run('whoami', True)
    if 'root' not in ck:
        raise Exception('please run with root')
    
    app.run('0.0.0.0', port=8000)