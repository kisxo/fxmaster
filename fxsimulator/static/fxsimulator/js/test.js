let socketio = io();

socketio.on('connect', () => {
    console.log("connected")
});

socketio.on("message", (data) => {
    console.log(data.data);
});

