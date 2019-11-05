import os
from datetime import datetime

from models.object import *
from models.bullet import *
from models.button import *
from models.bird import *
from materials.images import *
from materials import parameters as p
from materials.effects import *
from materials.sounds import *


class Game:
    def __init__(self):
        pygame.display.set_caption('Run Away!')  # название игры

        pygame.mixer_music.load('sounds/Attack.mp3')  # музыка
        pygame.mixer_music.set_volume(0.15)

        pygame.display.set_icon(icon)

        self.cactus_option = [69, 449, 37, 410, 40, 420]
        self.img_counter = 0
        self.health = 2
        self.make_jump = False
        self.jump_counter = 30
        self.scores = 0
        self.max_scores = 0
        self.max_above = 0
        self.cd = 0

    def show_menu(self):
        menu_bckgr = pygame.image.load('images/Menu.jpg')

        start_btn = Button(288, 70)
        quit_btn = Button(120, 70)

        show = True
        while show:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            display.blit(menu_bckgr, (0, 0))
            start_btn.draw(270, 200, 'Начать игру!', self.start_game, 38)
            quit_btn.draw(358, 300, 'Выход', quit, 30)

            pygame.display.update()
            clock.tick(60)

    def start_game(self):
        """ Функция расширения run_game()
        Введена для работы с рекордами
        Обнуляет положение игрока(без нее можно было начать новую игру в прыжке)
        """

        self.scores = 0
        self.make_jump = False
        self.jump_counter = 30
        p.usr_y = display_height - usr_height - 100
        self.health = 2
        self.cd = 0
        while self.game_cycle():
            self.scores = 0
            self.make_jump = False
            self.jump_counter = 30
            p.usr_y = p.display_height - p.usr_height - 100
            self.health = 2
            self.cd = 0

    def game_cycle(self):  # главный цикл для работы игры
        pygame.mixer.music.play(-1)

        game = True
        barrier_arr = []
        self.create_barrier_arr(barrier_arr)
        land = pygame.image.load('images/Land.jpg')

        stone, cloud = self.open_random_objects()
        heart = Object(display_width, 280, 30, health_img, 4)

        all_btn_bullets = []
        all_ms_bullets = []

        bird1 = Bird(-80)
        bird2 = Bird(-49)

        all_birds = [bird1, bird2]

        while game:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            keys = pygame.key.get_pressed()
            mouse = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()
            self.count_scores(barrier_arr)

            # ниже описана прорисовка фона, препятствий, гг и элементов декора (камни, облака), а также вывод рекорда
            display.blit(land, (0, 0))
            print_text('Рекорд: ' + str(self.scores), 600, 10)

            self.draw_array(barrier_arr)
            self.move_objects(stone, cloud)

            self.draw_pers()

            # ниже идут "скрипты" на нажатие определенных клавиш
            if keys[pygame.K_SPACE]:
                self.make_jump = True

            if self.make_jump:
                self.jump()

            if keys[pygame.K_ESCAPE]:
                self.pause()
            if not self.cd:
                if keys[pygame.K_x]:
                    pygame.mixer.Sound.play(bullet_sound)
                    all_btn_bullets.append(Bullet(usr_x + usr_width, usr_y))
                    self.cd = 50
                elif click[0]:
                    pygame.mixer.Sound.play(bullet_sound)
                    add_bullet = Bullet(usr_x + usr_width, usr_y + 28)
                    add_bullet.find_path(mouse[0], mouse[1])

                    all_ms_bullets.append(add_bullet)
                    self.cd = 50

            else:
                print_text('Кд - ' + str(self.cd // 10), 600, 40)
                self.cd -= 1

            for bullet in all_btn_bullets:
                if not bullet.move():
                    all_btn_bullets.remove(bullet)

            for bullet in all_ms_bullets:
                if not bullet.move_to():
                    all_ms_bullets.remove(bullet)

            heart.move()
            self.hearts_plus(heart)

            if self.check_collision(barrier_arr):
                pygame.mixer.music.stop()
                pygame.mixer.Sound.play(loss_sound)
                game = False

            self.show_health()

            self.draw_birds(all_birds)
            self.check_birds_dmg(all_ms_bullets, all_birds)

            pygame.display.update()
            clock.tick(70)
        return self.game_over()

    def jump(self):
        """ Функция прыжка
        ГГ взлетает вверх в зависимости от параметра jump_counter, тот в свою очередь уменьшается,
        после чего уменьшается на единицу. Это обеспечивает плавный подъем.
        Для удобства изменение позиции по Y поделено на 2.5, тк ГГ подлетал под верхнюю границу.
        """
        if self.jump_counter >= -30:
            if self.jump_counter == -10:
                pygame.mixer.Sound.play(fall_sound)

            p.usr_y -= self.jump_counter / 2.5
            self.jump_counter -= 1
        else:
            self.jump_counter = 30
            self.make_jump = False

    def create_barrier_arr(self, array):
        # Функция создания препятствия и введение всех его параметров
        choice = random.randrange(0, 3)
        img = barrier_img[choice]
        width = barrier_options[choice * 2]
        height = barrier_options[choice * 2 + 1]
        array.append(Object(display_width + 20, height, width, img, 4))

        choice = random.randrange(0, 3)
        img = barrier_img[choice]
        width = barrier_options[choice * 2]
        height = barrier_options[choice * 2 + 1]
        array.append(Object(display_width + 300, height, width, img, 4))

        choice = random.randrange(0, 3)
        img = barrier_img[choice]
        width = barrier_options[choice * 2]
        height = barrier_options[choice * 2 + 1]
        array.append(Object(display_width + 600, height, width, img, 4))

    @staticmethod
    def find_radius(array):
        """ Функция поиска расстояния между препятствиями.
        Метод используются только для адекватной рисовки препятствий.
        Нужен для избежания ситуаций, в которых игрок не может перепрыгнуть препятствия.
        если между объектами непреодолимое расстояние, то один из объектов либо будет отодвинут на большое расстояние,
        либо придвинут влотную к впереди идущему объекту(работает при расстоянии менее 50 пикселей).
        """
        maximum = max(array[0].x, array[1].x, array[2].x)

        if maximum < display_width:
            radius = display_width
            if radius - maximum < 50:
                radius += 280
        else:
            radius = maximum

        choice = random.randrange(0, 5)
        if choice == 0:
            radius += random.randrange(10, 15)
        else:
            radius += random.randrange(250, 400)

        return radius

    def draw_array(self, array):
        """ Функция прориссовки массива перпятствий.
        Если не будет проблем с радиусом (метод find_radius), то будет прорисован рандомное препятствие.
        После нахождения рандомного числа будут взять параметры из barrier_options.
        Для получения ширины возьмем из массива рандомное число*2, для высоты добавим еще 1.
        Далее случайное препятствие будет отрисованно на дисплее.

        P.S
        randrange не выдает как рандомное числа свою верхнюю границу (в нашем случае - 3).

        V.10
        Функция изменена
        все вынесено в отдельную, обощающую функцию object_return
        """
        for barrier in array:
            check = barrier.move()
            if not check:
                self.object_return(array, barrier)

    def object_return(self, objects, obj):
        """Вспомогательная функция
        Выделена как общий случай.
        Используется check_collision'ом.При столкновении с ГГ сдвигает за край экрана.
        Также используется draw_array'ом для прорисовки препятствий.
        """
        radius = self.find_radius(objects)

        choice = random.randrange(0, 3)
        img = barrier_img[choice]
        width = barrier_options[choice * 2]
        height = barrier_options[choice * 2 + 1]

        obj.return_self(radius, height, width, img)

    @staticmethod
    def open_random_objects():
        """ Функция задающий параметры дополнительным объектам.
        Задает параметры для облаков и камней.
        Выбирает рандомно одну из 2 моделей облака/камня.
        """
        choice = random.randrange(0, 2)
        img_of_stone = stone_img[choice]

        choice = random.randrange(0, 2)
        img_of_cloud = cloud_img[choice]

        stone = Object(display_width, display_height - 80, 10, img_of_stone, 4)
        cloud = Object(display_width, 80, 70, img_of_cloud, 2)

        return stone, cloud

    @staticmethod
    def move_objects(stone, cloud):
        """ Функция выполняющий движение дополнительных объектов.
        Прописывает движение облаков выше игрока, а камней - под игроком(эффект движения земли).
        """
        check = stone.move()
        if not check:
            choice = random.randrange(0, 2)
            img_of_stone = stone_img[choice]
            stone.return_self(p.display_width, 500 + random.randrange(10, 80), stone.width, img_of_stone)

        check = cloud.move()
        if not check:
            choice = random.randrange(0, 2)
            img_of_cloud = cloud_img[choice]
            cloud.return_self(p.display_width, random.randrange(10, 200), stone.width, img_of_cloud)

    def draw_pers(self):
        """ Функция анимации ГГ.
        Перебирает 5 картинок, каждая срабатывает по 5 раз, тк
        быстрые тики в игре делают анимацию слишком быстрой.
        """
        if self.img_counter == 25:
            self.img_counter = 0

        display.blit(pers_img[self.img_counter // 5], (p.usr_x, p.usr_y))
        self.img_counter += 1

    @staticmethod
    def pause():
        """ Функция работы паузы.
        Объявление параметров текста, скрипт остановки игры на Esc и активации на Enter.
        Остановка музыки на паузе.
        """
        paused = True

        pygame.mixer.music.pause()

        while paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            print_text('Игра на паузе', 160, 300)

            keys = pygame.key.get_pressed()
            if keys[pygame.K_RETURN]:
                paused = False

            pygame.display.update()
            clock.tick(15)

        pygame.mixer.music.unpause()

    def check_collision(self, barriers):
        """ Функция улучшенной логики столкновения ГГ с препятствием.
        Обработка случаев когда правый нижний угол ГГ задевает препятствие.
        Описание поведения для встречи с низким объектом (не задевает верхний правый участок ГГ),
        а также поведения пр прыжке (пустые пиксели в "прямоугольнике ГГ" не должны вызывать скрипт столкновения).
        При срабатывании функции игра заканчивается.
        Отнимает здоровья для ударов.

        V.10
        Проверяет в check_health, отлично ли от нуля кол-во жизней у ГГ
        Если значение отлично от нуля, то мы рисуем кактус в новой позиции с помощью object_return
        """
        for barrier in barriers:
            if barrier.y == 449:  # маленьний кактус
                if not self.make_jump:
                    if barrier.x <= p.usr_x + p.usr_width - 35 <= barrier.x + barrier.width:
                        if self.check_health():
                            self.object_return(barriers, barrier)
                            pygame.mixer.Sound.play(fall_sound)
                            return False
                        else:
                            return True

                elif self.jump_counter >= 0:
                    if p.usr_y + p.usr_height - 5 >= barrier.y:
                        if barrier.x <= p.usr_x + p.usr_width - 35 <= barrier.x + barrier.width:
                            if self.check_health():
                                self.object_return(barriers, barrier)
                                pygame.mixer.Sound.play(fall_sound)
                                return False
                            else:
                                return True
                else:
                    if p.usr_y + usr_height - 10 >= barrier.y:
                        if barrier.x <= p.usr_x <= barrier.x + barrier.width:
                            if self.check_health():
                                self.object_return(barriers, barrier)
                                pygame.mixer.Sound.play(fall_sound)
                                return False
                            else:
                                return True
            else:
                if not self.make_jump:
                    if barrier.x <= p.usr_x + p.usr_width - 5 <= barrier.x + barrier.width:
                        if self.check_health():
                            self.object_return(barriers, barrier)
                            pygame.mixer.Sound.play(fall_sound)
                            return False
                        else:
                            return True
                elif self.jump_counter == 10:
                    if p.usr_y + usr_height - 5 >= barrier.y:
                        if barrier.x <= p.usr_x + p.usr_width - 5 <= barrier.x + barrier.width:
                            if self.check_health():
                                self.object_return(barriers, barrier)
                                pygame.mixer.Sound.play(fall_sound)
                                return False
                            else:
                                return True
                elif self.jump_counter >= -1:
                    if p.usr_y + usr_height - 5 >= barrier.y:
                        if barrier.x <= p.usr_x + p.usr_width - 35 <= barrier.x + barrier.width:
                            if self.check_health():
                                self.object_return(barriers, barrier)
                                pygame.mixer.Sound.play(fall_sound)
                                return False
                            else:
                                return True
                    else:
                        if p.usr_y + usr_height - 10 >= barrier.y:
                            if barrier.x <= p.usr_x + 5 <= barrier.x + barrier.width:
                                if self.check_health():
                                    self.object_return(barriers, barrier)
                                    pygame.mixer.Sound.play(fall_sound)
                                    return False
                                else:
                                    return True
        return False

    def count_scores(self, barriers):
        """ Функция засчитывания очков
        Увеличивает кол-во очков за каждое перепрыгнутое препятствие
        Отдельно обработан случай для перепрыгивания 2 объектов
        """
        above_barrier = 0

        if -20 <= self.jump_counter < 25:
            for barrier in barriers:
                if p.usr_y + p.usr_height - 5 <= barrier.y:
                    if barrier.x <= p.usr_x <= barrier.x + barrier.width:
                        above_barrier += 1
                    elif barrier.x <= p.usr_x + p.usr_width <= barrier.x + barrier.width:
                        above_barrier += 1

            self.max_above = max(self.max_above, above_barrier)
        else:
            if self.jump_counter == -30:
                self.scores += self.max_above
                self.max_above = 0

    def game_over(self):
        """ Функция описывающая поведение при окончании игры
        выводит текст/информирует о набранных очках
        """
        restart_btn = Button(257, 60)
        leave_btn = Button(127, 50)
        if self.scores > self.max_scores:
            self.max_scores = self.scores

        stopped = True
        while stopped:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            print_text('Вы проиграли!', 280, 100)

            restart_btn.draw(271.5, 200, 'Начать заново', self.start_game, 30)

            leave_btn.draw(336.5, 270, 'Выход', self.show_menu, 30)
            print_text('Максимальный рекорд: ' + str(self.max_scores), 200, 150)

            keys = pygame.key.get_pressed()
            if keys[pygame.K_RETURN]:
                return True
            if keys[pygame.K_ESCAPE]:
                return False

            pygame.display.update()
            clock.tick(15)

            file = open("records.txt", 'w')
            file.write(str(self.max_scores))
            file.write(" очков ")
            file.write("\n")
            file.close()

    def show_health(self):
        # прорисовка сердечек
        show = 0
        x = 20
        while show != self.health:
            display.blit(health_img, (x, 20))
            x += 40
            show += 1

    def check_health(self):
        # проверка на наличие сердечек. 0 = конец
        self.health -= 1
        if self.health == 0:
            return False
        else:
            return True

    def hearts_plus(self, heart):
        if heart.x <= -heart.width:
            radius = p.display_width + random.randrange(500, 1700)
            heart.return_self(radius, heart.y, heart.width, heart.image)

        if p.usr_x <= heart.x <= p.usr_x + p.usr_width:
            if p.usr_y <= heart.y <= p.usr_y + p.usr_height:
                if self.health < 5:
                    pygame.mixer.Sound.play(heart_plus_sound)
                    self.health += 1

                radius = p.display_width + random.randrange(500, 1700)
                heart.return_self(radius, heart.y, heart.width, heart.image)

    @staticmethod
    def draw_birds(birds):
        for bird in birds:
            action = bird.draw()
            if action == 1:
                bird.show()
            elif action == 2:
                bird.hide()

    @staticmethod
    def check_birds_dmg(bullets, birds):
        for bird in birds:
            for bullet in bullets:
                bird.check_dmg(bullet)
