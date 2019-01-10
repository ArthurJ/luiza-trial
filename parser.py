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
    return {}, {}, {}

if __name__ ==  '__main__':
    import doctest
    doctest.testmod()
    
    f_input = open('games.log', 'r')

    commands = {'Kill:':kill}
    games = []
    game = {}
    kills = {}
    players_dict = {}

    for line in f_input:
        print(game, kills)
        minute, action, details = break_line(line)
        kills, game, players_dict = commands.get(action, ignore)\
                                        (details, kills, game, games, players_dict)
    