let statsChart; //makes it so that the chart can be changed, instead of rewriting over it, which could be aproblem in multiple ways

function returnToHome(){
    window.location.href = "/"
}

async function setUpResultsData(id) {

    const response = await fetch (`/player/${id}`);
    const player = await response.json();

    console.log(player); //helps with debugging alot

    document.getElementById("player-image").src = `https://cdn.nba.com/headshots/nba/latest/260x190/${id}.png`
    document.getElementById("team-logo").src = `https://cdn.nba.com/logos/nba/${player.team}/global/L/logo.svg`

    document.getElementById("player-box-name").innerHTML = player.name;
    document.getElementById("player-position-and-team").innerHTML = `${player.position}, ${player.teamName}`;

    document.getElementById("PPG").innerHTML = player.ppg;
    document.getElementById("APG").innerHTML = player.apg;
    document.getElementById("RPG").innerHTML = player.rpg;
    document.getElementById("FG%").innerHTML = player.fgPct;

    const currentMon = player.six_closest[0].pokemon //allow this to be changed

    createMainDisplay(player, 1)

    document.getElementById("mini-box-container").append(createMiniBox(player, 1));
    document.getElementById("mini-box-container").append(createMiniBox(player, 2));
    document.getElementById("mini-box-container").append(createMiniBox(player, 3));
    document.getElementById("mini-box-container").append(createMiniBox(player, 4));
    document.getElementById("mini-box-container").append(createMiniBox(player, 5));


    // const x = player.six_closest[1].pokemon
    // document.getElementById("first-box-image").src = `https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/${x.id}.png`;
    // document.getElementById("first-box-name").innerHTML = capitalize(x.name);

    // document.getElementById("first-box-type-1").src = `https://raw.githubusercontent.com/luizbinario/pokemon-type-icons/main/icons/${x.type1}.svg`
    // document.getElementById("first-box-type-2").src = `https://raw.githubusercontent.com/luizbinario/pokemon-type-icons/main/icons/${x.type2}.svg`
    // document.getElementById("first-box-type-names").innerHTML = capitalize(x.type1) + " " + capitalize(x.type2);

    // document.getElementById("first-box-match-display").innerHTML = `MATCH: <span>${player.six_closest[1].similarity}%</span>`
}

function createMiniBox(p, num){
    
    const x = p.six_closest[num].pokemon

    const mini_box = document.createElement("div");
    mini_box.classList.add("mini-box");
    mini_box.id = `mini-box-${num}`;

    mini_box.dataset.number = num + 1;

    const num_display = document.createElement("h2");
    num_display.classList.add("num-display");
    num_display.innerHTML = `#${num + 1}`

    const img = document.createElement("img");
    img.classList.add("mini-box-image")
    img.src = `https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/${x.id}.png`;

    const name_display = document.createElement("p");
    name_display.classList.add("mini-box-name");
    name_display.innerHTML = capitalize(x.name);

    const details = document.createElement("div");
    details.classList.add("mini-box-details")

    const type_1 = document.createElement("img");
    type_1.classList.add("mini-box-type-1")
    type_1.src = `https://raw.githubusercontent.com/luizbinario/pokemon-type-icons/main/icons/${x.type1}.svg`

    const type_2 = document.createElement("img");

    if (x.type2 != null) {
        type_2.classList.add("mini-box-type-2");
        type_2.src = `https://raw.githubusercontent.com/luizbinario/pokemon-type-icons/main/icons/${x.type2}.svg`;
    }
   
    const type_names = document.createElement("p");
    type_names.classList.add("mini-box-type-names")
    if (x.type2 != null) {
        type_names.innerHTML = capitalize(x.type1) + " " + capitalize(x.type2);
    } else {
        type_names.innerHTML = capitalize(x.type1);
    }


    details.append(type_1);
    if (x.type2 != null) details.append(type_2);
    details.append(type_names);

    const match_display = document.createElement("p");
    match_display.classList.add("mini-box-match-display");
    match_display.innerHTML = `MATCH: <span>${p.six_closest[num].similarity}%</span>`;
    

    mini_box.append(num_display);
    mini_box.append(img);
    mini_box.append(name_display);

    mini_box.append(details);
    mini_box.append(match_display);

    mini_box.onclick = function () {swapMainDisplay(p, Number(mini_box.dataset.number), num);}; //added 1 cuz the first box is really the second best result

    return mini_box;
}


