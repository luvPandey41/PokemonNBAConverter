function returnToHome(){
    window.location.href = "/"
}

async function setUpResultsData(id) {

    const response = await fetch (`/player/${id}`);
    const res = await response.json();
    
    const player = res.player;
    const mons = res.pokemons;


    document.getElementById("player-name").innerHTML = `Results For: ${player.Name}`;

    document.getElementById("player-image").src = `https://cdn.nba.com/headshots/nba/latest/260x190/${id}.png`
    document.getElementById("team-logo").src = `https://cdn.nba.com/logos/nba/${player.TeamID}/global/L/logo.svg`

    document.getElementById("player-box-name").innerHTML = player.Name;
    document.getElementById("player-position-and-team").innerHTML = `${player.Position}, ${player.Team}`;

    document.getElementById("PPG").innerHTML = player.PPG;
    document.getElementById("APG").innerHTML = player.APG;
    document.getElementById("RPG").innerHTML = player.RPG;
    document.getElementById("FG%").innerHTML = player.FGPct;

    const pokemonNames = Object.keys(mons);

    const currentMon = mons[pokemonNames[0]]; //allow this to be changed

    document.getElementById("pokemon-img").src = `https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/${currentMon.ID}.png`;

    document.getElementById("pokemon-box-name").innerHTML = pokemonNames[0].charAt(0).toUpperCase() + pokemonNames[0].substring(1, pokemonNames[0].length);
   
    document.getElementById("pokemon-type-1").src = `https://raw.githubusercontent.com/luizbinario/pokemon-type-icons/main/icons/${currentMon.Type1}.svg`
    document.getElementById("pokemon-type-2").src = `https://raw.githubusercontent.com/luizbinario/pokemon-type-icons/main/icons/${currentMon.Type2}.svg`

    if(currentMon.Type2 == "None") {
        const x = document.getElementById("pokemon-type-2")
        x.style.visibility = "hidden";
        x.style.width = "0px";
    }
    else {
        const x = document.getElementById("pokemon-type-2")
        x.style.visibility = "visible";
        x.style.width = "40px";
    }

    document.getElementById("pokemon-genus").innerHTML = currentMon.Genus //Make this real later

    document.getElementById("HP").innerHTML = currentMon.HP;
    document.getElementById("ATK").innerHTML = currentMon.ATK;
    document.getElementById("DEF").innerHTML = currentMon.DEF;
    document.getElementById("SPCA").innerHTML = currentMon.SPCA;
    document.getElementById("SPCD").innerHTML = currentMon.SPCD;
    document.getElementById("SPD").innerHTML = currentMon.SPD;

    document.getElementById("match-display").innerHTML = `MATCH: <span>${currentMon.Similarity}%</span>`;

    const pokemonStats = [currentMon.HP, currentMon.ATK, currentMon.DEF, currentMon.SPCA, currentMon.SPCD, currentMon.SPD];
    const playerStats = [player.HP, player.ATK, player.DEF, player.SPCA, player.SPCD, player.SPD];
    const largestStat = Math.max( ...pokemonStats, ...playerStats); //equivalent of *pokemonStats in python
    const chartMax = Math.max(Math.ceil(largestStat / 20) * 20, 100);

    const ctx = document.getElementById("stats-chart");

    new Chart(ctx, {

        type: "radar",

        data: {

            labels: ["HP", "Attack", "Defense", "Sp. Atk", "Sp. Def", "Speed"],

            datasets: [
                {
                    label: pokemonNames[0],

                    data: pokemonStats,

                    borderColor: "#46A497",
                    backgroundColor: "rgba(70, 164, 151, 0.20)",

                    pointBackgroundColor: "#46A497", 
                    pointBorderColor: "#FFFFFF", 
                    pointBorderWidth: 2,

                    borderWidth: 3
                },

                {
                    label: player.Name,

                    data: playerStats,

                    borderColor: "#2F3E46",
                    backgroundColor: "rgba(47, 62, 70, 0.12)",

                    pointBackgroundColor: "#2F3E46",
                    pointBorderColor: "#FFFFFF",
                    pointBorderWidth: 2,

                    borderWidth: 3
                }

            ]
        },

        options: {
            responsive: true,

            maintainAspectRatio: false,

            plugins: {
                legend: {
                    position: "top",

                    labels: {
                        usePointStyle: true, pointStyle: "circle", padding: 20, color: "#2F3E46", font: {family: "Poppins", size: 13, weight: "600"}
                    }
                }
            },

            scales: {
                r: {
                    min: 0,

                    max: chartMax,

                    ticks: {
                        stepSize: chartMax / 5, color: "#7E989F", backdropColor: "transparent", font: {family: "Poppins", size: 11}
                    },

                    grid: {
                        color: "rgba(47, 62, 70, 0.12)", lineWidth: 1
                    },

                    angleLines: {
                        color: "rgba(47, 62, 70, 0.10)", lineWidth: 1
                    },

                    pointLabels: {
                        color: "#2F3E46", font: {family: "Poppins",size: 13, weight: "600"}
                    }
                }
            }
        }

    });
}