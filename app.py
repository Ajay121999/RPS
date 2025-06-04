from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'secret!')
socketio = SocketIO(app, cors_allowed_origins="*")

players = {}
moves = {}

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('join')
def handle_join(data):
    name = data['name']
    players[request.sid] = name
    emit('status', {'msg': f'{name} joined the game.'}, broadcast=True)

@socketio.on('move')
def handle_move(data):
    player = players[request.sid]
    move = data['move']
    moves[request.sid] = move
    emit('status', {'msg': f'{player} has made their move.'}, broadcast=True)

    if len(moves) == 2:
        sids = list(moves.keys())
        p1, p2 = sids[0], sids[1]
        m1, m2 = moves[p1], moves[p2]
        result = get_result(m1, m2)

        emit('result', {
            'p1': players[p1], 'p1_move': m1,
            'p2': players[p2], 'p2_move': m2,
            'result': result
        }, broadcast=True)

        moves.clear()

def get_result(m1, m2):
    if m1 == m2:
        return "It's a draw!"
    wins = {'rock': 'scissors', 'paper': 'rock', 'scissors': 'paper'}
    return "Player 1 wins!" if wins[m1] == m2 else "Player 2 wins!"

if __name__ == '__main__':
    socketio.run(app, port=5000, host="0.0.0.0")
