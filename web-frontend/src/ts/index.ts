import "../styles/index.scss";
import $ from "jquery";

function loadHtmlPage(page: string) {
  $("#contentWrapper").load(`./html/${page}.html`);
  fetch(`./html/${page}.html`)
    .then((response) => response.text())
    .then((html) => {
      $("#contentWrapper").html(html);
      loadSim(); // TODO: remove (refactor, put into class)
    })
    .catch((error) => {
      console.error("Error loading the HTML file:", error);
    });
}

loadHtmlPage("sim");

function loadSim() {
  updatePoints();
}

let playerPoints = 501;
let botPoints = 501;

function updatePoints() {
  $(".player .player-name").each(function () {
    var playerName = $(this).text();
    if (playerName === "Player") {
      $(this).siblings(".player-score").text(playerPoints);
    } else if (playerName === "Bot") {
      $(this).siblings(".player-score").text(botPoints);
    }
  });
}
