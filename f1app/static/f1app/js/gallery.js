let position = 0;

const translationConstraints = {
  duration: 1000,
  fill: 'forwards',
  iterations: 1,
}

function plusSlides(number) {
    let images = document.querySelectorAll('.transition-image');
    oldPos = position
    if(number == -1) position += number;
    images.forEach((image, index) => {
        let translation = [
            { transform: 'translate(-100%, 0%)' },
            { transform: 'translate(' + 100*(-number-1) + '%, 0%)', offset: 1.0 },
        ];
        translation.push({ transform: 'translate(-100%, 0%)' });
        let anim = image.animate(translation, translationConstraints);
        if(index == (position%5 + 5)%5) {
            anim.onfinish = () => {
                if(image.style.order == '') image.style.order = number;
                else image.style.order = parseInt(image.style.order) + number;
            };
        }
    })
    if(number == 1) position += number;
}

// let execute_again = setInterval("plusSlides(1)", 5000);