from turtle import right
from numpy import average
import pandas as pd
import plotly.express as px
from sqlalchemy import column
import streamlit as st


st.set_page_config(page_title = "Sales Dashboard",
                    page_icon=":bar_chart:",
                    layout="wide",
                    )
def get_data_from_excel():

    df = pd.read_excel(
        io="supermarkt_sales.xlsx",
        engine="openpyxl",
        sheet_name='Sales',
        skiprows=3,
        usecols='B:R',
        nrows = 1000,
    )
    
    # Added Hour column
    df["Hour"] = pd.to_datetime(df["Time"],format="%H:%M:%S").dt.hour

    return df


df = get_data_from_excel()

# Sidebar

st.sidebar.header("Please Filter in Here")

city = st.sidebar.multiselect(
    "Select a City",
    options=df['City'].unique(),
    default=df['City'].unique()
)

customer_type = st.sidebar.multiselect(
    "Select a Customer Type",
    options=df['Customer_type'].unique(),
    default=df['Customer_type'].unique()
)

gender = st.sidebar.multiselect(
    "Select a Gender Type",
    options=df['Gender'].unique(),
    default=df['Gender'].unique()
)

df_selection = df.query(
    "City == @city & Customer_type == @customer_type & Gender == @gender "
)

st.dataframe(df_selection)


# Main Page

st.title(":bar_chart:Sales Dashboard")
st.markdown('##')


# Top KPI's

total_sales = int(df_selection['Total'].sum())
average_rating = round(df_selection['Rating'].mean(),1)
star_rating = ":star:" * int(round(average_rating,0))
average_sale_by_transaction = round(df_selection["Total"].mean(),2)

left_column,middle_column,right_column = st.columns(3)

with left_column:
    st.subheader('Total Sales')
    st.subheader(f"US ${total_sales}")

with middle_column:
    st.subheader('Average Rating')
    st.subheader(f"{average_rating} {star_rating}")

with right_column:
    st.subheader('Average Sale By Transaction')
    st.subheader(f"US ${average_sale_by_transaction}")


st.markdown("----")

# Sales by Product [Bar Chart]
sales_by_product_line = (
    df_selection.groupby(by=["Product line"]).sum()[["Total"]].sort_values(by="Total")
    )

fig_product_sales = px.bar(
                    sales_by_product_line,
                    x="Total",
                    y=sales_by_product_line.index,
                    orientation="h",
                    title="<b>Sales by Product Line</b>",
                    color_discrete_sequence=["#0C4B83"] * len(sales_by_product_line),
                    template = "plotly_white")


fig_product_sales.update_layout(
    plot_bgcolor = "rgba(0,0,0,0)",
    xaxis = (dict(showgrid = False))

)

# Sales by hour [Bar Chart]

sales_by_hour = df_selection.groupby(by = ["Hour"]).sum()[["Total"]]

fig_hour_sales = px.bar(
                    sales_by_hour,
                    x=sales_by_hour.index,
                    y="Total",
                    title="<b>Sales by Hour</b>",
                    color_discrete_sequence=["#16501C"] * len(sales_by_hour),
                    template = "plotly_white")

fig_hour_sales.update_layout(
    plot_bgcolor = "rgba(0,0,0,0)",
    yaxis = (dict(showgrid = False)),
    xaxis = dict(tickmode = "linear")

)



left_column , right_column = st.columns(2)
left_column.plotly_chart(fig_product_sales, use_container_width=True)
right_column.plotly_chart(fig_hour_sales, use_container_width=True)


# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """