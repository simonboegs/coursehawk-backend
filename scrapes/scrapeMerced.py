import requests
from bs4 import BeautifulSoup
import json

urlBase = 'https://catalog.ucmerced.edu/'
urlExt = 'content.php?catoid=17&navoid=1650'

courses = []
currentPageNum = 1
subjectArr = []
subjectIndex = -1
currentCode = ''
while(currentPageNum <= 19):
    page = requests.get(urlBase + urlExt)
    soup = BeautifulSoup(page.content, 'html.parser')
    tables = soup.findAll('table', class_='table_default')
    table = tables[6]
    ps = table.findAll('p')
    subjects = [p.text for p in ps]
    for sub in subjects:
        subjectArr.append(sub)
    courseLinks = table.findAll('a')
    for l in courseLinks:
        link = l['href']
        if(not ('preview_course' in link)):
            break
        courseHeader = l.text
        s = courseHeader.split(': ')
        s2 = s[0].split(' ')
        subjectCode = s2[0]
        if(subjectCode != currentCode):
            currentCode = subjectCode
            subjectIndex += 1
            print('subjectIndex', subjectIndex - 1, '->', subjectIndex)
        courseNumber = s2[1]
        courseTitle = s[1]
        newUrl = urlBase + link
        coursePage = requests.get(urlBase + link)
        newSoup = BeautifulSoup(coursePage.content, 'html.parser')
        h1 = newSoup.find('h1', id='course_preview_title').text
        ts = newSoup.findAll('table', class_='table_default')
        infoTable = ts[3]
        #print(infoTable.text)
        td = newSoup.find('td', class_='block_content')
        text = td.text
        idx = text.find(courseHeader) + len(courseHeader)
        text = text[idx:]
        prereqIdx = text.find('Prerequisite:')
        if(prereqIdx != -1):
            coursePrereqs = text[prereqIdx + 14:text.find('Instructor Permission Required:')]
            openIdx = coursePrereqs.find('Open only to the following class level(s):')
            if(openIdx != -1):
                coursePrereqs = coursePrereqs[:openIdx]
        else:
            coursePrereqs = ''
        if(text[:6] == 'Units:'):
            courseUnits = text[7]
            courseDesc = text[8:]
        elif(text[:17] == 'Lower Unit Limit:'):
            unitsLower = text[18]
            unitsUpper = text[37]
            courseUnits = unitsLower + ' - ' + unitsUpper
            courseDesc = text[38:]
        idx2 = courseDesc.find('Course Details')
        courseDesc = courseDesc[:idx2]
        try:
            course = {
                'subjectFull': subjectArr[subjectIndex],
                'subjectCode': subjectCode,
                'number': courseNumber,
                'title': courseTitle,
                'units': courseUnits,
                'prereqs': coursePrereqs,
                'desc': courseDesc
                }
        except:
            print(subjectArr)
            print(subjectIndex)
        courses.append(course)
        print(course['subjectCode'], course['number'])
    trs = table.findAll('tr')
    pageNumbers = trs[-1]
    nextPageLink = pageNumbers.findAll('a')[currentPageNum]
    urlExt = nextPageLink['href']
    print('next page')

data = {'courses': courses}
with open('courses_uc-merced.json','w') as writeFile:
    json.dump(data. writeFile)