function createMainDisplay(player, num){

    const currentMon = player.six_closest[num-1].pokemon //allow this to be changed

    document.getElementById("main-num-display").dataset.number = num;

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

    document.getElementById("main-num-display").innerHTML = `#${num}`

    document.getElementById("match-display").innerHTML = `MATCH: <span>${player.six_closest[num - 1].similarity}%</span>`;

    const pokemonStats = [currentMon.hp, currentMon.atk, currentMon.defs, currentMon.spcA, currentMon.spcD, currentMon.spd];
    const playerStats = [player.hp, player.atk, player.defs, player.spcA, player.spcD, player.spd];
    const largestStat = Math.max( ...pokemonStats, ...playerStats); //equivalent of *pokemonStats in python
    const chartMax = Math.max(Math.ceil(largestStat / 20) * 20, 100);

    const ctx = document.getElementById("stats-chart");

    if (statsChart != null) {

        statsChart.data.datasets[0].label = capitalize(currentMon.name);
        statsChart.data.datasets[0].data = pokemonStats;
    
        statsChart.options.scales.r.max = chartMax;
        statsChart.options.scales.r.ticks.stepSize = chartMax / 5; //so no overflows, even though its really rare b/c player is same
    
        statsChart.update(); // This makes it so I don't have to recall the whole method, and makes the code look better
    
    }
    else {
    
        statsChart = new Chart(ctx, {
    
            type: "radar",
    
            data: {
    
                labels: ["HP", "Attack", "Defense", "Sp. Atk", "Sp. Def", "Speed"],
    
                datasets: [{
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
                responsive: true, //w animationating
    
                maintainAspectRatio: false,
    
                plugins: {
                    legend: {
                        position: "top",
    
                        labels: {
                            usePointStyle: true,
                            pointStyle: "circle",
                            padding: 20,
                            color: "#2F3E46",
                            font: {
                                family: "Poppins",
                                size: 13,
                                weight: "600"
                            }
                        }
                    }
                },
    
                scales: {
                    r: {
                        min: 0,
    
                        max: chartMax,
    
                        ticks: {
                            stepSize: chartMax / 5,
                            color: "#7E989F",
                            backdropColor: "transparent",
                            font: {
                                family: "Poppins",
                                size: 11
                            }
                        },
    
                        grid: {
                            color: "rgba(47, 62, 70, 0.12)", lineWidth: 1},
    
                        angleLines: {color: "rgba(47, 62, 70, 0.10)",
                            lineWidth: 1
                        },
    
                        pointLabels: {
                            color: "#2F3E46",
                            font: {family: "Poppins", size: 13, weight: "600"}
                        }
                    }
                }
            }
    
        });
    
    }

}


function swapMainDisplay(p, pokemonNumber, boxNumber){
    const prevMain = Number(document.getElementById("main-num-display").dataset.number);

    createMainDisplay(p, pokemonNumber);

    replaceMiniBox(prevMain, boxNumber, p);
}

function replaceMiniBox(newMonNumber, oldMonNumber, p){

    const mon = p.six_closest[newMonNumber - 1].pokemon;
    const relevantBox = document.getElementById(`mini-box-${oldMonNumber}`);

    relevantBox.querySelector(".num-display").innerHTML = `#${newMonNumber}`;

    relevantBox.querySelector(".mini-box-image").src = `https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/${mon.id}.png`;
    relevantBox.querySelector(".mini-box-name").innerHTML = capitalize(mon.name);

    relevantBox.querySelector(".mini-box-type-1").src = `https://raw.githubusercontent.com/luizbinario/pokemon-type-icons/main/icons/${mon.type1}.svg`;

    const type2 = relevantBox.querySelector(".mini-box-type-2");

    if (mon.type2 != null) {
        if (type2 != null) {
            type2.src =
                `https://raw.githubusercontent.com/luizbinario/pokemon-type-icons/main/icons/${mon.type2}.svg`;
            type2.style.display = "inline";
        }

        else {
            const newType2 = document.createElement("img");
            newType2.classList.add("mini-box-type-2");
            newType2.src =
                `https://raw.githubusercontent.com/luizbinario/pokemon-type-icons/main/icons/${mon.type2}.svg`;

            const type1 = relevantBox.querySelector(".mini-box-type-1");
            type1.after(newType2);
        }
    }
    else {
        if (type2 != null) {
            type2.style.display = "none";
        }
    }

    const typeNames = relevantBox.querySelector(".mini-box-type-names");

    if (mon.type2 != null) {
        typeNames.innerHTML = capitalize(mon.type1) + " " + capitalize(mon.type2);
    }
    else {
        typeNames.innerHTML = capitalize(mon.type1);
    }

    relevantBox.querySelector(".mini-box-match-display").innerHTML = `MATCH: <span>${p.six_closest[newMonNumber - 1].similarity}%</span>`;

    relevantBox.dataset.number = newMonNumber;

    relevantBox.onclick = function () {swapMainDisplay(p, Number(relevantBox.dataset.number), oldMonNumber);};
}


function capitalize(x){
    return x.charAt(0).toUpperCase() + x.substring(1, x.length).toLowerCase() //suprising how many times I had to capitalize
}