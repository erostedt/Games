import pygame
import math
import random as rnd


class Letter:

    def __init__(self, letter, pos, visible=True):
        self.letter = letter
        self.pos = pos
        self.visible = visible


class Hangman:

    def __init__(self, window_shape=(800, 500), gap=15, pad=(10, 10), radius=20):
        pygame.init()
        self.window_shape = window_shape
        self.gap = gap
        self.pad = pad
        self.radius = radius
        self.word = None
        self.guessed = []
        self.num_letters = 26
        self.lives = 7
        self.letters = self._construct_letters()
        self.font = pygame.font.SysFont('comicsans', 30)
        self.screen = pygame.display.set_mode(self.window_shape)
        pygame.display.set_caption('Hangman')

    def _get_pos(self, index):
        linebreak = self.num_letters // 2
        return 2 * (self.pad[0] + self.radius) + (2 * self.radius + self.gap) * (index % linebreak), \
            (self.window_shape[1] - self.pad[1] - self.gap - 3 * self.radius) + (2 * self.radius + self.gap) * (index // linebreak)

    def _construct_letters(self):
        _A = 65
        return [Letter(letter=chr(_A + shift), pos=self._get_pos(shift), visible=True)
                for shift in range(self.num_letters)]

    @staticmethod
    def _get_random_word():
        return rnd.choice([
            'HEJ', 'HOLA', 'WADDUP', 'PYTHON', 'HANGMAN'
        ])

    def _check_state(self):
        if self.lives < 0:
            return 'LOST'

        for word in self.word:
            if word not in self.guessed:
                return 'ALIVE'

        return 'WON'

    @staticmethod
    def dist(p1, p2):
        return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

    def _check_pressed(self, mouse_pos):
        for i, letter in enumerate(self.letters):
            if self.dist(letter.pos, mouse_pos) < self.radius and letter.visible:
                return letter
        return None

    def draw(self):
        self.screen.fill((255, 255, 255))

        for letter in self.letters:
            if letter.visible:
                pygame.draw.circle(self.screen, (0, 0, 0), letter.pos, self.radius, 3)
                text = self.font.render(letter.letter, 1, (0, 0, 0))
                x_shifted, y_shifted = letter.pos[0] - text.get_width()/2, letter.pos[1] - text.get_height()/2
                self.screen.blit(text, (x_shifted, y_shifted))

        disp = ''.join(letter + ' ' if letter in self.guessed else '_ ' for letter in self.word)
        disptext = self.font.render(disp, 1, (0, 0, 0))
        self.screen.blit(disptext, (self.window_shape[0]/2, self.window_shape[1]/2))

        pygame.display.update()

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        letter_pressed = self._check_pressed(mouse_pos)
        if letter_pressed:
            if letter_pressed.letter not in self.word:
                self.lives -= 1
            self.guessed.append(letter_pressed.letter)
            letter_pressed.visible = False
            state = self._check_state()

            if state != 'ALIVE':
                print(state)
                return True
            else:
                print('Lives left:', self.lives)

    def reset(self):
        self.guessed.clear()
        self.lives = 7
        for letter in self.letters:
            letter.visible = True

    def play(self, fps=60):
        self.word = self._get_random_word()
        clock = pygame.time.Clock()
        print('Lives:', self.lives)
        while True:
            clock.tick(fps)
            self.draw()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return

                if event.type == pygame.MOUSEBUTTONDOWN:
                    game_over = self.update()
                    if game_over:
                        self.draw()
                        self.reset()
                        return


if __name__ == '__main__':
    hangman = Hangman()
    while True:
        _input = input('Play?, y/n \n')
        if _input != 'y':
            break
        hangman.play()
