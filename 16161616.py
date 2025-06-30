import pygame
import random
import math

pygame.init()
screen = pygame.display.set_mode((800, 600))

image_assets = {
    "monster": pygame.transform.scale(
        pygame.image.load("images/monster.webp").convert_alpha(), (40, 40)
    ),
    "mid_boss": pygame.transform.scale(
        pygame.image.load("images/middle_boss.webp").convert_alpha(), (50, 50)
    ),
    "final_boss": pygame.transform.scale(
        pygame.image.load("images/final_boss.webp").convert_alpha(), (100, 100)
    ),
    "warrior_normal": pygame.transform.scale(
        pygame.image.load("images/normal.png").convert_alpha(), (50, 50)
    ),
    "warrior_knight": pygame.transform.scale(
        pygame.image.load("images/knight.png").convert_alpha(), (50, 50)
    ),
    "warrior_berserker": pygame.transform.scale(
        pygame.image.load("images/berserker.png").convert_alpha(), (50, 50)
    ),
    "archer_normal": pygame.transform.scale(
        pygame.image.load("images/archer.png").convert_alpha(), (50, 50)
    ),
    "archer_triple": pygame.transform.scale(
        pygame.image.load("images/triple.png").convert_alpha(), (50, 50)
    ),
    "archer_arrow": pygame.transform.scale(
        pygame.image.load("images/arrow.png").convert_alpha(), (50, 50)
    ),
    "start": pygame.transform.scale(
        pygame.image.load("images/start.png").convert(), (800, 600)
    ),
    "shop": pygame.transform.scale(
        pygame.image.load("images/shop.png").convert(), (800, 600)
    ),
    "background": pygame.transform.scale(
        pygame.image.load("images/background.png").convert(), (800, 600)
    ),
    "final": pygame.transform.scale(
        pygame.image.load("images/final.png").convert(), (800, 600)
    ),
    "victory": pygame.transform.scale(
        pygame.image.load("images/victory.png").convert(), (800, 600)
    ),
}






pygame.display.set_caption("보스 물리치기 RPG")
clock = pygame.time.Clock()
font = pygame.font.Font("C:/Windows/Fonts/malgun.ttf", 24)
# 색상 정의
CYAN = (0, 255, 255)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
PURPLE = (160, 32, 240)
GOLD = (255, 215, 0)  # ✨ 황금색 추가

# 기본 스탯
WARRIOR_BASE = {"attack": 18, "atk_speed": 2.25, "move_speed": 4.0, "hp": 150}
ARCHER_BASE = {"attack": 160, "atk_speed": 1.2, "move_speed": 5.0, "hp": 130}

font = pygame.font.Font("C:/Windows/Fonts/malgun.ttf", 20) # 설명서 추가 코드 (1/3)

