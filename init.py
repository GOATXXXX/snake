from tkinter import Tk, Canvas, Button, PhotoImage
import huohua1


def start_game(mode):
    root.destroy()
    if mode == "正常":
        huohua1.start(0.5)
    elif mode == "困难":
        huohua1.start(0.3)
    elif mode == "地狱":
        huohua1.start(0.1)


# 创建Tkinter窗口
root = Tk()

# 加载背景图片
bg_image = PhotoImage(file="background_image.png")

# 创建画布，并设置背景图片
canvas = Canvas(root, width=1164, height=554)
canvas.pack()
canvas.create_image(0, 0, image=bg_image, anchor="nw")

# start_button = Button(canvas, text="开始游戏", command=start_game, font=("Helvetica", 18), bg="orange", fg="black")
# start_button.place(relx=0.5, rely=0.85, anchor="center")
# 创建三个模式选择按钮
normal_button = Button(canvas, text="正常", command=lambda: start_game("正常"), font=("Helvetica", 14), bg="green", fg="black")
normal_button.place(relx=0.4, rely=0.85, anchor="center")

hard_button = Button(canvas, text="困难", command=lambda: start_game("困难"), font=("Helvetica", 14), bg="orange", fg="black")
hard_button.place(relx=0.5, rely=0.85, anchor="center")

hell_button = Button(canvas, text="地狱", command=lambda: start_game("地狱"), font=("Helvetica", 14), bg="red", fg="black")
hell_button.place(relx=0.6, rely=0.85, anchor="center")


# 显示窗口
root.mainloop()