const classes = ['.left-image', '.middle-image', '.right-image'];
let indexes = [1, 2, 3];

for(let i=0; i<3; i++) {
    let elements = document.querySelectorAll(classes[i]);
    if (elements[indexes[i] - 1]) {
        elements[indexes[i] - 1].style.display = "block";
    }
}

const leftTranslation = [
  { transform: 'translate(-100%, 0%)' },
];

const rightTranslation = [
  { transform: 'translate(100%, 0%)' },
];

const translationConstraints = {
  duration: 1000,
  iterations: 1,
}

function plusSlides(number) {
    let transitionElements = document.querySelectorAll('.transition-image');
    transitionElements.forEach((x) => x.style.display = "none");
    // if(number == 1) {
    //     transitionElements[indexes[0] - 1].style.display = "block";
    //     document.querySelector('.transition-column').style.order = 0;
    // }
    // if(number == -1) {
    //     transitionElements[indexes[2] - 1].style.display = "block";
    //     document.querySelector('.transition-column').style.order = 1;
    //     document.querySelector('.transition-column').style.transform = "translate(-100%, 0%)";
    // }
    for(let i=0; i<3; i++) {
        indexes[i] += number;
        if (indexes[i] > 5) {indexes[i] = 1;}
        if (indexes[i] < 1) {indexes[i] = 5;}
        let elements = document.querySelectorAll(classes[i]);
        elements.forEach((x) => x.style.display = "none");
        if (elements[indexes[i] - 1]) {
            elements[indexes[i] - 1].style.display = "block";
        }
        // if(number == -1) {
        //     document.querySelector(classes[i]).style.transform = "translate(-100%, 0%)";
        // }
    }
    // if(number == 1) {
    //     document.querySelector('.transition-column').animate(translationConstraints, leftTranslation)
    //     for(let i=0; i<3; i++) {
    //         document.querySelector(classes[i]).animate(transitionConstraints, leftTranslation)
    //     }
    // }
    // if(number == -1) {
    //     document.querySelector('.transition-column').animate(translationConstraints, rightTranslation)
    //     for(let i=0; i<3; i++) {
    //         document.querySelector(classes[i]).animate(transitionConstraints, rightTranslation)
    //     }
    // }
}

// let execute_again = setInterval("plusSlides(1)", 5000);