def draw_help(): # 설명서 추가 코드 (2/3)
    help_lines = [
        "📘 게임 도움말 (Enter 키로 시작)",
        "",
        "🎯 목표: 최종 보스를 물리치세요!",
        "",
        "🧑‍🎮 조작법:",
        "- 이동: W A S D",
        "- 공격: 전사(Space), 궁수(마우스 클릭)",
        "- 스킬: LSHIFT",
        "- 메뉴: 방향키 + Enter",
        "",
        "⚔ 직업 및 전직:",
        "- 전사: 버서커(스탯 2배), 기사(무적)",
        "- 궁수: 트리플(3갈래), 애로우(광선)",
        "",
        "🛍 상점:",
        "- 공격력, 속도, 체력 업그레이드 가능",
        "",
        "👹 보스:",
        "- 3스테이지부터 등장, 8스테이지 최종보스",
        "- 회전탄막, 체력바 있음",
        "",
        "💡 팁:",
        "- 궁수는 거리 유지, 버서커는 타이밍 중요"
    ]
    screen.fill(BLACK)
    for i, line in enumerate(help_lines):
        text = font.render(line, True, WHITE)
        screen.blit(text, (50, 30 + i * 24))

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect(center=(400, 300))
        self.job = None
        self.subjob = None
        self.attack_power = 0
        self.attack_speed = 0
        self.speed = 0
        self.health = 0
        self.max_health = 0
        self.gold = 200
        self.attack_cooldown = 0
        self.invincible = False
        self.invincible_time = 0
        self.skill_cooldown = 0
        self.skill_active = False
        self.skill_time = 0

    def set_job(self, job):
        self.job = job
        if job == "Warrior":
            self.image = image_assets["warrior_normal"]
            base = WARRIOR_BASE
        else:
            base = ARCHER_BASE
            self.image = image_assets["archer_normal"]
        self.attack_power = base["attack"]
        self.attack_speed = base["atk_speed"]
        self.speed = base["move_speed"]
        self.health = base["hp"]
        self.max_health = self.health

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]: self.rect.x -= self.speed
        if keys[pygame.K_d]: self.rect.x += self.speed
        if keys[pygame.K_w]: self.rect.y -= self.speed
        if keys[pygame.K_s]: self.rect.y += self.speed
        self.rect.clamp_ip(screen.get_rect())
        if self.attack_cooldown > 0: self.attack_cooldown -= 1
        if self.invincible:
            self.invincible_time -= 1
            if self.invincible_time <= 0: self.invincible = False
        if self.skill_cooldown > 0:
            self.skill_cooldown -= 1
        if self.skill_active:
            self.skill_time -= 1
            if self.skill_time <= 0:
                self.skill_active = False
                if self.subjob == "Berserker":
                    self.attack_power //= 2
                    self.attack_speed /= 2
                    self.speed /= 2
    def take_damage(self, damage):
        if not self.invincible and self.health > 0:
            self.health = max(0, self.health - damage)
            self.invincible = True
            self.invincible_time = 60

    def attack(self, pos=None):
        if self.attack_cooldown <= 0 and self.health > 0:
            self.attack_cooldown = int(60 / self.attack_speed)
            if self.job == "Warrior":
                return WarriorAttack(self)
            elif self.job == "Archer" and pos:
                if self.subjob == "Triple":
                    return TripleShot(self.rect.center, pos).projectiles
                else:
                    return [ArcherProjectile(self.rect.center, pos)]
        return None

    def use_skill(self, mouse_pos):
        if self.skill_cooldown > 0 or not self.subjob:
            return []
        projectiles = []
        if self.subjob == "Berserker":
            self.skill_active = True
            self.skill_time = 180
            self.skill_cooldown = 1800
            self.attack_power *= 2
            self.attack_speed *= 2
            self.speed *= 2
        elif self.subjob == "Knight":
            self.invincible = True
            self.invincible_time = 120
            self.skill_cooldown = 600
        elif self.subjob == "Arrow":
            self.skill_cooldown = 60
            directions = ["up", "down", "left", "right"]
            for dir in directions:
                beam = LaserBeam(self.rect.center, dir, self.attack_power * 3)
                projectiles.append(beam)


        return projectiles

class WarriorAttack(pygame.sprite.Sprite):
    def __init__(self, player):
        super().__init__()
        self.radius = 40
        self.image = pygame.Surface((80, 80), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (255, 0, 0, 100), (40, 40), self.radius)
        self.rect = self.image.get_rect(center=player.rect.center)
        self.damage = player.attack_power
        self.lifetime = 10

    def update(self):
        self.lifetime -= 1
        if self.lifetime <= 0:
            self.kill()

class ArcherProjectile(pygame.sprite.Sprite):
    def __init__(self, start_pos, target_pos):
        super().__init__()
        self.image = pygame.Surface((10, 10))
        self.image.fill(ORANGE)
        self.rect = self.image.get_rect(center=start_pos)
        dx = target_pos[0] - start_pos[0]
        dy = target_pos[1] - start_pos[1]
        dist = math.hypot(dx, dy)
        self.dx = dx / dist * 12 if dist != 0 else 0
        self.dy = dy / dist * 12 if dist != 0 else 0
        self.damage = ARCHER_BASE["attack"]

    def update(self):
        self.rect.x += self.dx
        self.rect.y += self.dy
        if not (0 <= self.rect.x <= 800 and 0 <= self.rect.y <= 600):
            self.kill()

class TripleShot(pygame.sprite.Sprite):
    def __init__(self, start_pos, target_pos):
        self.projectiles = []
        dx = target_pos[0] - start_pos[0]
        dy = target_pos[1] - start_pos[1]
        angle = math.atan2(dy, dx)
        for offset in [-0.3, 0, 0.3]:
            angle_offset = angle + offset
            end_pos = (
                start_pos[0] + math.cos(angle_offset) * 100,
                start_pos[1] + math.sin(angle_offset) * 100
            )
            proj = ArcherProjectile(start_pos, end_pos)
            self.projectiles.append(proj)

    def update(self):
        pass  # 관리만, 직접 그리진 않음
    
