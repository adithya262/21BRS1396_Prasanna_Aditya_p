import json
import asyncio
import websockets

class Game:
    def __init__(self):
        self.board = [["" for _ in range(5)] for _ in range(5)]
        self.players = {"A": [], "B": []}
        self.current_player = "A"
        self.game_over = False

    def initialize_board(self, player_a_positions, player_b_positions):
        for i in range(5):
            self.board[0][i] = f"A-{player_a_positions[i]}"
            self.board[4][i] = f"B-{player_b_positions[i]}"
            self.players["A"].append((0, i))
            self.players["B"].append((4, i))

    def move(self, player, start_pos, direction):
        if self.current_player != player or self.game_over:
            return {"status": "failure", "reason": "Not your turn or game over"}
        
        r, c = start_pos
        piece = self.board[r][c]
        if not piece or piece[0] != player:
            return {"status": "failure", "reason": "Invalid move"}
        
        new_r, new_c = self.calculate_new_position(r, c, piece, direction)
        
        if not self.is_within_bounds(new_r, new_c):
            return {"status": "failure", "reason": "Out of bounds"}
        
        target = self.board[new_r][new_c]
        kill_message = None
        if target and target[0] != player:
            kill_message = f"{piece.split('-')[1]} killed {target.split('-')[1]}!"
            self.players[target[0]].remove((new_r, new_c))

        if "Hero1" in piece or "Hero2" in piece:
            self.clear_path(r, c, new_r, new_c)

        self.board[r][c] = ""
        self.board[new_r][new_c] = piece
        self.update_position(player, (r, c), (new_r, new_c))
        
        self.current_player = "B" if player == "A" else "A"
        self.check_game_over()

        return {"status": "success", "board": self.board, "kill_message": kill_message}

    def calculate_new_position(self, r, c, piece, direction):
        movement = {
            "L": (0, -1), "R": (0, 1),
            "F": (-1, 0), "B": (1, 0),
            "FL": (-1, -1), "FR": (-1, 1),
            "BL": (1, -1), "BR": (1, 1)
        }
        dr, dc = movement.get(direction, (0, 0))
        
        if "Hero1" in piece:
            return (r + dr * 2, c + dc * 2) if direction in ["L", "R", "F", "B"] else (r, c)
        elif "Hero2" in piece:
            return (r + dr * 2, c + dc * 2) if direction in ["FL", "FR", "BL", "BR"] else (r, c)
        else:  # Pawn
            return r + dr, c + dc

    def is_within_bounds(self, r, c):
        return 0 <= r < 5 and 0 <= c < 5

    def clear_path(self, r1, c1, r2, c2):
        if r1 == r2 or c1 == c2 or abs(r2 - r1) == abs(c2 - c1):
            step_r = 1 if r2 > r1 else -1 if r2 < r1 else 0
            step_c = 1 if c2 > c1 else -1 if c2 < c1 else 0
            r, c = r1 + step_r, c1 + step_c
            while r != r2 or c != c2:
                if self.board[r][c]:
                    self.board[r][c] = ""
                r += step_r
                c += step_c

    def update_position(self, player, old_pos, new_pos):
        self.players[player].remove(old_pos)
        self.players[player].append(new_pos)
        self.check_game_over()

    def check_game_over(self):
        if not self.players["A"] or not self.players["B"]:
            self.game_over = True

async def handler(websocket):
    game = Game()
    game.initialize_board(["Pawn", "Pawn", "Hero1", "Hero2", "Pawn"], ["Pawn", "Pawn", "Hero2", "Hero1", "Pawn"])
    await websocket.send(json.dumps({"type": "init", "state": {"board": game.board}}))

    while True:
        message = await websocket.recv()
        data = json.loads(message)

        if data["type"] == "move":
            response = game.move(data["player"], tuple(map(int, data["move"].split(":")[0].split(","))), data["move"].split(":")[1])
            if response["status"] == "success":
                await websocket.send(json.dumps({"type": "update", "state": {"board": game.board}}))
            await websocket.send(json.dumps({"type": "move_response", "response": response}))
        elif data["type"] == "init":
            game = Game()
            game.initialize_board(["Pawn", "Pawn", "Hero1", "Hero2", "Pawn"], ["Pawn", "Pawn", "Hero2", "Hero1", "Pawn"])
            await websocket.send(json.dumps({"type": "init", "state": {"board": game.board}}))
        if game.game_over:
            winner = "A" if game.current_player == "B" else "B"
            kill_message = f"Player {winner} has defeated all enemies!"
            await websocket.send(json.dumps({"type": "game_over", "winner": winner, "kill_message": kill_message}))
            break

async def main():
    async with websockets.serve(handler, "localhost", 12345):
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())
