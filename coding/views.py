from django.shortcuts import render
from django.http import HttpResponse
import urllib.request, urllib.parse, urllib.error
import json
import re
import requests
from bs4 import BeautifulSoup

# Create your views here.
def index(request):
 return render(request,'index.html')
def mine(request):
 return render(request,'mine.html')
def progress(request):
 return render(request,'progress.html')
def competitions(request):
 return render(request,'competitions.html')
def submitquery(request):
 q= request.GET['query']
 j=request.GET['Platform']
 if j=='1':
  contest= requests.get('https://codeforces.com/api/user.rating?handle={}'.format(q))
  k=contest.json()
  t=[]
  if k['status']=='OK':
    
    for i in k['result']:
        p=[]
        p.append(i['contestId'])
        p.append(i['rank'])
        p.append(i['newRating'])
        p.append(i['newRating']-i['oldRating'])
        t.append(p)
    context= { "contest":t, "report": True}
    return render(request,'mine.html',context)
  else :
    context= { "contest":t, "report": False}
    return render(request,'mine.html',context) 
 else:
  
  con= requests.get('https://www.codechef.com/users/{}'.format(q))
  k=BeautifulSoup(con.text,'html.parser')
  a=[]
  try:
    p=k.find('div',class_='tabs-content')
    q= p.find_all('section',class_='content')
    for i in q:
     b=[]
     s=i.find('div',class_='contest-name').text
     m=s.split()
     b.append(m[0]+" "+m[1])
     b.append(i.find('strong',class_='global-rank').text)
     s=i.find('a',class_='rating').text
     m=s.split()
     b.append(m[0])
     b.append(m[1])
     a.append(b)
    context= { "contest":a, "report": True}
    return render(request,'mine.html',context)
  except:
    context= { "contest":a, "report": False}
    return render(request,'mine.html',context)

def details(request):
 q= request.GET['query']
 j=request.GET['Platform']
 if j=='2':
  con= requests.get('https://www.codechef.com/users/{}'.format(q))
  k=BeautifulSoup(con.text,'html.parser')
  
  try:
    a=k.find('div',class_="user-details-container plr10")
    p=a.find('h2').text
    c=k.find('span',class_="user-country-name").text
    b=k.find('div',class_="rating-number").text
    l=k.find('div',class_="rating-ranks")
    v=l.find('a').text
    context= { "name":p, "report": True, "Country":c, "rating":b, "rank":v, "user":q}
    return render(request,'progress.html',context)
  except:
    context= { "contest":a, "report": False}
    return render(request,'progress.html',context)
 if j=='1':
  contest= requests.get('https://codeforces.com/api/user.info?handles={}'.format(q))
  k=contest.json()
  
  if k['status']=='OK':
    try:
     for i in k['result']:
        p=i['lastname']
        c=i['country']
        v=['rank']
        b=['rating']
    
    except KeyError:
        p="--"
        c="--"
        v="--"
        b="--"
    context= { "name":p, "report": True, "Country":c, "rating":b, "rank":v, "user":q}    
    return render(request,'progress.html',context)
  else :
    context= {  "report": False}
    return render(request,'progress.html',context) 
 elif j=='3':
  con= requests.get('https://www.hackerearth.com/@{}'.format(q))
  k=BeautifulSoup(con.text,'html.parser')
  
  try:
    p=k.find('h1',class_="name ellipsis larger").text
    r=k.find_all('div',class_="skill-snippet less-margin-2")
    for i in r:
     if i.find('div',class_="skill-type float-left light").text=='Education:':
      c=i.find('span',class_="inline-block less-margin-right").text
      break 
    b=k.find('span',class_="track-following-num").text
    v="--"
    context= { "name":p, "report": True, "Country":c, "rating":b, "rank":v, "user":q}
    return render(request,'progress.html',context)
  except:
    context= {  "report": False}
    return render(request,'progress.html',context)
 
def contest(request):
  con= requests.get('https://clist.by')
  k=BeautifulSoup(con.text,'html.parser')
  a=k.find_all('div',class_="row contest running bg-success")
  c=0
  f=[]
  for i in a:
    b=[]
    b.append(c)
    c+=1
    q=i.find('span',class_="contest_title")
    b.append(q.find_all('a')[1].text)
    q=i.find('div',class_="resource")
    b.append(q.find('a').text)
    q=i.find('div',class_="col-md-4 col-sm-6 timeleft countdown")
    b.append(q.text)
    b.append(i.find('div',class_="col-md-3 col-sm-6 duration").text)
    f.append(b)
    
  contest= requests.get('https://codeforces.com/api/contest.list')
  k=contest.json()
  for i in k['result']:
    b=[]
    c+=1
    b.append(c)
    b.append(i['name'])
    b.append('Codeforces')
    b.append(i['durationSeconds'])
    b.append(i['startTimeSeconds'])
    f.append(b)
    if c>15:
      break
  context= { "list":f, "report": True} 
  return render(request,'competitions.html',context)