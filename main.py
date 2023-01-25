from pong.game import CoreGame, GameInformation
import pygame as pg
import sys
import neat
import os
import pickle

MAX_GENERATION = 100


class Game:
    def __init__(self) -> None:
        self.game = CoreGame()
        self.left_paddle = self.game.left_paddle
        self.right_paddle = self.game.right_paddle
        self.ball = self.game.ball

    def test_ai(self, net) -> None:
        clock = pg.time.Clock()

        while True:
            clock.tick(144)
            _ = self.game.loop()

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()

            output = net.activate((
                self.right_paddle.y,
                self.ball.y,
                abs(self.right_paddle.x - self.ball.x)
            ))
            decision = output.index(max(output))

            if decision == 1:
                self.game.move_paddle(left=False, up=True)
            elif decision == 2:
                self.game.move_paddle(left=False, up=False)

            keys = pg.key.get_pressed()
            if keys[pg.K_w]:
                self.game.move_paddle(left=True, up=True)
            if keys[pg.K_s]:
                self.game.move_paddle(left=True, up=False)
            if keys[pg.K_r]:
                self.game.reset()

            self.game.draw(draw_score=True, draw_hits=False)
            pg.display.update()

    def move_ai_paddles(self, net1, net2) -> None:
        players = [(self.genome1, net1, self.left_paddle, True), (self.genome2, net2, self.right_paddle, False)]
        for (genome, net, paddle, left) in players:
            output = net.activate((
                paddle.y,
                self.ball.y,
                abs(paddle.x - self.ball.x)
            ))
            decision = output.index(max(output))

            valid = True
            if decision == 0:
                genome.fitness -= 0.01
            elif decision == 1:
                valid = self.game.move_paddle(left=left, up=True)
            else:
                valid = self.game.move_paddle(left=left, up=False)

            if not valid:
                genome.fitness -= 1

    def train_ai(self, genome1, genome2, config, max_hits: int = 25, draw: bool = False) -> None:
        net1 = neat.nn.FeedForwardNetwork.create(genome1, config)
        net2 = neat.nn.FeedForwardNetwork.create(genome2, config)
        self.genome1 = genome1
        self.genome2 = genome2

        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    return

            game_info = self.game.loop()
            self.move_ai_paddles(net1, net2)

            if draw:
                self.game.draw(draw_score=False, draw_hits=True)

            pg.display.update()

            if game_info.left_score >= 1 or game_info.right_score >= 1 or game_info.left_hits > max_hits:
                self.compute_fitness(game_info)
                break

    def compute_fitness(self, game_info: GameInformation) -> None:
        self.genome1.fitness += game_info.left_hits
        self.genome2.fitness += game_info.right_hits


def eval_genomes(genomes, config) -> None:
    for i, (genome_id1, genome1) in enumerate(genomes):
        print(round(i / len(genomes) * 100), end=" ")
        genome1.fitness = 0
        for genome_id2, genome2 in genomes[min(i + 1, len(genomes) - 1):]:
            genome2.fitness = 0 if genome2.fitness is None else genome2.fitness
            game = Game()
            game.train_ai(genome1, genome2, config, draw=False)


def run_neat(config: neat.config.Config, max_generation: int, checkpoint: str | None = None) -> None:
    if checkpoint is None:
        p = neat.Population(config)
    else:
        p = neat.Checkpointer.restore_checkpoint(checkpoint)

    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(1))
    best = p.run(eval_genomes, max_generation)

    with open("best.pickle", "wb") as f:
        pickle.dump(best, f)


def best_ai(config) -> None:
    with open("best.pickle", "rb") as f:
        best = pickle.load(f)
    best_net = neat.nn.FeedForwardNetwork.create(best, config)

    game = Game()
    game.test_ai(best_net)


if __name__ == "__main__":
    current_dir = os.path.dirname(__file__)
    config_path = os.path.join(current_dir, "config.txt")

    neat_config = neat.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_path
    )

    # run_neat(neat_config, 100, "./checkpoints/neat-checkpoint-117")
    best_ai(neat_config)
