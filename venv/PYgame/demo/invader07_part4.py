#!/usr/bin/env python
# coding: utf-8

# 参考　https://blog.formzu.com/?s=AI+pygame

import os
import random
import sys

import numpy as np
import pygame
from PIL import Image
from pygame.locals import *

START, PLAY, GAMEOVER, STAGECLEAR = (0, 1, 2, 3)  # ゲーム状態
SCR_RECT = Rect(0, 0, 640, 480)
PLAYER_MOVE_RECT = Rect(40, 0, 560, 480)


class Invader:
    def __init__(self, step=False, image=False):
        self.lives = 5  # 残機数
        self.wave = 1  # Wave数
        self.counter = 0  # タイムカウンター(60カウント=1秒)
        self.score = 0  # スコア(エイリアン 10点、UFO 50点にWaveを乗算)
        self.step_flag = step  # 学習用にstep実行するかどうか
        self.image_flag = image  # 学習用データを画像にするかどうか
        self.observation_space = None  # 学習環境の情報
        self.num_aliens = None  # エイリアンの数
        self.prev_lives = None  # 直前のステップの残機
        self.prev_num_aliens = None  # 直前のステップのエイリアン数
        pygame.init()
        self.screen = pygame.display.set_mode(SCR_RECT.size, pygame.DOUBLEBUF)
        pygame.display.set_caption("Invader Part4")
        # 素材のロード
        self.load_images()
        self.load_sounds()
        # ゲームオブジェクトを初期化
        self.init_game()
        self._get_observation()
        # メインループ開始
        if not self.step_flag:  # 通常モード
            clock = pygame.time.Clock()
            while True:
                clock.tick(60)
                self.update()
                self.draw(self.screen)
                pygame.display.update()
                self.key_handler()
        else:  # step実行時はタイトル画面を飛ばす
            self.game_state = PLAY

    # ここからgym互換関数群
    def reset(self):
        self.score = 0  # スコア初期化
        self.wave = 1
        self.lives = 5
        self.counter = 0
        self.no_kill_counter = 0  # エイリアンを撃破できていない時間（60カウント=1秒）
        self.init_game()  # ゲームを初期化して再開
        self.game_state = PLAY
        self._get_observation()
        return self.observation_space

    def render(self, mode=None):
        pass

    def step(self, action):
        if not self.step_flag:
            sys.stdout.write("Not running in stepping mode!\n")
            return None

        reward = 0
        done = False
        self._key_action(action)
        self.update()
        self.draw(self.screen)
        pygame.display.update()
        self._get_observation()
        self.no_kill_counter += 1

        if self.player.rect.center[0] < 80 or self.player.rect.center[0] > 560:
            reward += -1
        if self.prev_lives > self.lives:
            reward += -15
            self.prev_lives = self.lives
        elif self.prev_lives < self.lives:
            reward += 15
            self.prev_lives = self.lives

        num_aliens = len(self.aliens)
        if self.prev_num_aliens > num_aliens:
            reward += 1
            self.no_kill_counter = 0
            self.prev_num_aliens = num_aliens
        if self.no_kill_counter > 900:
            reward += -1

        if num_aliens == 0:
            reward += 300
            done = True
            sys.stdout.write("Cleared!\n")
        elif self.lives < 0:
            reward += -20
            done = True
        elif self.counter == 4500:
            reward += -1000
            done = True
            sys.stdout.write("Time up!\n")
        return self.observation_space, reward, done, dict()

    def _key_action(self, action):  # キー入力を代替
        # 常にミサイル発射
        if self.player.reload_timer == 0:
            Shot(self.player.rect.center)
            self.player.reload_timer = self.player.reload_time
        # 左移動
        if action == 1:
            self.player.rect.move_ip(-self.player.speed, 0)
            self.player.rect.clamp_ip(PLAYER_MOVE_RECT)
        # 右移動
        elif action == 2:
            self.player.rect.move_ip(self.player.speed, 0)
            self.player.rect.clamp_ip(PLAYER_MOVE_RECT)
        pass

    def _get_observation(self):
        if self.image_flag:
            resize_x = 160
            resize_y = 120
            cut_y_rate = 0.06
            pilImg = Image.fromarray(pygame.surfarray.array3d(self.screen))
            resizedImg = pilImg.resize((resize_x, resize_y), Image.LANCZOS)
            self.observation_space = np.asarray(resizedImg)[:][int(resize_y * cut_y_rate):]
            return None

        observation_list = list()
        for index, alien in enumerate(self.alien_list):
            if alien.alive:
                observation_list.append((alien.rect.center[0] - self.player.rect.center[0]) / 640)
                observation_list.append((alien.rect.center[1] - self.player.rect.center[1]) / 480)
                observation_list.append(alien.speed / 2)
            else:
                observation_list.extend([0, 0, 0])
        observation_list.append(len(self.alien_list))

        # ビーム位置情報
        beam_check_range = np.array([64, 64, 192, 24])  # L,R,U,D(学習に使う範囲を指定)
        margin = 60  # ビーム位置用行列の余白
        compressed_rate = 5  # ビーム位置行列の圧縮

        comp_beam_check_range = beam_check_range // compressed_rate
        beam_pos_all = np.zeros(((640 + margin * 2) // compressed_rate
                                 , (480 + margin * 2) // compressed_rate), dtype=int)
        for index, beam in enumerate(self.beams):
            beam_pos_all[(beam.rect.center[0] + margin) // compressed_rate] \
                [(beam.rect.center[1] + margin) // compressed_rate] = 1

        comp_x_pos = (self.player.rect.center[0] + margin) // compressed_rate
        comp_y_pos = (self.player.rect.center[1] + margin) // compressed_rate
        beam_pos = beam_pos_all[
                   comp_x_pos - comp_beam_check_range[0]:comp_x_pos + comp_beam_check_range[1],
                   comp_y_pos - comp_beam_check_range[2]:comp_y_pos + comp_beam_check_range[3]
                   ]

        observation_list.extend(beam_pos.flatten())

        for index, shot in enumerate(self.shots):
            observation_list.append((shot.rect.center[0] - self.player.rect.center[0]) / 640)
            observation_list.append((shot.rect.center[1] - self.player.rect.center[1]) / 480)
        observation_list.extend([0 for _ in range(10 - len(self.shots) * 2)])

        for ufo in self.ufos:
            observation_list.append((ufo.rect.center[0] - self.player.rect.center[0]) / 640)
            observation_list.append((ufo.rect.center[1] - self.player.rect.center[1]) / 480)
            observation_list.append(ufo.speed)
        observation_list.extend([0 for _ in range(3 - len(self.ufos) * 3)])

        observation_list.append((self.player.rect.center[0] - 320) / 320)
        observation_list.append((self.player.rect.center[1] - 240) / 240)
        observation_list.append(self.player.reload_timer / 15)
        self.observation_space = np.array(observation_list, dtype=float)

        pass

    # ここまでgym互換関数群

    def init_game(self):
        """ゲームオブジェクトを初期化"""
        # ゲーム状態
        self.game_state = START
        # スプライトグループを作成して登録
        self.all = pygame.sprite.RenderUpdates()
        self.invisible = pygame.sprite.RenderUpdates()
        self.aliens = pygame.sprite.Group()  # エイリアングループ
        self.shots = pygame.sprite.Group()  # ミサイルグループ
        self.beams = pygame.sprite.Group()  # ビームグループ
        self.walls = pygame.sprite.Group()  # 壁グループ
        self.ufos = pygame.sprite.Group()  # UFOグループ
        # デフォルトスプライトグループを登録
        Player.containers = self.all
        Shot.containers = self.all, self.shots, self.invisible
        Alien.containers = self.all, self.aliens, self.invisible
        Beam.containers = self.all, self.beams, self.invisible
        Wall.containers = self.all, self.walls, self.invisible
        UFO.containers = self.all, self.ufos, self.invisible
        Explosion.containers = self.all, self.invisible
        ExplosionWall.containers = self.all, self.invisible
        # 自機を作成
        self.player = Player()
        # エイリアンを作成
        self.alien_list = list()
        for i in range(0, 50):
            x = 10 + (i % 10) * 40
            y = 50 + (i // 10) * 40
            self.alien_list.append(Alien((x, y), self.wave))
        # 壁を作成
        '''
        self.wall_list = list()
        for i in range(4):
            x = 95 + i * 150
            y = 400
            self.wall_list.append(Wall((x, y), self.wave))
        '''
        self.num_aliens = len(self.aliens)
        self.prev_num_aliens = self.num_aliens
        self.prev_lives = self.lives

    def update(self):
        """ゲーム状態の更新"""
        if self.game_state == PLAY:
            # タイムカウンターを進める
            self.counter += 1
            # リロード時間を減らす
            if self.player.reload_timer > 0:
                self.player.reload_timer -= 1
            # UFOの出現判定(15秒後に出現する)
            if self.counter == 900:
                UFO((10, 30), self.wave)

            self.all.update()
            # エイリアンの方向転換判定
            turn_flag = False
            for alien in self.aliens:
                if (alien.rect.center[0] < 10 and alien.speed < 0) or \
                        (alien.rect.center[0] > SCR_RECT.width - 10 and alien.speed > 0):
                    turn_flag = True
                    break
            if turn_flag:
                for alien in self.aliens:
                    alien.speed *= -1
            # エイリアンの追加ビーム判定（プレイヤーが近くにいると反応する）
            for alien in self.aliens:
                alien.shoot_extra_beam(self.player.rect.center[0], 32, 2)
            # ミサイルとエイリアン、壁の衝突判定
            self.collision_detection()
            # エイリアンをすべて倒したら次のステージへ
            if len(self.aliens.sprites()) == 0:
                self.game_state = STAGECLEAR

    def draw(self, screen):
        """描画"""
        screen.fill((0, 0, 0))
        if self.game_state == START:  # スタート画面
            # タイトルを描画
            title_font = pygame.font.SysFont(None, 80)
            title = title_font.render("INVADER GAME", False, (255, 0, 0))
            screen.blit(title, ((SCR_RECT.width - title.get_width()) // 2, 100))
            # エイリアンを描画
            alien_image = Alien.images[0]
            screen.blit(alien_image, ((SCR_RECT.width - alien_image.get_width()) // 2, 200))
            # PUSH STARTを描画
            push_font = pygame.font.SysFont(None, 40)
            push_space = push_font.render("PUSH SPACE KEY", False, (255, 255, 255))
            screen.blit(push_space, ((SCR_RECT.width - push_space.get_width()) // 2, 300))
            # クレジットを描画
            credit_font = pygame.font.SysFont(None, 20)
            credit = credit_font.render("2019 http://pygame.skr.jp", False, (255, 255, 255))
            screen.blit(credit, ((SCR_RECT.width - credit.get_width()) // 2, 380))
        elif self.game_state == PLAY:  # ゲームプレイ画面
            # 無敵時間中は自機が点滅する
            if self.player.invisible % 10 > 4:
                self.invisible.draw(screen)
            else:
                self.all.draw(screen)
            # wave数と残機数を描画
            stat_font = pygame.font.SysFont(None, 20)
            stat = stat_font.render("Wave:{:2d}  Lives:{:2d}  Score:{:05d}  pos_X:{:3d}".format(
                self.wave, self.lives, self.score,
                self.player.rect.center[0]), False, (255, 255, 255))
            screen.blit(stat, ((SCR_RECT.width - stat.get_width()) // 2, 10))
            # 壁の耐久力描画
            shield_font = pygame.font.SysFont(None, 30)
            for wall in self.walls:
                shield = shield_font.render(str(wall.shield), False, (0, 0, 0))
                text_size = shield_font.size(str(wall.shield))
                screen.blit(shield, (wall.rect.center[0] - text_size[0] // 2,
                                     wall.rect.center[1] - text_size[1] // 2))
        elif self.game_state == GAMEOVER:  # ゲームオーバー画面
            # GAME OVERを描画
            gameover_font = pygame.font.SysFont(None, 80)
            gameover = gameover_font.render("GAME OVER", False, (255, 0, 0))
            screen.blit(gameover, ((SCR_RECT.width - gameover.get_width()) // 2, 100))
            # エイリアンを描画
            alien_image = Alien.images[0]
            screen.blit(alien_image, ((SCR_RECT.width - alien_image.get_width()) // 2, 200))
            # PUSH SPACEを描画
            push_font = pygame.font.SysFont(None, 40)
            push_space = push_font.render("PUSH SPACE KEY", False, (255, 255, 255))
            screen.blit(push_space, ((SCR_RECT.width - push_space.get_width()) // 2, 300))

        elif self.game_state == STAGECLEAR:  # ステージクリア画面
            # wave数と残機数を描画
            stat_font = pygame.font.SysFont(None, 20)
            stat = stat_font.render("Wave:{:2d}  Lives:{:2d}  Score:{:05d}".format(
                self.wave, self.lives, self.score), False, (255, 255, 255))
            screen.blit(stat, ((SCR_RECT.width - stat.get_width()) // 2, 10))
            # STAGE CLEARを描画
            gameover_font = pygame.font.SysFont(None, 80)
            gameover = gameover_font.render("STAGE CLEAR", False, (255, 0, 0))
            screen.blit(gameover, ((SCR_RECT.width - gameover.get_width()) // 2, 100))
            # エイリアンを描画
            alien_image = Alien.images[0]
            screen.blit(alien_image, ((SCR_RECT.width - alien_image.get_width()) // 2, 200))
            # PUSH SPACEを描画
            push_font = pygame.font.SysFont(None, 40)
            push_space = push_font.render("PUSH SPACE KEY", False, (255, 255, 255))
            screen.blit(push_space, ((SCR_RECT.width - push_space.get_width()) // 2, 300))

    def key_handler(self):
        """キーハンドラー"""
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN and event.key == K_SPACE:
                if self.game_state == START:  # スタート画面でスペースを押したとき
                    self.game_state = PLAY
                elif self.game_state == GAMEOVER:  # ゲームオーバー画面でスペースを押したとき
                    self.score = 0  # スコア初期化
                    self.wave = 1
                    self.lives = 5
                    self.counter = 0
                    self.init_game()  # ゲームを初期化して再開
                    self.game_state = PLAY
                elif self.game_state == STAGECLEAR:
                    self.wave += 1
                    self.lives += 1
                    self.counter = 0
                    self.init_game()  # ゲームを初期化して再開
                    self.game_state = PLAY

    def collision_detection(self):
        """衝突判定"""
        # エイリアンとミサイルの衝突判定
        alien_collided = pygame.sprite.groupcollide(self.aliens, self.shots, True, True)
        for alien in alien_collided.keys():
            Alien.kill_sound.play()
            self.score += 10 * self.wave
            Explosion(alien.rect.center)  # エイリアンの中心で爆発
        # UFOとミサイルの衝突判定
        ufo_collided = pygame.sprite.groupcollide(self.ufos, self.shots, True, True)
        for ufo in ufo_collided.keys():
            Alien.kill_sound.play()
            self.score += 50 * self.wave
            Explosion(ufo.rect.center)
            self.lives += 1
        # プレイヤーとビームの衝突判定
        # 無敵時間中なら判定せずに無敵時間を1減らす
        if self.player.invisible > 0:
            beam_collided = False
            self.player.invisible -= 1
        else:
            beam_collided = pygame.sprite.spritecollide(self.player, self.beams, True)
        if beam_collided:  # プレイヤーと衝突したビームがあれば
            Player.bomb_sound.play()
            Explosion(self.player.rect.center)
            self.lives -= 1
            self.player.invisible = 0  # DQN用は無敵時間無し
            if self.lives < 0:
                self.game_state = GAMEOVER  # ゲームオーバー！
        # 壁とミサイル、ビームの衝突判定
        hit_dict = pygame.sprite.groupcollide(self.walls, self.shots, False, True)
        hit_dict.update(pygame.sprite.groupcollide(self.walls, self.beams, False, True))
        for hit_wall in hit_dict:
            hit_wall.shield -= len(hit_dict[hit_wall])
            for hit_beam in hit_dict[hit_wall]:
                Alien.kill_sound.play()
                Explosion(hit_beam.rect.center)  # ミサイル・ビームの当たった場所で爆発
            if hit_wall.shield <= 0:
                hit_wall.kill()
                Alien.kill_sound.play()
                ExplosionWall(hit_wall.rect.center)  # 壁の中心で爆発

    def load_images(self):
        """イメージのロード"""
        # スプライトの画像を登録
        Player.image = load_image("player.png")
        Shot.image = load_image("shot.png")
        Alien.images = split_image(load_image("alien.png"), 2)
        UFO.images = split_image(load_image("ufo.png"), 2)
        Beam.image = load_image("beam.png")
        Wall.image = load_image("wall.png")
        Explosion.images = split_image(load_image("explosion.png"), 16)
        ExplosionWall.images = split_image(load_image("explosion2.png"), 16)

    def load_sounds(self):
        """サウンドのロード"""
        Alien.kill_sound = load_sound("kill.wav")
        Player.shot_sound = load_sound("shot.wav")
        Player.bomb_sound = load_sound("bomb.wav")


class Player(pygame.sprite.Sprite):
    """自機"""
    speed = 5  # 移動速度
    reload_time = 15  # リロード時間
    invisible = 0  # 無敵時間

    def __init__(self):
        # imageとcontainersはmain()でセット
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.rect = self.image.get_rect()
        self.rect.center = (SCR_RECT.width // 2, SCR_RECT.bottom - 9)
        self.reload_timer = 0

    def update(self):
        # 押されているキーをチェック
        pressed_keys = pygame.key.get_pressed()
        # 押されているキーに応じてプレイヤーを移動
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-self.speed, 0)
        elif pressed_keys[K_RIGHT]:
            self.rect.move_ip(self.speed, 0)
        # self.rect.clamp_ip(SCR_RECT)
        self.rect.clamp_ip(PLAYER_MOVE_RECT)
        # ミサイルの発射
        if pressed_keys[K_SPACE]:
            # リロード時間が0になるまで再発射できない
            '''
            if self.reload_timer > 0:
                # リロード中
                self.reload_timer -= 1
            '''
            if self.reload_timer == 0:
                # 発射！！！
                Player.shot_sound.play()
                Shot(self.rect.center)  # 作成すると同時にallに追加される
                self.reload_timer = self.reload_time


class Alien(pygame.sprite.Sprite):
    """エイリアン"""

    def __init__(self, pos, wave):
        self.speed = 1 + wave  # 移動速度
        self.animcycle = 18  # アニメーション速度
        self.frame = 0
        self.prob_beam = (1.5 + wave) * 0.002  # ビームを発射する確率
        # imagesとcontainersはmain()でセット
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.center = pos

    def update(self):
        # 横方向への移動
        self.rect.move_ip(self.speed, 0)
        # ビームを発射
        if random.random() < self.prob_beam:
            Beam(self.rect.center)
        # キャラクターアニメーション
        self.frame += 1
        self.image = self.images[self.frame // self.animcycle % 2]

    def shoot_extra_beam(self, target_x_pos, border_dist, rate):
        if random.random() < self.prob_beam * rate and \
                abs(self.rect.center[0] - target_x_pos) < border_dist:
            Beam(self.rect.center)


class UFO(pygame.sprite.Sprite):
    """UFO"""

    def __init__(self, pos, wave):
        self.speed = 1 + wave // 2  # 移動速度
        # side => 0: left, 1: right
        side = 0 if random.random() < 0.5 else 1
        if side:
            self.speed *= -1  # 右から出現する場合、速度を反転する
        self.animcycle = 18  # アニメーション速度
        self.frame = 0
        # imagesとcontainersはmain()でセット
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.center = (SCR_RECT.width - pos[0] if side else pos[0], pos[1])  # 開始位置(x)
        self.pos_kill = pos[0] if side else SCR_RECT.width - pos[0]  # 消滅位置(x)

    def update(self):
        # 横方向への移動
        self.rect.move_ip(self.speed, 0)
        # 指定位置まで来たら消滅
        if (self.rect.center[0] > self.pos_kill and self.speed > 0) or \
                (self.rect.center[0] < self.pos_kill and self.speed < 0):
            self.kill()
        # キャラクターアニメーション
        self.frame += 1
        self.image = self.images[int(self.frame // self.animcycle % 2)]


class Shot(pygame.sprite.Sprite):
    """プレイヤーが発射するミサイル"""
    speed = 12  # 移動速度

    def __init__(self, pos):
        # imageとcontainersはmain()でセット
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.rect = self.image.get_rect()
        self.rect.center = pos  # 中心座標をposに

    def update(self):
        self.rect.move_ip(0, -self.speed)  # 上へ移動
        if self.rect.top < 0:  # 上端に達したら除去
            self.kill()


class Beam(pygame.sprite.Sprite):
    """エイリアンが発射するビーム"""
    speed = 5  # 移動速度

    def __init__(self, pos):
        # imagesとcontainersはmain()でセット
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.rect = self.image.get_rect()
        self.rect.center = pos

    def update(self):
        self.rect.move_ip(0, self.speed)  # 下へ移動
        if self.rect.bottom > SCR_RECT.height:  # 下端に達したら除去
            self.kill()


class Explosion(pygame.sprite.Sprite):
    """爆発エフェクト"""
    animcycle = 2  # アニメーション速度
    frame = 0

    def __init__(self, pos):
        # imagesとcontainersはmain()でセット
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.max_frame = len(self.images) * self.animcycle  # 消滅するフレーム

    def update(self):
        # キャラクターアニメーション
        self.image = self.images[self.frame // self.animcycle]
        self.frame += 1
        if self.frame == self.max_frame:
            self.kill()  # 消滅


class ExplosionWall(Explosion):
    pass


class Wall(pygame.sprite.Sprite):
    """ミサイル・ビームを防ぐ壁"""

    def __init__(self, pos, wave):
        self.shield = 80 + 20 * wave  # 耐久力
        # imagesとcontainersはmain()でセット
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.rect = self.image.get_rect()
        self.rect.center = pos

    def update(self):
        pass


def load_image(filename, colorkey=None):
    """画像をロードして画像と矩形を返す"""
    filename = os.path.join("data", filename)
    try:
        image = pygame.image.load(filename)
    except pygame.error as message:
        print("Cannot load image:", filename)
        raise SystemExit(message)
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image


def split_image(image, n):
    """横に長いイメージを同じ大きさのn枚のイメージに分割
    分割したイメージを格納したリストを返す"""
    image_list = []
    w = image.get_width()
    h = image.get_height()
    w1 = w // n
    for i in range(0, w, w1):
        surface = pygame.Surface((w1, h))
        surface.blit(image, (0, 0), (i, 0, w1, h))
        surface.set_colorkey(surface.get_at((0, 0)), RLEACCEL)
        surface.convert()
        image_list.append(surface)
    return image_list


def load_sound(filename):
    """サウンドをロード"""
    filename = os.path.join("data", filename)
    return pygame.mixer.Sound(filename)


if __name__ == "__main__":
    Invader()
