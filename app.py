import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

from db import get_db_engine, format_dataframe

load_dotenv()

def fetch_data(search_query=None):
    engine = get_db_engine()
    if search_query and search_query.strip():  # Check if there's a search query and it's not just empty or spaces
        query = "SELECT title, price, rating, in_stock FROM books WHERE title ILIKE %s"
        params = ('%' + search_query.strip() + '%',)
    else:
        query = "SELECT title, price, rating, in_stock FROM books"  # No search filter applied
        params = ()

    with engine.connect() as conn:
        df = pd.read_sql(query, conn, params=params)
    return df



def main():
    st.title('📚 The Paradise Library')
    st.subheader('🌟 Search, filter, and sort books.')

    # User inputs for search
    search_query = st.text_input("Enter the book title", "")

    # Fetch data based on the presence of a search query
    df = fetch_data(search_query)
    df = format_dataframe(df)

    if not df.empty:
        gb = GridOptionsBuilder.from_dataframe(df)
        gb.configure_pagination(enabled=True)
        gb.configure_side_bar()
        gb.configure_default_column(groupable=True, value=True, enableRowGroup=True, aggFunc='sum', filterable=True, sortable=True, editable=True)
        grid_options = gb.build()

        # Display the interactive grid
        AgGrid(df, gridOptions=grid_options, enable_enterprise_modules=True, fit_columns_on_grid_load=True)
    else:
        st.write("No books found or no search query entered.")

if __name__ == "__main__":
    main()
