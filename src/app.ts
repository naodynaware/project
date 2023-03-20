import fetch from 'node-fetch';

const url = '[ENDPOINT REMOVED FOR PERSONAL PRIVACY]';
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