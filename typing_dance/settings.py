import os

class Settings:
    WIDTH = 800
    HEIGHT = 600
    FPS = 60
    TRACK_COUNT = 4
    TRACK_WIDTH = WIDTH // TRACK_COUNT
    BLOCK_WIDTH = TRACK_WIDTH - 20
    BLOCK_HEIGHT = 50
    BLOCK_SPEED = 3
    BLOCK_SPAWN_RATE = 1000
    JUDGE_LINE_Y = HEIGHT - 100
    JUDGE_LINE_HEIGHT = 10

    # 更炫彩的颜色列表
    NEON_COLORS = [
        (255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0),
        (255, 0, 255), (0, 255, 255), (128, 0, 128), (255, 165, 0),
        (0, 128, 0), (128, 0, 0), (0, 0, 128), (255, 20, 147)
    ]

    CHARACTER_WIDTH = 150
    CHARACTER_HEIGHT = 300
    CHARACTER_X = (WIDTH - CHARACTER_WIDTH) // 2
    CHARACTER_Y = HEIGHT - CHARACTER_HEIGHT - 50

    ASSETS_DIR = os.path.join(os.path.dirname(__file__), 'assets')
    IMAGE_DIR = os.path.join(ASSETS_DIR, 'images')
    CHARACTER_IMAGES = [
        os.path.join(IMAGE_DIR, 'pose0.jpg'),
        os.path.join(IMAGE_DIR, 'pose1-left.jpg'),
        os.path.join(IMAGE_DIR, 'pose1-right.jpg'),
        os.path.join(IMAGE_DIR, 'pose2-left.jpg'),
        os.path.join(IMAGE_DIR, 'pose2-right.jpg'),
        os.path.join(IMAGE_DIR, 'pose3-left.jpg'),
        os.path.join(IMAGE_DIR, 'pose3-right.jpg'),
        os.path.join(IMAGE_DIR, 'pose4-left.jpg'),
        os.path.join(IMAGE_DIR, 'pose4-right.jpg'),
        os.path.join(IMAGE_DIR, 'pose5-left.jpg'),
        os.path.join(IMAGE_DIR, 'pose5-right.jpg'),
        os.path.join(IMAGE_DIR, 'pose6-left.jpg'),
        os.path.join(IMAGE_DIR, 'pose6-right.jpg'),
    ]
    # 背景图片路径
    BACKGROUND_IMAGE = os.path.join(IMAGE_DIR, 'stage.jpg')

    INITIAL_BLOCK_SPEED = 3
    SPEED_INCREASE_INTERVAL = 30000
    SPEED_INCREMENT = 0.5
    MAX_SPEED = 10

    SOUND_DIR = os.path.join(ASSETS_DIR, 'sounds')
    HIT_SOUND = os.path.join(SOUND_DIR, 'hit.MP3')
    GOOD_SOUND = os.path.join(SOUND_DIR, 'good.MP3')
    PERFECT_SOUND = os.path.join(SOUND_DIR, 'perfect.MP3')
    COMBO_SOUND = os.path.join(SOUND_DIR, 'combo.MP3')
    FAIL_SOUND = os.path.join(SOUND_DIR, 'fail.MP3')
    LEVEL_UP_SOUND = os.path.join(SOUND_DIR, 'level_up.MP3')

    PERFECT_RANGE = 30
    GOOD_RANGE = 40
    BLOCK_LETTER_FONT_SIZE = 36

    CHARACTER_ANIMATIONS = {
        "basic": {
            "idle": [0],
            "dance": [[1, 2], [3, 4], [5, 6], [7, 8], [9, 10], [11, 12]],  # 确保帧索引不超出范围
            "transition": [0, 1, 2, 1, 0]  # 过渡动画
        },
        "advanced": {
            "idle": [0, 7],  # 带呼吸效果的待机
            "dance": [[1, 2], [3, 4], [5, 6], [7, 8], [9, 10], [11, 12]],  # pose2+pose3组合
            "special": [1, 3, 2, 4]  # 特殊动作
        },
        "epic": {
            "idle": [8],
            "dance": [[9, 10], [11, 12]],  # 确保帧索引不超出范围
            "special": [9, 10, 11, 12, 11, 10, 9]
        },
        "ultimate": {
            "idle": [11],  # 调整到有效索引
            "dance": [[11, 12]],  # 确保帧索引不超出范围
            "special": [11, 12, 11, 12, 11, 12, 11]
        }
    }