const workerCards = document.getElementsByClassName('worker-card');
const cardPrefix = 'worker-card-';
const timeButtonPrefix = 'time-button-'
let selectedTime = null;

initSpecialist();


function initSpecialist(){
    for (const card of workerCards) {
        card.getElementsByClassName('worker')[0].addEventListener('click', () => {
            selectSpecialist(card.id.replace(cardPrefix, ''));
        });

        const timeButtons = card.getElementsByClassName('time-button')
        for (const timeButton of timeButtons){
            timeButton.addEventListener('click', () => {
                selectTime(card.id.replace(cardPrefix, ''), timeButton.name)
            })
        }
    }

    const selectElement = document.getElementById(cardPrefix + selectedSpecialistId);

    if (selectElement){
        selectElement.classList.toggle('selected', true);
    }

    refreshNextButton();
}

function selectSpecialist(id, force=false){
    if (!force && id === selectedSpecialistId){
        selectedSpecialistId = -1
    }
    else{
        selectedSpecialistId = id;
    }

    console.log(selectedSpecialistId);
    unselectAll();
    const selectElement = document.getElementById(cardPrefix + selectedSpecialistId);

    if (selectElement){
        selectElement.classList.toggle('selected', true);
    }

    refreshNextButton();
}

function selectTime(specialist_id, datetime){
    console.log('selectTime ' + specialist_id + ' ' + datetime)
    if (specialist_id === selectedSpecialistId && datetime === selectedTime){
        selectedTime = null
    }
    else{
        selectedSpecialistId = specialist_id;
        selectedTime = datetime;
    }

    unselectAll();
    const selectElement = document.getElementById(cardPrefix + selectedSpecialistId);
    if (selectElement){
        selectElement.classList.toggle('selected', true);

        const timeButton = selectElement.querySelector(`[name="${selectedTime}"]`)

        if (timeButton){
            timeButton.classList.toggle('selected', true)
        }
    }

    refreshNextButton();
}

function unselectAll(){
    for (const card of workerCards) {
        card.classList.toggle('selected', false)

        const timeButtons = card.getElementsByClassName('time-button')
        for (const timeButton of timeButtons){
            timeButton.classList.toggle('selected', false)
        }

    }
}

function refreshNextButton(){
    const bottomMenu = document.getElementById('bottom-menu')
    bottomMenu.classList.toggle('disabled', selectedSpecialistId === -1);
}