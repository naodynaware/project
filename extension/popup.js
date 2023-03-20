let cookie = null;

async function setCookie() {
    cookie = await chrome.cookies.get({
        name: "USERSESSIONID",
        url: "https://www.enel.it/it/area-clienti/residenziale"
    });

    document.getElementById("cookie-value").innerHTML = cookie.value;
}

document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("cookie-button").addEventListener("click", setCookie);
});