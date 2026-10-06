function returnToHome(){
    window.location.href = "/"
}

async function setUpResultsData(id) {

    const response = await fetch (`/player/${id}`);
    const player = await response.json();
    

    console.log(player);

    document.getElementById("player-name").innerHTML = `Results For: ${player.name}`;

    document.getElementById("player-image").src = `https://cdn.nba.com/headshots/nba/latest/260x190/${id}.png`
    document.getElementById("team-logo").src = `https://cdn.nba.com/logos/nba/${player.team}/global/L/logo.svg`

    document.getElementById("player-box-name").innerHTML = player.name;
    document.getElementById("player-position-and-team").innerHTML = `${player.position}, ${player.teamName}`;

    document.getElementById("PPG").innerHTML = player.ppg;
    document.getElementById("APG").innerHTML = player.apg;
    document.getElementById("RPG").innerHTML = player.rpg;
    document.getElementById("FG%").innerHTML = player.fgPct;

    const currentMon = player.six_closest[0].pokemon //allow this to be changed

    document.getElementById("pokemon-img").src = `https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/${currentMon.id}.png`;

    document.getElementById("pokemon-box-name").innerHTML = capitalize(currentMon.name)
    document.getElementById("pokemon-type-1").src = `https://raw.githubusercontent.com/luizbinario/pokemon-type-icons/main/icons/${currentMon.type1}.svg`
    document.getElementById("pokemon-type-2").src = `https://raw.githubusercontent.com/luizbinario/pokemon-type-icons/main/icons/${currentMon.type2}.svg`

    if(currentMon.type2 == null) {
        const x = document.getElementById("pokemon-type-2")
        x.style.visibility = "hidden";
        x.style.width = "0px";
    }
    else {
        const x = document.getElementById("pokemon-type-2")
        x.style.visibility = "visible";
        x.style.width = "40px";
    }

    document.getElementById("pokemon-genus").innerHTML = currentMon.genus

    document.getElementById("HP").innerHTML = currentMon.hp;
    document.getElementById("ATK").innerHTML = currentMon.atk;
    document.getElementById("DEF").innerHTML = currentMon.defs;
    document.getElementById("SPCA").innerHTML = currentMon.spcA;
    document.getElementById("SPCD").innerHTML = currentMon.spcD;
    document.getElementById("SPD").innerHTML = currentMon.spd;

    document.getElementById("match-display").innerHTML = `MATCH: <span>${player.six_closest[0].similarity}%</span>`;

    const pokemonStats = [currentMon.hp, currentMon.atk, currentMon.defs, currentMon.spcA, currentMon.spcD, currentMon.spd];
    const playerStats = [player.hp, player.atk, player.defs, player.spcA, player.spcD, player.spd];
    const largestStat = Math.max( ...pokemonStats, ...playerStats); //equivalent of *pokemonStats in python
    const chartMax = Math.max(Math.ceil(largestStat / 20) * 20, 100);

    const ctx = document.getElementById("stats-chart");

    new Chart(ctx, {

        type: "radar",

        data: {

            labels: ["HP", "Attack", "Defense", "Sp. Atk", "Sp. Def", "Speed"],

            datasets: [
                {
                    label: capitalize(currentMon.name),

                    data: pokemonStats,

                    borderColor: "#46A497",
                    backgroundColor: "rgba(70, 164, 151, 0.20)",

                    pointBackgroundColor: "#46A497", 
                    pointBorderColor: "#FFFFFF", 
                    pointBorderWidth: 2,

                    borderWidth: 3
                },

                {
                    label: player.name,

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

function capitalize(x){
    return x.charAt(0).toUpperCase() + x.substring(1, x.length).toLowerCase() //suprising how many times I had to capitalize
}