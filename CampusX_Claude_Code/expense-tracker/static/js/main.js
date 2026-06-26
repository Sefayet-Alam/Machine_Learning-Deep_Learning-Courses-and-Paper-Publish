// main.js — students will add JavaScript here as features are built

document.addEventListener("DOMContentLoaded", function () {
    var flashes = document.querySelectorAll(".flash");
    flashes.forEach(function (el) {
        setTimeout(function () {
            el.style.transition = "opacity 0.4s";
            el.style.opacity = "0";
            setTimeout(function () { el.remove(); }, 400);
        }, 5000);
    });
});
