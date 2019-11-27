# リバーシ

SPACE = 0
BLACK = 1
WHITE = -1

BOARD_PX_SIZE = 500
CELL_PX_SIZE = BOARD_PX_SIZE \ 8


# マスの座標を管理する

class Position:
    def __int__(self):
        self.y = 0
        self.x = 0

    def __init__(self, y, x):
        self.y = y
        self.x = x


# 盤面クラス
# -----------------------------------
class Board:
    # 8方向のyxの加算値
    DIR = [[-1, -1], [-1, 0], [-1, 1],
           [0, -1], [0, 1],
           [1, -1], [1, 0], [1, 1]]


def __init__(self):
    # 盤面、8×8の2次元リストを生成
    self.board = \
        [[SPACE for i in range(8)] for j in range(8)]
    self.turn = BLACK  # 手番
    self.move_num = 1  # 手数


# 盤面の初期化
def init_board(self):
    for y in range(8):
        for x in range(8):
            self.board[y][x] = SPACE
    self.board[3][3] = WHITE
    self.board[3][4] = BLACK
    self.board[4][3] = BLACK
    self.board[4][4] = WHITE

    self.turn = BLACK  # 手番
    self.mobe_num = 1  # 手数


# 白黒の石数をタプルで返す
def get_discs(self):
    black_discs = 0
    white_discs = 0
    for y in range(8):
        for x in range(8):
            disc = self.board[y][x]
            if disc == BLACK:
                black_discs += 1
            elif disc == WHITE:
                white_discs += 1
        return (black_discs, white_discs)


# 指定のマスに石は打てるか
def is_movable(self, position):
    # 空きでなければ打てない
    if self.board[position.y][position.x] != SPACE:
        return False

        # 各方向に石をひっくり返せるか？
    for dir in Board.DIR:
        y = position.y + dir[0]
        x = position.x + dir[1]
        if y >= 0 and x >= 0 and y < 8 and x < 8 and self.board[y][x] == -self.turn:
            # 隣が相手の石
            y += dir[0]
            x += dir[1]
            while y >= 0 and x >= 0 and y < 8 and x < 8 and x < 8 and self.board[y][x] == -self.turn:
                y += dir[0]
                x += dir[1]
            if y >= 0 and x >= 0 and y < 8 and x < 8 \
                    and self.board[y][x] == self.turn:
                return True
        return False


# 石を打てるマスのリストを返す
def get_move_list(self):
    move_list = []
    for y in range(8):
        for x in range(8):
            if self.board[y][x] == SPACE:
                position = Position(y, x)
                if self.is_movable(position):
                    move_list.append(position)
        return move_list


# 局面をすすめる
def move(self, position):
    # 石を打つ
    self.board[position.y][position.x] = self.turn

    # 石をひっくり返す
    # 各方向に医師をひっくり返せるか調べる
    for dir in Board.DIR:
        y = position.y = dir[0]
        x = position.x = dif[1]
        if y >= and x >= and y < 8 and x < 8 \
                and self.board[y][x] == -self.turn:
            # 隣が相手の石
            y += dir[0]
            x += dir[1]
            while y >= 0 and x >= 0 and y < 8 and \
                    x < 8 and self.board[y][x] == -self.turn:
                y += dir[0]
                x += dir[1]
            if y >= 0 and x >= 0 and y < 8 and x < 8 \
                    and self.board[y][x] == self.turn:
                # この方向は返せる
                # 1マス戻る
                y -= dir[0]
                x -= dir[1]
                # 戻りながら返す
                while y >= 0 and x >= 0 and y < 8 and \
                        x < 8 and self.board[y][x] == self.turn:
                y -= dir[0]
                x -= dir[1]

        self.turn = -self.turn # 手番を変更
        self. move_num += 1  # 手数を増やす

    # パスする
    def move_pass(self):
        self.turn = -self.turn  # Pass

    # 対局終了の判定
    def is_game_end(self):
        # 60手に達したとき
        if self.move_num == 61:
            return True
        # 白黒どちらかの石数がゼロになったとき
        # 白黒の石数をタプルで取得
        (black_discs, white_discs) = self.get_discs()
        if black_discs == or white_discs == 0:
            return True

        # 白黒どちらも手がないとき
        move_list1 = self.get_move_list()
        if len(move_list1) == 0:
            self.move_pass()  # パスして相手番にする。
            move_list2 = self.get_move_list()
            self, move_pass()  # パスして戻す
            if len(move_list2) == 0:
                return True

        return False

# ーーーーーーーーーーーーーーーーーーーーーーーーー
# ゲームクラス
# ーーーーーーーーーーーーーーーーーーーーーーーーー
class Game:
    def __init__(self):
        #ゲームの状態　０開始まち１対局中２対局終了
        self.game_mode = 0
        #　●　０プレイヤー１コンピュータ
        self.black_player = 0
        #　○　０プレイヤー１コンピュータ
        self.white_player = 0
        self.board = Board() #盤面作成
        self.board.init_board() #盤面の初期化

    #対局開始
    def start(self, _black_player, _white_player):
        self.black_player = _black_player
        self.white_player = _white_player
        self.game_mode = 1 #ゲームの状態：対局中
        self.board.init_board() #盤面の初期化