class LaserBeam(pygame.sprite.Sprite):
    def __init__(self, start_pos, direction, damage):
        super().__init__()
        self.image = pygame.Surface((200, 20), pygame.SRCALPHA)
        self.image.fill((200, 160, 255))  # 연보라색
        if direction in ["up", "down"]:
            self.image = pygame.transform.rotate(self.image, 90)
        if direction == "right":
            self.rect = self.image.get_rect(midleft=start_pos)
        elif direction == "left":
            self.rect = self.image.get_rect(midright=start_pos)
        elif direction == "up":
            self.rect = self.image.get_rect(midbottom=start_pos)
        elif direction == "down":
            self.rect = self.image.get_rect(midtop=start_pos)
        self.damage = damage
        self.lifetime = 15
        self.hit_targets = set()  # 여기에 이미 맞은 적 저장

    def update(self):
        self.lifetime -= 1
        if self.lifetime <= 0:
            self.kill()

class Enemy(pygame.sprite.Sprite):
    def __init__(self, health, damage, is_boss=False, is_ranged=False):
        super().__init__()
        if is_boss == "final":
            self.image = image_assets["final_boss"]
            self.rect = self.image.get_rect(center=(400, 200))  # 중앙 근처 등장
            self.speed = 1.0
            self.health = 3000   
            self.damage = 40
            self.is_boss = True
            self.is_ranged = True
            self.cooldown = 0
            self.projectiles = []
            self.is_final_boss = True
            return  # 일반 몹 설정은 스킵
        if is_boss == "final":
            self.image = pygame.Surface((30, 30))
            self.image = pygame.Surface((100, 100))  # 최종 보스는 나중에 따로 처리
            self.image.fill(PURPLE if is_boss else RED if not is_ranged else YELLOW)
            self.image.fill(GOLD)
        elif is_boss:
            self.image = image_assets["mid_boss"]
        else:
            self.image = image_assets["monster"]

        self.rect = self.image.get_rect(center=(random.randint(50, 750), random.randint(50, 550)))
        self.speed = random.uniform(1, 2.5)
        self.health = health
        self.damage = damage
        self.is_boss = is_boss
        self.is_ranged = is_ranged
        self.cooldown = 0
        self.projectiles = []

    def update(self, player):
        dx = player.rect.x - self.rect.x
        dy = player.rect.y - self.rect.y
        dist = math.hypot(dx, dy)
        if dist != 0:
            self.rect.x += self.speed * dx / dist
            self.rect.y += self.speed * dy / dist
        if self.rect.colliderect(player.rect):
            player.take_damage(self.damage)

        # 보스 원거리 공격
        if self.is_boss and self.is_ranged:
            if hasattr(self, "is_final_boss") and self.is_final_boss:
                if self.cooldown <= 0:
                    if not hasattr(self, "angle_offset"):
                        self.angle_offset = 0
                    self.angle_offset = (self.angle_offset + 10) % 360
                    for angle in range(0, 360, 30):
                        rad = math.radians(angle + self.angle_offset)
                        dx = math.cos(rad) * 3
                        dy = math.sin(rad) * 6
                        proj = BossProjectile(self.rect.center, dx, dy, self.damage)
                        self.projectiles.append(proj)
                    self.cooldown = 20
                else:
                     self.cooldown -=1
            else:
                if self.cooldown <= 0:
                    for angle in range(0, 360, 45):
                        rad = math.radians(angle)
                        dx = math.cos(rad) * 3
                        dy = math.sin(rad) * 6
                        proj = BossProjectile(self.rect.center, dx, dy, self.damage)
                        self.projectiles.append(proj)
                    self.cooldown = 120

                else:
                    self.cooldown -= 1









        

        
        for proj in self.projectiles:
            proj.update()

class BossProjectile(pygame.sprite.Sprite):
    def __init__(self, pos, dx, dy, damage):
        super().__init__()
        self.image = pygame.Surface((10, 10))
        self.image.fill(CYAN)
        self.rect = self.image.get_rect(center=pos)
        self.dx = dx
        self.dy = dy
        self.damage = damage

    def update(self):
        self.rect.x += self.dx
        self.rect.y += self.dy
        if not screen.get_rect().colliderect(self.rect):
            self.kill()

def draw_menu(screen, options, selected):
    for i, option in enumerate(options):
        color = RED if i == selected else WHITE
        text = font.render(option, True, color)
        screen.blit(text, (300, 250 + i*50))

