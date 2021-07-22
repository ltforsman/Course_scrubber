import re
from itertools import groupby

# print(type(re.search('(LEC)|(LAB)|(DIS)|(IND)|(SEM)|(RSC)','Class Section LAB 001').group()))

# t = 'DIS'
# regex = '(?=DIS).*$'
# print(re.findall(f'(?={t}).*$','Class Section DIS 202'))

print('\n-------------------------------------------------------------------------')
print('Welcome to the Cornell Course Scheduling Tool!\n\nPlease input course codes of the desired courses in the following format:')
print('\n{subject abreviation}_{course number}\n')
user_classes = input('Type course numbers separated by commas: ' )
user_classes = user_classes.upper()
user_classes = user_classes.split(',')
user_classes = [c.lstrip().rstrip() for c in user_classes]
user_classes.sort()

print('\n',user_classes,'\n')

# - group by subject - #

# grouped_classes = 

grouped_classes = [list(i) for j,i in groupby(user_classes,lambda a: a.split(' ')[0])]

print('\n',grouped_classes,'\n')

s1 = grouped_classes[0]

subject = s1[0].split(' ')[0]
print('\n',subject)

print('Git Test')