import json
from tempfile import NamedTemporaryFile
from markdown import markdown
from parser import process, commands
from flask import Flask, jsonify, render_template, Markup, send_file

app = Flask(__name__)

games = process(commands, open('games.log', 'r'))

@app.route('/')
def index():
    content = Markup(markdown('\n'.join(open('README.md', 'r').readlines())))
    return render_template('index.html', **locals())

@app.route('/api')
def get_all_games():
    return jsonify(games)

@app.route('/api/game/<number>')
def get_game(number, method=['GET']):
    return jsonify(games[f'game_{number}'])

@app.route('/api/game/<number>/download')
def get_game_file(number, method=['GET']):
    with NamedTemporaryFile('w') as temp:
        temp.write(json.dumps(games[f'game_{number}']))
        temp.seek(0)
        return send_file(temp.name, 
                         as_attachment=True, 
                         attachment_filename='response.json',
                         mimetype='text/json')

@app.route('/api/download')
def get_all_game_file(method=['GET']):
    with NamedTemporaryFile('w', dir='.') as temp:
        temp.write(json.dumps(games))
        temp.seek(0)
        return send_file(temp.name, as_attachment=True,
                         attachment_filename='response.json', 
                         mimetype='text/json')


if __name__ == '__main__':
    app.run(debug=True)

#response.json