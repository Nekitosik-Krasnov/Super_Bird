import sys, pygame_gui
from Sprites import *


def full_cleaning_sprites():
    background_sprites.empty()
    menu_button_sprites.empty()
    player_sprite.empty()
    pipe_sprites.empty()
    game_button_sprites.empty()
    temporary_sprites.empty()


class Main:
    def __init__(self):
        self.size = self.width, self.height = SIZE_SCREEN
        self.screen = pygame.display.set_mode(self.size, flags=pygame.NOFRAME)
        self.manager = pygame_gui.UIManager((600, 600), 'theme.json')
        self.language_selection()
        self.InitUI()
        self.loading_data()
        self.running = True

    def language_selection(self):
        if language == 'english':
            pygame.display.set_caption('Main menu')
            self.play_button_text = 'Play'
            self.shop_button_text = 'Shop'
            self.settings_button_text = 'Settings'
            self.about_button_text = 'About'
            self.exit_button_text = 'Exit'
            self.question = 'Do you really want to go out?'
        else:
            pygame.display.set_caption('Главное меню')
            self.play_button_text = 'Играть'
            self.shop_button_text = 'Магазин'
            self.settings_button_text = 'Настройки'
            self.about_button_text = 'Об игре'
            self.exit_button_text = 'Выход'
            self.question = 'Вы правда хотите выйти?'

    def InitUI(self):
        self.play_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((150, 150), (300, 60)),
            text=self.play_button_text,
            manager=self.manager,
        )
        self.shop_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((150, 220), (300, 60)),
            text=self.shop_button_text,
            manager=self.manager
        )
        self.settings_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((150, 290), (300, 60)),
            text=self.settings_button_text,
            manager=self.manager
        )
        self.about_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((150, 360), (300, 60)),
            text=self.about_button_text,
            manager=self.manager
        )
        self.exit_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((150, 430), (300, 60)),
            text=self.exit_button_text,
            manager=self.manager
        )

    def loading_data(self):
        self.background = load_image(f'sprites/decoration/main/backgrounds/clouds/background.png')
        self.bird = load_image(f'sprites/birds/{selected_bird}.png', color_key=-1)
        self.main_text = load_image('sprites/decoration/main/main_text.png', color_key=-1)
        self.version = load_image('sprites/decoration/main/version.png', color_key=-1)
        self.sound_on_button = load_image('sprites/decoration/main/sound_on.png', color_key=-1)
        self.sound_off_button = load_image('sprites/decoration/main/sound_off.png', color_key=-1)
        self.rating_button = load_image('sprites/decoration/main/rating.png', color_key=-1)
        self.hide_button = load_image('sprites/decoration/main/hide.png', color_key=-1)

    def add_sprites(self):
        Rating_button(menu_button_sprites)
        Sound_button(menu_button_sprites)
        Roll_up_button(menu_button_sprites)

    def rendering(self):
        self.screen.blit(self.background, (0, 0))
        if len(background_sprites) < COUNT_TILES_BACKGROUND:
            Background_sprite(temporary_sprites)
        background_sprites.update()
        background_sprites.draw(self.screen)
        self.screen.blit(self.bird, (40, 80))
        self.screen.blit(self.version, (500, 580))
        self.screen.blit(self.main_text, (120, 20))
        self.manager.update(self.time_delta)
        self.manager.draw_ui(self.screen)
        menu_button_sprites.draw(self.screen)
        if pygame.mouse.get_focused():
            main_sprites.draw(self.screen)

    def show_confirmation_dialog(self):
        confirmation_dialog = pygame_gui.windows.UIConfirmationDialog(
            rect=pygame.Rect((100, 150), (300, 200)),
            manager=self.manager,
            window_title='Exit',
            action_long_desc=self.question,
            action_short_name='Yes',
            blocking=True
        )

    def run(self):
        self.add_sprites()
        clock = pygame.time.Clock()
        while self.running:
            self.time_delta = clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.MOUSEMOTION:
                    main_sprites.update(event.pos)
                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    full_cleaning_sprites()
                    if event.ui_element == self.play_button:
                        self.running = False
                        Game().run()
                    if event.ui_element == self.shop_button:
                        print('Shop pressed')
                    if event.ui_element == self.settings_button:
                        print('Settings pressed')
                    if event.ui_element == self.about_button:
                        print('About pressed')
                    if event.ui_element == self.exit_button:
                        self.show_confirmation_dialog()
                if event.type == pygame_gui.UI_CONFIRMATION_DIALOG_CONFIRMED:
                    self.running = False
                    sys.exit()
                menu_button_sprites.update(event)
                self.manager.process_events(event)
            self.rendering()
            pygame.display.update()


