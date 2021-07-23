from tkinter import *
import Scheduling as sc

root = Tk(className = ' Cornell Course Scheduler ')
root.geometry('+100+100')

Label(root,text='',height=5, width=3).grid(row = 0, column = 0)
Label(root,text='',height=3, width=3).grid(row = 10, column = 10)

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
    test = Label(text = 'test')
    test.grid(row = 5,column = 1,columnspan = 2)
    

search = Button(root,text = 'Search',command = runSearch)
search.grid(row = 4, column = 2)









root.mainloop()