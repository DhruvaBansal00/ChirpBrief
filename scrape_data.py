from get_search_results import *
import pickle as pkl
import tqdm

file = open("Top-1000-Celebrity-Twitter-Accounts.csv", "r")
user_to_dict = {}
for i, line in tqdm.tqdm(enumerate(file)):
    try:
        curr_user_name = line.split(",")[0]
        topics = generate_topic_tags(curr_user_name)
        user_to_dict[curr_user_name] = topics.replace("#", "")
        if i % 100 == 0:
            pkl.dump(user_to_dict, open("user_to_dict.pkl", "wb"))
    except:
        pass
