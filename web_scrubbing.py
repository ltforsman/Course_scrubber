from bs4 import BeautifulSoup
import requests
import re
from itertools import groupby


def WS_main(subject = 'ECE', visual = False):

    # -- use if only searching single subject -- #
    # selected_classes = singleSubject(subject)

    # -- use if multiple subjects -- #
    selected_classes = WS_user2()
    
    if visual:
        for c in selected_classes:

            print(c)
            print()

    return selected_classes



def singleSubject(subject = 'ECE'):
    classes = grabClasses(subject)
    selected_classes = WS_user(classes,subject)
    return selected_classes

def grabClasses(subject = 'ECE'):
    ''' Documentation
        function that grabs all the courses from one subject and creates a dictionary structure of all the necessary information in the class
        input:
        - subject = string in all caps representing the subject abbreviation at Cornell
        output:
        - classes = dictionary of all the classes and their information. Structured like:
            {
                Class: {
                    code:
                    name:
                    link:
                    sections:{
                        LEC : [
                            {
                                number:
                                instructor:
                                days:
                                time:
                                dates:
                                open-status:
                                instr_mode:
                            }
                        ]
                    }
                },
                Class:...
            }
    '''


    print('Fetching Classes...')
    text = "https://classes.cornell.edu/browse/roster/FA21/subject/%s" % subject
    result = requests.get(text)
    src = result.content

    soup = BeautifulSoup(src,'lxml')


    nodes = list(soup.find_all('div',{'class':'node'}))
    
    # prints to check nodes
        # print(len(nodes))
        # print(nodes[62])
        # print(nodes[1].prettify())

    classes = dict()
    for node in nodes[1:]:
        course = dict()
        code = node.find('div', {'class':'title-subjectcode'}).string
        course['code'] = code

        name_item = node.find('div',{'class':'title-coursedescr'})
        name = name_item.find('a').string
        link = name_item.find('a').attrs['href']
        course['name'] = name
        course['link'] = link

        classes[code] = course


        #SECTIONS:
        sections = node.find_all('ul',{'class':'section'})
        secs = dict()
        for section in sections:
            sec = dict()

            title = section.attrs['aria-label']
            sec_type = re.search('(LEC)|(LAB)|(DIS)|(IND)|(SEM)|(RSC)',title).group()
            sec['number'] = re.findall(f'(?={sec_type}).*$',title)[0]

            instructor_item = section.find('li',{'class':'instructors'})
            instructor = instructor_item.find('span')
            if instructor == None:
                sec['instructor'] = None
            else:
                sec['instructor'] = instructor.string
            

            days_item = section.find('span',{'class':'pattern-only'})
            days = days_item.find('span').string
            if days != None:
                sec['days'] = re.findall('[A-Z]',days)

            time = section.find('time')
            if time == None:
                sec['time'] = None
            else:
                sec['time'] = time.string

            
            dates = section.find('li',{'class':'date-range'})
            if dates == None or dates.string == None:
                sec['dates'] = None
            else:
                sec['dates'] = re.findall('(?<=\n )(.*)(?=\n)',dates.string)[0]

            open_status_item = section.find('li',{'class':'open-status'})
            open_status = open_status_item.find('span').attrs['data-content']
            sec['open_status'] = open_status

            instruc_item = section.find('li',{'class':'notes'})
            instruc_mode = instruc_item.find('span',{'class':'instr-mode'}).string
            sec['instr_mode'] = instruc_mode

            if days != None:
                if sec_type in secs.keys():
                    secs[sec_type].append(sec)
                else:
                    secs[sec_type] = [sec]
            

        course['sections'] = secs

    print('Done')
    return classes

# - test of grab classes - #
    # classes = grabClasses()
    # print(classes)

def WS_user(classes,subject = 'ECE'):
    '''
    Function that asks the user for which classes they want to schedule together and returns a list of classes(+info)

    inputs:
     - classes = dictionary all classes from one subject
     - subject = string of the subject that 'classes' is from

    output:
     - selected = list of the classes(+info) that the user asked for [currently only one subject]

    '''
    user_classes = input('Type course numbers separated by commas: ' )
    user_classes = user_classes.replace(' ','')
    user_classes = user_classes.split(',')

    uclasses = [subject + ' ' + uc for uc in user_classes]
    # uclasses = ['CS ' + uc for uc in user_classes]

    selected = []
    for c in uclasses:
        try:
            course_sections = classes[c]['sections']
            selected.append(classes[c])
            # extra prints 
                # for t,s in course_sections.items():
                #     print(t)
                #     print(s)
                #     print()
        except KeyError:
            print('Class ', c, ' does not exist. Please rerun.')
            break

    return selected



