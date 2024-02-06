import "../styles/index.scss";
import $ from "jquery";

function loadHtmlPage(page: string) {
    fetch(`./html/${page}.html`)
        .then(response => response.text())
        .then(html => {
            document.getElementById('contentWrapper').innerHTML = html;
        })
        .catch(error => {
            console.error('Error loading the HTML file:', error);
        });
}


loadHtmlPage('sim'); 