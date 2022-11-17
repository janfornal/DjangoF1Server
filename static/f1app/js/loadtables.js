function getResourceAddress(entity, resource_name, resource_type) {
    return `http://localhost:8000/f1app/${entity}/${resource_name}/${resource_type}/`
}

function getEntity() {
    return document.getElementById('entity_name').textContent
}

function loadDoc(resource_name, div_id) {
    fetch(getResourceAddress(getEntity(), resource_name, div_id)).then((response)=>response.text())
        .then((data)=>document.getElementById(div_id).innerHTML = data)
}

function collapsePanel(resource_name, item) {
    console.log(item)
    let sibling = item.siblings('.panel-collapse')
    if(sibling.hasClass('active') == false) {
        loadDoc(resource_name, $(sibling)[0].id)
        sibling.addClass('active')
        sibling.show()
    }
    else {
        sibling.removeClass('active')
        sibling.hide()
    }
}