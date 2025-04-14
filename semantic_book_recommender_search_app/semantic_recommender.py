import pandas as pd
from semantic_book_recommender_search_app.text_loader import text_loader



# retrieve the semantic recommendations with a filter feature based on category and tone
def retrieve_semantic_recommendation(query:str, 
                                     initial_top_k:int = 30, 
                                     final_top_k:int = 10, 
                                     category:str = None,
                                     tone:str=None) -> pd.DataFrame:
    books, db_books = text_loader()
    docs = db_books.similarity_search(query, k =initial_top_k)

    book_lists_isbn = [int(doc.page_content.split()[0].strip('"')) for doc in docs]
    book_recs = books[books['isbn13'].isin(book_lists_isbn)].head(final_top_k)

    # filering by category
    if category != 'All':
        book_recs = book_recs[book_recs['categories']==category]
    else:
        book_recs = book_recs.head(final_top_k)

    # filtering by tone
    if tone == 'happy':
        book_recs.sort_values(by='Joy', ascending=False, inplace=True)
    elif tone == 'surprising':
        book_recs.sort_values(by='surprise', ascending=False, inplace=True)
    elif tone == 'angry':
        book_recs.sort_values(by='anger', ascending=False, inplace=True)
    elif tone == 'suspenseful':
        book_recs.sort_values(by='fear', ascending=False, inplace=True)
    elif tone == 'sad':
        book_recs.sort_values(by='sadness', ascending=False, inplace=True)
    elif tone == 'irritating':
        book_recs.sort_values(by='disgust', ascending=False, inplace=True)
    else:
        book_recs.sort_values(by='neutral', ascending=False, inplace=True)
    
    return book_recs