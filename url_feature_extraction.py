
#importing necessary liabraries to extract lexical features of a URL
import numpy as np
from urllib.parse import urlparse,urlencode
import ipaddress
import re
import socket


featuresLst = []
validResponse = True
lengthURL = 0
tableDict = dict()
dmn = None
"""###  Lexical Features """

# Getting the length of URL
def getURLLength(url):
  global lengthURL
  lengthURL = len(url)
  if(len(url)>55):
    return 0
  return 1


# Getting the count of dots(.)
def countDots(url):
  if(url.count('.')>3):
    return 0
  return 1


# Checking presence of '@' symbol in the URL
def checkAtSymbol(url):
  if('@' in url):
    return 0
  return 1


# Checking the presence of redirection symbol '//' in the URL
def locRedirection(url):
  last_loc = url.rfind('//')
  if(last_loc > 6):
    return 0
  return 1


# Checking the presence of "www" in the domain part 
def wwwInDomain(url):
  loc_www = url.rfind("www.")
  if(url.startswith('http')):
    if(loc_www > 8):
      return 0
  else:
    if(loc_www > 1):
      return 0      
  return 1


# Checking if the URL contains IP Address 
def containsIP(url):
    isPresent = re.search('\.*\d+\.\d+\.\d+\.\d+\.*', url)
    if(isPresent):
        return 0
    return 1


# Counting the no. of Unique Character in URL 
def countUniqueChar(url):    
    return(len(set(url)))


# Counting the no. of digits in URL 
def countDigits(url):
    nod = sum(map(str.isdigit, url))
    return nod

# Checking the presence of "#" in URL
def containsHash(url):
    if("#" in url):
        return 0
    return 1


# Checking the presence of "\" in URL
def containsBS(url):
    if("\n" in url):        
        return 0
    return 1


# Checking the presence of some sensitive words in URL 
def containsSW(url):
    sensitive_words = ['secure', 'account', 'update', 'login', 'sign-in', 'signin', 'banking', 'confirm', 'verify',
                       'password', 'click', 'notify', '.exe', '.tar', 'webscr','ebayisapi']
    if any(word in url for word in sensitive_words):
        return 0
    return 1


# Checking the presence of "-" in URL
def containsHyphen(url):
    init_pos = 0
    if("/" in url):
      end_pos = url.index("/")
    else:
      end_pos = 0
    if("-" in url[init_pos : end_pos+1]):
        return 0
    else:
        return 1


# Checking if the URL uses link shortening services 
shortening_services = r"bit\.ly|goo\.gl|shorte\.st|go2l\.ink|x\.co|ow\.ly|t\.co|tinyurl|tr\.im|is\.gd|cli\.gs|" \
                      r"yfrog\.com|migre\.me|ff\.im|tiny\.cc|url4\.eu|twit\.ac|su\.pr|twurl\.nl|snipurl\.com|" \
                      r"short\.to|BudURL\.com|ping\.fm|post\.ly|Just\.as|bkite\.com|snipr\.com|fic\.kr|loopt\.us|" \
                      r"doiop\.com|short\.ie|kl\.am|wp\.me|rubyurl\.com|om\.ly|to\.ly|bit\.do|t\.co|lnkd\.in|db\.tt|" \
                      r"qr\.ae|adf\.ly|goo\.gl|bitly\.com|cur\.lv|tinyurl\.com|ow\.ly|bit\.ly|ity\.im|q\.gs|is\.gd|" \
                      r"po\.st|bc\.vc|twitthis\.com|u\.to|j\.mp|buzurl\.com|cutt\.us|u\.bb|yourls\.org|x\.co|" \
                      r"prettylinkpro\.com|scrnch\.me|filoops\.info|vzturl\.com|qr\.net|1url\.com|tweez\.me|v\.gd|" \
                      r"tr\.im|link\.zip\.net"

def checkShortURL(url):
    match = re.search(shortening_services, url)
    if(match):
      return 0
    else:
      return 1

"""### Host-based Features : """
# importing the required packages for extracting host-basedfeatures of URLs

import re
from datetime import datetime
import whois
from urllib.parse import urlparse
import urllib.request
from bs4 import BeautifulSoup
import requests
from googlesearch import search


# Finding web traffic on the website 
def findWebTraffic(url):
  try:
    url = urllib.parse.quote(url)
    rank = BeautifulSoup(urllib.request.urlopen("http://data.alexa.com/data?cli=10&dat=s&url=" + url).read(), "xml").find("REACH")['RANK']
    rank = int(rank)
    if (rank<100000):
      return 1
    else:
      return 0
  except:
    return 0


