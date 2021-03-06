# -*- coding: utf-8 -*-
import os
from time import sleep
import datetime
import re
import random
import json

import requests
from pprint import pprint
import vk_tokens as vk

# определение путей в зависимости от расположения скрипта

where_i = os.popen('hostname').read()
where_i.encode('utf-8')

print(where_i)


if 'hostland' in where_i:
    
    # путь к рабочей папке на хостинге
    path_folder = '/home/host1336571/parser-yo.ga/htdocs/www/yoga/bot/bday_vk/'

else:

    # путь к рабочей папке на локалке
    path_folder = '/home/mint/projects/birthday_members_vk/'
    
print(path_folder)


# импорт токенов vk
token = vk.token
g_id = vk.g_id
g_id_post = vk.g_id_post
V = vk.V

# функция удаляет последний пост с поздравлением
def del_last_post(): 
    post_id = json.load(open(path_folder + 'last_post_id.json'))
    print(post_id)
    #post_id = json.load(open('last_post_id.json'))
    r = requests.get('https://api.vk.com/method/wall.delete',
                                    params={'access_token': token,
                                    'v': V,
                                    'owner_id': g_id_post,
                                    'post_id': post_id,})

    data = r.json()
    print('удаление', data)
    get_members()

 # получаем список всех участников группы
def get_members():
    offset = 0
    all_users = []
    while True:
        # спим между запросами, чтобы vk не забанил
        sleep(1)
        r = requests.get('https://api.vk.com/method/groups.getMembers',
                                    params={'access_token': token,
                                    'v': V,
                                    'group_id': g_id,
                                    'offset': offset,
                                    'fields': 'bdate',
                                    'count': 1000})
        data = r.json()
        count_users = data['response']['count']
        users = data['response']['items']
        all_users.extend(users)
        offset += 1000
        count_all_users = len(all_users)
        print('Собрано', count_all_users)

        # проверка на остутствие дублей
        if count_all_users >= count_users:
            perebor = count_all_users - count_users
            print('перебор:', perebor)
            search_bday(all_users)
            break

 # ищем именинников среди участников сообщества
def search_bday(all_users):

    users_bday = []

    # узнаём текущую дату
    current_datetime = datetime.datetime.now()
    day_today = current_datetime.day
    month_today = str(current_datetime.month)

    # формируем строку для поиска именинников из даты
    str_date = fr"('{day_today}.{month_today})"

    for u in all_users:
        u_values = str(u.values())
        result = re.search(str_date, u_values) # ищем
        if result != None:
            users_bday.append(u.values())
    pprint(users_bday)
    count_bday = len(users_bday)
    print('Найдено', count_bday, 'именинников')
    create_message(users_bday, count_bday) # если именинники есть запускаем создание сообщения


# функция создания рандомных поздравлений 
def create_message(users_bday, count_bday):
    list_bday = []
    n = 0
    for u in users_bday:
        user_bday = users_bday[n]
        n += 1
        user_bday = list(u)

        bday_in_list = f'''@id{user_bday[1]} ({user_bday[0]} {user_bday[2]})'''
        list_bday.append(bday_in_list)
        if n == count_bday:
            break
    vstuplenie = ['💥 Поздравляем наших подписчиков с днём рождения! 💥', '🔥 Сегодня среди наших подписчиков, есть именниники 🔥',
 'Спешим поздравить именинников нашего сообщества 💎', '💎 В этот замечательный день, хотим поздравить Вас, наших подписчиков 💎',
 'А Вы знали какой сегодня день? Сегодня день рождения наших подписчиков! 🔥',
 '💥 Сегодня будем потчивать именинников нашего сообщества 💥', 'Сегодня чествуем именинников нашей группы 💎', '🎁 И снова радость и подарки посетят дома наших подписчиков у которых сегодня день рождения 🎁']
    vstuplenie = random.choice(vstuplenie)

    procvetanie = ['процветания', 'научиться чему-то новому', 'быть востребованными по специальности', 'повысить профессиональную квалификацию']
    procvetanie = random.choice(procvetanie)
    cash = ['богатства', 'дорогую машину', 'прибавки жилой площади', 'свой самолёт', 'свою яхту', 'свой вертолёт', 'дом на Мальдивах']
    cash = random.choice(cash)
    love = ['много счастья 💖', 'много любви ❤', 'чтобы все ваши близкие были здоровы 🤸', 'никогда не грустить ☀', 'много добра 😀']
    love = random.choice(love)
    triger = ['Пусть Ваш день будет наполнен радостью 😀', 'Хорошего дня. Корпоративные подарки это к нам 😀',
    'А при заказе у нас подарка для именинника, сделаем скидку 15%!', 'Дарим именинникам скидку 10% на всё в течении 3 дней!', 'Сегодня включаем секретную скидку 10% по кодовой фразе Я К ВАМ СО ДНЯ РОЖДЕНИЯ. Напишите в наш чат.']
    triger = random.choice(triger)
    text = f'''{vstuplenie}
 {(', '.join(list_bday))}.
  Желаем Вам {procvetanie}, {cash} и {love}

  {triger}'''
    print(text)
    send_post(list_bday, text)


# функция отправки поста в ленту сообщества vk
def send_post(list_bday, text):
    
    r = requests.get('https://api.vk.com/method/photos.getWallUploadServer',
                 params={'access_token': token, 'v': V, 'group_id': g_id})
    data = r.json()
    
    
    random_img = [path_folder + 'bday_image/image2.jpg', path_folder + 'bday_image/image3.jpg', path_folder + 'bday_image/image4.jpg',
                  path_folder + 'bday_image/image0.jpg', path_folder + 'bday_image/image1.jpg']
    random_img = random.choice(random_img)
    
    server = requests.post(data['response']['upload_url'], files={'photo': open(random_img, "rb")})
    ser = server.json()
    
    
    load = requests.get('https://api.vk.com/method/photos.saveWallPhoto',
                        params={'access_token': token,
                                'v': V,
                                'group_id': g_id,
                                'server': ser['server'],
                                'photo': ser['photo'],
                                'hash': ser['hash']})
    
    save = load.json()
    
    # формирование имени фото
    photo_id = (f'''photo{save['response'][0]['owner_id']}_{save['response'][0]['id']}''')

    
    # вывод в консоль всего, что отправляется для отладки
    #print(f'''url error: https://api.vk.com/method/wall.post + токен: {token} + версия api: {V} + id группы: {g_id_post} + текст: {text} + id фото: {photo_id}''')
    
    
    # отправка поста
    post = requests.post('https://api.vk.com/method/wall.post',
                        params={'access_token': token, 'v': V, 'from_group': 1, 'owner_id': g_id_post, 'message': text,
                                'attachments': photo_id})
    
    post_id = post.json()
    print(post.content)
    
    save_post_id(post_id)

def save_post_id(post_id):
    print('пост айди', post_id)
    post_id = post_id['response']['post_id']

    with open(path_folder + 'last_post_id.json', 'w') as f:
    #with open('last_post_id.json', 'w') as f:
        json.dump(post_id, f, indent=2)
        pass


del_last_post()