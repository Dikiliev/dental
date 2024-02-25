const workerCards = document.getElementsByClassName('worker-card');

let selectedSpecialistId = -1;

init();



function init(){
    for (const card of workerCards) {
        card.addEventListener('click', () => {
            selectSpecialist(card.id);
        });
    }

}

function selectSpecialist(id){
    if (id === selectedSpecialistId){
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

function selectTime(specialist_id, )

function unselectAll(){
    for (const card of workerCards) {
        card.classList.toggle('selected', false)
    }
}

function enableNextButton(value){

}