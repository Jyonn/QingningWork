var VELOCITY = 1,
    PARTICLES = 50,
    particles = [],
    colors = [
        "#019AA0",
        "#AFD693",
        "#FCE680",
        "#F2AE25",
        "#CF181D",
    ],
    canvas = document.getElementById('bg-canvas'),
    context;

if (canvas && canvas.getContext) {
    context = canvas.getContext('2d');

    for(var i = 0; i < PARTICLES; i++ ) {
        particles.push( {
            x: Math.random()*window.innerWidth,
            y: Math.random()*window.innerHeight,
            vx: ((Math.random()*(VELOCITY*2))-VELOCITY),
            vy: ((Math.random()*(VELOCITY*2))-VELOCITY),
            size: 1+Math.random()*3,
            color: colors[ Math.floor(Math.random()*colors.length)]
        } );
    }

    Initialize();
}

function Initialize() {
    window.addEventListener('resize', ResizeCanvas, false);
    setInterval( TimeUpdate, 40 );

    ResizeCanvas();
}

function TimeUpdate() {
    context.clearRect(0, 0, window.innerWidth, window.innerHeight);
    const len = particles.length;
    var particle, i;

    for(i = 0; i < len; i++ ) {
        particle = particles[i];

        particle.x += particle.vx;
        particle.y += particle.vy;

        if (particle.x > window.innerWidth) {
            particle.vx = -VELOCITY - Math.random();
        }
        else if (particle.x < 0) {
            particle.vx = VELOCITY + Math.random();
        }
        else {
            particle.vx *= 1 + (Math.random() * 0.005);
        }

        if (particle.y > window.innerHeight) {
            particle.vy = -VELOCITY - Math.random();
        }
        else if (particle.y < 0) {
            particle.vy = VELOCITY + Math.random();
        }
        else {
            particle.vy *= 1 + (Math.random() * 0.005);
        }

        context.fillStyle = particle.color;
        context.beginPath();
        context.arc(particle.x, particle.y, particle.size, 0, Math.PI*2, true);
        context.closePath();
        context.fill();
    }
}

function ResizeCanvas() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
}