def grabClasses2(subject,requested):
    ''' Documentation
        Function that creates a list of all the requested courses from one subject by
        grabbing all the courses from one subject, creating a dictionary structure of all the necessary information for each class

        input:
        - subject = string in all caps representing the subject abbreviation at Cornell
        - requested = list of classes from one subject in the form [{subject abreviation}_{course number},...]

        output:
        - selected = list of all the requested classes (only the section information)
        
        Important: 
         each class is held as a dictionary structured like:
            {
                Class: {
                    code:
                    name:
                    link:
                    sections:{
                        LEC : [
                            {
                                number:
                                instructor:
                                days:
                                time:
                                dates:
                                open-status:
                                instr_mode:
                            }
                        ]
                    }
                },
                Class:...
            }
    '''

 # - access website - #
    text = "https://classes.cornell.edu/browse/roster/FA21/subject/%s" % subject
    print(text)
    result = requests.get(text)
    src = result.content

    soup = BeautifulSoup(src,'lxml')


    nodes = list(soup.find_all('div',{'class':'node'})) # each node is a class
    
    # prints to check nodes
        # print(len(nodes))
        # print(nodes[62])
        # print(nodes[1].prettify())

 # - get all classes(+info) - #
    classes = dict()
    for node in nodes[1:]:
        course = dict()
        code = node.find('div', {'class':'title-subjectcode'}).string
        course['code'] = code

        name_item = node.find('div',{'class':'title-coursedescr'})
        name = name_item.find('a').string
        link = name_item.find('a').attrs['href']
        course['name'] = name
        course['link'] = link

        classes[code] = course


        #SECTIONS:
        sections = node.find_all('ul',{'class':'section'})
        secs = dict()
        for section in sections:
            sec = dict()

            title = section.attrs['aria-label']
            sec_type = re.search('(LEC)|(LAB)|(DIS)|(IND)|(SEM)|(RSC)|(TA)',title).group()
            sec['number'] = re.findall(f'(?={sec_type}).*$',title)[0]

            instructor_item = section.find('li',{'class':'instructors'})
            instructor = instructor_item.find('span')
            if instructor == None:
                sec['instructor'] = None
            else:
                sec['instructor'] = instructor.string
            

            days_item = section.find('span',{'class':'pattern-only'})
            days = days_item.find('span').string
            if days != None:
                sec['days'] = re.findall('[A-Z]',days)

            time = section.find('time')
            if time == None:
                sec['time'] = None
            else:
                sec['time'] = time.string

            
            dates = section.find('li',{'class':'date-range'})
            if dates == None or dates.string == None:
                sec['dates'] = None
            else:
                sec['dates'] = re.findall('(?<=\n )(.*)(?=\n)',dates.string)[0]

            open_status_item = section.find('li',{'class':'open-status'})
            open_status = open_status_item.find('span').attrs['data-content']
            sec['open_status'] = open_status

            instruc_item = section.find('li',{'class':'notes'})
            instruc_mode = instruc_item.find('span',{'class':'instr-mode'}).string
            sec['instr_mode'] = instruc_mode

            if days != None:
                if sec_type in secs.keys():
                    secs[sec_type].append(sec)
                else:
                    secs[sec_type] = [sec]
            

        course['sections'] = secs

 # - get the requested classes - #

    selected = []
    for c in requested:
        try:
            course_sections = classes[c]['sections']
            selected.append(classes[c])
            # extra prints 
                # for t,s in course_sections.items():
                #     print(t)
                #     print(s)
                #     print()
        except KeyError:
            print('Class ', c, ' does not exist. Please start again.')
            return -1

 #
    return selected

def WS_user2():
    '''
    Function that asks the user for which classes they want to schedule together and returns a list of classes(+info)
    Updated to be able to take classes from multiple subjects

    output:
     - selected = list of the classes(+info) that the user asked for [any combination of subjects]

    '''
    print('\n-------------------------------------------------------------------------')
    print('Welcome to the Cornell Course Scheduling Tool!\n\nPlease input course codes of the desired courses in the following format:')
    print('\n{subject abreviation}_{course number}\n')
    user_classes = input('Type course numbers separated by commas: ' )
    user_classes = user_classes.upper()
    user_classes = user_classes.split(',')
    user_classes = [c.lstrip().rstrip() for c in user_classes]
    user_classes.sort()

    # print('\n',user_classes,'\n')

    # - group by subject - #
    grouped_classes = [list(i) for j,i in groupby(user_classes,lambda a: a.split(' ')[0])]

    # print('\n',grouped_classes,'\n')

    print('\nFetching Classes...')
    uclasses = []
    for sub_courses in grouped_classes:
        subject = sub_courses[0].split(' ')[0]
        subject_classes = grabClasses2(subject,sub_courses)
        if subject_classes == -1:
            return -1
        uclasses.extend(subject_classes)
    
    print('Done')
    
    return uclasses


    

def WS_user2_noText(user_classes):
    '''
    Function that asks the user for which classes they want to schedule together and returns a list of classes(+info)
    Updated to be able to take classes from multiple subjects

    input:
     - user_classes = string containing the user input in format ' {subject abreviation}_{course number}, ...'
    output:
     - selected = list of the classes(+info) that the user asked for [any combination of subjects]

    '''

    user_classes = user_classes.upper()
    user_classes = user_classes.split(',')
    user_classes = [c.lstrip().rstrip() for c in user_classes]
    user_classes.sort()

    # print('\n',user_classes,'\n')

    # - group by subject - #
    grouped_classes = [list(i) for j,i in groupby(user_classes,lambda a: a.split(' ')[0])]

    # print('\n',grouped_classes,'\n')

    print('\nFetching Classes...')
    uclasses = []
    for sub_courses in grouped_classes:
        subject = sub_courses[0].split(' ')[0]
        subject_classes = grabClasses2(subject,sub_courses)
        if subject_classes == -1:
            return -1
        uclasses.extend(subject_classes)
    
    print('Done')
    
    return uclasses

# WS_main()
# WS_user2()
