
function myaccfunc(id) {
        var x = document.getElementById(id);
        if (x.className.indexOf("w3-show") == -1) {
                x.className += " w3-show";
                x.previousElementSibling.className += " w3-green";
        } else {
                x.className = x
                        .className
                        .replace(" w3-show", "");
                x.previousElementSibling.className = x
                        .previousElementSibling
                        .className
                        .replace(" w3-green", "");
        }
}

function myDropFunc(id) {
        var x = document.getElementById(id);
        if (x.className.indexOf("w3-show") == -1) {
                x.className += " w3-show";
                x.previousElementSibling.className += " w3-green";
        } else {
                x.className = x
                        .className
                        .replace(" w3-show", "");
                x.previousElementSibling.className = x
                        .previousElementSibling
                        .className
                        .replace(" w3-green", "");
        }
}

function w3_open() {
        document
                .getElementById("mySidebar")
                .style
                .width = "100%";
        document
                .getElementById("mySidebar")
                .style
                .display = "block";
}
function w3_close() {
        document
                .getElementById("mySidebar")
                .style
                .display = "none";
}
