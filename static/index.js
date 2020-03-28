document.addEventListener('DOMContentLoaded', () => {
  var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);
  socket.on('connect', () => {
    document.querySelector('#new-message').onsubmit = () =>{
      const message = document.querySelector('#message').value;
      socket.emit('new message', {'message':message});
      document.querySelector('#message').value ='';
      return false
      };
    });

   socket.on('announce message', data => {
      const li = document.createElement('li');
      li.innerHTML= `${data.user} Said: ${data.message}`;
      document.querySelector('#messages').append(li);

    });
    socket.on('announce joined', data => {
      alert(`${data.user} joined`)
    });
  });
