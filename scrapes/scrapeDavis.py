import requests
from bs4 import BeautifulSoup
import json

url = 'https://ucdavis.pubs.curricunet.com/Catalog/'
page = requests.get(url + 'courses-subject-code')

soup = BeautifulSoup(page.content, 'html.parser')
labels = soup.find_all('span', class_='nav-label')[16:] #starts at 16
courses = []
for i in range(len(labels)):
    label = labels[i].text
    print(label[3])
    s = label.split("―")
    subjectCode = s[0]
    subjectFull = s[1]
    page = requests.get(url + subjectCode + '-courses-sc')
    soup = BeautifulSoup(page.content, 'html.parser')
    courseNums = soup.find_all('span', class_='course-number')
    courseTitles = soup.find_all('span', class_='course-title')
    courseCredits = soup.find_all('span', class_='course-credits')
    descDivs = soup.find_all('div', class_='row course-summary-paragraph')
    courseDescs = []
    courseInfos = []
    coursePrereqs = []
    for descDiv in descDivs:
        spans = descDiv.find_all('span')
        courseInfos.append(spans[0])
        if(spans[1].text != 'Prerequisite(s):'):
            courseDescs.append(spans[2])
            coursePrereqs.append('')
        else:
            coursePrereqs.append(spans[2])
            courseDescs.append(spans[4])
    for j in range(len(courseNums)):
        if(courseInfos[j].text[0:7] != 'Lecture'):
            continue
        if(coursePrereqs[j] == ''):
            prereqs = ''
        else:
            prereqs = coursePrereqs[j].text#.replace('.','').split('; ')
        course = {'subjectFull': subjectFull,
                  'subjectCode': subjectCode,
                  'number': courseNums[j].text,
                  'title': courseTitles[j].text,
                  'credits': courseCredits[j].text[1],
                  'prereqs': prereqs,
                  'desc': courseDescs[j].text}
        courses.append(course)
        print(course['subjectFull'],course['subjectCode'])
#print(courses)
data = {'courses': courses}
with open('courses_ucdavis.json','w') as writeFile:
    json.dump(data, writeFile)