# Finding age of the website 
def findAge(domain):
  if(domain ==""):    
    return(0, None, None)
    
  creation_date = domain.creation_date
  expiration_date = domain.expiration_date

  if (isinstance(creation_date,str) or isinstance(expiration_date,str)):
    try:
      creation_date = datetime.strptime(creation_date,'%Y-%m-%d')
      expiration_date = datetime.strptime(expiration_date,"%Y-%m-%d")
    except:
      return (0, None, None)
  elif ((expiration_date is None) or (creation_date is None)):
      return (0, None, None)
  elif((type(expiration_date) is list) or (type(creation_date) is list)):
    try:      
      creation_date = creation_date[0].date()
      expiration_date = expiration_date[0].date()
    except:        
      return(0, None, None)
       
  lifetime = abs((expiration_date - creation_date).days)

  if ((lifetime//30) < 12):
    lt = 0
  else:
    lt = 1
  return (lt, creation_date, expiration_date)

# 16. Finding DNS record of the URL 
def domainInfo(url):
  global dmn
  """This function returns all the host-based information in form of tupple containing 0/1"""
  foundDNS = 1
  domain = ""
  dmn = None
  if not( (url.startswith('//') or url.startswith('http://') or url.startswith('https://'))):
    url = 'http://www.' + url
  try:
    # dmn = urlparse(url).netloc
    domain = whois.whois(url)
    if(type(domain.domain_name) is list):
      dmn = domain.domain_name[0]
    elif(type(domain.domain_name) is str):
      dmn = domain.domain_name
    elif(domain.domain_name is None):
      dmn = None

    # dmn = domain.domain_name
    
  except:
    dmn = None
    foundDNS = 0
  
  webTraffic = findWebTraffic(url)
  (lifetime, cred, expd) = ((0, None, None) if foundDNS == 0 else findAge(domain))  
  
  return(foundDNS, webTraffic, lifetime, cred, expd, dmn)



"""### HTML and JavaScript based Features : """

# Finding the presence of IFrame element 
def iframe(response):
  if response == "":
      return 0
  else:
      if re.findall(r"[<iframe>|<frameBorder>]", response.text):
          return 1
      else:
          return 0


# Website redirecting count 
def websiteRedirect(response):
  if response == "":
    return 0
  else:
    if len(response.history) <= 2:
      return 1    
    else:
      return 0


# Status Bar Customization 


def mouseOver(response): 
  if response == "" :
    return 0
  else:
    if re.findall("<script>.+onmouseover.+</script>", response.text):
      return 0
    else:
      return 1

#this function will be used to get the response from the URL suing requests,
#so that it can be passed to above functions
def getResponse(url):
  if (not (url.startswith('http'))):
    url = 'http://www.' + url
  try:
    tableDict['validURL'] = True
    response = requests.get(url, timeout = 5)
    return response
  except requests.ConnectionError as exception:    
    tableDict['validURL'] = False
    response = ""
    return response
  except:
    tableDict['validURL'] = False
    response = ""
    return response



"""### Combining URL features 
In this section, we wil use the above defined features to create a list of features for each URL.
"""

def combineFeatures(url):
  global dmn
  features = []
  # #appending URL
  tableDict['url'] = url
  # #lexical features
  features.append(getURLLength(url))
  features.append(countDots(url))
  features.append(checkAtSymbol(url))
  features.append(locRedirection(url))
  features.append(wwwInDomain(url))  
  features.append(containsIP(url))
  features.append(countUniqueChar(url))
  features.append(countDigits(url))
  features.append(containsHash(url))
  features.append(containsBS(url))  
  features.append(containsSW(url))
  features.append(containsHyphen(url))
  features.append(checkShortURL(url))  

  #host-based features
  (foundDNS, webTraffic, lifetime, cred, expd, dmn) = domainInfo(url)
  features.append(foundDNS)
  features.append(webTraffic)  
  features.append(lifetime)  

  #html and java-script based features
  response = getResponse(url)
  features.append(websiteRedirect(response))
  features.append(iframe(response))
  features.append(mouseOver(response))

  tableDict['creation_date'] = cred
  tableDict['expiration_date'] = expd
  tableDict['domain'] = dmn
  tableDict['length'] = lengthURL
  # tableDict['validURL'] = validResponse
  
  try:
    ipad = socket.gethostbyname(dmn)
  except:
    ipad = None
  tableDict['ipadd'] = ipad
  return(features, tableDict)

# url = "newenglandvan.com/wp-admin/c400/verify/index.html"
# feats, td = combineFeatures(url)
# print(td)
# print(feats)