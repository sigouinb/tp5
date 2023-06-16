# Benjamin Sigouin
# Groupe 404
# TP5: Roche papier ciseaux

import random
import arcade

from attack_animation import AttackType, AttackAnimation
from game_state import GameState
# importe les fonctions des autres fichiers

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Roche, papier, ciseaux"
DEFAULT_LINE_HEIGHT = 45
# Dimensions de l'ecran


class MyGame(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        arcade.set_background_color(arcade.color.BLACK_OLIVE)

        self.player = None
        self.computer = None
        self.rock = None
        self.paper = None
        self.scissors = None
        self.player_score = 0
        self.computer_score = 0
        self.computer_attack_type = None
        self.computer_attack_sprite = None
        self.player_attack_chosen = False
        self.player_won_round = None
        self.draw_round = None
        self.game_state = None
        self.gameResults = None
        # liste des variables et sprites

    def setup(self):
        # positions des sprites
        self.game_state = GameState.NOT_STARTED
        self.player = arcade.Sprite("Assets/faceBeard.png", 0.5, center_x=200, center_y=350)
        self.computer = arcade.Sprite("Assets/compy.png", 2.40, center_x=800, center_y=350)

        self.rock = AttackAnimation(AttackType.ROCK)
        self.rock.center_x = 200
        self.rock.center_y = 150

        self.paper = AttackAnimation(AttackType.PAPER)
        self.paper.center_x = 300
        self.paper.center_y = 150

        self.scissors = AttackAnimation(AttackType.SCISSORS)
        self.scissors.center_x = 400
        self.scissors.center_y = 150


    def how_to_win(self):
        # determine quelles attaques gagne ou perd contre quelles attaques
        if self.player_attack_chosen == AttackType.ROCK and self.computer_attack_type == AttackType.ROCK:
            return "Draw"
        elif self.player_attack_chosen == AttackType.ROCK and self.computer_attack_type == AttackType.PAPER:
            return "Loss"
        elif self.player_attack_chosen == AttackType.ROCK and self.computer_attack_type == AttackType.SCISSORS:
            return "Win"

        if self.player_attack_chosen == AttackType.PAPER and self.computer_attack_type == AttackType.PAPER:
            return "Draw"
        elif self.player_attack_chosen == AttackType.PAPER and self.computer_attack_type == AttackType.SCISSORS:
            return "Loss"
        elif self.player_attack_chosen == AttackType.PAPER and self.computer_attack_type == AttackType.ROCK:
            return "Win"

        if self.player_attack_chosen == AttackType.SCISSORS and self.computer_attack_type == AttackType.SCISSORS:
            return "Draw"
        elif self.player_attack_chosen == AttackType.SCISSORS and self.computer_attack_type == AttackType.ROCK:
            return "Loss"
        elif self.player_attack_chosen == AttackType.SCISSORS and self.computer_attack_type == AttackType.PAPER:
            return "Win"

    def draw_possible_attack(self):
        # le contour des mains
        arcade.draw_rectangle_outline(
            200,
            150,
            70,
            70,
            arcade.color_from_hex_string("F04848"))

        arcade.draw_rectangle_outline(
            300,
            150,
            70,
            70,
            arcade.color_from_hex_string("F04848"))

        arcade.draw_rectangle_outline(
            400,
            150,
            70,
            70,
            arcade.color_from_hex_string("F04848"))

        arcade.draw_rectangle_outline(
            825,
            150,
            70,
            70,
            arcade.color_from_hex_string("F04848"))

        # ne dessine que la main que le joueur a choisie
        if self.player_attack_chosen == AttackType.ROCK:
            self.rock.draw()
        elif self.player_attack_chosen == AttackType.PAPER:
            self.paper.draw()
        elif self.player_attack_chosen == AttackType.SCISSORS:
            self.scissors.draw()
        else:
            self.rock.draw()
            self.paper.draw()
            self.scissors.draw()

    def draw_computer_attack(self):
        # dessine la main que la console a choisie
        if self.computer_attack_sprite:
            self.computer_attack_sprite.center_x = 825
            self.computer_attack_sprite.center_y = 150
            self.computer_attack_sprite.draw()

    def validate_victory(self):
        # anime les mains
        attack_index = random.randint(0, 2)
        if attack_index == 0:
            self.computer_attack_type = AttackType.ROCK
            self.computer_attack_sprite = AttackAnimation(AttackType.ROCK)
        elif attack_index == 1:
            self.computer_attack_type = AttackType.PAPER
            self.computer_attack_sprite = AttackAnimation(AttackType.PAPER)
        elif attack_index == 2:
            self.computer_attack_type = AttackType.SCISSORS
            self.computer_attack_sprite = AttackAnimation(AttackType.SCISSORS)

        # change le score
        player_results = self.how_to_win()
        if player_results:
            self.game_state = GameState.ROUND_DONE

        if player_results == "Win":
            self.player_score += 1
            self.gameResults = "Win"

        elif player_results == "Loss":
            self.computer_score += 1
            self.gameResults = "Loss"

        elif player_results == "Draw":
            self.gameResults = "Draw"

        if self.player_score == 3 or self.computer_score == 3:
            self.game_state = GameState.GAME_OVER


    def draw_text(self):
        # affiche les instructions au joueur dependamment de l'etat du jeu
        arcade.draw_text("Votre score est:" + str(self.player_score),
                         -220,
                         20,
                         arcade.color.GOLD,
                         20,
                         width=SCREEN_WIDTH,
                         align="center")

        arcade.draw_text("Le score de l'ordinateur est:" + str(self.computer_score),
                         220,
                         20,
                         arcade.color.RED,
                         20,
                         width=SCREEN_WIDTH,
                         align="center")
        string = None

        if self.game_state == GameState.GAME_OVER:
            if self.player_score > self.computer_score:
                string = "VICTOIRE! " \
                         "Appuyez sur espace pour rejouer."
            else:
                string = "DEFAITE. " \
                         "Appuyer sur espace pour rejouer."

        elif self.game_state == GameState.NOT_STARTED:
            string = "Appuyer sur espace pour commencer la partie."
        elif self.game_state == GameState.ROUND_ACTIVE:
            string = "Clicker sur une des mains pour jouer."
        elif self.game_state == GameState.ROUND_DONE:
            if self.gameResults == "Win":
                string = "Victoire. " \
                         "Appuyer sur espace pour commencer une nouvelle ronde."
            elif self.gameResults == "Loss":
                string = "Defaite. " \
                         "Appuyer sur espace pour commencer une nouvelle ronde."
            elif self.gameResults == "Draw":
                string = "Égalité. " \
                         "Appuyer sur espace pour commencer une nouvelle ronde."

        arcade.draw_text(string,
                         350,
                         300,
                         arcade.color.WHITE,
                         20,
                         width=300,
                         align="center", )

    def on_draw(self):
        # dessine tout
        arcade.start_render()
        arcade.draw_text(SCREEN_TITLE,
                         0,
                         SCREEN_HEIGHT - DEFAULT_LINE_HEIGHT * 2,
                         arcade.color.BLACK_BEAN,
                         60,
                         width=SCREEN_WIDTH,
                         align="center")
        self.player.draw()
        self.computer.draw()
        self.draw_computer_attack()
        self.draw_text()
        self.draw_possible_attack()

    def on_update(self, delta_time):
        # anime les mains
        if self.game_state == GameState.ROUND_ACTIVE:
            self.rock.on_update()
            self.paper.on_update()
            self.scissors.on_update()

    def on_key_press(self, key, key_modifiers):
        # change l'etat du jeu quand le joueur appuie sur espace
        if key == 32:
            if self.game_state == GameState.NOT_STARTED:
                self.game_state = GameState.ROUND_ACTIVE

            elif self.game_state == GameState.ROUND_DONE:
                self.game_state = GameState.ROUND_ACTIVE
                self.gameResults = None
                self.computer_attack_sprite = None
                self.player_attack_chosen = None

            elif self.game_state == GameState.GAME_OVER:
                self.game_state = GameState.ROUND_ACTIVE
                self.player_score = 0
                self.computer_score = 0
                self.computer_attack_type = None
                self.player_attack_chosen = False
                self.draw_round = None

    def on_mouse_press(self, x, y, button, key_modifiers):
         # permet au joueur de cliquer sur une des mains et de changer l'etat de jeu
        if self.game_state == GameState.ROUND_ACTIVE:
            if self.rock.collides_with_point((x, y)):
                self.player_attack_chosen = AttackType.ROCK
                self.validate_victory()

            elif self.paper.collides_with_point((x, y)):
                self.player_attack_chosen = AttackType.PAPER
                self.validate_victory()

            elif self.scissors.collides_with_point((x, y)):
                self.player_attack_chosen = AttackType.SCISSORS
                self.validate_victory()


def main():
    """ Main method """
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()