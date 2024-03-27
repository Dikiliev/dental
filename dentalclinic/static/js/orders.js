
const statusSwitchers = document.getElementsByClassName('order-status-switcher');

const button = (name, text, onclick) => {
    const el = document.createElement('button');
    el.classList.add('switch-button');
    el.name = `${name}`;
    el.innerHTML = text;

    el.addEventListener('click', () => {
       onclick();
    });
    return el;
};
const cancelButtonHtml = (switcher) => button('cancel', 'Отменить', () => {
    set_order_status(switcher, 5);
})
const acceptButtonHtml  = (switcher) => button('accept', 'Принять', () => {
    set_order_status(switcher, 2);
})
const processButtonHtml  = (switcher) => button('process', 'В&nbsp;процессе', () => {
    set_order_status(switcher, 3);
})
const finishButtonHtml  = (switcher) => button('finish', 'Завершить', () => {
    set_order_status(switcher, 4);
})

initOrders();


function initOrders(){
    for (const switcher of statusSwitchers){
        initOrder(switcher);
    }
}

function initOrder(switcher){
    if (!switcher){
        return;
    }

    refreshSwitcher(switcher);
}

function refreshSwitcher(switcher){
    switcher.innerHTML = '';

    switch (+switcher.dataset.status){
        case 1:
            switcher.appendChild(cancelButtonHtml(switcher));
            switcher.appendChild(acceptButtonHtml(switcher));
            break;
        case 2:
            switcher.appendChild(cancelButtonHtml(switcher));
            switcher.appendChild(processButtonHtml(switcher));
            break;
        case 3:
            switcher.appendChild(cancelButtonHtml(switcher));
            switcher.appendChild(finishButtonHtml(switcher));
            break;
    }

    switcher.classList.toggle('disabled', !switcher.innerHTML)

    const statusText = document.getElementById(switcher.id.replace('switcher-', 'status-'));
    statusText.innerHTML = [`Создан`, `Принят`, `В процессе`, `Завершен`, `Отменен`][+switcher.dataset.status - 1];
    statusText.classList.toggle('error', +switcher.dataset.status === 5);
}

function set_order_status(switcher, value){
    switcher.dataset.status = value;
    refreshSwitcher(switcher);

    set_state(+switcher.id.replace('switcher-', ''), value);
}



function set_state(order_id, value){
    let data = {
        'id': order_id,
        'value': value
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
        })
        .catch(error => {
            console.error("Ошибка:" + error);
        });
}

function getCsrfToken() {
    const csrfTokenElement = document.getElementsByName('csrfmiddlewaretoken')[0];
    return csrfTokenElement ? csrfTokenElement.value : '';
}