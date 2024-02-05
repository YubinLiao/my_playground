import tkinter as tk


def get_Clipboard_Text():
    r = tk.Tk()
    text = r.clipboard_get()
    r.withdraw()
    r.update()
    r.destroy()
    return text


if __name__ == "__main__":
    text = get_Clipboard_Text()
    print(text)
