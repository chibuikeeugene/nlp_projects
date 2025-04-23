# importing libraries
from langchain_text_splitters.character import CharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_community.document_loaders.text import TextLoader

from loguru import logger

import pandas as pd
import numpy as np

def text_loader():
    """ return the vector embedding and the original dataframe """

    # adding large thumbnails for our books while handling books without thumbnail
    books = pd.read_csv('semantic_book_recommender_search_app/research/books_with_emotions.csv')
    books['large_thumbnail'] = books['thumbnail'] + '&fife=w800'
    books['large_thumbnail'] = np.where(books['thumbnail'].isna(), './research/cover_not_found.png', 
                                        books['large_thumbnail'])

    # load the document, create embeddings and store in chromadb

    books['tagged_desc'].to_csv('tagged-desc.txt', index=False, header=False, sep='\n')

    # loading the text document
    raw_documents =  TextLoader('./tagged-desc.txt').load()
    logger.info('raw document loaded successfully...')

    # splitting the documents into seperate chunks
    text_splitter = CharacterTextSplitter(separator='\n',chunk_size = 0, chunk_overlap = 0)

    documents = text_splitter.split_documents(raw_documents)
    logger.info('document splitting completed!')

    # save document into a vector database locally
    db_books = Chroma.from_documents(
        documents,
        embedding = OllamaEmbeddings(model="llama3.1"))

    logger.info('vectorstore creation completed...')

    return books , db_books