const serviceCards = document.getElementsByClassName('service-card');
const serviceIdPrefix = 'service-card-';
function initService(){
    for (const card of serviceCards) {
        card.addEventListener('click', () => {
            selectService(+card.id.replace(serviceIdPrefix, ''));
        });

        card.classList.toggle('selected', selectedServiceIds.includes(+card.id.replace(serviceIdPrefix, '')))
    }

    refreshNextButton();
}

function selectService(id){
    const selectElement = document.getElementById(serviceIdPrefix + id);

    if (selectedServiceIds.includes(id)){
        selectedServiceIds = selectedServiceIds.filter(item => item !== id)
    }
    else{
        selectedServiceIds.push(id);
    }

    selectElement.classList.toggle('selected', selectedServiceIds.includes(id))
    refreshNextButton();

    console.log(selectedServiceIds);
}

function refreshNextButton(){
    const bottomMenu = document.getElementById('bottom-menu')
    bottomMenu.classList.toggle('disabled', selectedServiceIds.length === 0);

    if (selectedServiceIds.length > 0){
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
        bottomHTML += `<button class="button">Выбрать время</button>`
        bottomMenu.innerHTML = bottomHTML;
    }
}