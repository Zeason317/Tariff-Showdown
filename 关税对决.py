# -*- coding: utf-8 -*-
"""
关税对决：图形增强版（含实时图表、稳定机制与动态提示修复）
"""
import pygame
import sys
import os
import random

pygame.init()

# ---------- 配置 ----------
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800
MAX_ROUNDS = 20
FONT_PATH = os.path.join(os.path.dirname(__file__), "SimHei.ttf")

# ---------- 颜色 ----------
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
BLUE = (0, 0, 200)
GRAY = (230, 230, 230)
YELLOW = (240, 200, 0)
ORANGE = (255, 140, 0)
LIGHT_GRAY = (200, 200, 200)

# ---------- 字体 ----------
if os.path.exists(FONT_PATH):
    font_small = pygame.font.Font(FONT_PATH, 20)
    font_medium = pygame.font.Font(FONT_PATH, 26)
    font_large = pygame.font.Font(FONT_PATH, 38)
else:
    font_small = pygame.font.SysFont("SimHei", 20)
    font_medium = pygame.font.SysFont("SimHei", 26)
    font_large = pygame.font.SysFont("SimHei", 38)

# ---------- 屏幕 ----------
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("关税对决：图形增强版")
clock = pygame.time.Clock()

# ---------- 游戏状态 ----------
round_count = 1
messages = ["欢迎来到关税对决！"]

BASE_GDP = 10000
BASE_IMPORTS = 3000
BASE_PRODUCTION = 7000

current_tariff = 0.0
current_gdp = BASE_GDP
current_imports = BASE_IMPORTS
current_production = BASE_PRODUCTION
revenue = 0
services = 70.0
support = 75.0

# 历史趋势数据
gdp_history = [BASE_GDP]
support_history = [support]

# ---------- 模型参数 ----------
TARIFF_FACTOR = 2.0
SUBSTITUTION = 0.3
FRICTION = 0.15
REVENUE_GDP_MULTIPLIER = 0.1
SERVICE_MULTIPLIER = 0.5
GDP_SUPPORT = 0.002
SERVICE_SUPPORT = 0.3

# ---------- 绘图函数 ----------
def draw_text(txt, font, color, x, y, center=False):
    render = font.render(txt, True, color)
    rect = render.get_rect()
    rect.center = (x, y) if center else (x, y)
    screen.blit(render, rect)

def draw_line_chart(values, x0, y0, width, height, color, label):
    if len(values) < 2:
        return
    max_val = max(values)
    min_val = min(values)
    if max_val == min_val:
        max_val += 1  # 避免除0
    points = []
    for i, v in enumerate(values):
        x = x0 + i * (width / MAX_ROUNDS)
        y = y0 + height * (1 - (v - min_val) / (max_val - min_val))
        points.append((x, y))
    pygame.draw.lines(screen, color, False, points, 2)
    draw_text(label, font_small, color, x0, y0 - 20)

