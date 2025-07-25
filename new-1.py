import pygame
import sys
import math
import os
import random
import glob
from pygame import gfxdraw
from pygame import mixer
import threading

# Initialize pygame
pygame.init()
mixer.init()

# Screen dimensions
WIDTH, HEIGHT = 1000, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("HTF - Helping The Farmers")

# Colors
BACKGROUND = (240, 245, 240)
PRIMARY_GREEN = (46, 204, 113)
SECONDARY_GREEN = (88, 214, 141)
LIGHT_GREEN = (200, 240, 210)
ACCENT_ORANGE = (255, 165, 0)
ACCENT_YELLOW = (241, 196, 15)
WHITE = (255, 255, 255)
BLACK = (20, 20, 20)
GRAY = (200, 200, 200)
LIGHT_GRAY = (230, 230, 230)
TEXT_COLOR = (50, 50, 50)
DARK_BACKGROUND = (30, 35, 40)
DARK_TEXT = (220, 220, 220)

# Fonts
title_font = pygame.font.Font(None, 48)
header_font = pygame.font.Font(None, 36)
button_font = pygame.font.Font(None, 24)
text_font = pygame.font.Font(None, 22)
small_font = pygame.font.Font(None, 18)

# Animation variables
current_screen = "role_selection"
transition_alpha = 0
transition_in = False
transition_out = False
selected_role = ""
farmer_tab = 0
buyer_tab = 0
search_text = ""
theme = "light"
username = "Farmer John"
buyer_username = "Buyer123"
profile_emoji = "👨‍🌾"
buyer_profile_emoji = "👨"
product_images = {}
notification = {"text": "", "time": 0, "color": PRIMARY_GREEN}
form_fields = {"name": "", "price": "", "description": "", "emoji": "🌾"}
cart_items = []
flying_items = []
active_animations = []
search_active = False
adding_product = False
current_image_path = ""
image_preview = None
image_preview_rect = None
selected_image_path = ""
uploading_image = False
image_upload_progress = 0
new_screen_name = ""
cart_count = 0
cart_bounce = 0
cart_bounce_dir = 1
search_results = []

# Create directories if not exists
if not os.path.exists("product_images"):
    os.makedirs("product_images")

if not os.path.exists("profile_images"):
    os.makedirs("profile_images")

# Load sample product images
def load_product_images():
    product_surfaces = {}
    
    # Load any existing images
    for img_path in glob.glob("product_images/*.png"):
        try:
            img_name = os.path.basename(img_path)
            img = pygame.image.load(img_path)
            img = pygame.transform.scale(img, (100, 100))
            product_surfaces[img_name] = img
        except:
            pass
    
    # Generate sample images if none exist
    if not product_surfaces:
        for i in range(1, 13):
            img = pygame.Surface((150, 150), pygame.SRCALPHA)
            bg_color = (
                random.randint(200, 255),
                random.randint(230, 255),
                random.randint(200, 230)
            )
            pygame.draw.rect(img, bg_color, (0, 0, 150, 150), border_radius=20)
            
            # Draw a product representation
            emoji = ["🍎", "🥕", "🍅", "🥔", "🍓", "🥒", "🫑", "🧅", "🌽", "🥬", "🍆", "🥦"][i-1]
            text = pygame.font.Font(None, 72).render(emoji, True, (50, 50, 50))
            text_rect = text.get_rect(center=(75, 75))
            img.blit(text, text_rect)
            
            # Draw decorative elements
            pygame.draw.rect(img, (180, 220, 180), (0, 0, 150, 150), 3, border_radius=20)
            
            # Save to file
            path = f"product_images/product_{i}.png"
            pygame.image.save(img, path)
            img = pygame.transform.scale(img, (100, 100))
            product_surfaces[f"product_{i}.png"] = img
    
    return product_surfaces

# Load product images
product_surfaces = load_product_images()

# Load profile images
def load_profile_images():
    profile_surfaces = {}
    
    # Default profile images
    for i, emoji in enumerate(["👨‍🌾", "👩‍🌾", "🧑‍🌾", "👴‍🌾", "👵‍🌾", "👨", "👩", "🧑", "👴", "👵"]):
        img = pygame.Surface((150, 150), pygame.SRCALPHA)
        pygame.draw.circle(img, LIGHT_GREEN, (75, 75), 70)
        pygame.draw.circle(img, PRIMARY_GREEN, (75, 75), 70, 3)
        text = pygame.font.Font(None, 72).render(emoji, True, PRIMARY_GREEN)
        text_rect = text.get_rect(center=(75, 75))
        img.blit(text, text_rect)
        profile_surfaces[f"profile_{i}.png"] = img
    
    # Load any existing user-uploaded profile images
    for img_path in glob.glob("profile_images/*.png"):
        try:
            img_name = os.path.basename(img_path)
            img = pygame.image.load(img_path)
            img = pygame.transform.scale(img, (150, 150))
            profile_surfaces[img_name] = img
        except:
            pass
    
    return profile_surfaces

# Load profile images
profile_surfaces = load_profile_images()

# Sample data
farmer_products = [
    {"id": 1, "name": "Organic Apples", "price": "$2.99/kg", "description": "Freshly picked organic apples", "image": "product_1.png", "stock": 50},
    {"id": 2, "name": "Carrots", "price": "$1.49/kg", "description": "Sweet and crunchy carrots", "image": "product_2.png", "stock": 80},
    {"id": 3, "name": "Tomatoes", "price": "$3.29/kg", "description": "Vine-ripened tomatoes", "image": "product_3.png", "stock": 40},
    {"id": 4, "name": "Potatoes", "price": "$1.99/kg", "description": "Fresh from the farm potatoes", "image": "product_4.png", "stock": 60},
]
buyer_products = [
    {"id": 1, "name": "Organic Apples", "price": "$2.99/kg", "description": "Freshly picked organic apples", "image": "product_1.png", "stock": 50},
    {"id": 2, "name": "Carrots", "price": "$1.49/kg", "description": "Sweet and crunchy carrots", "image": "product_2.png", "stock": 80},
    {"id": 3, "name": "Tomatoes", "price": "$3.29/kg", "description": "Vine-ripened tomatoes", "image": "product_3.png", "stock": 40},
    {"id": 4, "name": "Potatoes", "price": "$1.99/kg", "description": "Fresh from the farm potatoes", "image": "product_4.png", "stock": 60},
    {"id": 5, "name": "Strawberries", "price": "$4.99/kg", "description": "Sweet and juicy strawberries", "image": "product_5.png", "stock": 30},
    {"id": 6, "name": "Cucumbers", "price": "$1.79/kg", "description": "Fresh cucumbers", "image": "product_6.png", "stock": 70},
    {"id": 7, "name": "Bell Peppers", "price": "$3.49/kg", "description": "Colorful bell peppers", "image": "product_7.png", "stock": 45},
    {"id": 8, "name": "Onions", "price": "$1.29/kg", "description": "Fresh onions", "image": "product_8.png", "stock": 65},
    {"id": 9, "name": "Corn", "price": "$0.99/ear", "description": "Sweet summer corn", "image": "product_9.png", "stock": 55},
    {"id": 10, "name": "Lettuce", "price": "$1.99/head", "description": "Crisp green lettuce", "image": "product_10.png", "stock": 35},
    {"id": 11, "name": "Eggplant", "price": "$2.49/kg", "description": "Fresh purple eggplant", "image": "product_11.png", "stock": 25},
    {"id": 12, "name": "Broccoli", "price": "$3.99/kg", "description": "Nutritious broccoli", "image": "product_12.png", "stock": 40},
]
orders = [
    {"id": 1001, "product": "Organic Apples", "quantity": "5 kg", "status": "Delivered"},
    {"id": 1002, "product": "Tomatoes", "quantity": "3 kg", "status": "Processing"},
    {"id": 1003, "product": "Carrots", "quantity": "2 kg", "status": "Cancelled"},
]

