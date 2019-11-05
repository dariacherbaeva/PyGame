import pygame

pygame.init()

icon = pygame.image.load('images/icon.png')  # иконка

barrier_img = [pygame.image.load('images/stone.png'), pygame.image.load('images/tree.png'),
               pygame.image.load('images/hydrant.png')]
stone_img = [pygame.image.load('images/Stone0.png'), pygame.image.load('images/Stone1.png')]
cloud_img = [pygame.image.load('images/cloud.png'), pygame.image.load('images/cloud.png')]

health_img = pygame.image.load('images/heart.png')
health_img = pygame.transform.scale(health_img, (30, 30))

bullet_img = pygame.image.load('images/shot.png')
bullet_img = pygame.transform.scale(bullet_img, (22, 5))

pers_img = [pygame.image.load('images/1.png'), pygame.image.load('images/2.png'), pygame.image.load('images/3.png'),
            pygame.image.load('images/4.png'), pygame.image.load('images/5.png')]

bird_img = [pygame.image.load('images/Bird0.png'), pygame.image.load('images/Bird1.png'),
            pygame.image.load('images/Bird2.png'),
            pygame.image.load('images/Bird3.png'), pygame.image.load('images/Bird4.png'),
            pygame.image.load('images/Bird5.png')]



