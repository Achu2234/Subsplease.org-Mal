from bs4 import BeautifulSoup
import requests
import re

def subsplease(text):
    templateURL = 'https://subsplease.org/rss/?r=``replaceme``'
    query = (requests.utils.quote(text))
    URL = templateURL.replace("``replaceme``",query)
    page = requests.get(URL)
    soup = BeautifulSoup(page.content,'html.parser')
    div = soup.findAll("tr",{"class":"success"})
    results=[]
    for i in div:
        temp=i.findAll("a")
        for j in temp:
            check=j.text.strip()
            if check!='' and check!=None:
                results.append(check)
    subbers=[]
    for i in results:
        try:
            result = re.search(r"\[([A-Za-z0-9@#$%^&+=!-_]+)\]", i)
            if result.group(1)not in subbers and result.group(1)!='720p' and result.group(1)!='1080p' and result.group(1)!='SD':
                subbers.append(result.group(1))
        except:
            continue
    print("Available Subbers: ")
    for i in range(len(subbers)):
        print(str(i+1)+") "+subbers[i])
    ch = int(input("Please Select one: "))
    if (ch-1)>=len(subbers) or (ch-1)<0:
        print("Invalid choice. Please try again.")
    else:
        print("Sub group chosen - "+str(subbers[ch-1]))
        txt = str(subbers[ch-1])+" "+text
        return rss(txt)

def rss(final):
    tempURL="https://subsplease.org/rss/?r=1080p+``replaceme``&c=0_0&f=0"
    query = (requests.utils.quote(final))
    return tempURL.replace("``replaceme``",query)

file = open("links.txt","w+")
URL = "https://myanimelist.net/anime/season"

page = requests.get(URL)

soup = BeautifulSoup(page.content,'html.parser')

#print(soup.prettify())


ids=[]
names=[]
links=[]


mydivs = soup.findAll("div",{"class" : "seasonal-anime js-seasonal-anime"})
for i in mydivs:
    main = (i.findAll("h2",{"class" : "h2_anime_title"}))
    #print(main)
    for j in main:
        temp = (j.find("a",{"class" : "link-title"}))
        names.append(temp.text.strip())
        l=(temp['href'])
        links.append(l)
        l=l.split("/")
        ids.append(l[l.index("anime")+1])
        
        
for i in range(len(names)):
    if "(TV)" in names[i]:
        a = names[i].replace(" (TV)","")
        names[i]=a
        
        
#print(names)
#print(ids)
#print(links)
'''
print("Anime Airing this season: ")
for i in names:
    print(i)
'''

#END OF MYANIMELIST PART

#USER SELECTION
selections=[]
menu = 'y'
while menu=='y':
    print("Hello Weebs")
    print("TOP 10 Anime Airing this season: ")
    for i in range(10):
        print(str(i+1)+") "+names[i])

    a = input("Select an anime from above or 'n' to exit: ")
    if a=='n':
        menu=='n'
        if len(selections)==0:
            continue
        else:
            for i in selections:
                file.write(i)
                file.write("\n")
        print("A txt file has been generated with the RSS Links! Have Fun!")
        file.close()
        print("BYE heee")
        xx = input("Press Enter to close app.")
        break
    else:
        a = int(a)
        if a>10 and a<=0:
            print("Invalid choice. Try again")
        else:
            a=a-1
            print("Anime Chosen - " + str(names[a]))
            print("Gathering info from nyaa.si ...")
            q = nyaa(names[a])
            if q!=None:
                selections.append(q)
                print("Successfully Gathered RSS!")
