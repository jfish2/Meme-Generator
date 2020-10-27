#meme-ifier.py

import requests
import urllib


def login_to_api(filename):
    filer = open("meme-info.txt","r")
    remove_newlines = [line.split("\n") for line in filer.read().splitlines()]
    username = remove_newlines[0][0]
    password = remove_newlines[1][0]
    user_agent = remove_newlines[2][0]
    filer.close()
    return username, password, user_agent



#Fetch available memes via requests.get
def retrieve_memes():
    data = requests.get('https://api.imgflip.com/get_memes').json()['data']['memes']
    images = [{'name':image['name'],'url':image['url'],'id':image['id']} for image in data]

    print('Welcome to the Your Meme Generator! Please choose from this list of available memes!:')
    identifier = 1
    for image in images:
        print(identifier, image['name'])
        identifier += 1

    return images


def create_meme(filename):
    images = retrieve_memes()
    username, password, user_agent = login_to_api(filename)
    serial = int(input('Enter the serial number for the meme you choose to caption: '))
    text1 = input('Enter text for the top box of the meme: ')
    text2 = input('Enter text for the bottom box of the meme: ')
    url = 'https://api.imgflip.com/caption_image'
    template_id = images[serial-1]['id']
    filename = images[serial-1]['name']

    params = {
        'username': username,
        'password':password,
        'template_id': template_id,
        'text1':text1,
        'text2':text2
    }
    response = requests.request('POST', url, params=params).json()


    open_meme = urllib.request.URLopener()
    open_meme.addheader('User-Agent', user_agent)
    save_as, headers = open_meme.retrieve(response['data']['url'], filename + '.jpg' )



create_meme("meme-info.txt")
