import re
import os
import requests
import json
from bs4 import BeautifulSoup
from PIL import Image
import pandas as pd


def description_parse(data):
    res=data.split('-')[0]
    re=res.split(" ")
    info={}
    info['followers']=re[0]
    info['followings']=re[2]
    info['posts']=re[4]
    return info

def save_img(img_url, img_path):
    img = Image.open(requests.get(img_url, stream = True).raw)
    img.save(img_path)

def scrape_user(user):

    if not os.path.exists(os.path.join(os.getcwd(), user)):
        os.makedirs(user)

    url = f"https://www.instagram.com/{user}"
    r = requests.get(url)
    bs = BeautifulSoup(r.text ,"html.parser")

    description_data = bs.find('meta',property ='og:description').attrs["content"]
    final_data = description_parse(description_data)

    title_data = bs.find('meta',property="og:title").attrs["content"]
    title_split = title_data.split(" ")
    final_data["name"] = title_split[0]
    # final_data["title"] = bs.title

    profile_img_url = bs.find('meta',property='og:image').attrs["content"]
    profile_img_path = os.path.join(os.getcwd(), user, f'{final_data["name"]}_profile_pic.jpg')
    save_img(profile_img_url, profile_img_path)

    nonce = bs.findAll("script", type="application/ld+json")
    profile_page = re.sub("<.*?>", "", str(nonce[0]))
    post_page = re.sub("<.*?>", "", str(nonce[1]))
    profile_page_json = json.loads(profile_page)    ## wont be using profile_page_json since no necessary data 
    post_page_json = json.loads(post_page)

    all_posts_data = []
    
    for X in post_page_json:
        result = {}
        result["caption"] = X["headline"]
        result["dateCreated"] = X["dateCreated"]
        result["dateModified"] = X["dateModified"]
        result["commentCount"] = X["commentCount"]
        try:
            ## Exclude if no content location
            result["contentLocation"] = X["contentLocation"]["name"]
        except:
            pass
        result["postUrl"] = X["url"]
        result["likeActions"] = X["interactionStatistic"][0]["userInteractionCount"]
        result["commentActions"] = X["interactionStatistic"][1]["userInteractionCount"]
        try:
            result["imgUrl"] = X["image"][0]["url"]
            img_path = os.path.join(os.getcwd(), user, result["postUrl"][28:-1]) + ".jpg"
            save_img(result["imgUrl"], img_path)
        except:
            ## Excludes the post_img when its a video
            pass
        all_posts_data.append(result)

    final_data["post_related_data"] = all_posts_data
    

    # for saving in individual csvs'
    # df = pd.DataFrame(final_data)
    # df.to_csv(f'{user}.csv')
    # print(f"{user} data saved to csv and folder")

    return final_data


users_to_scrape = ["simanchal10", "war.and.peas", "shencomix", "hikaru_etanaru"]
scrape_dict = {}

for user in users_to_scrape:
    try:
        scrape_dict.update({user:scrape_user(user)})
    except Exception as err:
        print(f"Scraping failed for {user}")
        print("ERR - ", err)


for X in scrape_dict:
    post_count = 0
    for Y in scrape_dict[X]["post_related_data"]:
        post_count += 1
        for I, J in Y.items():
            scrape_dict[X][f"post_{post_count}_{I}"] = J
    del scrape_dict[X]["post_related_data"]

# print("-----")
# print(scrape_dict)
# print("-----")

scrape_df = pd.DataFrame(scrape_dict)
scrape_df.to_csv(f'all_user_scrape_data.csv')
## If there is no postdata in the csv, the account is private
print("Data saved to csv and folder")