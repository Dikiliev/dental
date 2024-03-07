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
const timesGrid = document.getElementById('');

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
    !refresh && selectDate.setDate((selectDate.getMonth() === today.getMonth()) ? today.getDate() : 1);

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

    const response = fetchData('get_times/15/2024/3/7');
    response.then(result => {
        generateTimes(result.times)
    }).catch(error => {

    });
}

// TIMES
function generateTimesElement(time){
    const element = document.createElement('div');
    const button = document.createElement('button');

    button.classList.add('time-button');
    button.textContent = time;

    // disabled && button.setAttribute('disabled', 'disabled');
    // extraClass && button.classList.add(extraClass);

    element.classList.add('time-el');
    element.appendChild(button);

    return element;
}


function generateTimes(times){
    console.log(times);
    console.log(times[0]);
    // timesGrid.innerHTML = '';

    console.log(times.length)
    for (const time in times){
        console.log(times[i]);

        const element = generateTimesElement(time);
        timesGrid.appendChild(element);
    }
}