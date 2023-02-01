function hideColumn(classNames, columnNumber) {
    var selector = document.querySelectorAll(classNames + ' tr > *:nth-child(' + columnNumber + ')');
    for(let i=0; i < selector.length; i++) {
        selector[i].style.display = (selector[i].style.display == "none") ? "table-cell" : "none";
    }
}