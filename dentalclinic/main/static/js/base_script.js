BASE_URL = 'http://127.0.0.1:8000/'



function get_text(filename, id){
    fetch(filename)
        .then(response => response.text())
        .then(text => {
            document.getElementById(id).innerHTML = text;
        })
        .catch(error => {
            console.error('Ошибка при загрузке текста:', error);
            document.getElementById(id).innerHTML = 'Ошибка при загрузке текста.'
        });
}


function swipe_menu_response(url){
    url = 'http://127.0.0.1:8000/' + url;
    fetch(url)
        .then(response => {
            if (!response.ok) {
                console.log('errorr: ');
                throw new Error('Сетевая ошибка');
            }
            console.log('response: ' + response);
            return response.json(); // Парсим ответ как JSON
        })
        .then(data => {
            // Обрабатываем полученные данные
            console.log('get: ' + data);
        })
        .catch(error => {
            // Обрабатываем ошибку
            console.error('Произошла ошибка:', error);
        });

    console.log('READY')
}