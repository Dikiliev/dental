// BASE_URL = 'https://ldent.online/'
BASE_URL = 'http://localhost:8000/'


function toDate(valueStr){
  const parts = valueStr.split('-');
  return new Date(parts[0], parts[1] - 1, parts[2], parts[3], parts[4]);
}

async function fetchData(url) {
    url = BASE_URL + url;
  try {
    const response = await fetch(url);

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return await response.json();

  } catch (error) {
    console.error('There was a problem with your fetch operation:', error);
    throw error;
  }
}

function getCsrfToken() {
    const csrfTokenElement = document.getElementsByName('csrfmiddlewaretoken')[0];
    return csrfTokenElement ? csrfTokenElement.value : '';
}

function capitalize(str) {
  if (str && typeof str === 'string') {
    return str.charAt(0).toUpperCase() + str.slice(1);
  }
  return str;
}