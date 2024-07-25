from flask import Flask, request, render_template, redirect, url_for
import re
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

class Player:
    def __init__(self, number, name, id_, loc, total, results):
        self.number = number
        self.name = name
        self.id = id_
        self.loc = loc
        self.total = total
        self.results = results

def parse_file(filepath):
    players = []
    with open(filepath, 'r') as file:
        lines = file.readlines()

    for line in lines:
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

def get_player_results(players, player_number):
    player = next((p for p in players if p.number == player_number), None)
    if not player:
        return f"Player with number {player_number} not found."

    results = []
    for i, result in enumerate(player.results):
        opponent_number, outcome = result.split(':')
        opponent_number = int(opponent_number)
        outcome = outcome.strip()
        opponent = next((p for p in players if p.number == opponent_number), None)
        opponent_name = opponent.name if opponent else "Unknown"
        results.append({
            'round': i + 1,
            'opponent_name': opponent_name,
            'opponent_position': opponent_number,
            'result': outcome
        })

    return results

def print_round(players, round_number):
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
    return pairings

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'No file part'
        file = request.files['file']
        if file.filename == '':
            return 'No selected file'
        if file:
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)
            players = parse_file(filepath)
            return render_template('index.html', players=players)
    return render_template('index.html', players=None)

@app.route('/player_results', methods=['POST'])
def player_results():
    player_number = int(request.form['player_number'])
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], os.listdir(app.config['UPLOAD_FOLDER'])[0])
    players = parse_file(filepath)
    results = get_player_results(players, player_number)
    return render_template('results.html', results=results, player_number=player_number)

@app.route('/round_pairings', methods=['POST'])
def round_pairings():
    round_number = int(request.form['round_number'])
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], os.listdir(app.config['UPLOAD_FOLDER'])[0])
    players = parse_file(filepath)
    pairings = print_round(players, round_number)
    return render_template('pairings.html', pairings=pairings, round_number=round_number)

if __name__ == '__main__':
    app.run(debug=True)
