import gradio as gr

from functools import partial
from get_search_results import *

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

demo.launch()
