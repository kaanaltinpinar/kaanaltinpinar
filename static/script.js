console.log("Flight Operations Dashboard loaded.");
function openFlightOperations() {
    document.getElementById("flightModal").classList.add("show");
}

function closeFlightOperations() {
    document.getElementById("flightModal").classList.remove("show");
}

function startSimulation() {

    const aircraft = document.getElementById("aircraft").value;
    const departure = document.getElementById("departure").value;
    const destination = document.getElementById("destination").value;
    const passengers = document.getElementById("passengers").value;
    const fuel = document.getElementById("fuel").value;
    const weather = document.getElementById("weather").value;

    if (!aircraft || !departure || !destination) {
        alert("Lütfen uçak, kalkış ve varış meydanını seçin.");
        return;
    }

    if (departure === destination) {
        alert("Kalkış ve varış meydanı aynı olamaz.");
        return;
    }

    const params = new URLSearchParams({
        aircraft,
        departure,
        destination,
        passengers,
        fuel,
        weather
    });

    window.location.href = "/simulate?" + params.toString();
}
const plane = document.getElementById("plane");

let currentX = window.innerWidth / 2;
let currentY = window.innerHeight * 0.18;

let targetX = currentX;
let targetY = currentY;

document.addEventListener("mousemove", function(event) {

    targetX = event.clientX;
    targetY = event.clientY;

});

function animatePlane() {

    currentX +=
        (targetX - currentX) * 0.055;

    currentY +=
        (targetY - currentY) * 0.055;

    const dx =
        targetX - currentX;

    const dy =
        targetY - currentY;

    const angle =
        Math.atan2(dy, dx)
        * 180 / Math.PI + 90;

    plane.style.left =
        currentX + "px";

    plane.style.top =
        currentY + "px";

    plane.style.transform =
        `translate(-50%, -50%)
         rotate(${angle}deg)`;

    requestAnimationFrame(
        animatePlane
    );
}

animatePlane();