def job_upgrade_menu(player):
    options = []
    if player.job == "Warrior":
        options = ["버서커 (스탯 2배 + 피해감소)", "기사 (2초 무적)"]
    elif player.job == "Archer":
        options = ["트리플 슈터 (항상 3갈래)", "애로우 (강한 화살)"]
    selected = 0
    choosing = True
    while choosing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % 2
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % 2
                elif event.key == pygame.K_RETURN:
                    if player.job == "Warrior":
                        player.subjob = "Berserker" if selected == 0 else "Knight"
                        if player.subjob == "Berserker":
                            player.image = image_assets["warrior_berserker"]
                        else:
                            player.image = image_assets["warrior_knight"]
                    elif player.job == "Archer":
                        player.subjob = "Triple" if selected == 0 else "Arrow"
                         # 궁수 전직 시 이미지도 나중에 여기에 추가할 수 있음
                        if player.subjob == "Triple":
                             player.image = image_assets["archer_triple"]
                        else:
                            player.image = image_assets["archer_arrow"]
                    choosing = False
        screen.blit(image_assets["shop"], (0, 0))
        gold_text = font.render(f"보유 골드: {player.gold}", True, YELLOW)
        screen.blit(gold_text, (50, 50))
        for i, option in enumerate(options):
            color = RED if i == selected else WHITE
            text = font.render(option, True, color)
            screen.blit(text, (300, 200 + i * 40))
        pygame.display.flip()
        clock.tick(60)

def shop_menu(player):
    global font, YELLOW
    options = [
        "공격력+3 (200원)",
        "공격속도+0.1 (300원)",
        "이동속도+0.5 (250원)",
        "체력+20 (150원)",
        "나가기"
    ]
    selected = 0
    menu_active = True
    while menu_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    if options[selected] == "공격력+3 (200원)" and player.gold >= 200:
                        player.attack_power += 3
                        player.gold -= 200
                    elif options[selected] == "공격속도+0.1 (300원)" and player.gold >= 300:
                        player.attack_speed += 0.1
                        player.gold -= 300
                    elif options[selected] == "이동속도+0.5 (250원)" and player.gold >= 250:
                        player.speed += 0.5
                        player.gold -= 250
                    elif options[selected] == "체력+20 (150원)" and player.gold >= 150:
                        player.max_health += 20         # 영구적으로 최대체력 증가
                        player.health += 20             # 현재 체력도 같이 회복
                        player.gold -= 150

                    elif options[selected] == "나가기":
                        menu_active = False
        screen.blit(image_assets["shop"], (0, 0))
        gold_text = font.render(f"보유 골드: {player.gold}", True, YELLOW)
        screen.blit(gold_text, (50, 50))
        draw_menu(screen, options, selected)
        pygame.display.flip()
        clock.tick(60)
class GameStage:
    def __init__(self):
        self.stage = 1
        self.max_enemies = 5
        self.enemies_killed = 0

    def is_cleared(self):
        return self.enemies_killed >= self.max_enemies

    def next_stage(self):
        self.stage += 1
        self.max_enemies += 3
        self.enemies_killed = 0
        return {
            "enemy_health": 300 + (self.stage - 1) * 25,   # ← 변경
            "enemy_damage": 8 + (self.stage - 1) * 3
        }
def game_over_screen():
    screen.fill(BLACK)
    text = font.render("게임 오버! 엔터로 재시작", True, RED)
    screen.blit(text, (250, 300))
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                return

