const workerCards = document.getElementsByClassName('worker-card');
const cardPrefix = 'worker-card-';
const timeButtonPrefix = 'time-button-'
let selectedSpecialistId = -1;
let selectedTime = null;

init();



function init(){
    for (const card of workerCards) {
        card.getElementsByClassName('worker')[0].addEventListener('click', () => {
            selectSpecialist(card.id);
        });

        const timeButtons = card.getElementsByClassName('time-button')
        for (const timeButton of timeButtons){
            timeButton.addEventListener('click', () => {
                selectTime(card.id, timeButton.name)
            })
        }
    }

}

function selectSpecialist(id, force=false){
    if (!force && id === selectedSpecialistId){
        selectedSpecialistId = -1
    }
    else{
        selectedSpecialistId = id;
    }


    unselectAll();
    const selectElement = document.getElementById(selectedSpecialistId);

    if (selectElement){
        selectElement.classList.toggle('selected', true);
    }
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
    const selectElement = document.getElementById(selectedSpecialistId);
    if (selectElement){
        selectElement.classList.toggle('selected', true);

        const timeButton = selectElement.querySelector(`[name="${selectedTime}"]`)

        if (timeButton){
            timeButton.classList.toggle('selected', true)
        }
    }
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

function enableNextButton(value){

}