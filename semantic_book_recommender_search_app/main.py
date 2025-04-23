import gradio as gr
import pandas as pd
from semantic_recommender import dashboard


#load the books dataframe

# we create two lists for our filter components
books = pd.read_csv('semantic_book_recommender_search_app/research/books_with_emotions.csv')
categories = ['All'] + sorted(books['categories'].unique())

tones =  ['All'] + ['happy', 'surprising', 'angry', 'suspenseful', 'sad', 'irritating']

# UI elements
with gr.Blocks(theme = gr.themes.Glass()) as home:
    gr.Markdown('# Semantic Book search recommendation')
    with gr.Row():
        query = gr.Textbox(label = 'please enter a description of a book:', 
                           placeholder = 'e.g., a story about forgiveness')
        cat_dropdown = gr.Dropdown(choices = categories, label ='select a category', value ='All')
        tone_dropdown =  gr.Dropdown(choices = tones, label ='select an emotional tone', value ='All')

    submit_button = gr.Button('find recommendations')

    gr.Markdown('# Recommendations')
    output = gr.Gallery(label = 'Recommended books', columns = 8, rows =  2)

    submit_button.click(fn = dashboard,
                        inputs = [query,
                                  cat_dropdown,
                                  tone_dropdown],
                        outputs = output)

if __name__ == '__main__':
    home.launch()