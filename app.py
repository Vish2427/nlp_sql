from model_loading import MyVanna
import streamlit as st
import pandas as pd
import requests
import re
from training import run_training
vn=MyVanna(config={
    'n_results_sql':1,
    'n_results_documentation':1, 
    'n_results_ddl':1,
    'path':"./chroma_data"                        
                   })


def main(vn):
    # Initialize session state variables if not already set
    if 'counter' not in st.session_state:
        st.session_state.counter = 0
    if 'add_id' not in st.session_state:
        st.session_state.add_id = []
    if 'submit_clicked' not in st.session_state:
        st.session_state.submit_clicked = False
    if 'add_to_history_clicked' not in st.session_state:
        st.session_state.add_to_history_clicked = False
    if 'remove_history' not in st.session_state:
        st.session_state.remove_history = False
    # Run training only once
    if st.session_state.counter == 0:
        run_training(vn)
        st.session_state.counter = 1

    st.title("1DS NLP to SQL")
    
    submit_question(vn)

def submit_question(vn):
    col1, col2 = st.columns([2, 8])

    with col2:
        default_question = "Subcategory wise RoAS in last 90 days"
        
        # Text input for the question
        question = st.text_input("Enter Question:", value=default_question)
        
        if st.checkbox("Add to history"):
            st.session_state.add_to_history_clicked = True
        # Submit button
        if st.button("Submit"):
            if not question:
                st.warning("Please enter a question.")
                return
            
            # Set session state flag to indicate submit was clicked
            st.session_state.submit_clicked = True
            st.session_state.question = question

        # Execute the logic if submit was clicked
        if st.session_state.submit_clicked:
            output = f"You asked: {st.session_state.question}"
            st.write(output)
            
            # Get SQL query
            sql_query, _, _ = vn.ask(question=st.session_state.question, visualize=False, print_results=False, auto_train=False)
            if sql_query:
                st.write(sql_query)
                st.session_state.sql_query = sql_query
                st.session_state.submit_clicked = False
                # Button to add to history, which sets another session flag
        

                # Execute add to history logic if add_to_history_clicked flag is set
                if st.session_state.add_to_history_clicked:
                    id = vn.train(question=st.session_state.question, sql=st.session_state.sql_query)
                    st.session_state.add_id.append(id)
                    st.session_state.add_to_history_clicked = True  # Reset flag

    with col1:
        # Button to reset and give a new question
        if st.button('Give new question'):
            st.session_state.remove_history = True
        if len(st.session_state.add_id) > 0 and st.session_state.remove_history:
            for i in st.session_state.add_id:
                vn.remove_training_data(i)
            st.session_state.add_id = []
            st.session_state.submit_clicked = False  # Reset submit flag

if __name__ == "__main__":
    main(vn)
