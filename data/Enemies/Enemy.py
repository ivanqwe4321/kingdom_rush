import pygame as pg
import math
import os
import time

class Enemy():
    def __init__(self, size, health, path, image, lives_cost, speed = 1, delay_before_next_move=0):
        self.width = size[0]
        self.height = size[1]
        self.health = health
        self.max_health = health
        self.path = path
        self.image = image
        self.lives_cost = lives_cost
        self.speed = speed
        self.path_index = 0
        self.x = path[self.path_index][0]
        self.y = path[self.path_index][1]
        self.delay_before_next_move = delay_before_next_move
        self.last_move_time = time.time()
        self.animation_state = 0
        self.animation_imgs = []

    def draw(self, screen):
        self.image = self.animation_imgs[self.animation_state]
        screen.blit(self.image, (self.x - self.width / 2, self.y - self.height / 2))

    def move(self):
        if time.time() - self.last_move_time > self.delay_before_next_move:
            if self.animation_state < len(self.animation_imgs) - 1:
                self.animation_state += 1
            else:
                self.animation_state = 0
            self.last_move_time = time.time()

        # Calculate the distance between the enemy and the next point in the path and make a vector line to calculate the steps
        distance = math.sqrt((self.path[self.path_index + 1][0] - self.path[self.path_index][0]) ** 2 + (self.path[self.path_index + 1][1] - self.path[self.path_index][1]) ** 2)
        #calculate the move step for x and y
        x_step = (self.path[self.path_index + 1][0] - self.path[self.path_index][0]) * self.speed / distance
        y_step = (self.path[self.path_index + 1][1] - self.path[self.path_index][1]) * self.speed / distance

        # Move the enemy
        self.x += x_step
        self.y += y_step

        # Check if the enemy has reached the next point in the path
        if math.sqrt((self.path[self.path_index + 1][0] - self.x) ** 2 + (self.path[self.path_index + 1][1] - self.y) ** 2) < self.speed:
            self.path_index += 1
            self.x = self.path[self.path_index][0]
            self.y = self.path[self.path_index][1]

        # check if you need to flip the images
        if self.path[self.path_index + 1][0] < self.x:
            self.animation_imgs = [pg.transform.flip(img, True, False) for img in self.animation_imgs]
        else:
            self.animation_imgs = [pg.transform.flip(img, False, False) for img in self.animation_imgs]

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            return True
        return False
    
    def is_collided(self, x, y):
        if self.x - self.width / 2 < x < self.x + self.width / 2 and self.y - self.height / 2 < y < self.y + self.height / 2:
            return True
        return False