from urllib.parse import urlencode
import requests
from pprint import pprint

app_id = 6652248
auth_url = 'https://oauth.vk.com/authorize'
auth_data = {
    'client_id':app_id,
    'redirect_uri': 'https://oauth.vk.com/blank.html',
    'scope': 'friends',
    'display': 'page',
    'response_type': 'token',
    'v': 5.80
}
# access_token = 'd6e5eb4ff52ac19df4a55c314f3bfae227d12ed5636e4fff20f97f374627d822c9ffe66ea0a51ec402a59'
access_token = '3a12ff211ab8b2b8eb98a14700f4db7ee9cde3d6af528ee32a7b147ce14eb825cc95330d09ea96b935e73'
# print('?'.join((auth_url, urlencode(auth_data))))

def get_user_info(id):
    response = requests.get('https://api.vk.com/method/users.get',
                            params=dict(
                                user_ids=id,
                                access_token=access_token,
                                v=5.80
                            ))
    return response.json()

class User():
    def __init__(self, id, first_name, last_name, token):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.token = token
        self.url = 'vk.com/id{}'.format(id)

    def __repr__(self):
        return self.url

    def __and__(self, other):
        response = requests.get('https://api.vk.com/method/friends.getMutual',
                                    params=dict(
                                    source_uid=self.id,
                                    target_uids=other,
                                    access_token=self.token,
                                    v=5.80
                                ))
        our_friends = list()
        friends = response.json()['response']
        for result in friends:
            if 'common_friends' in result:
                for i in result['common_friends']:
                    user_info = get_user_info(i)
                    new_class = User(
                        id=user_info['response'][0]['id'],
                        first_name=user_info['response'][0]['first_name'],
                        last_name=user_info['response'][0]['last_name'],
                        token=access_token
                    )
                    our_friends.append(new_class)
        return our_friends


    def get_friends(self):
        response = requests.get('https://api.vk.com/method/friends.get',
                                    params=dict(
                                    access_token=self.token,
                                    v=5.80
                                ))
        return response

    def friends_mutual(self, source_uid, target_uid):
        response = requests.get('https://api.vk.com/method/friends.getMutual',
                                    params=dict(
                                    source_uid=source_uid,
                                    target_uids=target_uid,
                                    access_token=self.token,
                                    v=5.80
                                ))
        return response

response = requests.get('https://api.vk.com/method/users.get',
                                params=dict(
                                access_token=access_token,
                                v=5.80
                                ))

my_user = User(
    id=response.json()['response'][0]['id'],
    first_name=response.json()['response'][0]['first_name'],
    last_name=response.json()['response'][0]['last_name'],
    token=access_token
)

my_friends = []
if 'items' in my_user.get_friends().json()['response']:
    my_friends = my_user.get_friends().json()['response']['items']

pprint(my_user & my_friends)

