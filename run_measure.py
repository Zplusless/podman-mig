from flask import Flask
import threading

from measure import Measure



app = Flask(__name__)


# flag = {'end':False, 'data':[], 'id':None}

        




   
data = {'data': Measure()}


@app.route('/start/<int:log_id>/')
def start(log_id):
    m = data['data']
    m.init(log_id)

    p = threading.Thread(target=m.task)  #! 此处只能用Thread不能用Process，因为新的进程就是额外一套资源，不共享变量
    p.start()

    return 'start'



@app.route('/end/')
def end():
    m = data['data']
    m.end()

    m.write_data(node_id='1')

    return 'done'

if __name__ == "__main__":
    app.run('0.0.0.0', port=8000)