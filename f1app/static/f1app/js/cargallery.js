let data = JSON.parse(
    document.currentScript.nextElementSibling.textContent
);

let dataIndex = 1;
if (data.length > 0) {
    showSlides(dataIndex);
}
else {
    let links = document.getElementsByClassName("gallery-link");
    for(let i=0; i<links.length; i++) {
        console.log(links[i])
        links[i].style.display = "none";
    }
}

// Next/previous controls
function plusSlides(n) {
    showSlides(dataIndex += n);
}

function showSlides(n) {
    let slides = document.getElementsByClassName("car-slide");
    let comments = document.getElementsByClassName("car-comment");
    let images = document.getElementsByClassName("car-image");
    if (n > data.length) {dataIndex = 1;}
    if (n < 1) {dataIndex = data.length;}
    slides[0].style.display = "block";
    images[0].src = data[dataIndex - 1].photo;
    comments[0].textContent = data[dataIndex - 1].name + ' from ' + data[dataIndex - 1].debut?.year;
}

function orderByAge() {
    data.sort((x, y) => x.debut?.year - y.debut?.year);
    showSlides(dataIndex = 1);
}

function orderByWins() {
    data.sort((x, y) => y.wins - x.wins);
    showSlides(dataIndex = 1);
}