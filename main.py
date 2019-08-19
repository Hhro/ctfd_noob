from ctfd import CTFd
from user import User
from manager import Manager

ctf = CTFd("https://redpwn.net",'redpwn2019')
ctf.get_CTFd_sitemap()
ctf.get_CTFd_endpoints()

player = User(ctf)
player.login()
ctf.challenges=player.get_challenges()

downloader = Manager(ctf,player)
downloader.download_all_challenges_files()