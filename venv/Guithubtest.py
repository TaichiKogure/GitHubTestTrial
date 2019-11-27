#UIのテストプログラム
import tkinter
from tkinter import messagebox


def click_board(event):
    messagebox.showinfo(u"", u"クリックされました")


root = tkinter.Tk()
root.title(u"リバーシ")
root.geometry(str(532) + "x" + str(588))

# キャンバスを作成
canvas_board = tkinter.Canvas(root, width=500, height=500)
# キャンバスがクリックされたときに呼び出す件数を設定
canvas_board.bind("<Button-1>", click_board)
canvas_board.place(x=16, y=72)

root.mainloop()

#colab上では動作しないらしい