# Animation helper functions
def ease_in_out(t):
    return t * t * (3 - 2 * t)

def lerp(a, b, t):
    return a + (b - a) * t

def ease_out_back(t):
    c1 = 1.70158
    c3 = c1 + 1
    return 1 + c3 * pow(t - 1, 3) + c1 * pow(t - 1, 2)

def ease_out_bounce(t):
    n1 = 7.5625
    d1 = 2.75
    
    if t < 1 / d1:
        return n1 * t * t
    elif t < 2 / d1:
        t -= 1.5 / d1
        return n1 * t * t + 0.75
    elif t < 2.5 / d1:
        t -= 2.25 / d1
        return n1 * t * t + 0.9375
    else:
        t -= 2.625 / d1
        return n1 * t * t + 0.984375

def draw_rounded_rect(surface, rect, color, corner_radius):
    """Draw a rectangle with rounded corners"""
    pygame.draw.rect(surface, color, rect, border_radius=corner_radius)
    pygame.draw.rect(surface, (color[0]//2, color[1]//2, color[2]//2), rect, 1, border_radius=corner_radius)

def draw_button(surface, rect, text, color, hover=False, pressed=False, icon=None):
    """Draw a rounded button with hover and pressed states"""
    button_color = color
    shadow = pygame.Rect(rect.x, rect.y + 4, rect.width, rect.height)
    
    if pressed:
        button_color = (max(color[0] - 30, 0), max(color[1] - 30, 0), max(color[2] - 30, 0))
        rect.y += 2
    elif hover:
        button_color = (min(color[0] + 20, 255), min(color[1] + 20, 255), min(color[2] + 20, 255))
    
    # Draw shadow
    pygame.draw.rect(surface, (0, 0, 0, 30), shadow, border_radius=12)
    
    # Draw button
    draw_rounded_rect(surface, rect, button_color, 12)
    
    text_surf = button_font.render(text, True, WHITE)
    text_rect = text_surf.get_rect(center=rect.center)
    surface.blit(text_surf, text_rect)
    
    if pressed:
        rect.y -= 2

def draw_tab(surface, rect, text, active=False):
    """Draw a tab with sliding underline animation"""
    tab_color = LIGHT_GREEN
    text_color = TEXT_COLOR
    
    if active:
        tab_color = PRIMARY_GREEN
        text_color = WHITE
        
        # Draw animated underline
        underline_width = rect.width * 0.8
        pulse = abs(math.sin(pygame.time.get_ticks() / 300)) * 10
        underline = pygame.Rect(rect.centerx - underline_width/2, rect.bottom - 5, underline_width, 3 + pulse)
        pygame.draw.rect(surface, ACCENT_YELLOW, underline, border_radius=2)
    
    # Draw the main tab
    draw_rounded_rect(surface, rect, tab_color, 10)
    
    # Draw the text
    text_surf = text_font.render(text, True, text_color)
    text_rect = text_surf.get_rect(center=rect.center)
    surface.blit(text_surf, text_rect)

def draw_product_card(surface, rect, product, hover=False):
    """Draw a beautiful product card with animations"""
    card_color = WHITE
    border_color = SECONDARY_GREEN if hover else (200, 220, 200)
    scale = 1.02 if hover else 1.0
    
    # Apply hover scaling
    scaled_rect = pygame.Rect(
        rect.centerx - rect.width * scale / 2,
        rect.centery - rect.height * scale / 2,
        rect.width * scale,
        rect.height * scale
    )
    
    # Draw card background with shadow
    shadow = pygame.Rect(scaled_rect.x + 4, scaled_rect.y + 4, scaled_rect.width, scaled_rect.height)
    pygame.draw.rect(surface, (0, 0, 0, 30), shadow, border_radius=15)
    
    pygame.draw.rect(surface, card_color, scaled_rect, border_radius=15)
    pygame.draw.rect(surface, border_color, scaled_rect, 2, border_radius=15)
    
    # Draw product image
    image_rect = pygame.Rect(scaled_rect.left + 20, scaled_rect.top + 15, 100, 100)
    if product["image"] in product_surfaces:
        surface.blit(product_surfaces[product["image"]], image_rect)
    else:
        # Fallback if image not found
        pygame.draw.rect(surface, LIGHT_GRAY, image_rect, border_radius=10)
        pygame.draw.rect(surface, GRAY, image_rect, 1, border_radius=10)
        emoji = text_font.render("🌱", True, SECONDARY_GREEN)
        surface.blit(emoji, (image_rect.centerx - 10, image_rect.centery - 10))
    
    # Draw product info with perfect alignment
    name_surf = text_font.render(product["name"], True, TEXT_COLOR)
    surface.blit(name_surf, (scaled_rect.left + 20, scaled_rect.top + 125))
    
    price_surf = text_font.render(product["price"], True, ACCENT_ORANGE)
    surface.blit(price_surf, (scaled_rect.left + 20, scaled_rect.top + 155))
    
    desc_surf = small_font.render(product["description"], True, (100, 100, 100))
    surface.blit(desc_surf, (scaled_rect.left + 20, scaled_rect.top + 180))
    
    # Draw stock indicator
    stock_width = 120 * (product["stock"] / 100)
    pygame.draw.rect(surface, (220, 220, 220), (scaled_rect.left + 20, scaled_rect.top + 205, 120, 8), border_radius=4)
    pygame.draw.rect(surface, SECONDARY_GREEN, (scaled_rect.left + 20, scaled_rect.top + 205, stock_width, 8), border_radius=4)
    stock_text = small_font.render(f"Stock: {product['stock']}%", True, (80, 80, 80))
    surface.blit(stock_text, (scaled_rect.left + 20, scaled_rect.top + 218))
    
    return f"product_images/{product['image']}"

def draw_order_card(surface, rect, order, hover=False):
    """Draw a beautiful order card"""
    card_color = WHITE
    border_color = SECONDARY_GREEN if hover else (200, 220, 200)
    
    # Draw card background with shadow
    shadow = pygame.Rect(rect.x + 4, rect.y + 4, rect.width, rect.height)
    pygame.draw.rect(surface, (0, 0, 0, 30), shadow, border_radius=15)
    
    pygame.draw.rect(surface, card_color, rect, border_radius=15)
    pygame.draw.rect(surface, border_color, rect, 2, border_radius=15)
    
    # Draw order info
    order_id = text_font.render(f"Order #{order['id']}", True, TEXT_COLOR)
    surface.blit(order_id, (rect.left + 20, rect.top + 15))
    
    product = text_font.render(f"Product: {order['product']}", True, TEXT_COLOR)
    surface.blit(product, (rect.left + 20, rect.top + 45))
    
    quantity = text_font.render(f"Quantity: {order['quantity']}", True, TEXT_COLOR)
    surface.blit(quantity, (rect.left + 20, rect.top + 75))
    
    # Draw status with color coding
    status_color = PRIMARY_GREEN
    if order['status'] == "Processing":
        status_color = ACCENT_ORANGE
    elif order['status'] == "Cancelled":
        status_color = (200, 50, 50)
    
    status = text_font.render(f"Status: {order['status']}", True, status_color)
    surface.blit(status, (rect.left + 20, rect.top + 105))

def draw_search_bar(surface, rect, text, active=False):
    """Draw a beautiful search bar"""
    # Draw background
    bg_color = WHITE
    border_color = ACCENT_YELLOW if active else PRIMARY_GREEN
    draw_rounded_rect(surface, rect, bg_color, 25)
    
    # Draw border with animation
    border_width = 3 if active else 2
    pygame.draw.rect(surface, border_color, rect, border_width, border_radius=25)
    
    # Draw search icon
    icon_size = 15
    icon_x = rect.left + 20
    icon_y = rect.centery
    pygame.draw.circle(surface, (150, 150, 150), (icon_x, icon_y), icon_size, 1)
    handle_end_x = icon_x + math.cos(math.pi/4) * (icon_size + 5)
    handle_end_y = icon_y + math.sin(math.pi/4) * (icon_size + 5)
    pygame.draw.line(surface, (150, 150, 150), (icon_x + 5, icon_y + 5), (handle_end_x, handle_end_y), 2)
    
    # Draw text
    if text:
        text_surf = text_font.render(text, True, TEXT_COLOR)
    else:
        text_surf = text_font.render("Search products...", True, (150, 150, 150))
    surface.blit(text_surf, (rect.left + 50, rect.centery - text_surf.get_height() // 2))
    
    # Draw clear button if text is present
    if text:
        clear_rect = pygame.Rect(rect.right - 40, rect.centery - 12, 24, 24)
        pygame.draw.circle(surface, LIGHT_GRAY, clear_rect.center, 12)
        pygame.draw.line(surface, GRAY, (clear_rect.left+6, clear_rect.top+6), (clear_rect.right-6, clear_rect.bottom-6), 2)
        pygame.draw.line(surface, GRAY, (clear_rect.right-6, clear_rect.top+6), (clear_rect.left+6, clear_rect.bottom-6), 2)
        return clear_rect
    return None

def draw_profile_pic(surface, rect, size, emoji, profile_image=None):
    """Draw an animated profile picture"""
    pulse = math.sin(pygame.time.get_ticks() / 500) * 3
    pygame.draw.circle(surface, LIGHT_GREEN, rect.center, size + pulse)
    pygame.draw.circle(surface, PRIMARY_GREEN, rect.center, size + pulse, 2)
    
    # Draw profile image if available
    if profile_image and profile_image in profile_surfaces:
        img = pygame.transform.scale(profile_surfaces[profile_image], (size*2-10, size*2-10))
        img_rect = img.get_rect(center=rect.center)
        surface.blit(img, img_rect)
    else:
        # Draw placeholder icon
        user_icon = header_font.render(emoji, True, PRIMARY_GREEN)
        icon_rect = user_icon.get_rect(center=rect.center)
        surface.blit(user_icon, icon_rect)

def draw_image_uploader(surface, rect):
    """Draw the image uploader interface"""
    pygame.draw.rect(surface, WHITE, rect, border_radius=15)
    pygame.draw.rect(surface, PRIMARY_GREEN, rect, 2, border_radius=15)
    
    title = header_font.render("Upload Product Image", True, PRIMARY_GREEN)
    surface.blit(title, (rect.centerx - title.get_width()//2, rect.top + 20))
    
    # Draw preview area
    preview_rect = pygame.Rect(rect.centerx - 100, rect.top + 70, 200, 200)
    pygame.draw.rect(surface, LIGHT_GRAY, preview_rect, border_radius=10)
    pygame.draw.rect(surface, GRAY, preview_rect, 1, border_radius=10)
    
    # Draw preview if available
    if image_preview:
        scaled_img = pygame.transform.scale(image_preview, (180, 180))
        surface.blit(scaled_img, (preview_rect.centerx - 90, preview_rect.centery - 90))
    else:
        upload_text = text_font.render("No image selected", True, (150, 150, 150))
        surface.blit(upload_text, (preview_rect.centerx - upload_text.get_width()//2, 
                                 preview_rect.centery - upload_text.get_height()//2))
    
    # Draw upload button
    upload_btn = pygame.Rect(rect.centerx - 100, rect.top + 290, 200, 40)
    hover = upload_btn.collidepoint(pygame.mouse.get_pos())
    pressed = pygame.mouse.get_pressed()[0] and hover
    draw_button(surface, upload_btn, "Select Image", PRIMARY_GREEN, hover, pressed)
    
    # Draw progress bar if uploading
    if uploading_image:
        progress_rect = pygame.Rect(rect.left + 50, rect.top + 350, rect.width - 100, 20)
        pygame.draw.rect(surface, LIGHT_GRAY, progress_rect, border_radius=10)
        progress_width = max(10, (progress_rect.width - 4) * image_upload_progress / 100)
        progress_fill = pygame.Rect(progress_rect.left + 2, progress_rect.top + 2, progress_width, progress_rect.height - 4)
        pygame.draw.rect(surface, PRIMARY_GREEN, progress_fill, border_radius=8)
        
        progress_text = small_font.render(f"Uploading: {image_upload_progress}%", True, TEXT_COLOR)
        surface.blit(progress_text, (progress_rect.centerx - progress_text.get_width()//2, 
                                    progress_rect.bottom + 10))
    
    # Draw action buttons
    cancel_btn = pygame.Rect(rect.left + 50, rect.bottom - 60, 120, 40)
    hover_cancel = cancel_btn.collidepoint(pygame.mouse.get_pos())
    pressed_cancel = pygame.mouse.get_pressed()[0] and hover_cancel
    draw_button(surface, cancel_btn, "Cancel", (200, 50, 50), hover_cancel, pressed_cancel)
    
    confirm_btn = pygame.Rect(rect.right - 170, rect.bottom - 60, 120, 40)
    hover_confirm = confirm_btn.collidepoint(pygame.mouse.get_pos())
    pressed_confirm = pygame.mouse.get_pressed()[0] and hover_confirm
    btn_color = SECONDARY_GREEN if selected_image_path else GRAY
    draw_button(surface, confirm_btn, "Confirm", btn_color, hover_confirm, pressed_confirm and selected_image_path)
    
    return upload_btn, cancel_btn, confirm_btn

def draw_role_selection_screen():
    """Draw the beautiful role selection screen"""
    if theme == "dark":
        screen.fill(DARK_BACKGROUND)
    else:
        # Draw gradient background
        for y in range(HEIGHT):
            color_value = 240 - y / HEIGHT * 40
            pygame.draw.line(screen, (color_value, color_value + 10, color_value), (0, y), (WIDTH, y))
    
    # Draw animated background elements
    for i in range(8):
        angle = pygame.time.get_ticks() / 1000 + i * 0.5
        x = WIDTH // 2 + math.cos(angle) * 200
        y = HEIGHT // 3 + math.sin(angle) * 100
        size = 15 + math.sin(angle * 2) * 5
        color = (
            int(46 + math.sin(angle) * 20),
            int(204 + math.cos(angle) * 20),
            int(113 + math.sin(angle * 0.7) * 20)
        )
        pygame.draw.circle(screen, color, (x, y), size, 3)
    
    # Draw header with shadow
    title_surf = title_font.render("HTF - Helping The Farmers", True, PRIMARY_GREEN)
    title_shadow = title_font.render("HTF - Helping The Farmers", True, (30, 80, 50))
    screen.blit(title_shadow, (WIDTH // 2 - title_surf.get_width() // 2 + 2, 82))
    screen.blit(title_surf, (WIDTH // 2 - title_surf.get_width() // 2, 80))
    
    subtitle_surf = header_font.render("Direct from Farm to Table", True, SECONDARY_GREEN)
    subtitle_shadow = header_font.render("Direct from Farm to Table", True, (50, 120, 80))
    screen.blit(subtitle_shadow, (WIDTH // 2 - subtitle_surf.get_width() // 2 + 1, 151))
    screen.blit(subtitle_surf, (WIDTH // 2 - subtitle_surf.get_width() // 2, 150))
    
    # Draw farmer card with animation
    farmer_rect = pygame.Rect(WIDTH // 4 - 150, HEIGHT // 2 - 100, 300, 250)
    pygame.draw.rect(screen, (255, 255, 255, 200), farmer_rect, border_radius=20)
    pygame.draw.rect(screen, PRIMARY_GREEN, farmer_rect, 2, border_radius=20)
    
    # Animate farmer icon
    icon_y = farmer_rect.top + 80 + math.sin(pygame.time.get_ticks() / 300) * 10
    icon_rect = pygame.Rect(farmer_rect.centerx - 50, icon_y - 50, 100, 100)
    draw_profile_pic(screen, icon_rect, 50, "👨‍🌾")
    
    farmer_title = header_font.render("Farmer", True, PRIMARY_GREEN)
    farmer_title_rect = farmer_title.get_rect(center=(farmer_rect.centerx, farmer_rect.top + 140))
    screen.blit(farmer_title, farmer_title_rect)
    
    farmer_desc = text_font.render("Sell your products directly", True, TEXT_COLOR)
    farmer_desc_rect = farmer_desc.get_rect(center=(farmer_rect.centerx, farmer_rect.top + 180))
    screen.blit(farmer_desc, farmer_desc_rect)
    
    farmer_button = pygame.Rect(farmer_rect.centerx - 80, farmer_rect.bottom - 60, 160, 45)
    hover = farmer_button.collidepoint(pygame.mouse.get_pos())
    pressed = pygame.mouse.get_pressed()[0] and hover
    draw_button(screen, farmer_button, "I'm a Farmer", PRIMARY_GREEN, hover, pressed)
    
    # Draw buyer card with animation
    buyer_rect = pygame.Rect(3 * WIDTH // 4 - 150, HEIGHT // 2 - 100, 300, 250)
    pygame.draw.rect(screen, (255, 255, 255, 200), buyer_rect, border_radius=20)
    pygame.draw.rect(screen, PRIMARY_GREEN, buyer_rect, 2, border_radius=20)
    
    # Animate buyer icon
    icon_y = buyer_rect.top + 80 + math.cos(pygame.time.get_ticks() / 300) * 10
    icon_rect = pygame.Rect(buyer_rect.centerx - 50, icon_y - 50, 100, 100)
    draw_profile_pic(screen, icon_rect, 50, "👨")
    
    buyer_title = header_font.render("Buyer", True, PRIMARY_GREEN)
    buyer_title_rect = buyer_title.get_rect(center=(buyer_rect.centerx, buyer_rect.top + 140))
    screen.blit(buyer_title, buyer_title_rect)
    
    buyer_desc = text_font.render("Buy fresh products directly from farmers", True, TEXT_COLOR)
    buyer_desc_rect = buyer_desc.get_rect(center=(buyer_rect.centerx, buyer_rect.top + 180))
    screen.blit(buyer_desc, buyer_desc_rect)
    
    buyer_button = pygame.Rect(buyer_rect.centerx - 80, buyer_rect.bottom - 60, 160, 45)
    hover = buyer_button.collidepoint(pygame.mouse.get_pos())
    pressed = pygame.mouse.get_pressed()[0] and hover
    draw_button(screen, buyer_button, "I'm a Buyer", PRIMARY_GREEN, hover, pressed)
    
    # Draw footer
    footer_color = (150, 150, 150) if theme == "light" else (100, 100, 100)
    footer = small_font.render("Connecting Farmers and Buyers Directly Since 2023", True, footer_color)
    screen.blit(footer, (WIDTH // 2 - footer.get_width() // 2, HEIGHT - 40))
    
    # Draw notification if any
    if notification["text"] and pygame.time.get_ticks() - notification["time"] < 3000:
        notif_alpha = min(255, (3000 - (pygame.time.get_ticks() - notification["time"])) // 12)
        notif_surf = text_font.render(notification["text"], True, WHITE)
        notif_rect = notif_surf.get_rect(center=(WIDTH//2, HEIGHT-80))
        
        overlay = pygame.Surface((notif_rect.width + 40, notif_rect.height + 20), pygame.SRCALPHA)
        overlay.fill((*notification["color"], notif_alpha))
        pygame.draw.rect(overlay, WHITE, (0, 0, notif_rect.width + 40, notif_rect.height + 20), 2, border_radius=10)
        
        screen.blit(overlay, (notif_rect.x - 20, notif_rect.y - 10))
        screen.blit(notif_surf, notif_rect)
    
    return farmer_button, buyer_button

def draw_farmer_home_screen():
    """Draw the farmer home screen with beautiful tabs"""
    if theme == "dark":
        screen.fill(DARK_BACKGROUND)
    else:
        # Draw gradient background
        for y in range(HEIGHT):
            color_value = 240 - y / HEIGHT * 40
            pygame.draw.line(screen, (color_value, color_value + 10, color_value), (0, y), (WIDTH, y))
    
    # Draw header with shadow
    header_rect = pygame.Rect(0, 0, WIDTH, 80)
    pygame.draw.rect(screen, PRIMARY_GREEN, header_rect)
    pygame.draw.line(screen, (30, 120, 50), (0, 80), (WIDTH, 80), 2)
    
    title = header_font.render("HTF Farmer Dashboard", True, WHITE)
    title_shadow = header_font.render("HTF Farmer Dashboard", True, (200, 240, 200))
    screen.blit(title_shadow, (22, 22))
    screen.blit(title, (20, 20))
    
    # Draw profile preview with animation
    profile_rect = pygame.Rect(WIDTH - 50, 40, 60, 60)
    draw_profile_pic(screen, profile_rect, 30, profile_emoji)
    
    # Draw tabs with sliding indicator
    tabs_rect = pygame.Rect(0, 80, WIDTH, 60)
    pygame.draw.rect(screen, LIGHT_GREEN, tabs_rect)
    pygame.draw.line(screen, (180, 220, 180), (0, 140), (WIDTH, 140), 2)
    
    products_tab = pygame.Rect(50, 90, 180, 40)
    orders_tab = pygame.Rect(250, 90, 180, 40)
    profile_tab = pygame.Rect(450, 90, 180, 40)
    
    draw_tab(screen, products_tab, "My Products", farmer_tab == 0)
    draw_tab(screen, orders_tab, "Orders", farmer_tab == 1)
    draw_tab(screen, profile_tab, "Profile", farmer_tab == 2)
    
    # Draw content based on selected tab
    if farmer_tab == 0:
        # My Products tab
        add_product_rect = pygame.Rect(WIDTH - 220, 160, 180, 45)
        hover = add_product_rect.collidepoint(pygame.mouse.get_pos())
        pressed = pygame.mouse.get_pressed()[0] and hover
        draw_button(screen, add_product_rect, "+ Add Product", ACCENT_ORANGE, hover, pressed)
        
        # Draw products with animations
        for i, product in enumerate(farmer_products):
            card_y = 220 + i * 150
            # Animation effect for new products
            if product.get("new", False):
                anim_progress = min(1.0, (pygame.time.get_ticks() - product["added_time"]) / 500)
                card_y = lerp(HEIGHT, 220 + i * 150, ease_in_out(anim_progress))
                if anim_progress == 1.0:
                    product["new"] = False
            
            card_rect = pygame.Rect(WIDTH//2 - 250, card_y, 500, 180)
            hover_card = card_rect.collidepoint(pygame.mouse.get_pos())
            image_path = draw_product_card(screen, card_rect, product, hover_card)
            
            # Show image path on hover
            if hover_card:
                path_surf = small_font.render(f"Image: {image_path}", True, (100, 100, 100))
                screen.blit(path_surf, (card_rect.left, card_rect.bottom + 5))
            
            # Draw edit button
            edit_rect = pygame.Rect(card_rect.right - 110, card_rect.top + 135, 90, 35)
            hover_edit = edit_rect.collidepoint(pygame.mouse.get_pos())
            pressed_edit = pygame.mouse.get_pressed()[0] and hover_edit
            draw_button(screen, edit_rect, "Edit", SECONDARY_GREEN, hover_edit, pressed_edit)
        
        # Draw "Add Product" form if active
        if adding_product:
            form_rect = pygame.Rect(WIDTH//2 - 200, HEIGHT//2 - 200, 400, 400)
            pygame.draw.rect(screen, (255, 255, 255, 240), form_rect, border_radius=20)
            pygame.draw.rect(screen, PRIMARY_GREEN, form_rect, 2, border_radius=20)
            
            # Draw form title
            title = header_font.render("Add New Product", True, PRIMARY_GREEN)
            screen.blit(title, (form_rect.centerx - title.get_width()//2, form_rect.top + 20))
            
            # Draw image preview
            preview_rect = pygame.Rect(form_rect.centerx - 75, form_rect.top + 60, 150, 150)
            pygame.draw.rect(screen, LIGHT_GRAY, preview_rect, border_radius=10)
            pygame.draw.rect(screen, GRAY, preview_rect, 1, border_radius=10)
            
            if image_preview:
                scaled_img = pygame.transform.scale(image_preview, (140, 140))
                screen.blit(scaled_img, (preview_rect.centerx - 70, preview_rect.centery - 70))
            else:
                upload_text = text_font.render("No image", True, (150, 150, 150))
                screen.blit(upload_text, (preview_rect.centerx - upload_text.get_width()//2, 
                                         preview_rect.centery - upload_text.get_height()//2))
            
            # Draw upload button
            upload_btn = pygame.Rect(form_rect.centerx - 80, form_rect.top + 220, 160, 35)
            hover_upload = upload_btn.collidepoint(pygame.mouse.get_pos())
            pressed_upload = pygame.mouse.get_pressed()[0] and hover_upload
            draw_button(screen, upload_btn, "Upload Image", PRIMARY_GREEN, hover_upload, pressed_upload)
            
            # Draw form fields
            name_label = text_font.render("Product Name:", True, TEXT_COLOR)
            screen.blit(name_label, (form_rect.left + 30, form_rect.top + 270))
            
            name_rect = pygame.Rect(form_rect.left + 30, form_rect.top + 300, form_rect.width - 60, 35)
            pygame.draw.rect(screen, LIGHT_GRAY, name_rect, border_radius=5)
            pygame.draw.rect(screen, GRAY, name_rect, 1, border_radius=5)
            
            name_text = text_font.render(form_fields["name"], True, TEXT_COLOR)
            screen.blit(name_text, (name_rect.left + 10, name_rect.centery - name_text.get_height()//2))
            
            # Draw action buttons
            cancel_btn = pygame.Rect(form_rect.left + 50, form_rect.bottom - 60, 120, 40)
            hover_cancel = cancel_btn.collidepoint(pygame.mouse.get_pos())
            pressed_cancel = pygame.mouse.get_pressed()[0] and hover_cancel
            draw_button(screen, cancel_btn, "Cancel", (200, 50, 50), hover_cancel, pressed_cancel)
            
            save_btn = pygame.Rect(form_rect.right - 170, form_rect.bottom - 60, 120, 40)
            hover_save = save_btn.collidepoint(pygame.mouse.get_pos())
            pressed_save = pygame.mouse.get_pressed()[0] and hover_save
            btn_color = SECONDARY_GREEN if form_fields["name"] and selected_image_path else GRAY
            draw_button(screen, save_btn, "Save", btn_color, hover_save, pressed_save and form_fields["name"] and selected_image_path)
            
            return upload_btn, cancel_btn, save_btn
    
    elif farmer_tab == 1:
        # Orders tab
        # Draw orders
        for i, order in enumerate(orders):
            card_rect = pygame.Rect(WIDTH//2 - 250, 160 + i * 140, 500, 120)
            hover = card_rect.collidepoint(pygame.mouse.get_pos())
            draw_order_card(screen, card_rect, order, hover)
            
            # Draw message button
            msg_rect = pygame.Rect(card_rect.right - 110, card_rect.top + 75, 90, 35)
            hover_msg = msg_rect.collidepoint(pygame.mouse.get_pos())
            pressed_msg = pygame.mouse.get_pressed()[0] and hover_msg
            draw_button(screen, msg_rect, "Message", PRIMARY_GREEN, hover_msg, pressed_msg)
    
    elif farmer_tab == 2:
        # Profile tab
        profile_rect = pygame.Rect(WIDTH // 2 - 175, 160, 350, 400)
        pygame.draw.rect(screen, (255, 255, 255, 200), profile_rect, border_radius=20)
        pygame.draw.rect(screen, PRIMARY_GREEN, profile_rect, 2, border_radius=20)
        
        # Draw profile picture with animation
        pulse = math.sin(pygame.time.get_ticks() / 500) * 5
        profile_img_rect = pygame.Rect(profile_rect.centerx - 60, profile_rect.top + 30, 120, 120)
        draw_profile_pic(screen, profile_img_rect, 60, profile_emoji, "profile_0.png")
        
        # Draw username
        username_surf = header_font.render(username, True, TEXT_COLOR)
        screen.blit(username_surf, (profile_rect.centerx - username_surf.get_width() // 2, profile_rect.top + 160))
        
        # Draw buttons
        theme_btn = pygame.Rect(profile_rect.left + 75, profile_rect.top + 220, 200, 40)
        hover_theme = theme_btn.collidepoint(pygame.mouse.get_pos())
        pressed_theme = pygame.mouse.get_pressed()[0] and hover_theme
        draw_button(screen, theme_btn, "Change Theme", SECONDARY_GREEN, hover_theme, pressed_theme)
        
        username_btn = pygame.Rect(profile_rect.left + 75, profile_rect.top + 280, 200, 40)
        hover_username = username_btn.collidepoint(pygame.mouse.get_pos())
        pressed_username = pygame.mouse.get_pressed()[0] and hover_username
        draw_button(screen, username_btn, "Change Username", SECONDARY_GREEN, hover_username, pressed_username)
        
        photo_btn = pygame.Rect(profile_rect.left + 75, profile_rect.top + 340, 200, 40)
        hover_photo = photo_btn.collidepoint(pygame.mouse.get_pos())
        pressed_photo = pygame.mouse.get_pressed()[0] and hover_photo
        draw_button(screen, photo_btn, "Change Photo", SECONDARY_GREEN, hover_photo, pressed_photo)
        
        signout_btn = pygame.Rect(profile_rect.left + 75, profile_rect.top + 400, 200, 40)
        hover_signout = signout_btn.collidepoint(pygame.mouse.get_pos())
        pressed_signout = pygame.mouse.get_pressed()[0] and hover_signout
        draw_button(screen, signout_btn, "Sign Out", ACCENT_ORANGE, hover_signout, pressed_signout)
    
    # Draw notification if any
    if notification["text"] and pygame.time.get_ticks() - notification["time"] < 3000:
        notif_alpha = min(255, (3000 - (pygame.time.get_ticks() - notification["time"])) // 12)
        notif_surf = text_font.render(notification["text"], True, WHITE)
        notif_rect = notif_surf.get_rect(center=(WIDTH//2, 40))
        
        overlay = pygame.Surface((notif_rect.width + 40, notif_rect.height + 20), pygame.SRCALPHA)
        overlay.fill((*notification["color"], notif_alpha))
        pygame.draw.rect(overlay, WHITE, (0, 0, notif_rect.width + 40, notif_rect.height + 20), 2, border_radius=10)
        
        screen.blit(overlay, (notif_rect.x - 20, notif_rect.y - 10))
        screen.blit(notif_surf, notif_rect)
    
    return products_tab, orders_tab, profile_tab

def draw_buyer_home_screen():
    """Draw the buyer home screen with beautiful tabs"""
    global cart_bounce, cart_bounce_dir
    
    if theme == "dark":
        screen.fill(DARK_BACKGROUND)
    else:
        # Draw gradient background
        for y in range(HEIGHT):
            color_value = 240 - y / HEIGHT * 40
            pygame.draw.line(screen, (color_value, color_value + 10, color_value), (0, y), (WIDTH, y))
    
    # Draw header with shadow
    header_rect = pygame.Rect(0, 0, WIDTH, 80)
    pygame.draw.rect(screen, PRIMARY_GREEN, header_rect)
    pygame.draw.line(screen, (30, 120, 50), (0, 80), (WIDTH, 80), 2)
    
    title = header_font.render("HTF Marketplace", True, WHITE)
    title_shadow = header_font.render("HTF Marketplace", True, (200, 240, 200))
    screen.blit(title_shadow, (22, 22))
    screen.blit(title, (20, 20))
    
    # Draw profile preview with animation
    profile_rect = pygame.Rect(WIDTH - 50, 40, 60, 60)
    draw_profile_pic(screen, profile_rect, 30, buyer_profile_emoji)
    
    # Draw cart icon with animation
    cart_rect = pygame.Rect(WIDTH - 120, 40, 60, 60)
    pygame.draw.circle(screen, LIGHT_GREEN, cart_rect.center, 30)
    pygame.draw.circle(screen, PRIMARY_GREEN, cart_rect.center, 30, 2)
    
    cart_icon = text_font.render("🛒", True, PRIMARY_GREEN)
    cart_icon_rect = cart_icon.get_rect(center=cart_rect.center)
    screen.blit(cart_icon, cart_icon_rect)
    
    # Draw cart count with bounce animation
    if cart_count > 0:
        bounce_scale = 1.0 + cart_bounce * 0.2
        cart_count_rect = pygame.Rect(cart_rect.right - 15, cart_rect.top + 5, 30, 30)
        
        # Update bounce animation
        if cart_bounce_dir == 1:
            cart_bounce = min(cart_bounce + 0.1, 1.0)
            if cart_bounce == 1.0:
                cart_bounce_dir = -1
        else:
            cart_bounce = max(cart_bounce - 0.1, 0.0)
            if cart_bounce == 0.0:
                cart_bounce_dir = 1
        
        # Draw animated circle
        pygame.draw.circle(screen, ACCENT_ORANGE, cart_count_rect.center, 15 * bounce_scale)
        count_text = small_font.render(str(cart_count), True, WHITE)
        count_rect = count_text.get_rect(center=cart_count_rect.center)
        screen.blit(count_text, count_rect)
    
    # Draw tabs with sliding indicator
    tabs_rect = pygame.Rect(0, 80, WIDTH, 60)
    pygame.draw.rect(screen, LIGHT_GREEN, tabs_rect)
    pygame.draw.line(screen, (180, 220, 180), (0, 140), (WIDTH, 140), 2)
    
    browse_tab = pygame.Rect(50, 90, 180, 40)
    cart_tab = pygame.Rect(250, 90, 180, 40)
    orders_tab = pygame.Rect(450, 90, 180, 40)
    
    draw_tab(screen, browse_tab, "Browse Products", buyer_tab == 0)
    draw_tab(screen, cart_tab, "My Cart", buyer_tab == 1)
    draw_tab(screen, orders_tab, "My Orders", buyer_tab == 2)
    
    # Draw content based on selected tab
    if buyer_tab == 0:
        # Browse Products tab
        # Draw search bar
        search_rect = pygame.Rect(WIDTH // 2 - 200, 160, 400, 40)
        clear_btn = draw_search_bar(screen, search_rect, search_text, search_active)
        
        # Draw products grid
        num_cols = 3
        card_width, card_height = 250, 220
        spacing = 20
        start_x = (WIDTH - (num_cols * card_width + (num_cols - 1) * spacing)) // 2
        start_y = 220
        
        # Filter products based on search text
        if search_text:
            search_results = [p for p in buyer_products 
                             if search_text.lower() in p['name'].lower() 
                             or search_text.lower() in p['description'].lower()]
        else:
            search_results = buyer_products
        
        # Show search results count
        if search_text:
            results_text = text_font.render(f"Found {len(search_results)} products", True, PRIMARY_GREEN)
            screen.blit(results_text, (search_rect.left, search_rect.bottom + 10))
        
        for i, product in enumerate(search_results):
            col = i % num_cols
            row = i // num_cols
            x = start_x + col * (card_width + spacing)
            y = start_y + row * (card_height + spacing)
            
            card_rect = pygame.Rect(x, y, card_width, card_height)
            hover_card = card_rect.collidepoint(pygame.mouse.get_pos())
            
            # Add entrance animation for search results
            if product.get("new", False) or search_text:
                anim_progress = min(1.0, (pygame.time.get_ticks() - product.get("appear_time", 0)) / 500)
                if anim_progress < 1.0:
                    # Slide in from right
                    card_rect.x = lerp(WIDTH + 100, x, ease_out_back(anim_progress))
            
            image_path = draw_product_card(screen, card_rect, product, hover_card)
            
            # Draw add to cart button
            cart_btn = pygame.Rect(card_rect.right - 110, card_rect.bottom - 40, 100, 30)
            hover_cart = cart_btn.collidepoint(pygame.mouse.get_pos())
            pressed_cart = pygame.mouse.get_pressed()[0] and hover_cart
            draw_button(screen, cart_btn, "Add to Cart", PRIMARY_GREEN, hover_cart, pressed_cart)
    
    elif buyer_tab == 1:
        # My Cart tab
        cart_title = header_font.render("Your Shopping Cart", True, PRIMARY_GREEN)
        screen.blit(cart_title, (WIDTH // 2 - cart_title.get_width() // 2, 160))
        
        if not cart_items:
            empty_text = text_font.render("Your cart is empty. Start shopping!", True, TEXT_COLOR)
            screen.blit(empty_text, (WIDTH // 2 - empty_text.get_width() // 2, 220))
        else:
            # Draw cart items
            for i, item in enumerate(cart_items):
                item_rect = pygame.Rect(WIDTH//2 - 250, 200 + i * 100, 500, 80)
                pygame.draw.rect(screen, WHITE, item_rect, border_radius=10)
                pygame.draw.rect(screen, SECONDARY_GREEN, item_rect, 2, border_radius=10)
                
                # Draw item info
                name = text_font.render(item["name"], True, TEXT_COLOR)
                screen.blit(name, (item_rect.left + 20, item_rect.top + 15))
                
                price = text_font.render(item["price"], True, ACCENT_ORANGE)
                screen.blit(price, (item_rect.left + 20, item_rect.top + 45))
                
                # Draw remove button
                remove_btn = pygame.Rect(item_rect.right - 100, item_rect.top + 20, 80, 40)
                hover_remove = remove_btn.collidepoint(pygame.mouse.get_pos())
                pressed_remove = pygame.mouse.get_pressed()[0] and hover_remove
                draw_button(screen, remove_btn, "Remove", (200, 50, 50), hover_remove, pressed_remove)
        
        # Draw checkout button
        checkout_btn = pygame.Rect(WIDTH - 220, HEIGHT - 100, 180, 45)
        hover = checkout_btn.collidepoint(pygame.mouse.get_pos())
        pressed = pygame.mouse.get_pressed()[0] and hover
        draw_button(screen, checkout_btn, "Proceed to Checkout", ACCENT_ORANGE, hover, pressed)
        
        # Draw total
        total = sum(float(item["price"].replace("$", "").split("/")[0]) for item in cart_items)
        total_text = header_font.render(f"Total: ${total:.2f}", True, PRIMARY_GREEN)
        screen.blit(total_text, (WIDTH//2 - total_text.get_width()//2, HEIGHT - 160))
    
    elif buyer_tab == 2:
        # My Orders tab
        orders_title = header_font.render("Your Orders", True, PRIMARY_GREEN)
        screen.blit(orders_title, (WIDTH // 2 - orders_title.get_width() // 2, 160))
        
        for i, order in enumerate(orders):
            card_rect = pygame.Rect(WIDTH//2 - 250, 220 + i * 140, 500, 120)
            hover = card_rect.collidepoint(pygame.mouse.get_pos())
            draw_order_card(screen, card_rect, order, hover)
    
    # Draw notification if any
    if notification["text"] and pygame.time.get_ticks() - notification["time"] < 3000:
        notif_alpha = min(255, (3000 - (pygame.time.get_ticks() - notification["time"])) // 12)
        notif_surf = text_font.render(notification["text"], True, WHITE)
        notif_rect = notif_surf.get_rect(center=(WIDTH//2, 40))
        
        overlay = pygame.Surface((notif_rect.width + 40, notif_rect.height + 20), pygame.SRCALPHA)
        overlay.fill((*notification["color"], notif_alpha))
        pygame.draw.rect(overlay, WHITE, (0, 0, notif_rect.width + 40, notif_rect.height + 20), 2, border_radius=10)
        
        screen.blit(overlay, (notif_rect.x - 20, notif_rect.y - 10))
        screen.blit(notif_surf, notif_rect)
    
    return browse_tab, cart_tab, orders_tab, clear_btn if search_active else None

def draw_image_upload_screen():
    """Draw the image upload screen"""
    screen.fill(BACKGROUND)
    
    # Draw header
    header_rect = pygame.Rect(0, 0, WIDTH, 80)
    pygame.draw.rect(screen, PRIMARY_GREEN, header_rect)
    
    title = header_font.render("Upload Product Image", True, WHITE)
    screen.blit(title, (20, 20))
    
    # Draw uploader
    uploader_rect = pygame.Rect(WIDTH//2 - 200, HEIGHT//2 - 150, 400, 350)
    upload_btn, cancel_btn, confirm_btn = draw_image_uploader(screen, uploader_rect)
    
    # Draw notification if any
    if notification["text"] and pygame.time.get_ticks() - notification["time"] < 3000:
        notif_alpha = min(255, (3000 - (pygame.time.get_ticks() - notification["time"])) // 12)
        notif_surf = text_font.render(notification["text"], True, WHITE)
        notif_rect = notif_surf.get_rect(center=(WIDTH//2, 40))
        
        overlay = pygame.Surface((notif_rect.width + 40, notif_rect.height + 20), pygame.SRCALPHA)
        overlay.fill((*notification["color"], notif_alpha))
        pygame.draw.rect(overlay, WHITE, (0, 0, notif_rect.width + 40, notif_rect.height + 20), 2, border_radius=10)
        
        screen.blit(overlay, (notif_rect.x - 20, notif_rect.y - 10))
        screen.blit(notif_surf, notif_rect)
    
    return upload_btn, cancel_btn, confirm_btn

def show_notification(text, color=PRIMARY_GREEN):
    notification["text"] = text
    notification["color"] = color
    notification["time"] = pygame.time.get_ticks()

def start_transition(new_screen):
    """Start a transition to a new screen"""
    global transition_in, transition_out, transition_alpha, current_screen, new_screen_name
    transition_out = True
    transition_alpha = 0
    new_screen_name = new_screen

def simulate_image_upload():
    """Simulate an image upload process"""
    global uploading_image, image_upload_progress
    
    uploading_image = True
    for i in range(101):
        image_upload_progress = i
        pygame.time.delay(20)  # Simulate upload time
        pygame.event.pump()  # Keep the app responsive
    
    # Save the uploaded image
    if current_image_path and image_preview:
        img_name = f"product_{len(product_surfaces) + 1}.png"
        pygame.image.save(image_preview, f"product_images/{img_name}")
        
        # Add to product surfaces
        img = pygame.transform.scale(image_preview, (100, 100))
        product_surfaces[img_name] = img
        
        # Set as selected image
        global selected_image_path
        selected_image_path = img_name
        show_notification("Image uploaded successfully!")
    
    uploading_image = False

def add_to_cart_animation(product, start_pos):
    """Create a flying item animation when adding to cart"""
    global flying_items
    flying_items.append({
        "product": product,
        "start_pos": start_pos,
        "end_pos": (WIDTH - 120, 70),  # Cart position
        "progress": 0.0,
        "size": 30,
        "image": pygame.transform.scale(product_surfaces[product["image"]], (30, 30))
    })

# Main game loop
clock = pygame.time.Clock()
running = True
search_active = False
clear_btn = None
button_pressed = None
button_press_time = 0
search_results = buyer_products.copy()

while running:
    mouse_pos = pygame.mouse.get_pos()
    mouse_pressed = pygame.mouse.get_pressed()[0]
    
    # Update flying items animation
    for item in flying_items[:]:
        item["progress"] = min(item["progress"] + 0.05, 1.0)
        if item["progress"] == 1.0:
            cart_items.append(item["product"])
            cart_count = len(cart_items)
            flying_items.remove(item)
            show_notification(f"Added {item['product']['name']} to cart!")
    
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if current_screen == "buyer_home" and buyer_tab == 0 and search_active:
                if event.key == pygame.K_BACKSPACE:
                    search_text = search_text[:-1]
                elif event.key == pygame.K_RETURN:
                    show_notification(f"Searching for: {search_text}")
                elif event.key == pygame.K_ESCAPE:
                    search_active = False
                else:
                    search_text += event.unicode
            
            elif (current_screen == "farmer_home" and farmer_tab == 0 and adding_product) or \
                 (current_screen == "image_upload"):
                if event.key == pygame.K_BACKSPACE:
                    if form_fields["name"]:
                        form_fields["name"] = form_fields["name"][:-1]
                else:
                    form_fields["name"] += event.unicode
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if current_screen == "role_selection":
                farmer_btn, buyer_btn = draw_role_selection_screen()
                if farmer_btn.collidepoint(mouse_pos):
                    selected_role = "farmer"
                    start_transition("farmer_home")
                    button_pressed = "farmer"
                    button_press_time = pygame.time.get_ticks()
                elif buyer_btn.collidepoint(mouse_pos):
                    selected_role = "buyer"
                    start_transition("buyer_home")
                    button_pressed = "buyer"
                    button_press_time = pygame.time.get_ticks()
            
            elif current_screen == "farmer_home":
                products_tab, orders_tab, profile_tab = draw_farmer_home_screen()
                if products_tab.collidepoint(mouse_pos):
                    farmer_tab = 0
                    button_pressed = "products_tab"
                    button_press_time = pygame.time.get_ticks()
                elif orders_tab.collidepoint(mouse_pos):
                    farmer_tab = 1
                    button_pressed = "orders_tab"
                    button_press_time = pygame.time.get_ticks()
                elif profile_tab.collidepoint(mouse_pos):
                    farmer_tab = 2
                    button_pressed = "profile_tab"
                    button_press_time = pygame.time.get_ticks()
                
                # Handle profile actions
                if farmer_tab == 2:
                    theme_btn = pygame.Rect(WIDTH//2-175+75, 160+220, 200, 40)
                    username_btn = pygame.Rect(WIDTH//2-175+75, 160+280, 200, 40)
                    photo_btn = pygame.Rect(WIDTH//2-175+75, 160+340, 200, 40)
                    signout_btn = pygame.Rect(WIDTH//2-175+75, 160+400, 200, 40)
                    
                    if theme_btn.collidepoint(mouse_pos):
                        theme = "dark" if theme == "light" else "light"
                        show_notification(f"Theme changed to {theme} mode")
                    elif username_btn.collidepoint(mouse_pos):
                        form_fields["name"] = username
                        show_notification("Click and type new username, press Enter to save")
                    elif photo_btn.collidepoint(mouse_pos):
                        # In a real app, this would open an image selector
                        show_notification("Feature coming soon: Custom profile photos")
                    elif signout_btn.collidepoint(mouse_pos):
                        start_transition("role_selection")
                        show_notification("Signed out successfully")
                
                # Handle add product button
                if farmer_tab == 0:
                    add_btn = pygame.Rect(WIDTH - 220, 160, 180, 45)
                    if add_btn.collidepoint(mouse_pos):
                        adding_product = True
                        form_fields = {"name": "", "price": "", "description": "", "emoji": "🌾"}
                        current_image_path = ""
                        selected_image_path = ""
                        image_preview = None
                    
                    # Handle product form buttons
                    if adding_product:
                        form_rect = pygame.Rect(WIDTH//2 - 200, HEIGHT//2 - 200, 400, 400)
                        upload_btn = pygame.Rect(form_rect.centerx - 80, form_rect.top + 220, 160, 35)
                        cancel_btn = pygame.Rect(form_rect.left + 50, form_rect.bottom - 60, 120, 40)
                        save_btn = pygame.Rect(form_rect.right - 170, form_rect.bottom - 60, 120, 40)
                        
                        if upload_btn.collidepoint(mouse_pos):
                            # Transition to image upload screen
                            current_screen = "image_upload"
                        elif cancel_btn.collidepoint(mouse_pos):
                            adding_product = False
                        elif save_btn.collidepoint(mouse_pos) and form_fields["name"] and selected_image_path:
                            # Add new product
                            new_product = {
                                "id": len(farmer_products) + 1,
                                "name": form_fields["name"],
                                "price": f"${random.uniform(1, 5):.2f}/kg",
                                "description": "Fresh from the farm",
                                "image": selected_image_path,
                                "stock": random.randint(30, 90),
                                "new": True,
                                "added_time": pygame.time.get_ticks()
                            }
                            farmer_products.append(new_product)
                            adding_product = False
                            show_notification("Product added successfully!")
            
            elif current_screen == "buyer_home":
                browse_tab, cart_tab, orders_tab, clear_btn = draw_buyer_home_screen()
                if browse_tab.collidepoint(mouse_pos):
                    buyer_tab = 0
                elif cart_tab.collidepoint(mouse_pos):
                    buyer_tab = 1
                elif orders_tab.collidepoint(mouse_pos):
                    buyer_tab = 2
                
                # Handle search bar
                if buyer_tab == 0:
                    search_rect = pygame.Rect(WIDTH // 2 - 200, 160, 400, 40)
                    if search_rect.collidepoint(mouse_pos):
                        search_active = True
                    elif clear_btn and clear_btn.collidepoint(mouse_pos):
                        search_text = ""
                    else:
                        search_active = False
                    
                    # Add "appear_time" for search results animation
                    for product in search_results:
                        if "appear_time" not in product:
                            product["appear_time"] = pygame.time.get_ticks()
                    
                    # Handle add to cart buttons
                    num_cols = 3
                    card_width, card_height = 250, 220
                    spacing = 20
                    start_x = (WIDTH - (num_cols * card_width + (num_cols - 1) * spacing)) // 2
                    start_y = 220
                    
                    for i, product in enumerate(search_results):
                        col = i % num_cols
                        row = i // num_cols
                        x = start_x + col * (card_width + spacing)
                        y = start_y + row * (card_height + spacing)
                        
                        card_rect = pygame.Rect(x, y, card_width, card_height)
                        cart_btn = pygame.Rect(card_rect.right - 110, card_rect.bottom - 40, 100, 30)
                        
                        if cart_btn.collidepoint(mouse_pos):
                            # Start flying animation
                            add_to_cart_animation(product, (cart_btn.centerx, cart_btn.centery))
                            # Add appear time for animation
                            product["appear_time"] = pygame.time.get_ticks()
                
                # Handle cart actions
                if buyer_tab == 1:
                    # Handle remove buttons
                    for i, item in enumerate(cart_items):
                        item_rect = pygame.Rect(WIDTH//2 - 250, 200 + i * 100, 500, 80)
                        remove_btn = pygame.Rect(item_rect.right - 100, item_rect.top + 20, 80, 40)
                        
                        if remove_btn.collidepoint(mouse_pos):
                            cart_items.remove(item)
                            cart_count = len(cart_items)
                            show_notification(f"Removed {item['name']} from cart")
            
            elif current_screen == "image_upload":
                upload_btn, cancel_btn, confirm_btn = draw_image_upload_screen()
                
                if upload_btn.collidepoint(mouse_pos):
                    # Simulate image selection
                    # In a real app, this would open a file dialog
                    if not uploading_image:
                        # Generate a sample image
                        img = pygame.Surface((300, 300), pygame.SRCALPHA)
                        color = (random.randint(100, 200), random.randint(100, 200), random.randint(100, 200))
                        pygame.draw.rect(img, color, (0, 0, 300, 300), border_radius=20)
                        
                        # Draw a product representation
                        emoji = ["🍎", "🥕", "🍅", "🥔", "🍓", "🥒", "🫑", "🧅", "🌽", "🥬", "🍆", "🥦"][len(product_surfaces) % 12]
                        text = pygame.font.Font(None, 120).render(emoji, True, WHITE)
                        text_rect = text.get_rect(center=(150, 150))
                        img.blit(text, text_rect)
                        
                        # Draw decorative elements
                        pygame.draw.rect(img, (180, 220, 180), (0, 0, 300, 300), 5, border_radius=20)
                        
                        image_preview = img
                        current_image_path = f"product_{len(product_surfaces) + 1}.png"
                        
                        # Simulate upload
                        threading.Thread(target=simulate_image_upload).start()
                
                elif cancel_btn.collidepoint(mouse_pos):
                    current_screen = "farmer_home"
                    image_preview = None
                    current_image_path = ""
                    selected_image_path = ""
                
                elif confirm_btn.collidepoint(mouse_pos) and selected_image_path:
                    current_screen = "farmer_home"
    
    # Draw the current screen
    if current_screen == "role_selection":
        farmer_btn, buyer_btn = draw_role_selection_screen()
    elif current_screen == "farmer_home":
        products_tab, orders_tab, profile_tab = draw_farmer_home_screen()
    elif current_screen == "buyer_home":
        browse_tab, cart_tab, orders_tab, clear_btn = draw_buyer_home_screen()
    elif current_screen == "image_upload":
        upload_btn, cancel_btn, confirm_btn = draw_image_upload_screen()
    
    # Draw flying items
    for item in flying_items:
        t = item["progress"]
        # Use ease out bounce for more playful animation
        t_eased = ease_out_bounce(t)
        current_x = lerp(item["start_pos"][0], item["end_pos"][0], t_eased)
        current_y = lerp(item["start_pos"][1], item["end_pos"][1], t_eased)
        
        # Draw the flying item
        img_rect = item["image"].get_rect(center=(current_x, current_y))
        screen.blit(item["image"], img_rect)
    
    # Handle transitions
    if transition_out:
        transition_alpha = min(transition_alpha + 8, 255)
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, transition_alpha))
        screen.blit(overlay, (0, 0))
        
        if transition_alpha == 255:
            transition_out = False
            transition_in = True
            current_screen = new_screen_name
            transition_alpha = 255
    
    if transition_in:
        transition_alpha = max(transition_alpha - 8, 0)
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, transition_alpha))
        screen.blit(overlay, (0, 0))
        
        if transition_alpha == 0:
            transition_in = False
    
    # Draw animated background elements
    for i in range(20):
        x = (pygame.time.get_ticks() // 20 + i * 50) % (WIDTH + 100) - 50
        y = HEIGHT - 20 + math.sin(pygame.time.get_ticks() / 400 + i) * 10
        size = 3 + math.sin(pygame.time.get_ticks() / 300 + i) * 2
        color = (
            int(46 + math.sin(i) * 20),
            int(204 + math.cos(i) * 20),
            int(113 + math.sin(i * 0.7) * 20)
        )
        pygame.draw.circle(screen, color, (x, y), size)
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
