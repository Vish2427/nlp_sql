__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

from model_loading import MyVanna, client_name_loader
import streamlit as st
import pandas as pd
import requests
import traceback
import re
from training import run_training, update_google_sheet


vn=MyVanna(config={
    'n_results_sql':3,
    'n_results_documentation':5, 
    'n_results_ddl':1,
    'path':"./chroma_data"                        
                   })
vn.run_sql_is_set = True

def main(vn):
    
    # Initialize session state variables if not already set
    if 'counter' not in st.session_state:
        st.session_state.counter = 0
    if 'add_id' not in st.session_state:
        st.session_state.add_id = []
    if 'submit_clicked' not in st.session_state:
        st.session_state.submit_clicked = False
    if 'generate_figure' not in st.session_state:
        st.session_state.generate_figure = False
    if 'feedback' not in st.session_state:
        st.session_state.feedback = False
    if 'like_button' not in st.session_state:
        st.session_state.like_button=False
    if 'dislike_button' not in st.session_state:
        st.session_state.dislike_button=False
    if st.session_state.counter == 0:
        run_training(vn)
        st.session_state.counter = 1

    st.title("1DS NLP to SQL")

    
    client_dict=client_name_loader()

    submit_question(vn,client_dict)

    

def submit_question(vn,client_dict):
    options=list(client_dict.keys())
    st.session_state.selected_option = st.selectbox(
    "Select the client:",
    options
        )
    st.session_state.client_id=client_dict[st.session_state.selected_option]
    col1, col2 = st.columns([2, 8])

    
    default_question = "Subcategory wise RoAS in last 90 days"
    
    # Text input for the question
    st.session_state.question = st.text_input("Enter Question:", value=default_question)

    # Submit button
    if st.button("Submit"):
        if not st.session_state.question:
            st.warning("Please enter a question.")
            return
        
        # Set session state flag to indicate submit was clicked
        st.session_state.submit_clicked = True
        

    # Execute the logic if submit was clicked
    if st.session_state.submit_clicked:
        output = f"You asked: {st.session_state.question}"
        st.write(output)
        st.session_state.question2=f"For client_id = {st.session_state.client_id}, " + st.session_state.question
        # Get SQL query
        
        st.session_state.sql_query, st.session_state.table, _ = vn.ask(question=st.session_state.question2, 
                                                                        visualize=False, 
                                                                        print_results=False, 
                                                                        auto_train=False,
                                                                        allow_llm_to_see_data=True)
        
        if st.session_state.sql_query:
            
            st.write(st.session_state.sql_query)
            
            st.session_state.submit_clicked = False
            st.dataframe(st.session_state.table,hide_index=True) 

            st.session_state.generate_figure=True
            st.session_state.feedback = True

    
    col1, col2,col3 = st.columns([3,1,1])       
    if st.session_state.feedback:
        
        with col1:
            st.write("Feedback")

        with col2:
            st.session_state.like_button = st.button("👍")
            if st.session_state.like_button:
                update_google_sheet(st.session_state.question2,st.session_state.sql_query,"Like")
                reset_feedback_state()
                st.rerun()

        with col3:
            st.session_state.dislike_button=st.button("👎")
            if st.session_state.dislike_button:
                update_google_sheet(st.session_state.question2,st.session_state.sql_query,"Dislike")
                reset_feedback_state()
                st.rerun()

    if st.session_state.generate_figure:
        if st.button("Generate graph"):
            generate_graph(vn)
            st.session_state.generate_figure=False
                

def reset_feedback_state():
    """Function to reset feedback and submission states."""
    st.session_state.feedback = False
    st.session_state.submit_clicked = False
    st.session_state.like_button = False
    st.session_state.dislike_button = False
    st.session_state.generate_figure = False
    st.session_state.question = ""

def generate_graph(vn):
    try:
        plotly_code = vn.generate_plotly_code(
            question=st.session_state.question,
            sql=st.session_state.sql_query,
            df_metadata=f"Running df.dtypes gives:\n {st.session_state.table.dtypes}",
        )
        fig = vn.get_plotly_figure(plotly_code=plotly_code, df=st.session_state.table)
        output = f"You asked: {st.session_state.question}"
        st.write(output)
        st.write(st.session_state.sql_query)
        st.dataframe(st.session_state.table,hide_index=True) 
        st.plotly_chart(fig)
            
    except Exception as e:
        traceback.print_exc()
        st.error(f"Couldn't generate graph: {e}")

    

if __name__ == "__main__":
    main(vn)
