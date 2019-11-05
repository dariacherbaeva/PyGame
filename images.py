import pygame

pygame.init()

icon = pygame.image.load('icon.png')  # иконка

barrier_img = [pygame.image.load('Cactus0.png'), pygame.image.load('Cactus1.png'), pygame.image.load('Cactus2.png')]
stone_img = [pygame.image.load('Stone0.png'), pygame.image.load('Stone1.png')]
cloud_img = [pygame.image.load('Cloud0.png'), pygame.image.load('Cloud1.png')]

health_img = pygame.image.load('heart.png')
health_img = pygame.transform.scale(health_img, (30, 30))

bullet_img = pygame.image.load('shot.png')
bullet_img = pygame.transform.scale(bullet_img, (22, 5))

pers_img = [pygame.image.load('Dino0.png'), pygame.image.load('Dino1.png'), pygame.image.load('Dino2.png'),
            pygame.image.load('Dino3.png'), pygame.image.load('Dino4.png')]

bird_img = [pygame.image.load('Bird0.png'), pygame.image.load('Bird1.png'), pygame.image.load('Bird2.png'),
            pygame.image.load('Bird3.png'), pygame.image.load('Bird4.png'), pygame.image.load('Bird5.png')]



