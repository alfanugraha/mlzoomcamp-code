import requests

#url = 'http://localhost:8080/2015-03-31/functions/function/invocations'

# url = 'http://localhost:9696/predict'

# url = 'http://localhost:8080/predict'

url = 'http://a4728612c114a46e2b1bdec34034a999-630464919.us-east-1.elb.amazonaws.com/predict'

data = { 'url': 'http://bit.ly/mlbookcamp-pants' }

result = requests.post(url, json=data).json()
print(result)
