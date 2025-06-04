let socket = io();
let playerName = '';

function joinGame() {
  playerName = document.getElementById('name').value;
  if (playerName.trim()) {
    socket.emit('join', { name: playerName });
    document.getElementById('game').style.display = 'block';
  }
}

function sendMove(move) {
  socket.emit('move', { move: move });
}

socket.on('status', function(data) {
  document.getElementById('status').innerText = data.msg;
});

socket.on('result', function(data) {
  document.getElementById('result').innerText =
    `${data.p1} chose ${data.p1_move}, ${data.p2} chose ${data.p2_move} → ${data.result}`;
});
