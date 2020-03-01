#from test import check_info
import requests
import time

def get_check(name, description, money):

	url = "https://demo.checkbook.io/v3/check/digital"

	name = str(name.rstrip())
	description = str(description.rstrip())

	payload = "{\"recipient\":\"testing@checkbook.io\",\"name\": \""+ name +"\",\"amount\":"+str(money)+",\"description\":\""+ description +"\"}"
	headers = {
		'accept': "application/json",
		'content-type': "application/json",
		'authorization': "d6aa2703655f4ba2af2a56202961ca86:dXbCgzYBMibj8ZwuQMd2NXr6rtvjZ8"
		}

	response = requests.request("POST", url, data=payload, headers=headers).json()

	#print(response.text)
	url = response['image_uri']
	#print(image_link)

	time.sleep(4)
	#url = 'https://checkbook-checks-dev.s3.amazonaws.com/53040bc3-26ee-48ac-8e4b-87ad4c3649a1.png'
	filename = url.split('/')[-1]
	filename = "filled_check.png"
	r = requests.get(url, allow_redirects=True)
	open(filename, 'wb').write(r.content)
