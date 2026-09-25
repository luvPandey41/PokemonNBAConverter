
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
        const card = document.createElement("div");
    
        card.classList.add("pokemon-card");
    
        const name = document.createElement("h2");
        name.textContent = pokemon;
    
        const score = document.createElement("p");
        score.textContent = `${data.stats[pokemon]}%`;
    
        card.appendChild(name);
        card.appendChild(score);
    
        results.appendChild(card);
    }
});