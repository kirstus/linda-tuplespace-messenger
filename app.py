#!flask/bin/python
from flask import Flask, jsonify, request
from server import Servidor

app = Flask(__name__)

@app.route('/messenger/topics/<string:topic_name>', methods=['PUT'])
def send_msg(topic_name):
    if 'passwd' not in request.json or request.json['passwd'] == '':
        return 'É necessário ser o autor da mensagem para envia-la!'
    if 'author' not in request.json or request.json['author'] == '':
        return 'É necessário um autor da mensagem para envia-la!'
    if 'topic' not in request.json or request.json['topic'] == '':
        return 'É necessário um tópico da mensagem para envia-la!'
    elif request.json['topic'] != topic_name:
        return 'Tópico do camingo não coincide com tópico na tupla!'
    if 'msg' not in request.json or request.json['msg'] == '':
        return 'É necessário o corpo da mensagem para envia-la!'
    t = []
    passwd = request.json['passwd']
    t.append(request.json['author'])
    t.append(request.json['topic'])
    t.append(request.json['msg'])
    t.append(0)
    t.append(0)
    r = s.send_msg(tuple(t), passwd)
    return 'ok'

@app.route('/messenger/topics/<string:topic_name>/<int:msg_id>', methods=['DELETE'])
def delete_msg(topic_name, msg_id):
    if 'passwd' not in request.json:
        return 'É necessário ser o autor da mensagem para deleta-la!'
    passwd = request.json['passwd']
    r = s.delete_msg(topic_name,msg_id,passwd)
    if r != False:
        return str(r)
    else:
        return 'Falha na remoção da mensagem.'

@app.route('/messenger/topics/<string:topic_name>', methods=['GET'])
def get_messages(topic_name):
    r = s.get_messages(topic_name)
    return jsonify(r)

@app.route('/messenger/authors', methods=['GET'])
def get_authors():
    r = s.get_authors()
    return jsonify(r)

@app.route('/messenger/topics', methods=['GET'])
def get_topics():
    r = s.get_topics()
    return jsonify(r)

if __name__ == '__main__':
    print('main')
    s = Servidor()
    print(s)
    app.run(debug=False, port='5000')
