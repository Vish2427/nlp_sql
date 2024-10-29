__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
import streamlit as st
from model_loading import MyVanna

vn=MyVanna(config={
    'n_results_sql':1,
    'n_results_documentation':1, 
    'n_results_ddl':1,
    'path':"./chroma_data"                        
                   })
# Import your pages
from app import main
from training import table

# Create a sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Query", "Training Data"])


# Render the selected page
if page == "Query":
    main(vn)
elif page == "Training Data":
    table(vn)

