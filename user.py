# user


from flask import Flask, request
app = Flask(__name__)

from call_cmd import cmd_run




@app.route('/connect/', methods=['POST'])
def recieve_data():


    ip = request.form.get('ip')
    cmd = f'bash script/run_ga_client.sh {ip}'
    cmd_run(cmd, True)


    return 'done'


@app.route('/end/', methods=['POST'])
def recieve_data():

    cmd = f'bash script/kill_ga_client.sh'
    cmd_run(cmd, True)
    return 'done'





if __name__ == '__main__':
    ck, _ = cmd_run('whoami', True)
    # if 'root' not in ck:
    #     raise Exception('please run with root')
    
    app.run('0.0.0.0', port=8000)