
import pygame
import os
import random

pygame.init()

# Create 12 sample product images
for i in range(1, 13):
    img = pygame.Surface((150, 150), pygame.SRCALPHA)
    bg_color = (
        random.randint(200, 255),
        random.randint(230, 255),
        random.randint(200, 230)
    )
    pygame.draw.rect(img, bg_color, (0, 0, 150, 150), border_radius=20)
    
    # Product emojis
    emojis = ['🍎', '🥕', '🍅', '🥔', '🍓', '🥒', '🫑', '🧅', '🌽', '🥬', '🍆', '🥦']
    text = pygame.font.Font(None, 72).render(emojis[i-1], True, (50, 50, 50))
    text_rect = text.get_rect(center=(75, 75))
    img.blit(text, text_rect)
    
    pygame.draw.rect(img, (180, 220, 180), (0, 0, 150, 150), 3, border_radius=20)
    pygame.image.save(img, f'product_images/product_{i}.png')
    print(f'Created product_images/product_{i}.png')

# Create sample profile images
emojis = ['👨‍🌾', '👩‍🌾', '🧑‍🌾', '👴‍🌾', '👵‍🌾', '👨', '👩', '🧑', '👴', '👵']
for i, emoji in enumerate(emojis):
    img = pygame.Surface((150, 150), pygame.SRCALPHA)
    pygame.draw.circle(img, (200, 240, 210), (75, 75), 70)
    pygame.draw.circle(img, (46, 204, 113), (75, 75), 70, 3)
    text = pygame.font.Font(None, 72).render(emoji, True, (46, 204, 113))
    text_rect = text.get_rect(center=(75, 75))
    img.blit(text, text_rect)
    pygame.image.save(img, f'profile_images/profile_{i}.png')
    print(f'Created profile_images/profile_{i}.png')

print('All sample images created successfully!')

