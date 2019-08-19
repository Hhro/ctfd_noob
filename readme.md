# CTFd_noob

## Description

CTFd와 관련된 유틸제공

---

## Install

```bash
git clone https://github.com/Hhro/ctfd_noob
```

### Using virtualenv

```bash
$source ./venv/bin/activate
```

### Without virtualenv

```bash
$python3 -m pip install -r requirements.txt
```

Install as python module is not supported yet.

---

## Examples

Documentation will be uploaded(maybe).

### Download challenges files

```python3
from ctfd import CTFd
from user import User
from manager import Manager

ctf = CTFd("https://redpwn.net",'redpwn2019') #EXAMPLE (URL, name)
ctf.get_CTFd_sitemap()
ctf.get_CTFd_endpoints()

player = User(ctf)
player.login()

input("Enter anything after validating your Email")

player.create_team()
ctf.challenges=player.get_challenges()

manager = Manager(ctf,player)
manager.download_all_challenges_files()
```

### Download challenges description(MarkDown)

```python3
from ctfd import CTFd
from user import User
from manager import Manager

ctf = CTFd("https://redpwn.net",'redpwn2019') #EXAMPLE (URL, name)
ctf.get_CTFd_sitemap()
ctf.get_CTFd_endpoints()

player = User(ctf)
player.login()

input("Enter anything after validating your Email")

player.create_team()
ctf.challenges=player.get_challenges()

manager = Manager(ctf,player)
manager.add_all_challenges_description()
```

---

## TODO

1. Project structure 갖추기
2. Docs 쓰기
3. Bot만들기(추가 챌린지, 공지 체크 후 디스코드 앱으로 ㄱ)
4. 커맨드라인 인터페이스 갖추기
