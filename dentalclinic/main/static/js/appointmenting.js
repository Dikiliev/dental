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
    const nextPage = nextPages[0];
    const nextButtonText = pages[nextPage].buttonText;

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
        bottomNextButton.innerHTML = nextButtonText;

        bottomNextButton.onclick = () => {
          console.log(nextPage);
        };

    }

}

function redirect_url(url){
    let resultUrl = `/${url}/m${selectedSpecialistId}s`

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
        resultUrl += `d${selectedDate.getFullYear()}-${selectedDate.getMonth()}-${selectedDate.getDate()}-${selectedDate.getHours()}-${selectedDate.getMinutes()}`
    }
    else{
        resultUrl += 'd-1'
    }


    window.location.assign(resultUrl);
}