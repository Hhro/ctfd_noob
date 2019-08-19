from ctfd import CTFd
from user import User
from manager import Manager
from reviewer import Reviewer

ctf = CTFd("https://redpwn.net",'redpwn2019')
ctf.get_CTFd_sitemap()
ctf.get_CTFd_endpoints()

player = User(ctf)
player.login()

ctf.challenges = player.get_challenges()

manager = Manager(ctf,player)
manager.download_all_challenges_files()
manager.add_all_challenges_description()

reviewer = Reviewer(ctf)
reviewer.init_chall_review()
reviewer.review_challs()
