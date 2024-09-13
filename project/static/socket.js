const WIDTH = 1000;
const HEIGHT = WIDTH;
const THRESHOLD = 200; 

var IS_DRAWING = false;

window.addEventListener("load",function(event) {

    canvas.width = WIDTH;
    canvas.height = HEIGHT;

    const socket = io({autoConnect: true});
    reset_mandlebrot(socket);

    const ctx = canvas.getContext("2d");

    canvas.addEventListener('mousedown', function(e) {
        var coords = getCursorPosition(canvas, e);
        console.log("x: " + coords[0] + " y: " + coords[1]);
        if (IS_DRAWING==false) {
            socket.emit("new_mandlebrot", {
                'range': window.C,
                'coordinates': coords
            });
        }
    })

    socket.on("draw_row", function(data) {
        IS_DRAWING = true;
        var i = data['row_idx'];
        var values = data['values'];
        if (i==window.WIDTH-1) {
            IS_DRAWING = false;
        }
        drawNextRow(ctx, i, values);
    });

    socket.on("stop_drawing", function() {
        IS_DRAWING = false;
    });

    socket.on("set_range", function(data) {
        IS_DRAWING = true;
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

    let btn = document.getElementById("save-button"); 
    btn.addEventListener('click', function() {
        if (IS_DRAWING==false) {
            save_new_settings();
            reset_mandlebrot(socket);
        }
    });

},false);

/* Helper functions */

function drawNextRow(ctx, row_idx, row_values) {
    for (let px = 0; px < window.WIDTH; px++) {

        iteration = row_values[px]

        const color = get_color(iteration);

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

function save_new_settings() {
    window.C = {
        'real': [-2.25, 0.75],
        'imaginary': [-1.5, 1.5]
    }
    window.THRESHOLD = parseInt(document.getElementById("threshold").value);
    window.PALETTE = document.getElementById("palette").value;
}


function reset_mandlebrot(socket){
    var threshold = window.THRESHOLD
    socket.emit("new_mandlebrot", {
        'range': window.C,
        'threshold': threshold
    });

}

const hue_ranges = {
    '1': [0, 360],
    '2': [260, 360],
    '3': [200, 300],
    '4': [0, 100],
}

function get_color(iteration) {
    var percentage = iteration / window.THRESHOLD;
    var range = hue_ranges[window.PALETTE]
    var val = (range[1]-range[0]) * percentage + range[0]

    const hue = Math.round(val);
    const saturation = 100;
    const lightness = iteration < window.THRESHOLD ? 50 : 0;

    return `hsl(${hue}, ${saturation}%, ${lightness}%)`;
}