import requests
import json
from pprint import pprint

my_key = 'lS0mFdGz0h6K8qPVK77kOM2atN4vQppp'

payload = {

}

q = 'spider-man'

limit = 2

endpoint = "https://api.giphy.com/v1/gifs/search?api_key=lS0mFdGz0h6K8qPVK77kOM2atN4vQppp&q=" + str(q) + "&limit=" + str(limit) + "&offset=0&rating=G&lang=en"

response = requests.get(endpoint)

# HANDLE EXCEPTIONS (WHICH OCCUR IF THERE IS NO RESPONSE TO A KEYWORD)
data = response.json()
#pprint(data)

#with open("response.txt", "w") as file:
	#file.write(json.dumps(data))

	

#for i in range(0, limit, 1):
# Get the url of the original gif
	print(data["data"][i]["images"]["original"]["url"])
	
#print("Done")