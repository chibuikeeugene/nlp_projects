from semantic_book_recommender_search_app.semantic_recommender import retrieve_semantic_recommendation

def dashboard(q:str, cat:str, t:str):

    """the UI business logic

    args:
    * q: str - user query input
    * cat: str -  user's selected category of interests
    * t: str - user's tone selection

    returns:
    the data layer for the gradio user interface
    """
    # retrieve the recommended books dataframe
    recommendations =  retrieve_semantic_recommendation(
        query=q,
        category=cat,
        tone=t
    )

    results =  []

    # retrieve truncated descriptions and authors
    for _ ,rows in recommendations.iterrows():
        description = rows['description']
        splited_description = description.split()
        truncated_desc = ' '.join(splited_description[:30] + '...')

        splited_authors = rows['authors'].split(';')

        if len(splited_authors)==2:
            authors = f'{splited_authors[0]} and {splited_authors[1]}'
        elif len(splited_authors) > 2:
            authors = f'{' '.join(splited_authors[:-1])} and {splited_authors[-1]}'
        else:
            authors = rows['authors']
        
        # display all info as a caption
        caption = f'{rows['title']} by {authors} : {truncated_desc}'
        results.append((rows['thumbnail'], caption))
    return results




