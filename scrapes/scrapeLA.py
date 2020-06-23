import requests
from bs4 import BeautifulSoup
import json

url = 'https://www.registrar.ucla.edu'
page = requests.get(url + '/Academics/Course-Descriptions')

soup = BeautifulSoup(page.content, 'html.parser')

lis = soup.find('div', class_='list-alpha').findAll('li')
courses = []
for li in lis:
    href = li.find('a')['href']
    page = requests.get(url + href)
    soup = BeautifulSoup(page.content, 'html.parser')
    subject = soup.find('span', id='dnn_ctr38600_CourseDetails_headerText').text
    if(subject[-1] == ' '):
        subject = subject[:-1]
    if("(" in subject):
        s = subject.split(" (")
        subjectFull = s[0]
        subjectCode = s[1].replace(")","")
    else:
        subjectFull = subject[0] + subject[1:].lower()
        subjectCode = subject.upper()
    divisions = [soup.find('div', id='lower'), soup.find('div', id='upper')]
    for division in divisions:
        if(division == None):
            continue
        divs = division.findAll('div', class_='media-body')
        for div in divs:
            header = div.find('h3').text.split('. ')
            courseNumber = header[0]
            courseTitle = header[1]
            ps = div.findAll('p')
            courseUnits = ps[0].text.replace('Units: ','')
            if(' ' in courseUnits):
                continue
            body = ps[1].text
            idx1 = body.find('(')
            idx2 = body.find(')')
            courseDesc = body[idx2+1:]
            sentances = courseDesc.split('. ')
            coursePrereqs = ''
            for sentance in sentances:
                if 'Requisite' in sentance or 'Enforced requisite' in sentance:
                    coursePrereqs = sentance.split(': ')[1]
                    sentances.remove(sentance)
                    courseDesc = '. '.join(sentances)
                    break
            if(len(courseDesc) > 0 and  courseDesc[0] == ' '):
                courseDesc = courseDesc[1:]
            course = {
                'subjectFull': subjectFull,
                'subjectCode': subjectCode,
                'number': courseNumber,
                'title': courseTitle,
                'units': courseUnits,
                'prereqs': coursePrereqs,
                'desc': courseDesc
                }
            courses.append(course)
            print(course['subjectFull'],course['subjectCode'])
data = {'courses': courses}
with open('la.json','w') as writeFile:
    json.dump(data, writeFile)
