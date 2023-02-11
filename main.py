from PIL import Image
import numpy as np
import os
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk


def read_image(path):
    try:
        image_src = Image.open(path)
        return image_src
    except Exception as e:
        print(e)


def create_black(width_src, height_src):
    new_black = [[0, 0, 0]] * width_src
    new_black = [new_black] * ((width_src - height_src) // 2)
    new_black = np.array(new_black)
    new_black = Image.fromarray((new_black * 255).astype(np.uint8))
    return new_black


def get_concat_v(im1, im2):
    dst = Image.new('RGB', (im1.width, im1.height + im2.height))
    dst.paste(im1, (0, 0))
    dst.paste(im2, (0, im1.height))
    return dst


def process(file_src, mode, done):
    image = read_image(file_src)
    width, height = image.size
    if width != height:
        progress['value'] = done
        window.update_idletasks()
        if mode == '1':
            cut = (width-height) // 2
            image = image.crop((cut, 0, width-cut, height))

        elif mode == '2':
            black_im = create_black(width, height)
            image = get_concat_v(get_concat_v(black_im, image), black_im)

        if image.size[0] > int(size_ent.get()):
            image = image.resize((int(size_ent.get()), int(size_ent.get())))

    return image


def btn_akt_start():
    path = tk.filedialog.askopenfilenames(title="Select file",
                                          filetypes=(("JPEG files", "*.jpg"), ("all files", "*.*")))
    total = len(path)

    progress['maximum'] = total
    done = 0
    progress['value'] = done
    progress.pack()
    window.update_idletasks()
    if total != 0:
        for infile in path:
            done += 1
            file, ext = os.path.splitext(infile)
            process(infile, chosen_mode.get(), done).save(file + " Cover" + ".jpg", "JPEG")

    progress['value'] = 100
    progress.pack_forget()


window = tk.Tk()
window.title("Cover Maker - v1.2")
window.geometry("300x200")
window.resizable(0, 0)
window.config(bg="grey")

top_frm = tk.Frame(master=window, relief=tk.FLAT, borderwidth=1, width=151, height=46, bg="grey")
top_frm.pack()

info_size_lbl = tk.Label(master=top_frm, text="Cover size (px):", bg="grey", fg="white")
info_size_lbl.place(x=0, y=20, width=110, height=25)
size_ent = tk.Entry(master=top_frm, relief=tk.SOLID, borderwidth=1)
size_ent.insert(0, "600")
size_ent.place(x=110, y=20, width=40, height=25)

cent_frm = tk.Frame(master=window, relief=tk.FLAT, borderwidth=1, width=210, height=35, bg="grey")
cent_frm.pack()

chosen_mode = tk.StringVar()
mode_one_r_btn = tk.Radiobutton(master=cent_frm, text='Cut Sides', variable=chosen_mode,
                                value='1', fg="white", bg="grey",
                                activebackground="grey", activeforeground="white", selectcolor="grey")
mode_one_r_btn.select()
mode_one_r_btn.place(x=0, y=5, width=80, height=25)
mode_two_r_btn = tk.Radiobutton(master=cent_frm, text='Add Top & Bottom', variable=chosen_mode, value='2',
                                fg="white", bg="grey",
                                activebackground="grey", activeforeground="white", selectcolor="grey")
mode_two_r_btn.deselect()
mode_two_r_btn.place(x=90, y=5, width=120, height=25)

bot_frm = tk.Frame(master=window, relief=tk.FLAT, borderwidth=1, width=150, height=70, bg="grey")
bot_frm.pack()

start_btn = tk.Button(bot_frm, text="Select & Start", width=10, command=btn_akt_start)
start_btn.place(x=0, y=30, width=90, height=25)
exit_btn = tk.Button(bot_frm, text="Exit", width=40, command=window.quit)
exit_btn.place(x=100, y=30, width=50, height=25)

progress = ttk.Progressbar(window, orient=tk.HORIZONTAL, length=200, mode='determinate')

window.mainloop()
