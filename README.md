# 关税对决：公共经济模拟游戏

## 项目简介

> “细雨轻拂，晨钟响起。谁能预见，一纸关税，如何撼动国家命运？”  

《关税对决》是一款基于 Python + Pygame 的回合制模拟游戏，旨在直观理解公共经济学中关税政策的运作逻辑及其对国家经济与社会福祉的多重影响。玩家扮演执政者，通过每轮调整进口关税，体验如何在贸易摩擦、公共支出与民意支持之间寻找平衡。

本项目既可作为经济学教学实践示例，也适合作为编程训练素材，帮助你将抽象的经济学原理转化为可视化、交互式的游戏体验。

---

## 一、背景设定

在某个海岸之国，海风与潮声日夜交替；商船川流不息，为繁华带来外来商品与财富。  
然而，国家财政日益拮据，公共服务质量下滑，民众愈发不满。  
为了重振经济，政府决定对外来商品征收关税：  
- 提高关税可短期增加财政收入，用于教育、医疗等公共项目；  
- 但过高的关税也会抬高进口成本，减少贸易往来，甚至引发外部制裁。  

你，作为这片土地的掌舵者，需要在 **国家富强** 与 **民众福祉** 之间作出抉择。  
当晨钟再度敲响，新的回合即将开始：你将如何制定关税，以平衡经济与社会？

---

## 二、经济学原理与机制详解

本游戏根据公共经济学中的经典模型，将经济变量拆解为以下主要部分，并以 Python 代码模拟其动态变化。

1. **关税对进口的影响**  
   - 设定基础进口额 `BASE_IMPORTS`（例如 3000 亿美元）；  
   - 实际进口额随关税上升而下降：  
     ```
     imports = BASE_IMPORTS / (1 + tariff * TARIFF_FACTOR)
     ```  
     其中，`tariff` 为关税税率（0.0 ~ 1.0），`TARIFF_FACTOR` 为敏感度系数（设为 2.0），表示关税每增加 1%，进口额下降的强度。  

2. **进口减少与国内生产替代**  
   - 当进口减少时，部分需求会转向本国生产，带来国内生产的增加：  
     ```
     production = BASE_PRODUCTION + (import_reduction * SUBSTITUTION)
     ```  
     其中，`BASE_PRODUCTION` 是初始国内产量，`import_reduction = BASE_IMPORTS - imports`，`SUBSTITUTION`（如 0.3）表示每减少 1 单位进口，就有 0.3 单位需求转向国内。  

3. **关税收入与政府财政**  
   - 政府征收关税带来直接的财政收入：  
     ```
     revenue = imports * tariff
     ```  
     这部分收入可作为公共支出的来源。  

4. **GDP 计算模型**  
   - 游戏中将 GDP 拆分为三部分：  
     1. **国内生产带来的增量**：`production - BASE_PRODUCTION`；  
     2. **贸易摩擦损失**：当进口减少时，伴随着交易成本与资源错配，会产生效率损失，按 `import_reduction * FRICTION` 扣减；  
     3. **政府支出对 GDP 的正向乘数效应**：`revenue * REVENUE_GDP_MULTIPLIER`。  
   - 最终 GDP 计算如下：  
     ```
     GDP = BASE_GDP + (production - BASE_PRODUCTION) - (import_reduction * FRICTION) + (revenue * REVENUE_GDP_MULTIPLIER)
     ```  
     - `BASE_GDP` 为初始 GDP（例如 10000 亿美元）；  
     - `FRICTION`（如 0.15）表示贸易摩擦损失率；  
     - `REVENUE_GDP_MULTIPLIER`（如 0.1）表示政府支出产生的 GDP 乘数效应。  

5. **公共服务质量（Public Services Quality）**  
   - 假设公共服务质量初始在 70 分（满分 100）；  
   - 政府将关税收入的一部分用于公共服务提升，设 `SERVICE_MULTIPLIER = 0.5`：  
     ```
     Δservices = revenue * SERVICE_MULTIPLIER * 0.01
     ```  
   - 每轮更新后，服务质量为上一轮服务值加上 `Δservices`，并限制在 [0, 100] 范围内。  

6. **民众支持度（Citizen Support）**  
   - 民众支持度由 GDP 变化与公共服务质量共同决定，设基准支持度为 50%，再叠加：  
     ```
     support = 50 + (GDP - BASE_GDP) * GDP_SUPPORT + (services - 70) * SERVICE_SUPPORT
     ```  
     - `GDP_SUPPORT`（如 0.002）表示 GDP 每多增长 1 单位，支持度提升 0.002%；  
     - `SERVICE_SUPPORT`（如 0.3）表示服务质量每高于 70 分，支持度提升 0.3%。  
   - 最终 `support` 被限定在 [0, 100] 范围内。  

