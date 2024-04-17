const serviceCards = document.getElementsByClassName('service-card');
const serviceIdPrefix = 'service-card-';
function initService(){
    for (const card of serviceCards) {
        card.addEventListener('click', () => {
            selectService(+card.id.replace(serviceIdPrefix, ''));
        });

        card.classList.toggle('selected', selectedServiceIds.includes(+card.id.replace(serviceIdPrefix, '')))
    }
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
}
