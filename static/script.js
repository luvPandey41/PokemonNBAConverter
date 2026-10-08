async function openBox(teamID) {

    const team = teams.find(function(team) {
        return team.id === teamID;
    });

    document.getElementById("box").classList.add("active");
    document.getElementById("bg-blur").classList.add("active");

    const logoURL = `https://cdn.nba.com/logos/nba/${teamID}/global/L/logo.svg`;

    document.getElementById("team-logo").src = logoURL;
    document.getElementById("team-box-title").innerHTML = team.name;

    const playerList = document.getElementById("player-list");

    const response = await fetch(`/roster/${teamID}`);

    const players = await response.json();

    playerList.innerHTML = "";

    players.forEach(function(player) {

        const button = createPlayer(player);

        playerList.append(button);

    });

    document.addEventListener("click", HandleBoxClick); //Apparently you have to send functions this way instead of inline declerations for the removeEventListener to work
    
}

function HandleBoxClick(event){
    if(!document.getElementById("box").contains(event.target)){
        document.removeEventListener("click", HandleBoxClick);
        closeBox();
    }
}

function closeBox() {
    document.getElementById("box").classList.remove("active");
    document.getElementById("bg-blur").classList.remove("active");
}

function createPlayer(player) {

    const button = document.createElement("button");
    button.classList.add("player-button");

    const image = document.createElement("img");
    image.classList.add("player-image");
    image.src = `https://cdn.nba.com/headshots/nba/latest/260x190/${player.PlayerID}.png`;
    const details = document.createElement("div");
    details.classList.add("player-details");

    const name = document.createElement("span");
    name.classList.add("player-name");
    name.innerHTML = player.Name;

    const position = document.createElement("span");
    position.classList.add("player-position");
    position.innerHTML = player.Position;

    button.append(image);

    button.append(details); 
    details.append(name);
    details.append(position);

    button.onclick = function () {
        window.location.href = `/results?player_id=${player.PlayerID}`;
    };

    return button;
}

const teams = [
    { name: "Lakers", id: 1610612747 },
    { name: "Nuggets", id: 1610612743 },
    { name: "Mavericks", id: 1610612742 },
    { name: "Hawks", id: 1610612737 },
    { name: "Celtics", id: 1610612738 },
    { name: "Bulls", id: 1610612741 },
    { name: "Warriors", id: 1610612744 },
    { name: "Timberwolves", id: 1610612750 },
    { name: "Rockets", id: 1610612745 },
    { name: "Hornets", id: 1610612766 },
    { name: "Nets", id: 1610612751 },
    { name: "Cavaliers", id: 1610612739 },
    { name: "Kings", id: 1610612758 },
    { name: "Thunder", id: 1610612760 },
    { name: "Grizzlies", id: 1610612763 },
    { name: "Heat", id: 1610612748 },
    { name: "Knicks", id: 1610612752 },
    { name: "Pistons", id: 1610612765 },
    { name: "Clippers", id: 1610612746 },
    { name: "Trail Blazers", id: 1610612757 },
    { name: "Pelicans", id: 1610612740 },
    { name: "Magic", id: 1610612753 },
    { name: "76ers", id: 1610612755 },
    { name: "Pacers", id: 1610612754 },
    { name: "Suns", id: 1610612756 },
    { name: "Jazz", id: 1610612762 },
    { name: "Spurs", id: 1610612759 },
    { name: "Wizards", id: 1610612764 },
    { name: "Raptors", id: 1610612761 },
    { name: "Bucks", id: 1610612749 }
];

const teamContainer = document.getElementById("team-container");

teams.forEach(function(team) {
    const button = document.createElement("button");

    button.classList.add("team-button");

    button.innerHTML = `
        <img class = "team-logo" src="https://cdn.nba.com/logos/nba/${team.id}/global/L/logo.svg">
        <span> ${team.name} </span>
        `;

    button.onclick = function() {openBox(team.id);};

    teamContainer.append(button);
});

let players = [];

async function loadPlayers() {
    const response = await fetch("/all_players");
    const data = await response.json();

    for (const [teamID, roster] of Object.entries(data)) {

        for (const player of roster) {
            player.teamID = teamID;
            players.push(player);
        }
    
    }
}

function updateSuggestions() {
    const input = document.getElementById("search-box").value;

    document.getElementById("autofill-container").innerHTML = "";

    if(input == "") {
        return; //I dont even wanna deal with this case, looks to weird ot have autofill there
    }

    matches = []   

    for(const player of players){
        if(player.Name.toLowerCase().substring(0, input.length) == input.toLowerCase()){ //later make this work with last names (proabbly straightforward ash)
            matches.push(player)
        }
    }

    console.log(matches);

    displayedMatches = matches.slice(0, 5) //sometimes you get matches of length 50 and its unreasonable to display allat

    for(const i of displayedMatches){
        createAutofillBox(i);
    }
}

function createAutofillBox(player){
    const autofillContainer = document.getElementById("autofill-container"); 

    const box = document.createElement("div");
    box.classList.add("search-suggestion");
    
    const img = document.createElement("img");
    img.classList.add("autofill-box-image")
    img.src = `https://cdn.nba.com/headshots/nba/latest/260x190/${player.PlayerID}.png`;

    const text = document.createElement("div");
    text.innerHTML = `${player.Name} • ${player.Position}, ${getTeamNameFromID(player.teamID)}`;

    box.append(img);
    box.append(text);

    box.onclick = function() {
        window.location.href = `/results?player_id=${player.PlayerID}`;
    };

    autofillContainer.append(box);
}

function getTeamNameFromID(id){
    for (i of  teams){
        if(i.id == id) return i.name;
    }
    console.log(`Team of id ${id} does not exist.`);
}

loadPlayers();

document.getElementById("search-box").addEventListener("input", updateSuggestions); //input is hte HTML DOM event that works best with this case


