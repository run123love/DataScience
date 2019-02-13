
def cookies_to_dict(cookies):
    cookies = cookies.strip()
    cookies = cookies.split(';')
    my_dict = dict()
    for i in cookies:
        s = i.split('=')
        my_dict[s[0]] = s[1]
    return my_dict