# ---------- 按钮类 ----------
class Button:
    def __init__(self, label, x, y, w, h, action):
        self.rect = pygame.Rect(x, y, w, h)
        self.label = label
        self.action = action

    def draw(self):
        pygame.draw.rect(screen, BLUE, self.rect, border_radius=6)
        pygame.draw.rect(screen, BLACK, self.rect, 2, border_radius=6)
        draw_text(self.label, font_small, WHITE, self.rect.centerx, self.rect.centery, center=True)

    def handle(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.action()

# ---------- 核心逻辑 ----------
def update_economy():
    global current_imports, current_production, current_gdp, revenue, services, support
    imports = BASE_IMPORTS / (1 + current_tariff * TARIFF_FACTOR)
    import_reduction = BASE_IMPORTS - imports
    production = BASE_PRODUCTION + import_reduction * SUBSTITUTION
    revenue = imports * current_tariff
    gdp = BASE_GDP + (production - BASE_PRODUCTION) - import_reduction * FRICTION + revenue * REVENUE_GDP_MULTIPLIER
    services_incr = revenue * SERVICE_MULTIPLIER * 0.01
    services = max(0, min(100, services + services_incr))
    support = max(0, min(100, 50 + (gdp - BASE_GDP) * GDP_SUPPORT + (services - 70) * SERVICE_SUPPORT))

    current_imports = imports
    current_production = production
    current_gdp = gdp

    gdp_history.append(gdp)
    support_history.append(support)

# ---------- 游戏机制 ----------
def add_message(msg):
    if msg:
        messages.append(msg)
        if len(messages) > 5:
            messages.pop(0)

def increase_tariff():
    global current_tariff
    current_tariff = min(1.0, current_tariff + 0.05)
    next_round()

def decrease_tariff():
    global current_tariff
    current_tariff = max(0.0, current_tariff - 0.05)
    next_round()

def next_round():
    global round_count
    round_count += 1
    update_economy()
    trigger_event()
    add_message(f"第{round_count}轮：税率为{current_tariff*100:.1f}%")
    if round_count > MAX_ROUNDS:
        show_ending()

def trigger_event():
    global current_imports, services
    r = random.random()
    if r < 0.15:
        evt = random.choice(["全球金融危机，GDP 下滑。", "盟国断供，进口急剧下降。", "公共腐败事件，服务信任下降。"])
        add_message(f"[事件] {evt}")
        if "金融" in evt:
            current_gdp *= 0.9
        elif "盟国" in evt:
            current_imports *= 0.8
        elif "腐败" in evt:
            services = max(0, services - 8)

# ---------- 结局 ----------
def show_ending():
    score = current_gdp + services * 10 + support * 20
    screen.fill(GRAY)
    draw_text("游戏结束", font_large, BLACK, SCREEN_WIDTH//2, 100, center=True)
    draw_text(f"总评分：{int(score)}", font_medium, BLUE, SCREEN_WIDTH//2, 180, center=True)
    if support > 80:
        msg = "你成功连任，获得压倒性支持！"
    elif support > 60:
        msg = "你勉强维持政权，改革仍需努力。"
    else:
        msg = "你被罢免，改革失败。"
    draw_text(msg, font_medium, RED, SCREEN_WIDTH//2, 260, center=True)
    draw_text("关闭窗口以退出游戏。", font_small, BLACK, SCREEN_WIDTH//2, 330, center=True)
    pygame.display.flip()
    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

# ---------- 初始化 ----------
update_economy()
inc_btn = Button("提高关税 (+5%)", 180, 700, 200, 45, increase_tariff)
dec_btn = Button("降低关税 (-5%)", 600, 700, 200, 45, decrease_tariff)

# ---------- 主循环 ----------
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        inc_btn.handle(event)
        dec_btn.handle(event)

    screen.fill(GRAY)
    draw_text(f"第 {round_count} / {MAX_ROUNDS} 回合", font_large, BLACK, SCREEN_WIDTH//2, 20, center=True)
    draw_text(f"当前关税：{current_tariff*100:.1f}%", font_medium, BLACK, 60, 70)
    draw_text(f"GDP: {current_gdp:.0f} 亿美元", font_medium, BLACK, 60, 120)
    draw_text(f"服务质量: {services:.1f}/100", font_medium, BLUE, 60, 170)
    draw_text(f"民众支持度: {support:.1f}%", font_medium, RED, 60, 220)

    # 动态信息
    draw_text("最新动态：", font_medium, BLACK, 60, 280)
    for i, msg in enumerate(messages):
        draw_text(msg, font_small, BLACK, 80, 320 + i * 28)

    # 曲线图区域
    draw_line_chart(gdp_history, 550, 100, 380, 120, BLUE, "GDP 曲线")
    draw_line_chart(support_history, 550, 280, 380, 120, RED, "支持度曲线")

    inc_btn.draw()
    dec_btn.draw()

    pygame.display.flip()
    clock.tick(30)
