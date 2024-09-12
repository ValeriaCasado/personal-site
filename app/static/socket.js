function drawNextRow(row_idx, row_values) {
    for (let px = 0; px < window.WIDTH; px++) {

        pixel_iteration = row_values[px]

        const hue = (360 * pixel_iteration) / window.MAX_ITERATIONS;
        const saturation = 100;
        const lightness = iteration < window.MAX_ITERATIONS ? 50 : 0;

        const color = `hsl(${hue}, ${saturation}%, ${lightness}%)`;

        ctx.fillStyle = color;
        ctx.fillRect(px, row_idx, 1, 1);
    }
}

var DRAWING = false;

window.addEventListener("load",function(event) {

    socket.emit("coordinates", {
        'x': coords[0],
        'y': coords[1]
    });
    
    console.log("Do we have the globals?");
    console.log(window.WIDTH);

    const socket = io({autoConnect: true});

    function getCursorPosition(canvas, event) {
        const rect = canvas.getBoundingClientRect();
        const x = event.clientX - rect.left;
        const y = event.clientY - rect.top;
        return [x, y];
    }

    canvas.addEventListener('mousedown', function(e) {
        var coords = getCursorPosition(canvas, e);
        console.log("x: " + coords[0] + " y: " + coords[1]);
        if (DRAWING==false) {
            socket.emit("coordinates", {
                'x': coords[0],
                'y': coords[1]
            });
        }
    })

    socket.on("draw_row", function(data) {
        DRAWING = true;

        var row_idx = data['row_idx'];
        var values = data['values'];

        if (row_idx==window.WIDTH-1) {
            DRAWING = false;
        }
        console.log(row_idx);
    })

    socket.on("stop_drawing", function() {
        DRAWING = false;
    })

},false);