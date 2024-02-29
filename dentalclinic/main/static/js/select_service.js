const serviceCards = document.getElementsByClassName('service-card');

let selectedServiceIds = [];



function initService(){
    console.log(services);

    for (const card of serviceCards) {
        card.addEventListener('click', () => {
            selectService(card.id);
        });
    }

    refreshNextButton();
}

function selectService(id){
    const selectElement = document.getElementById(id);

    if (selectedServiceIds.includes(id)){
        selectedServiceIds = selectedServiceIds.filter(item => item !== id)
    }
    else{
        selectedServiceIds.push(id);
    }

    selectElement.classList.toggle('selected', selectedServiceIds.includes(id))
    refreshNextButton();
}

function refreshNextButton(){
    const bottomMenu = document.getElementById('bottom-menu')
    bottomMenu.classList.toggle('disabled', selectedServiceIds.length === 0);
}