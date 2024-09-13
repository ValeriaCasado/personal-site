const WIDTH = 1000;
const HEIGHT = WIDTH;
const MAX_ITERATIONS = 200; 

var DRAWING = false;

window.addEventListener("load",function(event) {

    canvas.width = WIDTH;
    canvas.height = HEIGHT;

    const socket = io({autoConnect: true});
    socket.emit("new_mandlebrot");

    const ctx = canvas.getContext("2d");

    canvas.addEventListener('mousedown', function(e) {
        var coords = getCursorPosition(canvas, e);
        console.log("x: " + coords[0] + " y: " + coords[1]);
        if (DRAWING==false) {
            socket.emit("new_mandlebrot", {
                'range': window.C,
                'coordinates': coords
            });
        }
    })

    socket.on("draw_row", function(data) {
        DRAWING = true;
        var i = data['row_idx'];
        var values = data['values'];
        if (i==window.WIDTH-1) {
            DRAWING = false;
        }
        drawNextRow(ctx, i, values);
    });

    socket.on("stop_drawing", function() {
        DRAWING = false;
    });

    socket.on("set_range", function(data) {
        DRAWING = true;
        console.log(data);
        window.C=data;
    });

    socket.on("draw_entire_mandlebrot", function(data) {
        for (let i = 0; i < data.length; i++) {
            
            setTimeout(function() {
                drawNextRow(ctx, i, data[i]);
            }, 0.3);

          }
    });

},false);

/* Helper functions */

function drawNextRow(ctx, row_idx, row_values) {
    for (let px = 0; px < window.WIDTH; px++) {

        iteration = row_values[px]

        const hue = (360 * iteration) / window.MAX_ITERATIONS;
        const saturation = 100;
        const lightness = iteration < window.MAX_ITERATIONS ? 50 : 0;

        const color = `hsl(${hue}, ${saturation}%, ${lightness}%)`;

        ctx.fillStyle = color;
        ctx.fillRect(px, row_idx, 1, 1);
    }
}

function getCursorPosition(canvas, event) {
    const rect = canvas.getBoundingClientRect();
    const x = event.clientX - rect.left;
    const y = event.clientY - rect.top;
    return [Math.round(x), Math.round(y)];
}