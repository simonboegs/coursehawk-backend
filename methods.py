import json
from rank_bm25 import BM25Okapi
from nltk.stem import PorterStemmer

def getRelevantCourses(school, interests):
    courses = getCourses(school)
    textArr = []
    for course in courses:
        text = course['title'] + '. ' + course['desc']
        textArr.append(process(text))
    bm25 = BM25Okapi(textArr)
    interests = interests.replace('-',' ')
    query = process(interests)
    scores = bm25.get_scores(query).tolist()
    #return bm25.get_top_n(query, textArr, n=1)
    idx = scores.index(max(scores))
    relevantCourses = []
    for i in range(len(scores)):
        courses[i]['relevancy'] = scores[i]
        if(scores[i] > 0):
            relevantCourses.append(courses[i])
    relevantCourses = insertionInverseSort(relevantCourses)
    return relevantCourses

def getCourses(school):
    with open('course_catalogs/courses_' + school + '.json', 'r') as jsonFile:
        data = json.load(jsonFile)
    return data['courses']

#getRelevantCourses('ucla', 'gang')

def process(text):
    text = text.lower()
    text = text.replace('.', '').replace('  ',' ')
    words = text.split(' ')
    porter = PorterStemmer()
    stems = []
    for word in words:
        stems.append(porter.stem(word))
    return stems

def insertionInverseSort(courses):
    for i in range(1, len(courses)):
        key = courses[i]
        j = i - 1
        while j >= 0 and key['relevancy'] > courses[j]['relevancy']:
            courses[j+1] = courses[j]
            j -= 1
        courses[j+1] = key
    return courses

#out = getRelevantCourses('ucdavis', 'chemical-engineering')