def main():
    player = Player()
    all_sprites = pygame.sprite.Group(player)
    enemies = pygame.sprite.Group()
    attacks = pygame.sprite.Group()
    projectiles = pygame.sprite.Group()

    showing_help = True #설명서 추가코드 (3/3)
    while showing_help:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                showing_help = False

        draw_help()
        pygame.display.flip()
        clock.tick(60)


    job_options = ["전사", "궁수"]
    selected = 0
    job_selected = False
    while not job_selected:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP: selected = (selected - 1) % 2
                elif event.key == pygame.K_DOWN: selected = (selected + 1) % 2
                elif event.key == pygame.K_RETURN:
                    player.set_job("Warrior" if selected == 0 else "Archer")
                    job_selected = True
        screen.blit(image_assets["start"], (0, 0))
        draw_menu(screen, job_options, selected)
        pygame.display.flip()
        clock.tick(60)

    stage = GameStage()
    stage_info = {
    "enemy_health": 80 + (stage.stage - 1) * 25,
    "enemy_damage": 8 + (stage.stage - 1) * 3
}

    while True:
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player.job == "Warrior":
                    atk = player.attack()
                    if atk:
                        attacks.add(atk)
                        all_sprites.add(atk)
                elif event.key == pygame.K_LSHIFT:
                    new_proj = player.use_skill(mouse_pos)
                    for p in new_proj:
                        projectiles.add(p)
                        all_sprites.add(p)
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if player.job == "Archer":
                    atk = player.attack(mouse_pos)
                    if atk:
                        if isinstance(atk, list):
                            for p in atk:
                                projectiles.add(p)
                                all_sprites.add(p)
                        else:
                            projectiles.add(atk)
                            all_sprites.add(atk)

        # 적 생성
        if not stage.is_cleared() and len(enemies) == 0:
            if stage.stage == 8:
                screen.blit(image_assets["final"], (0, 0))
                boss = Enemy(0, 0, is_boss="final")
                enemies.add(boss)
                all_sprites.add(boss)
                stage.max_enemies = 1
            else:
                for _ in range(3 + stage.stage):
                    is_boss = stage.stage >= 3 and random.random() < 0.3
                    is_ranged = is_boss and random.random() < 0.5
                    enemy = Enemy(stage_info["enemy_health"], stage_info["enemy_damage"], is_boss, is_ranged)
                    enemies.add(enemy)
                    all_sprites.add(enemy)
                stage.max_enemies = len(enemies)       


        
    
            
        # 업데이트
        player.update()
        enemies.update(player)
        attacks.update()
        projectiles.update()
        for enemy in enemies:
            for proj in enemy.projectiles:
                proj.update()
                if proj.rect.colliderect(player.rect):
                    player.take_damage(proj.damage)
                    proj.kill()

        # 공격 충돌 처리
        for atk in attacks:
            if isinstance(atk, WarriorAttack):
                for e in enemies:
                    if pygame.sprite.collide_circle(atk, e): e.health -= atk.damage
        for p in projectiles:
            for e in enemies:
                if pygame.sprite.collide_rect(p, e):
                    if isinstance(p, LaserBeam):
                        if e not in p.hit_targets:
                            e.health -= p.damage
                            p.hit_targets.add(e)
                    else:
                        e.health -= p.damage
                        p.kill()
        # 적 사망
        for e in enemies:
            if e.health <= 0:
                # ✅ 최종보스 즉시 클리어 처리
                if hasattr(e, "is_final_boss") and e.is_final_boss:

                    stage.enemies_killed = stage.max_enemies
                    
                player.gold += 10 + (40 if e.is_boss else 0)
                stage.enemies_killed += 1
                e.kill()
        # 게임 오버
        if player.health <= 0:
            game_over_screen()
            return

        # 스테이지 클리어
        if stage.is_cleared():
            if stage.stage == 2:
                job_upgrade_menu(player)
                player.skill_cooldown = 0
                player.skill_active = False
                player.skill_time = 0
            elif stage.stage == 8:
                screen.blit(image_assets["victory"], (0, 0))
                screen.blit(font.render("축하합니다! 최종 보스를 처치했습니다!", True, YELLOW), (150, 300))
                pygame.display.flip()
                pygame.time.delay(5000)
                return
            player.health = player.max_health
            player.gold += 150
            shop_menu(player)
            stage_info = stage.next_stage()

        # 그리기
        screen.blit(image_assets["background"], (0, 0))
                # 보스 체력바 그리기
        for enemy in enemies:
            if hasattr(enemy, "is_final_boss") and enemy.is_final_boss:
                # 바 위치 및 크기
                bar_width = 600
                bar_height = 20
                bar_x = 100
                bar_y = 20
                # 비율 계산
                health_ratio = enemy.health / enemy.health if enemy.health > 0 else 0
                health_ratio = enemy.health / 3000  # 전체 체력 기준
                # 배경 바
                pygame.draw.rect(screen, RED, (bar_x, bar_y, bar_width, bar_height))
                # 현재 체력
                pygame.draw.rect(screen, GREEN, (bar_x, bar_y, bar_width * health_ratio, bar_height))
                # 테두리
                pygame.draw.rect(screen, WHITE, (bar_x, bar_y, bar_width, bar_height), 2)
                # 텍스트
                boss_hp_text = font.render(f"보스 체력: {enemy.health}/3000", True, WHITE)
                screen.blit(boss_hp_text, (bar_x + 200, bar_y - 25))

        all_sprites.draw(screen)
        for enemy in enemies:
            for proj in enemy.projectiles:
                screen.blit(proj.image, proj.rect)
        stat_text = [
            f"HP: {player.health}/{player.max_health}",
            f"공격력: {player.attack_power}",
            f"공격속도: {player.attack_speed:.1f}/s",
            f"이동속도: {player.speed:.1f}",
            f"골드: {player.gold}",
            f"스테이지: {stage.stage}",
            f"처치: {stage.enemies_killed}/{stage.max_enemies}"
        ]
        for i, text in enumerate(stat_text):
            screen.blit(font.render(text, True, WHITE), (10, 10 + 25*i))
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
    pygame.quit()
    exit()
