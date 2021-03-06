from PIL import (
    Image,
    ImageDraw,
    ImageFont,
)

from tkinter import (
    Button,
    Entry,
    Label,
    Tk,
    StringVar,
    messagebox as msgbox,
    PhotoImage,
)

from contextlib import closing

import re
import os
import sys
import time
import _thread
import pathlib

AssetsPath = fr"{str(pathlib.Path().parent.resolve())}\{'assets'}"
FileName = os.urandom(10).hex()

if sys.platform.startswith("win"):
    import ctypes
    ctypes.windll.shcore.SetProcessDpiAwareness(2)

if not os.path.isfile(os.path.join(AssetsPath, "base.png")):
    with closing(Image.new("RGB", size=(500, 500))) as NewImage:
        NewImage.save(r"assets\base.png")

def _TextSetter(variable: StringVar, EntryBox: Entry):
    while True:
        if EntryBox.get() in ("", "텍스트"):
            variable.set("글자가 설정되지 않았습니다.")
        else:
            variable.set(EntryBox.get())
        time.sleep(.001)

def CreateStoryProfilePicture(Text, Size = None):
    if Size:
        if not str(Size).isnumeric():
            msgbox.showerror("오류", "글자 크기가 올바른 정수로 설정되지 않았습니다!")
            raise Exception("Exception for handling")

        if int(Size) >= 60:
            msgbox.showerror("오류", "글자 크기는 60보다 클 수 없습니다!")
            raise Exception("Exception for handling")        

    if len(Text) >= 100:
        msgbox.showerror("오류", "텍스트는 100 글자를 넘을 수 없습니다!")
        raise Exception("Exception for handling")

    if Text == "":
        msgbox.showerror("오류", "텍스트는 올바른 영어로 이루어져야 합니다!")
        raise Exception("Exception for handling")

    if not re.sub(r"[0-9]", "", Text).isalpha():
        msgbox.showerror("오류", "텍스트는 무조건 영어여야합니다!")
        raise Exception("Exception for handling")

    with closing(Image.open(os.path.join(AssetsPath, "base.png")) )as BaseImage:
        draw = ImageDraw.Draw(BaseImage, "RGB")
        draw.text((500/2, 500/2), Text, font=ImageFont.truetype(os.path.join(AssetsPath, "LuckiestGuy-Regular.ttf"), size=round(1000 / (len(Text) * 2)) if Size == None else Size * 2), align="center", anchor="mm")

        return BaseImage.save(f"{FileName}.png")

def ShowPreviewImage():
    try:
        CreateStoryProfilePicture(Text=BottomText.get(), Size=(int(SizeEntry.get()) if SizeEntry.get() not in ("글자 크기", "") else None))
    except Exception as e:
        print(e)
        return None

    _root = Tk()
    _root.title("미리보기")
    _root.geometry("500x500")
    _root.resizable(False, False)
    _root.iconbitmap(os.path.join(AssetsPath, "STORY.ico"))

    image = PhotoImage(file=f"{FileName}.png", master=_root)
    image_label = Label(_root, image=image)

    def purge():
        os.remove(f"{FileName}.png")
        _root.destroy()

    _root.protocol("WM_DELETE_WINDOW", purge)

    image_label.pack()
    _root.mainloop()

def SaveImage():
    global FileName
    try:
        CreateStoryProfilePicture(Text=BottomText.get(), Size=(SizeEntry.get() if SizeEntry.get() not in ("글자 크기", "") else None))
    except Exception as error:
        return print(error)
    else:
        msgbox.showinfo("저장 성공", f"{FileName}.png로 저장되었습니다.")
        FileName = os.urandom(10).hex()

root = Tk()
root.title("스토리 프사 생성기")
root.resizable(False, False)
root.geometry("500x500")
root.iconbitmap(os.path.join(AssetsPath, "STORY.ico"))

Text = StringVar(value="글자가 설정되지 않았습니다.")

BottomText = Entry(root)
SizeEntry = Entry(root)
TextViewer = Label(root, textvariable=Text)
PreviewButton = Button(root, text="미리 보기", command=ShowPreviewImage)
SaveButton = Button(root, text="저장하기", command=SaveImage)

if __name__ == "__main__":
    _thread.start_new_thread(_TextSetter, (Text, BottomText))
    BottomText.insert(0, "텍스트")
    SizeEntry.insert(0, "글자 크기")
    BottomText.pack(fill="x")
    SizeEntry.pack()
    TextViewer.pack()
    PreviewButton.pack()
    SaveButton.pack()
    root.mainloop()