7. **随机突发事件（External Shocks）**  
   - 每回合有一定概率触发一次事件（概率约 15%），包括：  
     - **全球金融危机**：GDP 直接下滑 10%；  
     - **盟国断供**：进口额骤降 20%；  
     - **公共腐败事件**：公共服务质量下降 8 分；  
   - 这些事件通过直接修改 `current_gdp`、`current_imports` 或 `services` 来体现。  

8. **回合与结局机制**  
   - **回合数**：共计 20 回合。每轮玩家只能选择“提高关税”或“降低关税”5 个百分点，游戏自动进入下一回合并更新经济变量与图表。  
   - **结局评分**：第 21 回合结束后，系统根据综合表现计算总评分：  
     ```
     score = current_gdp + (services * 10) + (support * 20)
     ```  
     并根据 `support` 值判定三种结局：  
     - 支持度 > 80：**连任成功**；  
     - 60 < 支持度 ≤ 80：**勉强维持政权**；  
     - 支持度 ≤ 60：**被罢免**。  

---

## 三、核心玩法与用户指南

1. **游戏目标**  
   - 在 20 回合内，通过关税政策平衡国家经济与民众福祉，争取“连任成功”。

2. **界面布局（文字说明）**  
   - **左上方**：显示“当前回合 / 总回合”（如 “第 5 / 20 回合”）。  
   - **左中部**：显示关键经济指标：当前关税（%）、GDP（单位：亿 美元）、公共服务质量（0–100）、民众支持度（0–100 %）。  
   - **左下方**：动态信息区域，展示近 5 条“最新动态”（政策说明、事件通告）。  
   - **右侧中部**：折线图区域，实时绘制 GDP 曲线（蓝色）和支持度曲线（红色），X 轴为回合数，Y 轴为指标值。  
   - **底部中央**：两个按钮：“提高关税 (+5%)” 和 “降低关税 (-5%)”，单击其中一种即完成当轮决策并触发下一回合刷新。

3. **操作流程**  
   1. **启动游戏**：在命令行输入  
      ```bash
      python tariff_game_enhanced.py
      ```  
   2. **调整政策**：点击“提高关税 (+5%)” 或 “降低关税 (-5%)” 按钮之一。  
   3. **观察反馈**：系统更新 GDP、服务、支持度，并在“最新动态”区显示本轮信息；如触发事件，则显示 `[事件]xxx` 说明。折线图自动添加新数据点。  
   4. **重复操作**：在左侧指标反馈更新后，继续点击下一步按钮进入下一回合，直至第 20 回合结束。  
   5. **查看结局**：第 21 回合自动进入结局界面，显示“游戏结束”与“总评分”，并给出连任 / 维持 / 被罢免三种结局提示。窗口停留在结局界面，点击右上角关闭即可退出游戏。

---

## 四、项目结构与关键代码解读

```
tariff_game_enhanced/
- tariff_game_enhanced.py     # 游戏主程序（含所有功能模块）
- SimHei.ttf                  # 中文字体文件（须放置于同目录）
- README.md                   # 项目说明文档（当前文件）
```

### 1. 文件编码与注释

```python
# -*- coding: utf-8 -*-
"""
关税对决：图形增强版（含实时图表、稳定机制与动态提示修复）
"""
```
- 声明 UTF-8 编码，支持中文注释和字符串。

### 2. 导入依赖

```python
import pygame
import sys
import os
import random
```
- `pygame`：负责窗口创建、图形绘制、事件处理等。
- `sys`：用于程序退出控制。
- `os`：用于判断字体文件路径。
- `random`：用于随机事件触发。

### 3. 全局常量与配色

```python
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800
MAX_ROUNDS = 20
FONT_PATH = os.path.join(os.path.dirname(__file__), "SimHei.ttf")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
BLUE = (0, 0, 200)
GRAY = (230, 230, 230)
YELLOW = (240, 200, 0)
ORANGE = (255, 140, 0)
LIGHT_GRAY = (200, 200, 200)
```
- 界面尺寸、回合总数、字体路径；
- 常用 RGB 颜色定义，便于在绘图时调用。

### 4. 字体加载逻辑

```python
if os.path.exists(FONT_PATH):
    font_small  = pygame.font.Font(FONT_PATH, 20)
    font_medium = pygame.font.Font(FONT_PATH, 26)
    font_large  = pygame.font.Font(FONT_PATH, 38)
else:
    font_small  = pygame.font.SysFont("SimHei", 20)
    font_medium = pygame.font.SysFont("SimHei", 26)
    font_large  = pygame.font.SysFont("SimHei", 38)
```
- 优先加载项目目录下的 `SimHei.ttf`，否则使用系统自带 “SimHei” 字体。

