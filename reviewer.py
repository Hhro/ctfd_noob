import json
import utils
from pathlib import Path
from ctfd import CTFd

class Reviewer(object):
    def __init__(self,ctfd):
        self.ctfd = ctfd
        self.loc = self.ctfd.loc / "review"
        self.categories = []
        self.chall_reviews = {}
    
    def extract_review_ctgr(self):
        chall_reviews = self.chall_reviews
        categories = set()

        for chall_review_id in chall_reviews.keys():
            chall_review = chall_reviews[chall_review_id]
            categories.add(chall_review['category'])
        
        return list(categories)

    def review_ctf(self):
        print("[Reviewng CTF]")
        ctf_review = {}
        review_dir = self.loc
        review_dir.mkdir(parents=True,exist_ok=True)
        
        print("{}".format(self.ctfd.name))
        difficulty = input("Difficulty(1~5): ")
        worth = input("Worth(1~5): ")
        brief_review = input("Brief review: ")

        ctf_review = {"diff":difficulty,"worth":worth,"brief_review":brief_review}

        utils.save_json_into_file(ctf_review,review_dir,"ctf_review.json",opt="new")
        return True
    
    def init_chall_review(self):
        print("[Init challenge review json]")
        challs = self.ctfd.challenges
        challs_review = {}
        categories = self.ctfd.get_categories()
        review_dir = self.loc
        review_dir.mkdir(parents=True,exist_ok=True)
        save_path = review_dir / "chall_reviews.json"

        if save_path.exists():
            print("Read review file...")
            with open(str(save_path),"r") as chall_review_json:
                self.chall_reviews = json.load(chall_review_json)
                chall_review_json.close()
            self.categories = self.extract_review_ctgr()
            return True

        print("Which category would you review?")
        for idx,category in enumerate(categories):
            print("{}. {}".format(str(idx+1),category))
        idxs = input("categories(idx1, idx2, ...)? > ").split(' ')
        categories = [categories[int(idx)-1] for idx in idxs]
        self.categories = categories

        for chall_id in challs:
            chall = challs[chall_id]
            if chall['category'] in categories:
                chall_review = {
                    chall_id:{
                        "name":chall["name"],
                        "category":chall["category"],
                        "solves":chall["solves"],
                        "state":"0",
                        "diff":"",
                        "worth":"",
                        "tags":"",
                        "overview":""
                    }
                }
                challs_review.update(chall_review)
        
        utils.save_json_into_file(challs_review,review_dir,"chall_reviews.json",opt="new")
        return True

    def review_challs(self):
        print("[Reviewng Challenges]")
        chall_review = {}

        if self.categories == []:
            print("You must init it first")
            self.init_chall_review()
        categories = self.categories

        while 1:
            for idx,category in enumerate(categories):
                print("{}. {}".format(str(idx+1),category))
            idx = int(input("category(idx)? > "))
            category = categories[idx-1]

            challs = self.ctfd.get_challenges(filters={"category":category})
            for chall_id in challs.keys():
                chall = challs[chall_id]
                print("{}. {}".format(chall_id,chall["name"]))
            chall_id = input("chall(id)? > ")

            reviewee = challs[chall_id]
            print("{}".format(reviewee["name"]))
            difficulty = input("Difficulty(1~5): ")
            worth = input("Worth(1~5): ")
            tags = input("Tags: ").split(' ')
            overview = input("Overview: ")

            print("State")
            print("1.Only write-up")
            print("2.Write-up will be uploaded")
            print("3.Write-up is uploaded")
            state = input("> ")

            chall_review = {
                chall_id: {
                    "name":reviewee["name"],
                    "category":reviewee["category"],
                    "solves":reviewee["solves"],
                    "state":state,
                    "diff":difficulty,
                    "worth":worth,
                    "tags":tags,
                    "overview":overview
                }
            }

            self.chall_reviews.update(chall_review)
            
            choice = input("Are you done?(y/n) ")
            if(choice == 'y'):
                break

        self.save_chall_reviews() 
        return True
    
    def save_chall_reviews(self):
        utils.save_json_into_file(self.chall_reviews,self.loc,"chall_reviews.json",opt="modify")
        return True
