function calendarGridElement(children, disabled = false, extraClass = ''){
    const dayCell = document.createElement('div');
    const dayButton = document.createElement('button');

    dayButton.classList.add('calender-grid-element-button');
    dayButton.textContent = children;

    disabled && dayButton.setAttribute('disabled', 'disabled');
    extraClass && dayButton.classList.add(extraClass);

    dayCell.classList.add('calender-grid-element');
    dayCell.appendChild(dayButton);

    return dayCell;
}

function calendarGridButton(date, disabled = false, extraClass = ''){
    const result = calendarGridElement(date.getDate(), disabled, extraClass);

    result.setAttribute('datetime', Date.parse(date));
    result.addEventListener('click', () => {
        setDay(date);
    });

    return result;
}

const daysOfWeek = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс'];

const monthTitle = document.getElementById('month-title');
const previousButton = document.getElementById('previous-month-button');
const nextButton = document.getElementById('next-month-button');

const calendarGrid = document.getElementById('calender-grid')
const timesGrid = document.getElementById('times-grid');

const today = new Date();
let selectDate = new Date(today.getFullYear(), today.getMonth(), today.getDate());

const daysOfWeekHTML = () => {
    calendarGrid.innerHTML = '';

    const childs = daysOfWeek.map((element) => calendarGridElement(element));
    for (const child of childs){
        calendarGrid.appendChild(child);
    }
};

function initDates(){
    previousButton.addEventListener('click', () => {
       setMonth(-1);
    });

    nextButton.addEventListener('click', () => {
       setMonth(1);
    });

}

function generateCalendar(refresh = false) {
    !refresh && selectDate.setDate((selectDate.getMonth() === today.getMonth()) ?
        isSelectedDate() ? selectedDate.getDate() : today.getDate()
        :
        1);

    const firstDayOfMonth = new Date(selectDate.getFullYear(), selectDate.getMonth(), 0).getDay();
    const adjustedFirstDay = (firstDayOfMonth + 6) % 7;

    const daysInPreviousMonth = new Date(selectDate.getFullYear(), selectDate.getMonth(), 0).getDate();
    const daysInMonth = new Date(selectDate.getFullYear(), selectDate.getMonth() + 1, 0).getDate();

    monthTitle.innerHTML = capitalize(selectDate.toLocaleString('ru-RU', { month: 'long' }));
    daysOfWeekHTML();

    if (adjustedFirstDay < 6){
        for (let i = adjustedFirstDay; i >= 0; i--) {
            const disabled = new Date(selectDate.getFullYear(), selectDate.getMonth() - 1, daysInPreviousMonth - i) < today;
            calendarGrid.appendChild(calendarGridButton(new Date(selectDate.getFullYear(), selectDate.getMonth() - 1, daysInPreviousMonth - i), disabled));
        }
    }

    for (let day = 1; day <= daysInMonth; day++) {
        const disabled = selectDate.getMonth() === today.getMonth() && day < today.getDate();
        calendarGrid.appendChild(calendarGridButton(new Date(selectDate.getFullYear(), selectDate.getMonth(), day), disabled, day === selectDate.getDate() ? 'selected' : ''));
    }

    if (refresh){
        selectedDate = null;
    }

    generateTimes();
}

function setMonth(direction){
    selectDate.setMonth(selectDate.getMonth() + direction);

    const selectedMonth = selectDate.getFullYear() * 12 + selectDate.getMonth()
    const todayMonth = today.getFullYear() * 12 + today.getMonth()

    if (selectedMonth <= todayMonth){
        previousButton.setAttribute("disabled", "disabled");
    }
    else{
        previousButton.removeAttribute("disabled")
    }

    if (selectedMonth >= todayMonth + 10){
        nextButton.setAttribute("disabled", "disabled");
    }
    else{
        nextButton.removeAttribute("disabled")
    }

    generateCalendar();
}

function setDay(value){
    selectDate = value;

    generateCalendar(true);
}

// TIMES
function generateTimesElement(time, extraClass){
    const element = document.createElement('button');

    element.classList.add('time-el');
    element.textContent = time;

    extraClass && element.classList.add(extraClass);

    let time_parts = time.split(':').map(element => parseInt(element));
    const date = new Date(selectDate.getFullYear(), selectDate.getMonth(), selectDate.getDate(), time_parts[0], time_parts[1]);

    element.setAttribute('datetime', Date.parse(date));
    element.addEventListener('click', () => {
        setTime(date);
    });

    refreshTimes();

    return element;
}

function generateTimes(){
    timesGrid.innerHTML = '';

    const date = [selectDate.getFullYear(), selectDate.getMonth() + 1, selectDate.getDate()].join('/');
    const specialist = selectedSpecialistId;

    console.log(date, selectedSpecialistId);

    const response = fetchData(`get_times/${selectedSpecialistId}/${date}`);
    response.then(result => {

        for (const time of result.times){
            const element = generateTimesElement(time);
            timesGrid.appendChild(element);
        }

        refreshNextButton();

    }).catch(error => {
        console.error(error);
    });
}

function refreshTimes(){
    const timeElements = timesGrid.getElementsByClassName('time-el')
    for (const timeElement of timeElements){
        const date = parseInt(timeElement.getAttribute('datetime'))

        timeElement.classList.toggle('selected', isSelectedDate() && date === selectedDate.getTime());
    }

    refreshNextButton();
}

function setTime(date){
    console.log(`set date from ${selectedDate} to ${date}`);
    selectedDate = date;
    refreshTimes();
}
