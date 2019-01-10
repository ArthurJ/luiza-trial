def break_line(line):
    minute, action, *details  = line.strip().split(' ')
    return minute, action, details


def ignore(details, kills, game, games, players_dict):
    # print(details)
    return kills, game, players_dict

def kill(details, kills, game, games, players_dict):
    '''
        # Morte por <world> subtraí pontuação da vítima
        >>> kill(['1022', '7', '22:', '<world>', 'killed', 'Mal', 'by', 'MOD_TRIGGER_HURT'], {}, {}, [], {})
        ({'7': -1}, {'total_kills': 1}, {})

        # Morte por jogador adiciona pontuação ao jogador
        >>> kill(['22', '7', '22:', '<world>', 'killed', 'Mal', 'by', 'MOD_TRIGGER_HURT'], {}, {}, [], {})
        ({'22': 1}, {'total_kills': 1}, {})

        # Suicídio não afeta pontuação
        >>> kill(['7', '7', '22:', '<world>', 'killed', 'Mal', 'by', 'MOD_TRIGGER_HURT'], {}, {}, [], {})
        ({}, {'total_kills': 1}, {})
    '''
    killer, victim, *_ = details

    game['total_kills'] = game.get('total_kills', 0) + 1

    if killer == '1022':
        kills[victim] = kills.get(victim, 0) - 1
    elif killer != victim:
        kills[killer] = kills.get(killer, 0) + 1

    return kills, game, players_dict

def end_game(details, kills, game, games, players_dict):
    '''
        # Fim de jogo deve retornar um novo estado vazio
        >>> kills = {'4': 12, '6': 19, '7': 6, '2': 17, '5': 16, '3': 21}
        >>> game = {'total_kills': 131, 'kills': {'4': 12, '6': 19, '7': 6}}
        >>> games = [{'kills': {}}, {'total_kills': 15, 'kills': {'2': -8, '3': 1, '4': -2}}]
        >>> end_game([], kills, game, games, {})
        ({}, {}, {})

        # game deve conter kills, e deve ser colocado na lista `games`
        >>> kills = {'4': 12, '6': 19, '7': 6, '2': 17, '5': 16, '3': 21}
        >>> game = {'total_kills': 131, 'kills': {'4': 12, '6': 19, '7': 6}}
        >>> games = [{'kills': {}}, {'total_kills': 15, 'kills': {'2': -8, '3': 1, '4': -2}}]
        >>> end_game([], kills, game, games, {})
        ({}, {}, {})
        >>> game['kills'] == kills
        True
        >>> games[-1] == game
        True
    '''
    game['kills'] = kills
    games.append(game)
    return {}, {}, {}

def client_connect(details, kills, game, games, players_dict):
    '''
        # novo jogador deve ser acrescentado na lista de jogadores
        >>> client_connect(['7'], {}, {}, [], {})
        ({}, {'players': {'7'}}, {})
    '''
    players = game.get('players', set())
    players.add(details[0])
    game['players'] = players
    return kills, game, players_dict

def client_change(details, kills, game, games, players_dict):
    '''
        # Atualizações de nome devem ser registradas
        >>> client_change(['7', r'n\\Mal\\t\\0...'],{},{}, [], {})
        ({}, {}, {'7': 'Mal'})
        >>> client_change(['7', r'n\\Bem\\t\\0...'],{},{}, [], {'7': 'Mal'})
        ({}, {}, {'7': 'Bem'})
    '''
    # print(details, kills, game, games, players_dict, end='\n\n')
    player, *player_name = details
    player_name = player_name[0].split('\\t')[0][2:]
    players_dict[player] = player_name
    # print(players_dict)
    return kills, game, players_dict

if __name__ ==  '__main__':
    import doctest
    doctest.testmod()
    
    f_input = open('games.log', 'r')

    commands = {'Kill:':kill,
                'ShutdownGame:':end_game,
                'ClientConnect:':client_connect,
                'ClientUserinfoChanged:': client_change}
    games = []
    game = {}
    kills = {}
    players_dict = {}

    for line in f_input:
        # print(game, kills)
        minute, action, details = break_line(line)
        kills, game, players_dict = commands.get(action, ignore)\
                                        (details, kills, game, games, players_dict)
    