class Game:
    def __init__(self):
        self.size = self.width, self.height = SIZE_SCREEN
        self.screen = pygame.display.set_mode(self.size, flags=pygame.NOFRAME)
        self.language_selection()
        self.processes()
        self.loading_data()

    def language_selection(self):
        if language == 'english':
            pygame.display.set_caption('Game')
        else:
            pygame.display.set_caption('Игра')

    def processes(self):
        self.running = True
        self.stop = False
        self.score = -(COUNT_PIPES // 2)

    def loading_data(self):
        self.background = load_image(f'sprites/decoration/main/backgrounds/clouds/background.png')
        self.wallUp = load_image("sprites/decoration/game/bottom_pipe.png")
        self.wallDown = load_image("sprites/decoration/game/top_pipe.png")
        self.pause_button = load_image('sprites/decoration/game/pause.png', color_key=-1)

    def add_sprites(self):
        Player(load_image("sprites/birds/blue_sheet.png"), 4, 1, 50, 50)
        Pause_button(game_button_sprites)

    def rendering(self):
        self.screen.blit(self.background, (0, 0))
        if len(background_sprites) < COUNT_TILES_BACKGROUND:
            Background_sprite(temporary_sprites)
        background_sprites.update()
        background_sprites.draw(self.screen)
        if len(pipe_sprites) < COUNT_PIPES:
            self.score += 1
            Top_pipe(temporary_sprites)
            Bottom_pipe(temporary_sprites)
        pipe_sprites.update()
        pipe_sprites.draw(self.screen)
        player_sprite.update()
        player_sprite.draw(self.screen)
        self.font = pygame.font.SysFont("Orbitron", 50)
        self.screen.blit(self.font.render(str(self.score), -1, '#c76906'), (500, 10))
        game_button_sprites.draw(self.screen)

    def stop_game(self):
        pass

    def run(self):
        self.add_sprites()
        clock = pygame.time.Clock()
        while self.running:
            clock.tick(FPS)
            if self.stop is True:
                print(1)
                continue
            for event in pygame.event.get():
                game_button_sprites.update(event)
            self.rendering()
            if len(player_sprite) == 0:
                full_cleaning_sprites()
                global score
                score = self.score
                self.running = False
                Final().run()
            pygame.display.update()


class Final:
    def __init__(self):
        self.size = self.width, self.height = SIZE_SCREEN
        self.screen = pygame.display.set_mode(self.size, flags=pygame.NOFRAME)
        self.language_selection()
        self.processes()
        self.loading_data()

    def language_selection(self):
        if language == 'english':
            pygame.display.set_caption('Main menu')
            self.headline = 'Game over'
            self.points_text = 'points'
            self.prompt_text1 = 'Press the Space to start a new game'
            self.prompt_text2 = 'Press Esc to exit to the menu'
        else:
            self.headline = 'Конец игры'
            self.points_text = 'очков'
            self.prompt_text1 = 'Нажмите пробел, чтобы начать новую игру'
            self.prompt_text2 = 'Нажмите Esc, чтобы выйти в меню'

    def processes(self):
        self.running = True

    def loading_data(self):
        self.coin = load_image('sprites/decoration/game/big_coin.png')

    def rendering(self):
        intro_text = [(self.headline, 80, 90), (f'+ {score // 5}', 50, 60),
                      (f'{score} {self.points_text}', 30, 60),
                      (self.prompt_text1, 60, 23),
                      (self.prompt_text2, 60, 23)]
        self.screen.fill((255, 186, 0))
        self.screen.blit((self.coin), (210, 180))
        text_coord = 50
        for text, coord, fnt in intro_text:
            font = pygame.font.SysFont("Orbitron", fnt)
            string_rendered = font.render(text, 1, pygame.Color('black'))
            intro_rect = string_rendered.get_rect()
            intro_rect.x = 130
            intro_rect.top = text_coord
            text_coord += coord
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)

    def run(self):
        clock = pygame.time.Clock()
        pygame.font.init()
        while self.running:
            clock.tick(FPS)
            self.rendering()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    full_cleaning_sprites()
                    if event.key == pygame.K_SPACE:
                        self.running = False
                        Game().run()
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                        Main().run()
            pygame.display.update()


if __name__ == "__main__":
    language = "english"
    selected_bird = 'classic'
    selected_background = ''
    pygame.font.init()
    Cursor(main_sprites)
    pygame.display.set_icon(pygame.image.load("data/sprites/decoration/icon.png"))
    music_play()
    Main().run()
    pygame.quit()