from datetime import datetime, date, time, timedelta


def get_free_times(appointments: [(datetime, int)], start_time: time, end_time: time) -> (date, [time]):
    def round_datetime(value: datetime):
        result = datetime(value.year, value.month, value.day, value.hour, 0, 0)
        if value.minute >= 30:
            result += timedelta(hours=1)
        else:
            result += timedelta(minutes=30)

        return result

    def get_appointments_in(d: date):
        return list(filter(lambda x: x[0].date() == d, appointments))

    def get_correct_next_time(value: date):
        if value == date.today():
            return 'сегодня'
        if value == date.today() + timedelta(days=1):
            return 'завтра'

        return f'{value.day} ' + get_month(value)

    dt = round_datetime(datetime.now())
    result = get_free_times_in_day(dt.date(), get_appointments_in(dt.date()), max(start_time, dt.time()), end_time)
    while not result:
        dt += timedelta(days=1)
        result = get_free_times_in_day(dt.date(), get_appointments_in(dt.date()), start_time, end_time)

    return get_correct_next_time(dt.date()), [datetime.combine(dt, t) for t in result]


def get_free_times_in_day(d: date, appointments: [(datetime, int)], start_time: time, end_time: time):
    result = []

    d = datetime.combine(d, start_time)
    while d.time() < end_time:
        result.append(d.time())
        d += timedelta(minutes=30)

    for appointment in appointments:
        start_appointment = (appointment[0] - timedelta(minutes=30)).time()
        end_appointment = (appointment[0] + timedelta(minutes=appointment[1])).time()

        result = list(filter(lambda x: x >= end_appointment or x <= start_appointment, result))

    return result


def get_month(date: datetime):
    return ['января', 'февраля', 'марта', 'апреля', 'мая', 'июня', 'июля', 'августа', 'сентября', 'октября',
                'ноября', 'декабря'][date.month]


def get_week(date: datetime):
    return ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"][date.weekday()]
