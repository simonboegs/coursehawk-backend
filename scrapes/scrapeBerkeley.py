import requests
from bs4 import BeautifulSoup
import json

url = 'http://guide.berkeley.edu/courses/'
page = requests.get(url)

soup = BeautifulSoup(page.content, 'html.parser')
mainDiv = soup.find('div', id='atozindex')
labels = mainDiv.findAll('li')
courses = []
for i in range(len(labels)):
    labels[i] = labels[i].find('a').text
    idx1 = labels[i].find('(')
    idx2 = labels[i].find(')')
    subjectCode = labels[i][idx1+1:idx2]
    subjectFull = labels[i][:idx1-1]
    page = requests.get(url + subjectCode.replace(' ','_').lower())
    soup = BeautifulSoup(page.content, 'html.parser')
    courseNumber = soup.findAll('span', class_='code')
    courseTitles = soup.findAll('span', class_='title')
    courseUnits = soup.findAll('span', class_='hours')
    courseDescs = soup.findAll('span', ['descshow', 'descshow overflow'])
    coursePrereqs = []
    detailsDivs = soup.findAll('div', class_='coursedetails')
    for detailsDiv in detailsDivs:
        sections = detailsDiv.findAll('div', class_='course-section')
        if(len(sections) == 3):
            prereq = sections[0].findAll('p')[1].text
            if('Prerequisites' in prereq):
                prereq = prereq.replace('Prerequisites: ','')
            else:
                prereq = ''
        else:
            prereq = ''
        coursePrereqs.append(prereq)
    for j in range(len(courseTitles)):
        course = {
            'subjectFull': subjectFull,
            'subjectCode': subjectCode,
            'number': courseNumber[j].text.split('\xa0')[-1],
            'title': courseTitles[j].text,
            'units': courseUnits[j].text.replace(' Units',''),
            'prereqs': coursePrereqs[j],
            'desc': courseDescs[j].text.split('\n')[-1]
            }
        courses.append(course)
        print(course['subjectFull'],course['subjectCode'])
        
data = {'courses': courses}
with open('courses_ucberkeley.json','w') as writeFile:
    json.dump(data, writeFile)