### 5. 初始化状态与界面

```python
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("关税对决：图形增强版")
clock  = pygame.time.Clock()

round_count    = 1
messages       = ["欢迎来到关税对决！"]

BASE_GDP       = 10000
BASE_IMPORTS   = 3000
BASE_PRODUCTION= 7000

current_tariff    = 0.0
current_gdp       = BASE_GDP
current_imports   = BASE_IMPORTS
current_production= BASE_PRODUCTION
revenue           = 0
services          = 70.0
support           = 75.0

gdp_history     = [BASE_GDP]
support_history = [support]
```
- 创建主窗口 `screen` 与时钟 `clock`；
- 初始化回合计数、动态消息列表；
- 基础经济数据与当前状态变量的初始化，供后续建模调用。
- `gdp_history`、`support_history` 用于存储折线图数据。

### 6. 参数配置

```python
TARIFF_FACTOR         = 2.0
SUBSTITUTION          = 0.3
FRICTION              = 0.15
REVENUE_GDP_MULTIPLIER= 0.1
SERVICE_MULTIPLIER    = 0.5
GDP_SUPPORT           = 0.002
SERVICE_SUPPORT       = 0.3
```
- 调整这些参数可改变游戏难度与经济模型灵敏度。

### 7. 绘制辅助函数

- `draw_text(txt, font, color, x, y, center=False)`：在 `screen` 上绘制文字，可选择居中或左对齐。
- `draw_line_chart(values, x0, y0, width, height, color, label)`：根据给定的数值列表绘制折线图，并标注图例。

### 8. 经济模型函数

- `update_economy()`：  
  - 依据 `current_tariff` 计算新的 `current_imports`、`current_production`、`revenue`、`current_gdp`；  
  - 更新 `services` 与 `support`；  
  - 将当轮 `gdp` 和 `support` 添加至历史列表，用于后续折线图绘制。

### 9. 动态消息与事件系统

- `add_message(msg)`：在 `messages` 列表中追加新消息，保持列表长度不超过 5。  
- `trigger_event()`：以 15% 概率触发随机事件，并修改对应经济变量及 `messages`。

### 10. 按钮处理

- `Button` 类：封装按钮属性（位置、大小、标签）与方法 `draw()`、`handle(event)`，用于渲染与鼠标点击交互。

### 11. 回合推进与结局

- `increase_tariff()` / `decrease_tariff()`：调整税率并触发 `next_round()`。  
- `next_round()`：自增回合、更新经济、触发事件、添加消息、检查是否超过最大回合并调用 `show_ending()`。  
- `show_ending()`：计算总评分并根据民众支持度输出对应结局文字，将界面切换到结局画面，仅响应退出事件。

---

## 七、致学生的一些学习建议

1. **探索经济模型灵敏度**  
   - 修改 `SUBSTITUTION`、`FRICTION`、`GDP_SUPPORT` 等参数，观察 GDP 与支持度曲线的变化，理解模型敏感度。  

2. **事件逻辑扩展**  
   - 将 “突发事件” 部分改写成从 JSON/CSV 文件加载，实现事件的可配置化；  
   - 增加更多事件类型，如“贸易谈判成功”“自然灾害”“技术进步”等，丰富游戏情节。  

3. **模块化重构**  
   - 将不同功能拆分为多个 Python 文件，如 `economic_model.py`、`events.py`、`ui.py` 等，提高代码可读性与可维护性；  
   - 尝试使用面向对象或函数式编程的方式对项目进行重构。

4. **图表与界面美化**  
   - 尝试用 `matplotlib` 绘制更精美的图表，或在 Pygame 中加入动画效果；  
   - 增加背景音乐或按钮点击音效，提高游戏体验；  
   - 设计更丰富的 UI 元素，如进度条、动态提示框等。

5. **政策组合与决策树**  
   - 为玩家提供更多决策选择，比如“财政补贴”“公共债务”“调节利率”等，形成一个多维度的政策组合；  
   - 如果感兴趣，可将游戏改造成带分支剧情的决策树，模拟不同政策组合带来的长远影响。  

---

## 八、总结

通过《关税对决》可以亲身体验关税政策对经济运行与社会福祉的多层面影响：  
- 理解关税对进口、GDP、政府收入与公共服务的联动关系；  
- 掌握公共服务质量与民众支持度的动态计算方法；  
- 体验随机事件对经济的冲击及应对策略；  
- 在有限回合内根据数据与直觉制定最优解，实现理论与实践结合。
