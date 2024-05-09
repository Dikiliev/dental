const specialistButton = document.getElementById('specialist-button');
const serviceButton = document.getElementById('service-button');
const dateButton = document.getElementById('date-button');

class Page{
    constructor(url, buttonText) {
        this.url = url;
        this.buttonText = buttonText;
    }
}


const pages = {
    0: new Page('select_specialist', 'Выбрать специалиста'),
    1: new Page('select_service', 'Выбрать услугу'),
    2: new Page('select_date', 'Выбрать время'),
    3: new Page('completion_appointment', 'Перейти к оформлению'),
}


if (current_page === 0){
    specialistButton.classList.toggle('active', true);
}
else if (current_page === 1){
    serviceButton.classList.toggle('active', true);
}
else{
    dateButton.classList.toggle('active', true);
}

specialistButton.addEventListener('click', () =>{
    redirect_url('select_specialist');
});

serviceButton.addEventListener('click', () =>{
    redirect_url('select_service');
});

dateButton.addEventListener('click', () =>{
    redirect_url('select_date');
});

const isSelectedSpecialist = () => selectedSpecialistId !== -1;
const isSelectedServices = () => selectedServiceIds.length > 0;
const isSelectedDate = () => selectedDate != null && !isNaN(selectedDate);

function refreshNextButton(){
    const bottomMenu = document.getElementById('bottom-menu');

    let enable = false

    let nextPages = [...Array(4).keys()];
    let completedPages = []

    if (isSelectedSpecialist()){
        completedPages.push(0);
    }
    if (isSelectedServices()){
        completedPages.push(1);
    }
    if (isSelectedDate()){
        completedPages.push(2);
    }

    nextPages = nextPages.filter(page => !completedPages.includes(page));
    const nextPage = pages[nextPages[0]];
    const nextButtonText = nextPage.buttonText;

    switch (current_page){
        case 0:
            enable = isSelectedSpecialist();

            break;
        case 1:
            enable = isSelectedServices();

            if (enable){
                let bottomHTML = '<div class="services-check-info">';
                let total = 0;
                let totalDuration = 0;

                for (const selectedId of selectedServiceIds){
                    const ser = services[selectedId]
                    totalDuration += ser.duration;
                    total += ser.price;

                    bottomHTML += `<span class="services-check-info-p">${ser.title} - ${ser.price}</span>`
                }

                bottomHTML += '</div>'

                bottomHTML += `<span class="service-title">Итого: ${total} ₽ <span class="service-duration">(${totalDuration}) мин.</span></span>`
                bottomHTML += `<button id="next-button" class="button">Выбрать время</button>`
                bottomMenu.innerHTML = bottomHTML;
            }
            break;
        case 2:
            enable = isSelectedDate();
            break;
        default:
            enable = true
    }

    bottomMenu.classList.toggle('disabled', !enable);

    if (enable){
        const bottomNextButton = document.getElementById('next-button');

        if (isEditDate){
            bottomNextButton.innerHTML = 'Сохранить';

            bottomNextButton.onclick = () => {
                set_order_date(order_id, `${selectedDate.getFullYear()}-${selectedDate.getMonth() + 1}-${selectedDate.getDate()}-${selectedDate.getHours()}-${selectedDate.getMinutes()}`);
            };
        }
        else{
            bottomNextButton.innerHTML = nextButtonText;

            bottomNextButton.onclick = () => {
                redirect_url(nextPage.url)
            };
        }
    }
}

function set_order_date(order_id, value){
    let data = {
        'id': order_id,
        'value': value
    }

    console.log(data);

    fetch(BASE_URL + `set_order_date/`, {
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

            if (is_authenticated){
                window.location.assign('/orders');
            }
            else{
                window.location.assign('/');
            }

        })
        .catch(error => {
            console.error("Ошибка:" + error);
        });
}

function getCsrfToken() {
    const csrfTokenElement = document.getElementsByName('csrfmiddlewaretoken')[0];
    return csrfTokenElement ? csrfTokenElement.value : '';
}

function redirect_url(url){
    let resultUrl = `/${url}/${getUrlString()}`

    console.log(`[redirect_url] ${selectedDate}`);
    window.location.assign(resultUrl);
}


function getUrlString(){
    let resultUrl = `m${selectedSpecialistId}s`

    if (selectedServiceIds.length > 0){
        for (const id of selectedServiceIds){
            resultUrl += `${id},`
        }

        resultUrl = resultUrl.slice(0, -1);
    }
    else{
        resultUrl += '-1'
    }

    if (isSelectedDate()){
        resultUrl += `d${selectedDate.getFullYear()}-${selectedDate.getMonth() + 1}-${selectedDate.getDate()}-${selectedDate.getHours()}-${selectedDate.getMinutes()}`
    }
    else{
        resultUrl += 'd-1'
    }

    return resultUrl;
}