from kivy.app import App
from kivy.properties import StringProperty, NumericProperty
# import os
import pickle
import random
# import platform
import resources.tools.config as config
# import resources.tools.highscore as highscore


class GameObject:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        # color uses the GameObject class
        # background color = x and foreground color = y


class EscapeApp(App):
    life_count = NumericProperty('')
    score = NumericProperty('')
    grid_text = StringProperty('')
    try:
        with open('resources/data/config.pickle', 'rb') as config_file:
            grid_size, color, controls = pickle.load(config_file)
    except FileNotFoundError:
        config.setup('resources/data/config.pickle', 'continue')
        with open('resources/data/config.pickle', 'rb') as config_file:
            grid_size, color, controls = pickle.load(config_file)

    def grid(self):
        global matrix, li, guards
        matrix = [['  ' for x in range(self.grid_size.x)] for y in range(self.grid_size.y)]
        for sublist in matrix:
            # --top and bottom border--
            g = 0
            while g < self.grid_size.x:
                matrix[0][g] = ' -'
                matrix[self.grid_size.y - 1][g] = ' -'
                g += 1
            # --game objects--
            matrix[door][self.grid_size.x - 1] = ' }'
            matrix[player.y][player.x] = ' i'
            for guard in guards:
                matrix[guard.y][guard.x] = '#'
            if li is True:
                matrix[life_orb.y][life_orb.x] = ' *'
            else:
                matrix[life_orb.y][life_orb.x] = ' -'
            # --removes extra characters--
            s = str(sublist)
            s = s.replace('[', '|').replace(']', '|').replace(',', '').replace('\'', '')
            s = s + '\n'
            self.grid_text = self.grid_text + s
        return

    def new_round(self):
        global door, player, guards, life_orb, li
        door = random.randint(1, self.grid_size.y - 2)
        player = GameObject(0, random.randint(1, self.grid_size.y - 2))
        number_of_guards = round((self.grid_size.x * (self.grid_size.y - 2)) / (self.grid_size.x + (self.grid_size.y - 2)))
        guards = []
        index = 0
        while index < number_of_guards:
            guard = GameObject(random.randint(2, self.grid_size.x - 2), random.randint(1, self.grid_size.y - 2))
            guards.append(guard)
            index += 1
        if random.randint(1, 5) == 3:
            li = True
            life_orb = GameObject(random.randint(round(self.grid_size.x / 2), self.grid_size.x - 2),
                                  random.randint(1, self.grid_size.y - 2))
        else:
            li = False
            life_orb = GameObject(self.grid_size.x - 1, self.grid_size.y - 1)
        self.grid()
        return

    def new_game(self):
        self.root.current = 'game'
        self.life_count = 1
        self.score = 0
        self.new_round()


if __name__ == '__main__':
    app = EscapeApp()
    app.run()
