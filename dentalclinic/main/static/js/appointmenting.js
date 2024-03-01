
const specialistButton = document.getElementById('specialist-button');
const serviceButton = document.getElementById('service-button');
const dateButton = document.getElementById('date-button');


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
    redirect_url('select_service');
});

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

    resultUrl += 'd-1';
    console.log(resultUrl);

    window.location.assign(resultUrl);
}