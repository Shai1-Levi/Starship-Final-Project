import requests

   
url = "localhost:4500/vmInstance/"
data = {'img':'nginx',
    'version':'latest','vm_number':'1','vm_name':'test1'}
headers = {'Content-type': 'text/html; charset=UTF-8'}

# Send POST request 
r = requests.post(url, data=data, headers=headers)
