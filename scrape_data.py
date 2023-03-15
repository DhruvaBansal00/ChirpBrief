from get_search_results import *
import pickle as pkl
import tqdm
import json


def store_scraped_data():

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


def combine_scraped_data():
    users_and_topics = pkl.load(open("user_to_dict.pkl", "rb"))
    topics_to_users = {}
    for user in users_and_topics:
        all_topics = users_and_topics[user]
        for curr_topic in all_topics:
            curr_topic = curr_topic.strip("  ")
            if curr_topic not in topics_to_users:
                topics_to_users[curr_topic] = []
            topics_to_users[curr_topic].append(user)

    print(topics_to_users, len(topics_to_users))
    pkl.dump(topics_to_users, open("topic_to_user.pkl", "wb"))


combine_scraped_data()
