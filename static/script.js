
const form = document.getElementById("player-form");

form.addEventListener("submit", async function(event) {
    event.preventDefault();

    const playerName = document.getElementById("name").value;

    const response = await fetch("/match", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            player: playerName
        })
    });

    const data = await response.json();

    const results = document.getElementById("results");

    for (const pokemon in data.stats) {
        const pokemonElement = document.createElement("p");

        pokemonElement.textContent = pokemon + ": " + data.stats[pokemon] + "%"; 

        results.appendChild(pokemonElement);
    }
});