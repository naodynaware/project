let cookie = null;

async function setCookie() {
    cookie = await chrome.cookies.get({
        name: "USERSESSIONID",
        url: "https://www.enel.it/it/area-clienti/residenziale"
    });

    document.getElementById("cookie-value").innerHTML = cookie.value;
}

document.addEventListener("DOMContentLoaded", function () {
    setCookie();

    var btn = document.getElementById("copy");

    btn.addEventListener("click", function () {
        navigator.clipboard.writeText(cookie.value).then(function () {
            /* clipboard successfully set */
            btn.innerHTML = "Copied!";
        });
    })
});