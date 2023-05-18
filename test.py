from requests import get

print(get('http://localhost:5000/api/task/1').json())