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