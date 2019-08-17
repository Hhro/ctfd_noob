from ctfd import CTFd
from user import User

ctf = CTFd("https://redpwn.net")
ctf.get_CTFd_sitemap()
ctf.get_CTFd_endpoints()

player = User(ctf)
player.login()
ctf.challenges=player.get_challenges()

print(ctf.challenges)
