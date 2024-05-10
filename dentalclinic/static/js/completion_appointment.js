


function set_state(order_id){
    let data = {
        'id': order_id,
        'value': 5
    }

    fetch(BASE_URL + `set_order_status/`, {
        method: "POST",
        body: JSON.stringify(data),
        headers: {
            'Content-Type': 'application/json',
            "X-CSRFToken": getCsrfToken()
        }
    })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            window.location.reload()
        })
        .catch(error => {
            console.error("Ошибка:" + error);
        });
}

function getCsrfToken() {
    const csrfTokenElement = document.getElementsByName('csrfmiddlewaretoken')[0];
    return csrfTokenElement ? csrfTokenElement.value : '';
}

function redirectEditUrl(order_id){
    let resultUrl = `/edit_date/${order_id}`
    window.location.assign(resultUrl);
}
