import requests

base_url = 'http://httpbin.org'
resp = requests.get(base_url + '/cookies',cookies={
		'k1':'v1',
		'k2':'v2'
	})
print(resp.text)
