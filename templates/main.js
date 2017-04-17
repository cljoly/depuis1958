function toggle(element, query) {
    var elementList = document.querySelectorAll(query);
    for (var i = 0, len = elementList.length; i < len; i++) {
        if (elementList[i].style.display == "none") {
            elementList[i].style.display = "";
            element.innerHTML = "▲ Voir moins";
        } else {
            elementList[i].style.display = "none";
            element.innerHTML = "▼ Voir tout";
        }
    }
}

function setup() {
    // Click all hide buttons
    var elementList = document.getElementsByClassName('hide-button');
    for (var i = 0, len = elementList.length; i < len; i++) {
        elementList[i].click()
    }
}

document.addEventListener("DOMContentLoaded", function(event) {
    setup();
});

