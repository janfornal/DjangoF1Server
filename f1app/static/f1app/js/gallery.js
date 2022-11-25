const classes = ['.left-image', '.middle-image', '.right-image']
var currentIndex = 0

for(let i=0; i<3; i++) {
    var elements = document.querySelectorAll(classes[i]);
    if (elements[currentIndex + i]) {
        elements[currentIndex + i].style.display = "block";
    }
}

function plusSlides(number) {
    console.log('called')
    currentIndex += number
    for(let i=0; i<3; i++) {
        var elements = document.querySelectorAll(classes[i])
        elements.forEach((x) => x.style.display = "none")
        if (elements[currentIndex + i]) {
            elements[currentIndex + i].style.display = "block";
        }
    }
}