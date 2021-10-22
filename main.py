import json
 
# Opening JSON file
f = open('input.json',)
 
# returns JSON object as
# a dictionary
data = json.load(f)
 
# Iterating through the json
# list
# print (data[0])
for i in data:
	if i['type'] == 'customer':
		print(i['events'])
 
# Closing file
f.close()
