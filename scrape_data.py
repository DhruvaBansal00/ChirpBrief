from get_search_results import *
import pickle as pkl
import tqdm
import json

file = open("data", "r")
user_to_dict = {}
error_count = 0
for i, line in tqdm.tqdm(enumerate(file)):
    try:
        curr_user_name = json.loads(line)["screen_name"]
        topics = generate_topic_tags(curr_user_name)
        user_to_dict[curr_user_name] = topics.replace("#", "").split(",")
        if i % 100 == 0:
            pkl.dump(user_to_dict, open("user_to_dict.pkl", "wb"))
    except Exception as e:
        print(f"{e}. Error count = {error_count}")
        error_count += 1
