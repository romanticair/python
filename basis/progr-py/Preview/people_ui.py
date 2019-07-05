"""
实现一个图形界面，用于查看和更新存储于shelve中的类示列；
该shelve保存在脚本运行的机器上，可能是一个或多个本地文件；
"""

import shelve
from tkinter import *
from tkinter.messagebox import showerror

shelve_name = 'class-shelve'
field_names = ('name', 'age', 'job', 'pay')


def make_widgets():
    global entries
    entries = {}
    window = Tk()
    window.title('People shelve')
    form = Frame(window)
    form.pack()
    for (ix, label) in enumerate(('key',) + field_names):
        lab = Label(form, text=label)
        ent = Entry(form)
        lab.grid(row=ix, column=0)
        ent.grid(row=ix, column=1)
        entries[label] = ent

    Button(window, text='Fetch', command=fetch_record).pack(side=LEFT)
    Button(window, text='Update', command=update_record).pack(side=LEFT)
    Button(window, text='Quit', command=window.quit).pack(side=RIGHT)
    return window


def fetch_record():
    key = entries['key'].get()
    try:
        record = db[key]
    except KeyError:
        showerror(title='Error', message='No Such Key!')
    else:
        for field in field_names:
            entries[field].delete(0, END)
            entries[field].insert(0, repr(getattr(record, field)))


def update_record():
    key = entries['key'].get()
    if key in db:
        record = db[key]
    else:
        from person import Person
        record = Person(name='?', age='?')
    for field in field_names:
        setattr(record, field, eval(entries[field].get()))

    db[key] = record

if __name__ == '__main__':
    db = shelve.open(shelve_name)
    window = make_widgets()
    window.mainloop()
    db.close()


