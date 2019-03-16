import getpass
import requests
import vk

# чтобы получить app_id,
# нужно зарегистрировать своё приложение на https://vk.com/dev

APP_ID = 6900175


def get_user_login():
    user_login = input('Input User login:')
    return user_login


def get_user_password():
    password = getpass.getpass('Input User password:')
    return password


def get_online_friends(login, password):
    if not all([login, password]):
        return None

    try:
        session = vk.AuthSession(
            app_id=APP_ID,
            user_login=login,
            user_password=password,
            scope='friends, users'
        )
        api = vk.API(session)
    except (
            requests.exceptions.ConnectionError,
            requests.exceptions.ConnectTimeout,
            vk.exceptions.VkAuthError
    ):
        return None

    friends_online_ids = api.friends.getOnline(v=5.92)
    friends_online_list = [
        api.users.get(user_ids=user_id, v=5.89)
        for user_id in friends_online_ids
    ]

    return friends_online_list


def output_friends_to_console(friends_online):
    print('\nFriends online:')

    if not friends_online:
        exit('No friends online'
             '\n\nPossible reasons:'
             '\n\t- all friends offline'
             '\n\t- login and password are incorrect or empty'
             '\n\t- Internet connection error'
             )

    fields = ['first_name', 'last_name', ]

    for friend in friends_online:
        print(*[friend[0].get(field) for field in fields])


if __name__ == '__main__':
    login = get_user_login()
    password = get_user_password()
    friends_online = get_online_friends(login, password)
    output_friends_to_console(friends_online)
