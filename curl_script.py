import datetime
import re
import requests
import urllib3

# Get the current date and time
current_time = datetime.datetime.now()

# Format the date and time as a string
formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")

# Print the formatted date and time
#print("Current date and time:", formatted_time)
print(formatted_time)


requests.packages.urllib3.disable_warnings()
requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += 'HIGH:!DH:!aNULL'
try:
    requests.packages.urllib3.contrib.pyopenssl.DEFAULT_SSL_CIPHER_LIST += 'HIGH:!DH:!aNULL'
except AttributeError:
    # no pyopenssl support used / needed / available
    pass



# Create a session object
session = requests.Session()

# headers =  {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/109.0', 
#         'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
#         'Accept-Language': 'en-US,en;q=0.5',
#         'Connection': 'keep-alive',
#         'Upgrade-Insecure-Requests': '1',
#         'Cache-Control': 'max-age=0'} 



# 1
url = "https://ssologin.seagate.com/oam/server/authentication"
# headers = {
#     'referer': 'https://www.seagate.com/as/en/partners/'
# }
data = {
    "locale": "en_US",
    "username": "ipp_sfdc_monitoring@seagate.com",
    "password": "S3@g@teM0n1t0r",
    "successurl": "https://www.lacie.com/ww/secure/partner-redirect?newPage=true&",
    "failureurl": "/customLogin/pages/login_spp.jsp",
    "smauthreason": "0",
    "smagentname": "",
    "postpreservationdata": ""
}
if data:
    response = session.post(url, data=data, verify=False)
else: 
    response = session.get(url, verify=False)

if response.status_code == 200:
    #print(response.content.decode("utf-8"))

    var_url = re.search("var url = '(.*?)'", response.content.decode("utf-8")).group(1)

    # required_string = re.search('(Single Sign-Off)', response.content.decode("utf-8")).group(1)
    # print(required_string)
else:
    print("Request failed with status code: ", response.status_code)


# 2
url = "https://program.seagate.com" + var_url
# headers = {
#     'referer': 'https://program.seagate.com/s/?'
# }
data = {}
if data:
    response = session.post(url, data=data, verify=False)
else: 
    response = session.get(url, verify=False)

if response.status_code == 200:
    #print(response.content.decode("utf-8"))

    var_action = re.search('action="(.*?)"', response.content.decode("utf-8")).group(1)

    var_RelayState = re.search('name="RelayState".*?value="(.*?)"', response.content.decode("utf-8")).group(1)

    var_SAMLRequest = re.search('name="SAMLRequest".*?value="(.*?)"', response.content.decode("utf-8")).group(1)

    required_string = re.search('(Since your browser does not support JavaScript,)', response.content.decode("utf-8")).group(1)
    print(required_string)
else:
    print("Request failed with status code: ", response.status_code)

# 3
url = "https://ssologin.seagate.com/oamfed/idp/samlv20"
# headers = {
#     'referer': 'https://program.seagate.com/'
# }
data = {
    "RelayState": "/s/",
    "SAMLRequest": var_SAMLRequest
}
if data:
    response = session.post(url, data=data, verify=False)
else: 
    response = session.get(url, verify=False)

if response.status_code == 200:
    #print(response.content.decode("utf-8"))

    var_ACTION = re.search('ACTION="(.*?)"', response.content.decode("utf-8")).group(1)

    var_RelayState = re.search('NAME="RelayState".*?VALUE="(.*?)"', response.content.decode("utf-8")).group(1)

    var_SAMLResponse = re.search('NAME="SAMLResponse".*?VALUE="([\s\S]*?)"', response.content.decode("utf-8")).group(1)

    # required_string = re.search('(Single Sign-Off)', response.content.decode("utf-8")).group(1)
    # print(required_string)
else:
    print("Request failed with status code: ", response.status_code)


#4
url = var_ACTION
data = {
    "RelayState": var_RelayState,
    "SAMLResponse": var_SAMLResponse
}
if data:
    response = session.post(url, data=data, verify=False)
else: 
    response = session.get(url, verify=False)

if response.status_code == 200:
    #print(response.content.decode("utf-8"))

    required_string = re.search('(You do not have Javascript enabled.)', response.content.decode("utf-8")).group(1)
    print(required_string)
else:
    print("Request failed with status code: ", response.status_code)

#5
url = "https://program.seagate.com/secur/logout.jsp"
data={}
if data:
    response = session.post(url, data=data, verify=False)
else: 
    response = session.get(url, verify=False)

if response.status_code == 200:
    #print(response.content.decode("utf-8"))
    pass
else:
    print("Request failed with status code: ", response.status_code)

#6
url = "https://ssologin.seagate.com/oam/server/logout?end_url=/customLogin/pages/logout_ext.jsp"
data={}
if data:
    response = session.post(url, data=data, verify=False)
else: 
    response = session.get(url, verify=False)

if response.status_code == 200:
    #print(response.content.decode("utf-8"))

    required_string = re.search('(Single Sign-Off)', response.content.decode("utf-8")).group(1)
    print(required_string)
else:
    print("Request failed with status code: ", response.status_code)

#7
url = "https://ssologin.seagate.com/oamfed/user/spslooam11g?doneURL=https%3A%2F%2Fssologin.seagate.com%3A443%2FcustomLogin%2Fpages%2Flogout_ext.jsp"
data={}
if data:
    response = session.post(url, data=data, verify=False)
else: 
    response = session.get(url, verify=False)

if response.status_code == 200:
    #print(response.content.decode("utf-8"))

    required_string = re.search('(Seagate Login)', response.content.decode("utf-8")).group(1)
    print(required_string)
else:
    print("Request failed with status code: ", response.status_code)