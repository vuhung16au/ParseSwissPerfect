import re

# Define a class to hold the player information
class Player:
    def __init__(self, number, name, id_, loc, total, results):
        self.number = number
        self.name = name
        self.id = id_
        self.loc = loc
        self.total = total
        self.results = results

# Function to parse the input file and return a list of Player objects
def parse_file(filename):
    players = []
    
    with open(filename, 'r') as file:
        lines = file.readlines()

    for line in lines:
        # Extract the data using regular expressions
        match = re.match(r'(\d+)\s+(.+?)\s+(\d+)\s+(\d+)\s+([\d.]+)\s+(.*)', line)
        if match:
            number = int(match.group(1))
            name = match.group(2).strip()
            id_ = int(match.group(3))
            loc = int(match.group(4))
            total = float(match.group(5))
            results = match.group(6).strip().split()
            players.append(Player(number, name, id_, loc, total, results))

    return players

# Function to get results of a specific player
def get_player_results(players, player_number):
    player = next((p for p in players if p.number == player_number), None)
    if not player:
        return f"Player with number {player_number} not found."

    results = []
    for i, result in enumerate(player.results):
        round_number, outcome = result.split(':')
        round_number = int(round_number)
        opponent_number = int(round_number)
        outcome = outcome.strip()

        # Find the opponent's name
        opponent = next((p for p in players if p.number == opponent_number), None)
        opponent_name = opponent.name if opponent else "Unknown"

        results.append({
            'round': i + 1,
            'opponent_name': opponent_name,
            'opponent_position': opponent_number,
            'result': outcome
        })

    return results

# Function to display results in a readable format
def display_results(results):
    for result in results:
        print(f"Round {result['round']}: Played against {result['opponent_name']} (Position {result['opponent_position']}) - Result: {result['result']}")

# Function to print pairings for a specific round
def print_round(round_number):
    filename = "nswjcl-junior-u18-reserve-championship.txt"
    players = parse_file(filename)
    
    pairings = []
    
    for player in players:
        if len(player.results) >= round_number:
            result = player.results[round_number - 1]
            opponent_number, outcome = result.split(':')
            opponent_number = int(opponent_number)
            outcome = outcome.strip()
            
            opponent = next((p for p in players if p.number == opponent_number), None)
            opponent_name = opponent.name if opponent else "Unknown"
            
            if outcome == 'W':
                result_string = "1 - 0"
            elif outcome == 'L':
                result_string = "0 - 1"
            else:
                result_string = "1/2 - 1/2"
            
            pairings.append(f"{player.number} {player.name} {result_string} {opponent_number} {opponent_name}")
    
    for pairing in pairings:
        print(pairing)


# Main program
if __name__ == "__main__":

    # https://www.nswjcl.org.au/Results/2024/Orange2024WinterTournament.htm
    # https://www.nswjcl.org.au/Results/2024/j24nj18r.htm
    filename = "nswjcl-junior-u18-reserve-championship.txt"
    players = parse_file(filename)

    # Prnt result for a player
    player_number = int(input("Enter the player number: "))
    results = get_player_results(players, player_number)
    display_results(results)

    # Print pairing for a round
    round_number = int(input("Enter the round number: "))
    print_round(round_number)
