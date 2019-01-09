def break_line(line):
    minute, action, *details  = line.strip().split(' ')
    return minute, action, details


def ignore(details, kills, game, games, players_dict):
    print(details)
    return kills, game, players_dict


if __name__ ==  '__main__':
    f_input = open('games.log', 'r')

    commands = {}
    games = []
    game = {}
    kills = {}
    players_dict = {}

    for line in f_input:
        minute, action, details = break_line(line)
        kills, game, players_dict = commands.get(action, ignore)\
                                        (details, kills, game, games, players_dict)