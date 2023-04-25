import json

import vk_api

LOGIN = '79775446373'
PASSWORD = 'antirockwho'


def auth_handler():
    """ При двухфакторной аутентификации вызывается эта функция. """

    # Код двухфакторной аутентификации,
    # который присылается по смс или уведомлением в мобильное приложение
    with open('codes.json', mode='r') as file:
        res = json.loads(file.read())
    key = res[0]
    res.pop(0)
    with open('codes.json', mode='w') as file:
        json.dump(res, file)
    # Если: True - сохранить, False - не сохранять.
    remember_device = True

    return key, remember_device


def upload_photo(vk: vk_api.vk_api.VkApiMethod):
    up = vk_api.VkUpload(vk)
    up.photo(photos=[f'static/img/{i}.jpeg' for i in range(1, 4)], album_id=291455597,
             group_id=220062557)


def main():
    login, password = LOGIN, PASSWORD
    vk_session = vk_api.VkApi(
        login, password,
        # функция для обработки двухфакторной аутентификации
        auth_handler=auth_handler
    )

    try:
        vk_session.auth(token_only=True)
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return

    vk = vk_session.get_api()
    response = vk.photos.get(album_id=202082471, group_id=29166271)
    if response['items']:
        cnt = 1
        for i in response['items']:
            print(f"{cnt}.")
            d = i['sizes'][-1]
            print(f"Height: {d['height']}, Width: {d['width']}\nURL: {d['url']}")
            print()
            cnt += 1


if __name__ == '__main__':
    main()
