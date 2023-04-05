import fetch from 'node-fetch';

// Using this URL, you can get the data for the current month using the Cookie we gained from the browser.
const url = 'https://www.enel.it/bin/areaclienti/auth/aggregateConsumption?pod=IT001E68430672&userNumber=104389955&validityFrom=01042023&validityTo=05042023&_=1680697471053';
const cookie = `[COOKIE REMOVED FOR PERSONAL PRIVACY]`;

fetch(url, {
    headers: {
        'cookie': cookie,
    }
}).then((response) => {
    return response.json();
}).then((data) => {
    console.log(data);
});