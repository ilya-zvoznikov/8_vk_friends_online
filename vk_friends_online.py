import getpass
import requests
import vk

APP_ID = 6900175
api_version = 5.9


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
            scope='friends'
        )
        api = vk.API(session, v=api_version)
    except (
            requests.exceptions.ConnectionError,
            requests.exceptions.ConnectTimeout,
            vk.exceptions.VkAuthError
    ):
        return None

    friends_dict = api.friends.get(fields='online')
    friends_online_list = [
        friend for friend in friends_dict['items'] if friend['online']
    ]
    return friends_online_list


def output_friends_to_console(friends_online):
    for friend in friends_online:
        print(friend['first_name'], friend['last_name'])


if __name__ == '__main__':
    login = get_user_login()
    password = get_user_password()
    friends_online = get_online_friends(login, password)

    print('\nFriends online:')

    if not friends_online:
        exit('No friends online'
             '\n\nPossible reasons:'
             '\n\t- all friends offline'
             '\n\t- login and password are incorrect or empty'
             '\n\t- Internet connection error'
             )

    output_friends_to_console(friends_online)
