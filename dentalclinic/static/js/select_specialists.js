const workerCards = document.getElementsByClassName('worker-card');
const cardPrefix = 'worker-card-';
const timeButtonPrefix = 'time-button-'

initSpecialist();


function initSpecialist(){
    for (const card of workerCards) {
        card.getElementsByClassName('worker')[0].addEventListener('click', () => {
            selectSpecialist(+card.id.replace(cardPrefix, ''));
        });

        const timeButtons = card.getElementsByClassName('time-button')
        for (const timeButton of timeButtons){
            const dt = Date.parse(toDate(timeButton.getAttribute('name')));

            timeButton.setAttribute('datetime', dt);
            timeButton.addEventListener('click', () => {
                selectTime(card.id.replace(cardPrefix, ''), dt)
            })
        }
    }

    const selectElement = document.getElementById(cardPrefix + selectedSpecialistId);

    if (selectElement){
        selectElement.classList.toggle('selected', true);
    }
}

function selectSpecialist(id, force=false){
    console.log(`set spec from ${selectedSpecialistId} to ${id}`)

    if (!force && id === selectedSpecialistId){
        selectedSpecialistId = -1
    }
    else{
        selectedSpecialistId = id;
    }
    unselectAll();
    const selectElement = document.getElementById(cardPrefix + selectedSpecialistId);

    if (selectElement){
        selectElement.classList.toggle('selected', true);
    }

    refreshNextButton();
}

function selectTime(specialist_id, datetime){
    console.log(`select time: ${datetime}; previous: ${Date.parse(selectedDate)}; specialist_id: ${specialist_id}`);
    if (specialist_id === selectedSpecialistId && datetime === Date.parse(selectedDate)){
        selectedDate = null
    }
    else{
        selectedSpecialistId = specialist_id;
        selectedDate = new Date(datetime);
    }

    unselectAll();
    const selectElement = document.getElementById(cardPrefix + selectedSpecialistId);
    if (selectElement){
        selectElement.classList.toggle('selected', true);

        const timeButton = selectElement.querySelector(`[datetime="${Date.parse(selectedDate)}"]`)

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