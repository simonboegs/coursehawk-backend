import requests
from bs4 import BeautifulSoup
import json
from html.parser import HTMLParser

linkNumbers = [906,908,909,910,911,952,912,913,953,914,915,955,916,917,949,918,919,
           950,920,921,922,923,924,9242,959,925,926,951,927,929,957,958,930,931,932,
           954,934,935,936,937,938,939,940,941,942,943,944,956,945,946,948]

courses = []
for linkNum in linkNumbers:#[22:24]:
    if(linkNum == 9242):
        page = requests.get('https://catalog.ucmerced.edu/content.php?filter%5B27%5D=-1&filter%5B29%5D=&filter%5Bcourse_type%5D=' + str(924) + '&filter%5Bkeyword%5D=&filter%5B32%5D=1&filter%5Bcpage%5D=' + str(2) + '&cur_cat_oid=17&expand=&navoid=1650&search_database=Filter#acalog_template_course_filter')
    else:
        page = requests.get('https://catalog.ucmerced.edu/content.php?filter%5B27%5D=-1&filter%5B29%5D=&filter%5Bcourse_type%5D=' + str(linkNum) + '&filter%5Bkeyword%5D=&filter%5B32%5D=1&filter%5Bcpage%5D=1&cur_cat_oid=17&expand=&navoid=1650&search_database=Filter#acalog_template_course_filter')
    soup = BeautifulSoup(page.content, 'html.parser')
    tables = soup.findAll('table', class_='table_default')
    table = tables[6]
    trs = table.findAll('tr')
    trLast = trs[-1]
    if('Page: ' in trLast):
        numOfPages = 2
    else:
        numOfPages = 1
    subjectFull = table.find('p').text
    print(subjectFull)
    courseLinks = table.findAll('a')
    for l in courseLinks:
        if(l.text == '1' or l.text == '2'):
            continue
        link = l['href']
        courseHeader = l.text
        s = courseHeader.split(': ')
        s2 = s[0].split(' ')
        subjectCode = s2[0]
        courseNumber = s2[1]
        courseTitle = s[1]
        coursePage = requests.get('https://catalog.ucmerced.edu/' + link)
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
        course = {
            'subjectFull': subjectFull,
            'subjectCode': subjectCode,
            'number': courseNumber,
            'title': courseTitle,
            'units': courseUnits,
            'prereqs': coursePrereqs,
            'desc': courseDesc
            }
        for key in course:
            course[key] = course[key].replace('\u2013','-')
            course[key] = course[key].replace('\u2019','\'')
            course[key] = course[key].replace('\u00a0',' ')
            course[key] = course[key].replace('\u201c','\"')
            course[key] = course[key].replace('\u201d','\"')
        courses.append(course)
        print(course['subjectCode'], course['number'])

data = {'courses': courses}
with open('courses_uc-merced2.json','w') as writeFile:
    json.dump(data, writeFile)
