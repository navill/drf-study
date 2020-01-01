import json
import os

import requests

image_path = os.path.join(os.getcwd(), "python.png")
AUTH_ENDPOINT = 'http://127.0.0.1:8000/api/auth/'
# REFRESH_ENDPOINT = AUTH_ENDPOINT + 'refresh/'
headers = {
    'Content-Type': 'application/json',
}
data = {
    'username': 'jh',
    'password': '123',
}

r = requests.post(AUTH_ENDPOINT, data=json.dumps(data), headers=headers)
token = r.json()['token']
print(token)

ENDPOINT = 'http://127.0.0.1:8000/api/status/24/'
headers2 = {
    # 'Content-Type': 'application/json',
    'Authorization': 'JWT ' + token,
}
data2 = {
    'content': 'this new content post'
}
with open(image_path, 'rb') as image:
    file_data = {
        'image': image
    }
    r = requests.put(ENDPOINT, data=data2, headers=headers2, files=file_data)
    print(r.text)

# ENDPOINT = 'http://127.0.0.1:8000/api/status/'
# image_path = os.path.join(os.getcwd(), "python.png")
# AUTH_ENDPOINT = 'http://127.0.0.1:8000/api/auth/register/'
# # REFRESH_ENDPOINT = AUTH_ENDPOINT + 'refresh/'
# headers = {
#     'Content-Type': 'application/json',
#     'Authorization': 'JWT ' + 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxOSwidXNlcm5hbWUiOiJjZmUxOCIsImV4cCI6MTU3Nzc0OTgwNCwiZW1haWwiOiJjZmUxOEBjZmUuY29tIiwib3JpZ19pYXQiOjE1Nzc3NDk1MDR9.kGQKANx5vK2EPJRi1EW0hyAVTGR6qfdh9XdWvHbJiIs',
# }
# data = {
#     'username': 'cfe19',
#     'email': 'cfe19@cfe.com',
#     'password': '123',
#     'password2': '123'
# }
#
# r = requests.post(AUTH_ENDPOINT, data=json.dumps(data), headers=headers)
# token = r.json()  # ['token']
# print(token)

#
# refresh_data = {
#     'token': token
# }
# new_response = requests.post(REFRESH_ENDPOINT, data=json.dumps(refresh_data), headers=headers)
# new_token = new_response.json()
# print(new_token)

# # image update(put)
# headers = {
#     # 파일 업로드 시 Content-Type 생략
#     # 'Content-Type': 'application/json',
#     'Authorization': 'JWT ' + token,
# }
# with open(image_path, 'rb') as image:
#     file_data = {
#         'image': image
#     }
#     data = {
#         'content': 'update contents'
#     }
#     # json_data = json.dumps(data)
#     posted_response = requests.put(ENDPOINT + str(32) + '/', data=data, headers=headers, files=file_data)
#     print(posted_response.text)
#
# # content update(put)
# headers = {
#     'Content-Type': 'application/json',
#     'Authorization': 'JWT ' + token,
# }
# data = {
#     'content': 'update contents'
# }
# json_data = json.dumps(data)
# posted_response = requests.put(ENDPOINT + str(32) + '/', data=json_data, headers=headers)
# print(posted_response.text)

# r = requests.get(get_endpoint)
# print(r.text)
#
# r2 = requests.get(get_endpoint)
# print(r2.text)
#
# # authentication credentials were not provided
# # -> post 접근
# post_header = {
#     'content-type': 'application/json'
# }
# post_response = requests.post(ENDPOINT, data=post_data, headers=post_header)
# print(post_response.text)


# def do_img(method='get', data={}, is_json=True, img_path=None):
#     headers = {}
#     if is_json:
#         headers['content-type'] = 'application/json'
#         data = json.dumps(data)
#     if img_path is not None:
#         with open(image_path, 'rb') as image:
#             file_data = {
#                 'image': image
#             }
#             r = requests.request(method, ENDPOINT, data=data, files=file_data, headers=headers)
#     else:
#         r = requests.request(method, ENDPOINT, data=data, headers=headers)
#     print(r.text)
#     print(r.status_code)
#     return r
#
#
# # do_img(method='post', data={'user': 1, 'content': ''}, is_json=False, img_path=image_path)
# do_img(method='put', data={'id': 12, 'user': 1, 'content': 'some new content'}, is_json=False, img_path=image_path)
#
#
# def do(method='get', data={}, is_json=True):
#     headers = {}
#     if is_json:
#         headers['content-type'] = 'application/json'
#         data = json.dumps(data)
#     r = requests.request(method, ENDPOINT, data=data, headers=headers)
#     print(r.text)
#     print(r.status_code)
#     return r

# do(data={'id': 5})
# do(method='delete', data={'id': 100})
# do(method='put', data={'id': 5, 'content': 'id number 10', 'user': 2})
# do(method='post', data={'content': 'some cool new content', 'user': 2})
# do(method='delete', data={'id': 9})
