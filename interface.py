import pickle
from functools import partial

import gradio as gr

from get_search_results import *

topic_to_user_dict = pickle.load(open("topic_to_user.pkl", "rb"))


def find_users_for_topic(ind, list_of_topics):
    print(list_of_topics)
    print(ind)
    text = "# Users for topic:\n"
    return text + "\n".join(
        [
            f"{i+1}. [{username}](http://twitter.com/{username})"
            for i, username in enumerate(topic_to_user_dict[list_of_topics[ind]])
        ]
    )


def generate_topics_for_user(username):
    topics = generate_topic_tags(username)
    topics = topics.replace("#", "").split(",")
    topics = [i.strip() for i in topics]
    filtered_topics = []
    for topic in topics:
        if topic in topic_to_user_dict:
            filtered_topics.append(topic)
    filtered_topics = [
        (len(topic_to_user_dict[topic]), topic) for topic in filtered_topics
    ]
    filtered_topics.sort(reverse=True)
    filtered_topics = [topic for _, topic in filtered_topics]
    button_changes = []
    list_of_topics = []
    for topic in filtered_topics:
        if len(button_changes) >= 5:
            break
        if topic in topic_to_user_dict:
            button_changes.append(gr.update(value=topic, visible=True))
            list_of_topics.append(topic)
    print(topics)
    print(filtered_topics)
    print(list_of_topics)
    while len(button_changes) < 5:
        button_changes.append(gr.update(value="-"))
    return [list_of_topics] + button_changes


with gr.Blocks() as demo:
    gr.Markdown("Flip text or image files using this demo.")
    with gr.Tab("Get search summary"):
        search_input = gr.Textbox(label="Search input")
        search_output = gr.Textbox(label="Search summary")
        search_button = gr.Button("Search and Generate Summary")
        search_button.click(
            fn=generate_query_summary,
            inputs=search_input,
            outputs=search_output,
        )

    with gr.Tab("Get top trending summary"):
        topics = get_all_topics_from_trending()
        topic_summary_output = gr.Textbox(label="Summary of trend")
        for i in range(0, len(topics), 5):
            with gr.Row():
                for j in range(i, min(i + 5, len(topics))):
                    button_i = gr.Button(topics[j])
                    button_i.click(
                        fn=partial(generate_trending_topic_summary, topics[j]),
                        outputs=topic_summary_output,
                    )

    with gr.Tab("User Summary"):
        username_input = gr.Textbox(label="Username to summarize")
        username_output = gr.Textbox(label="Summarized profile")
        user_summary_button = gr.Button("Generate summary for user")
        user_summary_button.click(
            fn=generate_tweet_summary_for_user,
            inputs=username_input,
            outputs=username_output,
        )

    with gr.Tab("Generate User Bio"):
        bio_username_input = gr.Textbox(label="Username to summarize")
        bio_username_output = gr.Textbox(label="Generated Bio")
        generate_bio_button = gr.Button("Generate bio for user")
        generate_bio_button.click(
            fn=generate_bio,
            inputs=bio_username_input,
            outputs=bio_username_output,
        )

    with gr.Tab("Discover usernames"):
        discover_username_input = gr.Textbox(
            label="Username similar to which we want usernames"
        )
        username_button = gr.Button("Find topics for this user")
        user_topics = gr.State([])
        l = []
        with gr.Row():
            for i in range(5):
                button_i = gr.Button("-", visible=False)
                l.append(button_i)
        topic_summary_output = gr.Markdown("# Users for topic:")
        for i, button_i in enumerate(l):
            button_i.click(
                fn=partial(
                    find_users_for_topic,
                    i,
                ),
                inputs=user_topics,
                outputs=topic_summary_output,
            )
        username_button.click(
            fn=generate_topics_for_user,
            inputs=discover_username_input,
            outputs=[user_topics] + l,
        )

demo.launch()
