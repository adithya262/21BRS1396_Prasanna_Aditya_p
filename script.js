const ws = new WebSocket("ws://localhost:12345");
let currentPlayer = "A";
let selectedCharacter = null;

window.onload = () => {
    const moveGuide = document.getElementById('move-guide');
    
    setTimeout(() => {
        moveGuide.classList.add('fade-out');
    }, 5000);

    moveGuide.addEventListener('transitionend', () => {
        moveGuide.style.display = 'none';
    });
};

ws.onopen = () => {
    ws.send(JSON.stringify({ type: "init" }));
};

ws.onmessage = (message) => {
    const data = JSON.parse(message.data);
    if (data.type === "init") {
        renderBoard(data.state.board);
    } else if (data.type === "update") {
        renderBoard(data.state.board);
    } else if (data.type === "move_response") {
        handleMoveResponse(data.response);
    } else if (data.type === "game_over") {
        showGameOver(data.winner, data.kill_message);
    }
};

function renderBoard(board) {
    const gameBoard = document.getElementById("game-board");
    gameBoard.innerHTML = ""; 
    for (let i = 0; i < 5; i++) {
        for (let j = 0; j < 5; j++) {
            const cell = document.createElement("div");
            cell.className = "cell";
            const content = board[i][j];
            if (content) {
                cell.textContent = content.split("-")[1];
                cell.classList.add(content.split("-")[0] === "A" ? "playerA" : "playerB");
                cell.onclick = () => selectCharacter(i, j, content.split("-")[0]);
            }
            gameBoard.appendChild(cell);
        }
    }
}

function selectCharacter(row, col, player) {
    if (player !== currentPlayer) {
        alert("Not your turn!");
        return;
    }
    if (selectedCharacter) {
        deselectCharacter(selectedCharacter.row, selectedCharacter.col);
    }
    selectedCharacter = { row, col, player };
    const selectedCell = getCell(row, col);
    selectedCell.classList.add("selected");
    showMoveOptions();
}

function deselectCharacter(row, col) {
    const cell = getCell(row, col);
    cell.classList.remove("selected");
}

function getCell(row, col) {
    return document.querySelector(`#game-board .cell:nth-child(${row * 5 + col + 1})`);
}

function showMoveOptions() {
    const moveOptions = document.getElementById("move-options");
    moveOptions.innerHTML = "";

    const character = getCell(selectedCharacter.row, selectedCharacter.col).textContent;
    let directions;

    switch (character) {
        case "Pawn":
            directions = ["L", "R", "F", "B"];
            break;
        case "Hero1":
            directions = ["L", "R", "F", "B"];
            break;
        case "Hero2":
            directions = ["FL", "FR", "BL", "BR"];
            break;
        default:
            directions = ["L", "R", "F", "B", "FL", "FR", "BL", "BR"];
    }

    directions.forEach((dir) => {
        const button = document.createElement("button");
        button.textContent = dir;
        button.onclick = () => makeMove(dir);
        moveOptions.appendChild(button);
    });
}

function makeMove(direction) {
    if (!selectedCharacter) return;
    const move = `${selectedCharacter.row},${selectedCharacter.col}:${direction}`;
    ws.send(JSON.stringify({ type: "move", player: selectedCharacter.player, move }));
}

function handleMoveResponse(response) {
    if (response.status === "success") {
        if (response.kill_message) {
            updateHistory(response.kill_message);
        } else {
            updateHistory(`Player ${selectedCharacter.player} moved from (${selectedCharacter.row}, ${selectedCharacter.col})`);
        }
        deselectCharacter(selectedCharacter.row, selectedCharacter.col);
        selectedCharacter = null;
        currentPlayer = currentPlayer === "A" ? "B" : "A";
        document.getElementById("current-turn").textContent = `Current Turn: Player ${currentPlayer}`;
    } else {
        alert(response.reason);
    }
}

function updateHistory(message) {
    const history = document.getElementById("history-list");
    const entry = document.createElement("div");
    entry.textContent = message;
    history.appendChild(entry);
}

function showGameOver(winner, kill_message) {
    const gameOverDiv = document.getElementById("game-over");
    gameOverDiv.innerHTML = `<h2>Game Over! Player ${winner} wins!</h2><p>${kill_message}</p>`;
    gameOverDiv.classList.add("game-over-animation");
    gameOverDiv.style.display = "block";
    setTimeout(() => ws.close(), 3000); 
}
