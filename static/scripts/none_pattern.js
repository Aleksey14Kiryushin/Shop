const C = document.querySelector("canvas"),
  $ = C.getContext("2d"),
  W = (C.width = window.innerWidth),
  H = (C.height = window.innerHeight);

function draw() {
    $.fillStyle = "rgba(255, 255, 255, 0.1)";
    $.fillRect(0, 0, W, H);
    $.fillStyle = "#ffffff";
}

setInterval(draw, 123);

window.addEventListener("resize", () => location.reload());
