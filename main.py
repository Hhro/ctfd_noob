from ctfd import CTFd
from user import User
from manager import Manager

ctf = CTFd("https://redpwn.net",'redpwn2019')
ctf.get_CTFd_sitemap()
ctf.get_CTFd_endpoints()

player = User(ctf)
player.login()

input("Enter anything after validating your Email")

player.create_team()
ctf.challenges=player.get_challenges()

manager = Manager(ctf,player)
manager.download_all_challenges_files()
manager.add_all_challenges_description()