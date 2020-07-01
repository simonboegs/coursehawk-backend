import requests
from bs4 import BeautifulSoup
import json

url = 'http://catalogue.uci.edu'
page = requests.get(url + '/allcourses/')

soup = BeautifulSoup(page.content, 'html.parser')

mainDiv = soup.find('div', id='atozindex')
uls = mainDiv.findAll('ul')
links = []
for ul in uls:
    aTags = ul.findAll('a')
    for a in aTags:
        links.append(a['href'])

courses = []
for i in range(len(links)):
    page = requests.get(url + links[i])
    soup = BeautifulSoup(page.content, 'html.parser')
    h1 = soup.find('h1').text
    s = h1.split(' (')
    subjectFull = s[0]
    subjectCode = s[1].replace(')','')
    #print(subjectFull, subjectCode)
    courseDivs = soup.findAll('div', class_='courseblock')
    for courseDiv in courseDivs:
        blockTitle = courseDiv.find('p', class_='courseblocktitle').text
        s = blockTitle.split('.')
        classCode = s[0].strip()
        classCode = ' '.join(classCode.split())
        
        courseNum = classCode.split(' ')[-1]
        courseTitle = s[1].strip()
        courseUnits = s[2].strip().split(' ')[0]
        
        blockDesc = courseDiv.find('div', class_='courseblockdesc')
        pList = blockDesc.findAll('p')
        courseDesc = pList[0].text
        if(len(pList) > 1 and 'Prerequisite: ' in pList[1].text):
            coursePrereqs = pList[1].text.replace('Prerequisite: ', '').strip().replace('\xa0',' ')
        else:
            coursePrereqs = ''
        n = ''
        for c in courseNum:
            if(c.isdigit()):
                n += c
        n = int(n)
        if(n < 100):
            division = 'lower'
        elif(n < 200):
            division = 'upper'
        else:
            division = 'other'
        course = {
            'subjectFull': subjectFull,
            'subjectCode': subjectCode,
            'number': courseNum,
            'title': courseTitle,
            'units': courseUnits,
            'prereqs': coursePrereqs,
            'desc': courseDesc,
            'division': division
            }
        courses.append(course)
        print(courseCode,courseNum)

data = {'courses' : courses}
with open('courses_ucirvine.json','w') as writeFile:
    json.dump(data, writeFile)
