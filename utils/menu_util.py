def switch_stage(game,stage):
    game.load_stage(stage)

def stop(game):
    game.running = False

def reset_score(game):
    game.data = dict()