from django.shortcuts import render
import json
from json import dumps
import requests
# Create your views here.


def home_view(request):
    return render(request,'home.html')

def problem_opener(request,contestid,index):
    dict = {
        'fname' : str(contestid)+str(index),
        'lang' : 'cpp',
        'src' : '',
        'contestid': contestid,
        'problemid' : index
    } 
    dataJSON = dumps(dict) 
    return render(request,'problem_opener.html',{'data':dataJSON})

def dashboard_view(request,ID):
    response_path1 = requests.post('https://codeforces.com/api/user.rating?handle='+ID)
    result1 = json.loads(response_path1.text)

    if result1['status'] == 'FAILED':
        return render(request,'home.html',{'msg':"Please enter a valid handle"})
    contests = result1['result']
    # contests = contests[::-1][0:5]
    response_path2 = requests.post('https://codeforces.com/api/user.status?handle='+ID)
    result2 = json.loads(response_path2.text)
    data = result2['result']
    rating_problems = {}
    index_problems = {}
    tags = {}
    langs = {}
    for ele in data:
        if ele['verdict'] == 'WRONG_ANSWER':
            try:
                index1 = ele['problem']['index']
                rating1 = ele['problem']['rating']
                this_tags1 = ele['problem']['tags']
            except:
                continue
            
        if ele['verdict'] == 'OK':
            try:
                index = ele['problem']['index']
                rating = ele['problem']['rating']
                this_tags = ele['problem']['tags']
                lang = ele['programmingLanguage']
            except:
                continue
            if  index not in index_problems:
                index_problems[index[0]]=1
            else:
                index_problems[index[0]]+=1
            
            if rating not in rating_problems:
                rating_problems[rating]=1
            else:
                rating_problems[rating]+=1

            for tag in this_tags:
                if tag not in tags:
                    tags[tag]=1
                else:
                    tags[tag]+=1
            
            if lang not in langs:
                langs[lang]=1
            else:
                langs[lang]+=1

    return render(request,'dashboard.html',{'contests':dumps(contests),'rating_problems':dumps(rating_problems),'index_problems':dumps(index_problems),'tags':dumps(tags),'langs':dumps(langs)})