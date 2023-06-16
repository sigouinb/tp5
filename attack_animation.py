from enum import Enum
import arcade

class AttackType(Enum):
   """
   Simple énumération pour représenter les différents types d'attaques.
   """
   ROCK = 0,
   PAPER = 1,
   SCISSORS = 2

class AttackAnimation(arcade.Sprite):
   ATTACK_SCALE = 0.50
   ANIMATION_SPEED = 2.0

   def __init__(self, attack_type):
      super().__init__()
      self.attack_type = attack_type
      self.animation_update_time = 1/AttackAnimation.ANIMATION_SPEED
      self.time_since_last_frame = 0
      if self.attack_type == AttackType.ROCK:
         self.textures = [
            arcade.load_texture("assets/srock.png"),
            arcade.load_texture("assets/srock-attack.png"),
         ]
      elif self.attack_type == AttackType.PAPER:
         self.textures = [
            arcade.load_texture("assets/spaper.png"),
            arcade.load_texture("assets/spaper-attack.png"),
         ]
      else:
         self.textures = [
            arcade.load_texture("assets/scissors.png"),
            arcade.load_texture("assets/scissors-close.png"),
         ]

      self.scale = self.ATTACK_SCALE
      self.current_texture = 0
      self.set_texture(self.current_texture)


   def on_update(self, delta_time: float = 1 / 60):
      # fonction pour l'animation des mains
      self.time_since_last_frame += delta_time

      if self.time_since_last_frame > self.animation_update_time:
         self.current_texture += 1
         if self.current_texture < len(self.textures):
            self.set_texture(self.current_texture)
         else:
            self.current_texture = 0
            self.set_texture(self.current_texture)
         self.time_since_last_frame = 0
