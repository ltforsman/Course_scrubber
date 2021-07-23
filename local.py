from tkinter import *
import web_scrubbing as ws
import Scheduling as sch

root = Tk(className = ' Cornell Course Scheduler ')

Label(root,text='',height=5, width=3).grid(row = 0, column = 0)
Label(root,text='',height=3, width=3).grid(row = 100, column = 10)

title = Label(root,text = 'Welcome to the Cornell Course Scheduling Tool!',font = ('Arial',12))
title.grid(row = 0, column = 1, columnspan = 2)

Label(root,text=' ').grid(row = 1, column = 1,  columnspan = 2)

d = 'Type desired course numbers separated by commas below \nPlease input course codes of the desired courses in the following format:\n\n {subject abreviation}_{course number}'
directions = Label(root,text = d)
directions.grid(row = 2, column = 1, columnspan = 2)

Label(root,text=' ').grid(row = 3, column = 1,  columnspan = 2)


user = Entry(root, width = 50)
user.grid(row = 4,column = 1)


def runSearch():
    selected_classes = user.get()

    # test = Label(text = selected_classes)
    # test.grid(row = 5,column = 1,columnspan = 2)

    classes = ws.WS_user2_local(selected_classes)

    intervals, sections = sch.recScheduler([],classes,0,[])

    r = 5
    for section in sections:
        section = Label(text = section)
        section.grid(row = r,column = 1, columnspan = 2)
        r += 1
    



search = Button(root,text = 'Search',command = runSearch)
search.grid(row = 4, column = 2)









root.mainloop()