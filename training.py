import pandas as pd
import streamlit as st

def run_training(vanna_object):

    vn=vanna_object
    
    vn.train(ddl="""
    CREATE TABLE client_campaigns (
    client_name VARCHAR(255), -- Name of the client
    channel_name VARCHAR(255), -- ecommerce channel(amazon, flipkart) where the campaign is executed.
    campaign_name VARCHAR(255), -- Name of the campaign
    program_type VARCHAR(50), -- Type of advertising program
    impression INTEGER, -- Number of impressions
    click INTEGER, -- Number of clicks
    spend DECIMAL(10,2), -- spend on the campaign for report date
    sale DECIMAL(10,2), -- sales generated
    conversion_rate DECIMAL(5,2), -- Orders divided by the number of clicks
    orders INTEGER, -- Number of orders placed
    report_date DATE, -- Campaigns data reporting date in yyyy-mm-dd
    category VARCHAR(100), -- Category of the product being campainged
    subcategory VARCHAR(100), -- Subcategory of the product being campainged
    )
    """)
    vn.train(ddl="""
    TABLE client_sku_reports (
    client_name VARCHAR(255), -- Name of the client
    channel_name VARCHAR(255), -- ecommerce channel(amazon, flipkart) where the campaign is executed.
    sku_title VARCHAR(255), -- Title of the SKU/ASIN
    brand VARCHAR(100), -- Brand of the SKU/ASIN
    report_date DATE, -- Reporting date of the SKU/ASIN data in yyyy-mm-dd
    asin_id VARCHAR(100), -- SKU/ASIN of the product
    bsr INTEGER, -- Best Seller Rank of SKU
    category VARCHAR(100), -- Category of the SKU
    subcategory VARCHAR(100), -- Sub-category of the SKU
    bb_winner BOOLEAN, -- Name of the best buy winner
    price DECIMAL(10,2), -- Price of the SKU
    rating DECIMAL(3,2), -- Average rating of the SKU
    rating_count INTEGER, -- Count of ratings
    sale DECIMAL(10,2), -- Total sales amount
    spend DECIMAL(10,2), -- Total spend on advertising
    orders INTEGER, -- Number of orders placed
    click INTEGER, -- Number of clicks
    impression INTEGER, -- Number of impressions
    is_available BOOLEAN, -- Availability status of the SKU
    total_clicked_ad_units INTEGER, -- Total clicked ad units on flipkart
    total_view_ad_units INTEGER, -- Total viewed ad units on fipkart
    total_clicked_ad_sales DECIMAL(10,2), -- Total sales from clicked ads on flipkart
    total_view_ad_sales DECIMAL(10,2) -- Total sales from viewed ads on flipkart
    )
    """)
    vn.train(documentation="The Click Through Rate i.e. CTR is defeined as clicks per impression")
    vn.train(documentation="ROAS stands for “return on ad spend” and is a marketing metric that estimates the amount of revenue earned per spend allocated to advertising.")
    vn.train(documentation="to calculate CTR over time, such as daily, weekly, or monthly, you'll collect impressions and clicks for each time period and calculate the CTR separately for each interva.")
    vn.train(documentation="the data is SQLite, Query has to be write according to SQLite.")
    vn.train(documentation="if question is not related to the data, responsd 'I am not able to answer this question as data is not available.'")
    vn.train(
        question="sales in sept 2025",
        sql="SELECT SUM(sale) AS total_sales FROM client_campaigns WHERE strftime('%Y-%m', report_date) = '2025-09'"
    )

def table(vanna_object):
    vn=vanna_object
    table=vn.get_training_data()
    st.title("Training Data")
    st.dataframe(table) 

