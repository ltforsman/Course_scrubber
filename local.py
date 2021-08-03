from tkinter import *
import web_scrubbing as ws
import Scheduling as sch

root = Tk(className = ' Cornell Course Scheduler ')

Label(root,text='',height=5, width=3).grid(row = 0, column = 0)
Label(root,text='',height=3, width=3).grid(row = 100, column = 10)

title = Label(root,text = 'Welcome to the Cornell Course Scheduling Tool!',font = ('Arial',12))
title.grid(row = 0, column = 1, columnspan = 5)

Label(root,text=' ').grid(row = 1, column = 1,  columnspan = 5)

d = 'Type desired course numbers separated by commas below \nPlease input course codes of the desired courses in the following format:\n\n {subject abreviation}_{course number}'
directions = Label(root,text = d)
directions.grid(row = 2, column = 1, columnspan = 5)

Label(root,text=' ').grid(row = 3, column = 1,  columnspan = 5)


user = Entry(root, width = 50)
user.grid(row = 4,column = 3)


def runSearch():
    selected_classes = user.get()

    # test = Label(text = selected_classes)
    # test.grid(row = 5,column = 1,columnspan = 2)

    classes = ws.WS_user2_noText(selected_classes)

    intervals = sch.recScheduler([],classes,0)

    schedule = sch.readable(intervals)

    r = 5
    c = 1
    for day,value in schedule.items():
        d = Label(text = day)
        d.grid(row = r, column = c)

        for s in value:
            r += 1
            section = str(s[0])
            inter = str(s[1]) + ' - ' + str(s[2])
            t = section + '\n' + inter + '\n--------'
            i = Label(text = t)
            i.grid(row = r,column = c)

        r = 5
        c += 1
    



search = Button(root,text = 'Search',command = runSearch)
search.grid(row = 4, column = 4)









root.mainloop()