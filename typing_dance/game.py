import pygame
import random
import string
import os
from settings import Settings


class CharacterBlock:
    def __init__(self, track_index):
        settings = Settings()
        self.x = track_index * settings.TRACK_WIDTH + 10
        self.y = 0
        self.width = settings.BLOCK_WIDTH
        self.height = settings.BLOCK_HEIGHT
        self.speed = settings.BLOCK_SPEED
        # 随机选择颜色，避免与白色文字相近
        self.color = random.choice([c for c in settings.NEON_COLORS if sum(c) < 500])
        self.letter = random.choice(string.ascii_uppercase)
        self.font = pygame.font.Font(None, settings.BLOCK_LETTER_FONT_SIZE)

    def update(self):
        self.y += self.speed

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        text = self.font.render(self.letter, True, (255, 255, 255))
        text_rect = text.get_rect(center=(self.x + self.width // 2, self.y + self.height // 2))
        screen.blit(text, text_rect)


class SoundManager:
    def __init__(self, game):
        self.game = game
        settings = Settings()
        try:
            self.hit_normal_perfect = pygame.mixer.Sound(os.path.join(settings.SOUND_DIR, 'perfect.MP3'))
            self.hit_normal_good = pygame.mixer.Sound(os.path.join(settings.SOUND_DIR, 'good.MP3'))
            self.hit_normal_hit = pygame.mixer.Sound(os.path.join(settings.SOUND_DIR, 'hit.MP3'))
            self.hit_echo_perfect = pygame.mixer.Sound(os.path.join(settings.SOUND_DIR, 'perfect.MP3'))
            self.hit_echo_good = pygame.mixer.Sound(os.path.join(settings.SOUND_DIR, 'good.MP3'))
            self.hit_echo_hit = pygame.mixer.Sound(os.path.join(settings.SOUND_DIR, 'hit.MP3'))
            self.hit_stereo_perfect = pygame.mixer.Sound(os.path.join(settings.SOUND_DIR, 'perfect.MP3'))
            self.hit_stereo_good = pygame.mixer.Sound(os.path.join(settings.SOUND_DIR, 'good.MP3'))
            self.hit_stereo_hit = pygame.mixer.Sound(os.path.join(settings.SOUND_DIR, 'hit.MP3'))
            self.hit_orchestra_perfect = pygame.mixer.Sound(os.path.join(settings.SOUND_DIR, 'perfect.MP3'))
            self.hit_orchestra_good = pygame.mixer.Sound(os.path.join(settings.SOUND_DIR, 'good.MP3'))
            self.hit_orchestra_hit = pygame.mixer.Sound(os.path.join(settings.SOUND_DIR, 'hit.MP3'))
        except pygame.error as e:
            print(f"音效加载失败: {e}")

        fail_path = os.path.join(settings.SOUND_DIR, 'fail.MP3')
        if os.path.exists(fail_path):
            try:
                self.fail = pygame.mixer.Sound(fail_path)
            except pygame.error as e:
                print(f"加载失败音效时出现错误: {e}，请检查文件是否损坏。")
                self.fail = None
        else:
            print(f"未找到失败音效文件: {fail_path}，将不播放失败音效。")
            self.fail = None

    def play(self, sound_name):
        sound = getattr(self, sound_name, None)
        if sound is None:
            print(f"音效 {sound_name} 未加载，无法播放。")
            return

        # 根据阶段调整参数
        stage = self.game.current_stage
        if stage >= 2:
            sound.set_volume(min(1.0, 0.7 + stage * 0.1))

        sound.play()


class CharacterAnimator:
    def __init__(self, game):
        self.game = game
        self.settings = Settings()
        self.current_set = "basic"
        self.animations = self.settings.CHARACTER_ANIMATIONS[self.current_set]
        self.current_frame_index = 0
        self.last_frame_time = pygame.time.get_ticks()
        self.current_action = "idle"
        self.play_idle_animation()
        self.last_dance_switch_time = pygame.time.get_ticks()  # 记录上次切换舞蹈动作的时间
        self.current_dance_sequence_index = 0  # 当前舞蹈动作序列索引
        self.is_dancing = False  # 标记是否在舞蹈
        self.pose_switch_interval = 200  # pose-left 和 pose-right 的切换时间间隔（0.2秒）
        self.dance_sequence_interval = 5000  # 不同舞蹈动作序列的切换时间间隔（5秒）

    def set_animation_set(self, set_name):
        """切换动作资源组"""
        self.current_set = set_name
        self.animations = self.settings.CHARACTER_ANIMATIONS[set_name]
        self.play_idle_animation()

    def play_dance_animation(self, judge_type):
        """根据判定类型播放舞蹈"""
        if judge_type == "PERFECT" and "special" in self.animations:
            frames = self.animations["special"]
        else:
            frames = self.animations["dance"][self.current_dance_sequence_index]  # 获取当前舞蹈动作序列
        self.start_animation(frames, speed=self.get_stage_speed())

    def get_stage_speed(self):
        """根据阶段获取动画速度"""
        speed_map = {0: 1.0, 1: 1.2, 2: 1.5, 3: 2.0}
        return speed_map[self.game.current_stage]

    def play_idle_animation(self):
        self.current_action = "idle"
        self.current_frame_index = 0
        self.last_frame_time = pygame.time.get_ticks()

    def start_animation(self, frames, speed):
        self.current_action = "dance"
        self.current_frame_index = 0
        self.last_frame_time = pygame.time.get_ticks()
        self.animation_frames = frames
        self.animation_speed = speed

    def update(self):
        current_time = pygame.time.get_ticks()
        if self.current_action == "dance":
            # 切换 pose-left 和 pose-right
            frame_duration = self.pose_switch_interval
            if current_time - self.last_frame_time > frame_duration:
                self.current_frame_index = (self.current_frame_index + 1) % len(self.animation_frames)
                self.last_frame_time = current_time

        # 如果正在舞蹈且时间超过五秒，切换到下一个舞蹈动作
        if self.is_dancing and current_time - self.last_dance_switch_time > self.dance_sequence_interval:
            self.current_dance_sequence_index = (self.current_dance_sequence_index + 1) % len(self.animations["dance"])
            self.play_dance_animation(None)  # 切换舞蹈动作
            self.last_dance_switch_time = current_time

    def get_current_frame(self):
        if self.current_action == "idle":
            frames = self.animations["idle"]
            return frames[self.current_frame_index % len(frames)]
        frames = self.animation_frames
        return frames[self.current_frame_index % len(frames)]

    def start_dance(self):
        """开始舞蹈"""
        self.is_dancing = True
        self.current_dance_sequence_index = 0
        self.play_dance_animation(None)

    def stop_dance(self):
        """停止舞蹈"""
        self.is_dancing = False
        self.play_idle_animation()


class Character:
    def __init__(self, game):
        self.game = game
        settings = Settings()
        self.images = []
        for image_path in settings.CHARACTER_IMAGES:
            try:
                image = pygame.image.load(image_path)
                image = pygame.transform.scale(image, (settings.CHARACTER_WIDTH, settings.CHARACTER_HEIGHT))
                self.images.append(image)
            except pygame.error as e:
                print(f"Failed to load image: {image_path}, error: {e}")
        self.animator = CharacterAnimator(game)
        self.first_correct_key_pressed = False  # 新增：标记第一次按键正确

    def draw(self, screen):
        settings = Settings()
        frame_index = self.animator.get_current_frame()
        if self.images and frame_index < len(self.images):
            screen.blit(self.images[frame_index], (settings.CHARACTER_X, settings.CHARACTER_Y))

    def start_dance(self, judge_type):
        if not self.first_correct_key_pressed:
            self.first_correct_key_pressed = True
            self.animator.start_dance()  # 开始舞蹈
        self.animator.play_dance_animation(judge_type)

    def stop_dance(self):
        self.animator.stop_dance()
        self.first_correct_key_pressed = False  # 重置标志

    def update(self):
        self.animator.update()


class Game:
    def __init__(self):
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.WIDTH, self.settings.HEIGHT))
        pygame.display.set_caption("Game")
        self.clock = pygame.time.Clock()
        self.blocks = []
        self.last_spawn_time = pygame.time.get_ticks()
        self.last_speed_increase_time = pygame.time.get_ticks()
        self.font = pygame.font.Font(None, 36)
        self.show_judgment = False
        self.judgment_text = ""
        self.judgment_color = (255, 255, 255)  # 新增：判定文字颜色
        self.judgment_timer = 0
        self.combo = 0
        self.score = 0
        self.current_stage = 0
        self.stage_thresholds = [1000, 3000, 6000]
        self.stage_data = [
            {"anim": "basic", "sound": "hit_normal", "speed": 1.0},
            {"anim": "advanced", "sound": "hit_echo", "speed": 1.1},
            {"anim": "epic", "sound": "hit_stereo", "speed": 1.2},
            {"anim": "ultimate", "sound": "hit_orchestra", "speed": 1.3}
        ]
        self.sound_manager = SoundManager(self)
        self.character = Character(self)
        self.last_judge_time = 0
        self.judge_interval = 100
        self.current_speed = self.settings.INITIAL_BLOCK_SPEED
        try:
            self.background_image = pygame.image.load(self.settings.BACKGROUND_IMAGE)
            self.background_image = pygame.transform.scale(self.background_image,
                                                           (self.settings.WIDTH, self.settings.HEIGHT))
        except pygame.error as e:
            print(f"Failed to load background image: {self.settings.BACKGROUND_IMAGE}, error: {e}")
            self.background_image = None

        # 加载新的背景音乐
        music_dir = os.path.join(self.settings.ASSETS_DIR, 'music')
        bgm_path = os.path.join(music_dir, '背景音乐.mp3')
        try:
            pygame.mixer.music.load(bgm_path)
        except pygame.error as e:
            print(f"Failed to load background music: {bgm_path}, error: {e}")

        self.game_started = False  # 新增：游戏是否开始的标志
        self.start_text = self.font.render("Press Space to Start", True, (255, 255, 255))
        self.start_text_rect = self.start_text.get_rect(center=(self.settings.WIDTH // 2, self.settings.HEIGHT // 2))

    def init_audio(self):
        pass

    def init_stage_lights(self):
        pass

    def update_stage_lights(self):
        pass

    def draw_stage_lights(self):
        pass

    def spawn_block(self):
        track_index = random.randint(0, self.settings.TRACK_COUNT - 1)
        block = CharacterBlock(track_index)
        self.blocks.append(block)

    def handle_events(self):
        current_time = pygame.time.get_ticks()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if not self.game_started:
                        self.game_started = True
                        try:
                            pygame.mixer.music.play(-1)  # -1 表示循环播放
                        except pygame.error as e:
                            print(f"Failed to play background music: {e}")
                    else:
                        pygame.quit()
                        quit()
                elif self.game_started and current_time - self.last_judge_time > self.judge_interval:
                    key_char = pygame.key.name(event.key).upper()
                    self.check_key_press(key_char)
                    self.last_judge_time = current_time

    def check_key_press(self, key_char):
        if not self.blocks:
            return
        lowest_block = max(self.blocks, key=lambda block: block.y)
        if key_char != lowest_block.letter:
            self.combo = 0
            self.sound_manager.play("fail")  # 播放失败音效
            self.character.stop_dance()  # 停止舞蹈
            return
        distance = abs(lowest_block.y + lowest_block.height - self.settings.JUDGE_LINE_Y)
        if distance < self.settings.PERFECT_RANGE:
            judge_type = "PERFECT"
            self.judgment_text = f"Perfect +20"  # 显示具体得分
            self.judgment_color = (255, 215, 0)  # 金色
            self.score += 20  # PERFECT得20分
        elif distance < self.settings.GOOD_RANGE:
            judge_type = "GOOD"
            self.judgment_text = f"Good +50"  # 显示具体得分
            self.judgment_color = (0, 255, 0)  # 绿色
            self.score += 50  # GOOD得50分
        else:
            judge_type = "HIT"
            self.judgment_text = f"Hit +100"  # 显示具体得分
            self.judgment_color = (255, 0, 0)  # 红色
            self.score += 100  # HIT得100分

        self.show_judgment = True
        self.judgment_timer = pygame.time.get_ticks()
        self.play_hit_sound(judge_type)
        self.blocks.remove(lowest_block)
        self.combo += 1
        self.character.start_dance(judge_type)  # 开始舞蹈
        self.check_stage_transition()

    def check_stage_transition(self):
        """检查是否需要切换阶段"""
        new_stage = 0
        for i, threshold in enumerate(self.stage_thresholds):
            if self.score >= threshold:
                new_stage = i + 1

        if new_stage != self.current_stage:
            self.handle_stage_change(new_stage)

    def handle_stage_change(self, new_stage):
        """处理阶段切换"""
        # 播放升级音效
        try:
            self.sound_manager.play("level_up")
        except AttributeError:
            print("未找到升级音效，无法播放。")

        # 更新角色动画
        self.character.animator.set_animation_set(
            self.stage_data[new_stage]["anim"])

        # 调整游戏速度
        self.current_speed = (
                self.settings.INITIAL_BLOCK_SPEED *
                self.stage_data[new_stage]["speed"])
        for block in self.blocks:
            block.speed = self.current_speed

        # 触发特效
        # 这里原代码中 self.particle_system 未定义，暂时注释掉
        # self.particle_system.play_stage_effect(new_stage)

        self.current_stage = new_stage
        print(f"进入新阶段: {new_stage}")

    def play_hit_sound(self, judge_type):
        """根据当前阶段播放对应音效"""
        base_sound = self.stage_data[self.current_stage]["sound"]
        sound_name = f"{base_sound}_{judge_type.lower()}"
        self.sound_manager.play(sound_name)

    def update(self):
        if not self.game_started:
            return
        current_time = pygame.time.get_ticks()
        if current_time - self.last_spawn_time > self.settings.BLOCK_SPAWN_RATE:
            self.spawn_block()
            self.last_spawn_time = current_time

        if current_time - self.last_speed_increase_time > self.settings.SPEED_INCREASE_INTERVAL:
            if self.settings.BLOCK_SPEED < self.settings.MAX_SPEED:
                self.settings.BLOCK_SPEED += self.settings.SPEED_INCREMENT
                for block in self.blocks:
                    block.speed = self.settings.BLOCK_SPEED
            self.last_speed_increase_time = current_time

        for block in self.blocks[:]:
            block.update()
            if block.y > self.settings.HEIGHT:
                self.blocks.remove(block)
                self.combo = 0
                self.sound_manager.play(f"{self.stage_data[self.current_stage]['sound']}_hit")
                self.character.stop_dance()  # 停止舞蹈

        if self.show_judgment and current_time - self.judgment_timer > 500:
            self.show_judgment = False

        self.character.update()

    def draw(self):
        # 绘制背景图片
        if self.background_image:
            self.screen.blit(self.background_image, (0, 0))
        else:
            self.screen.fill((0, 0, 0))

        if not self.game_started:
            self.screen.blit(self.start_text, self.start_text_rect)
        else:
            self.draw_gradient_background()
            self.draw_stage_lights()
            for block in self.blocks:
                block.draw(self.screen)
            pygame.draw.rect(self.screen, (255, 255, 255),
                             (0, self.settings.JUDGE_LINE_Y, self.settings.WIDTH, self.settings.JUDGE_LINE_HEIGHT))
            if self.show_judgment:
                text = self.font.render(self.judgment_text, True, self.judgment_color)
                text_rect = text.get_rect(center=(self.settings.WIDTH // 2, self.settings.HEIGHT // 2))
                self.screen.blit(text, text_rect)
            combo_text = self.font.render(f"Combo: {self.combo}", True, (255, 255, 255))
            self.screen.blit(combo_text, (10, 10))
            score_text = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
            self.screen.blit(score_text, (10, 40))
            self.character.draw(self.screen)
        pygame.display.flip()

    def draw_gradient_background(self):
        pass

    def run(self):
        while True:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(self.settings.FPS)