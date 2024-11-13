import pandas as pd
import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
credentials_path ="runpod-files-a2225997f03.json"



def run_training(vanna_object):
    ids=[]
    
    vn=vanna_object

    def get_google_sheet():
        client = run_credentials()
        
        # Open the Google Sheet by name
        sheet = client.open("nlp_sql")
        return sheet
    
    workbook=get_google_sheet()

    data=workbook.worksheet('testing').get_all_records() 

    def process_inputs(inputs):
        # Your function that takes various inputs and processes them
        if 'training_data_type'in inputs and inputs['training_data_type']=='sql':
            id=vn.train(question=inputs["question"], sql=inputs["content"])
            ids.append(id)

        if 'training_data_type'in inputs and inputs['training_data_type']=='ddl':
            id=vn.train(ddl=inputs["content"])
            ids.append(id)

        if 'training_data_type'in inputs and inputs['training_data_type']=='documentation':
            id=vn.train(documentation=inputs["content"])
            ids.append(id)

        if len(inputs.keys())==1 and 'id' in inputs:
            vn.remove_training_data(inputs['id'])

    table=vn.get_training_data()
    table_ids=table['id'].unique()
    del_id= list(set(table_ids)-set(ids))
    if len(del_id)>0:
        for dids in del_id:
            vn.remove_training_data(dids)

    for inputs in data:
        cleaned_data = {k: v for k, v in inputs.items() if v.strip()}
        process_inputs(cleaned_data)

    sheet=workbook.worksheet('testing')
    try:
        # sheet_ids = data_ids.col_values(1)[1:]
        # sheet.worksheet('training').delete_rows(2,len(sheet_ids)+1)
        # data_n=[[i] for i in ids]
        current_data = sheet.col_values(1)[1:]
        for i in range(2, len(current_data) + 2):  
            sheet.update_cell(i, 1, '')
        all_data = sheet.get_all_values()

        # Iterate from the last row to the first row
        for i in range(len(all_data), 0, -1):
            # Check if the row is empty (all values are empty strings)
            if all(cell == '' for cell in all_data[i - 1]):
                sheet.delete_rows(i)
        for i, value in enumerate(ids, start=2):  
            sheet.update_cell(i, 1, value)
    except Exception as e:
        print(e)
        

def table(vanna_object):
    vn=vanna_object
    table=vn.get_training_data()
    st.session_state.generate_figure=False
    st.title("Training Data")
    st.dataframe(table, hide_index=True) 

def run_credentials():
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
    credentials_path,
    scopes=['https://www.googleapis.com/auth/drive']
    )
    client = gspread.authorize(credentials)
    return client

def update_google_sheet(question, Query, status):
    client = run_credentials()
    
    # Open the Google Sheet by name
    sheet = client.open("nlp_sql").sheet1
    
    try:
        headers = sheet.row_values(1)
        if headers==[]:
            sheet.append_row(["Question", "Query", "Status"])
    except IndexError:
        # Initialize headers if sheet is empty
        sheet.append_row(["Question", "Query", "Status"])
    sheet.append_row([question, Query, status])
def table(vanna_object):
    vn=vanna_object
    table=vn.get_training_data()
    st.title("Training Data")
    st.dataframe(table) 

