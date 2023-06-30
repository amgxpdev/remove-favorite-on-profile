from threading import Semaphore, Thread
from requests  import get
from colorama import Fore
from os       import system

semaphore = Semaphore(150)
success = 0
failed = 0

def unsave(aweme_id: str, sessionid: str) -> None:
    semaphore.acquire()
    global success
    global failed
    while True:
        try:
            url = f'https://api31-normal-useast2a.tiktokv.com/aweme/v1/aweme/collect/?aweme_id={aweme_id}&action=0&channel=beta&aid=1233&app_name=musical_ly&version_code=300015&device_platform=android&device_type=unknown&os_version=9'
            
            headers = {
                'cookie'     : f'sessionid={sessionid}',
                'user-agent' : 'com.zhiliaoapp.musically/2023000150 (Linux; U; Android 9; en; unknown; Build/PI;tt-ok/3.12.13.1)',
                'x-argus'    : '6/4Ixi5HhJlI9uQQ53v6tfgstiGWncc8cXAdJv3B4bYHhdfaOHbsTjhflGqNLOvkrjwx4dOgB7WkmBgfbzEpRJuTuOXbV/E3mpp5q50CGlxsj36HnopveP4HytXQz78l17XI4HmrtzIvynNT2+F3UfiFJxUbtAJoGtvqeGQeb7kg6V1O1dfCFI4jNJwmEso5zOH5F5keoBwvUiZhcf8FZOWNWuPKYgR26vVOlu90fxczeGnP6bvr2+gzuCbrNZ4rR+LQ7E0gEx2q9Uw6ev3nZyP8XaVmXRtqmCO4/nWqxiWtPZDxmbDAoRITB0/rt05MJ75eaYNwBzQ3SYboFk/f/RyJmKRb7q/eUAp25f1cD93N4S+RlYTBFzlbZlUodgdQDbDEhl8EK46mDJ4qJmwpd6dZo2hlTnuoxvnlJRgzZydJrvXNBsXpv3+cY6X80HExvOlOvcZQ9ZuuqKY9J6bk7M2o3Jvxr+ZuvJkIqHUwF3LmSGhG2CJuOlcDwoTlcb5KLN/7JL4Wi8nvvE7HsMt+Zd5MqsC12QYI9gHwqghu0U6W4A=='
            }
            
            if b'"unsave"' in get(url, headers=headers).content:
                print(f'{Fore.GREEN}unsave: +++ ({aweme_id}){Fore.RESET}')
                success += 1
                break
            else: 
                failed += 1
                continue
        except:
            continue
            
    semaphore.release()

def main(sessionid: str) -> None:
    cursor = 0
    
    while True:
        url = f'https://api31-normal-useast2a.tiktokv.com/aweme/v1/aweme/listcollection/?cursor={cursor}&count=20&ac=wifi&channel=beta&aid=1233'
        
        headers = {
            'cookie'     : f'sessionid={sessionid}',
            'user-agent' : 'com.zhiliaoapp.musically/2023000150 (Linux; U; Android 9; en; unknown; Build/PI;tt-ok/3.12.13.1)'
        }
        
        while True:
            try:
                response = get(url, headers=headers).json(); break
            except:
                continue
        
        if response['has_more'] == 1:
            cursor = response['cursor']
            for aweme in response['aweme_list']:
                Thread(target=unsave, args=[aweme['aweme_id'], sessionid]).start()
        else:
            for aweme in response['aweme_list']:
                Thread(target=unsave, args=[aweme['aweme_id'], sessionid]).start()
            break

if __name__ == '__main__':
    main(input('? Session ID: '))
    system(f"title Saved videos remover Made by @amgxp Succss: [{success}] Failed: [{failed}]")