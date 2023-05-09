import pandas as pd
import streamlit as st
import plotly.express as px


# Set page config
st.set_page_config(
    page_title="Mobile-friendly Streamlit App",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="auto",
    )


# Load data
@st.cache(allow_output_mutation=True)
def load_data(data_file):
    if data_file.name.endswith('.csv'):
        df = pd.read_csv(data_file)
    elif data_file.name.endswith(('.xls', '.xlsx')):
        df = pd.read_excel(data_file)
    elif data_file.name.endswith('.json'):
        df = pd.read_json(data_file)
    return df

# Sidebar - File upload
st.sidebar.title("Upload file")
data_file = st.sidebar.file_uploader("Upload CSV, XLSX, or JSON file", type=["csv", "xlsx", "json"])

# Show data
if data_file is not None:
    df = load_data(data_file)

    # Sidebar - Dataset summary
    st.sidebar.title("Dataset summary")
    st.sidebar.info(f"Number of rows: {df.shape[0]}")
    st.sidebar.info(f"Number of columns: {df.shape[1]}")
    st.sidebar.markdown("---")
    st.sidebar.subheader("Column descriptions")
    column_desc = dict(df.dtypes)
    for column in df.columns:
        st.sidebar.info(f"{column}: {column_desc[column]}")
    st.sidebar.markdown("---")
    #st.sidebar.subheader("Null values")
    #st.sidebar.info(f"{df.isnull().sum()}")

    # Main page
    st.title("Dataset Explorer")
    st.header("Head of dataset")
    st.write(df.head())

    # Generate graphs
    st.header("Visualization")
    plot_options = ["Select plot type", "Bar plot", "Histogram", "Scatter plot", "Line plot", "Bubble chart", "Pie chart"]
    plot_type = st.selectbox("Select plot type", plot_options)

    # Univariate plot
    if plot_type in ["Bar plot", "Histogram"]:
        st.subheader("Univariate plot")
        column = st.selectbox("Select a column", df.columns)
        if plot_type == "Bar plot":
            fig = px.bar(df.head(10), x=column, y='index', orientation='h')
            st.plotly_chart(fig)
        elif plot_type == "Histogram":
            fig = px.histogram(df.head(10), x=column)
            st.plotly_chart(fig)

    # Bivariate plot
    elif plot_type in ["Scatter plot", "Line plot", "Bubble chart", "Pie chart"]:
        st.subheader("Bivariate plot")
        x_column = st.selectbox("Select X-axis column", df.columns)
        y_column = st.selectbox("Select Y-axis column", df.columns)
        if plot_type == "Scatter plot":
            fig = px.scatter(df.head(10), x=x_column, y=y_column)
            st.plotly_chart(fig)
        elif plot_type == "Line plot":
            fig = px.line(df.head(10), x=x_column, y=y_column)
            st.plotly_chart(fig)
        elif plot_type == "Bubble chart":
            #size_column = st.selectbox("Select size column", df.columns)
            fig = px.scatter(df.head(10), x=x_column, y=y_column)
            st.plotly_chart(fig)
        elif plot_type == "Pie chart":
            fig = px.pie(df.head(10), values=y_column, names=x_column)
            st.plotly_chart(fig)

    # Summary
    st.header("Summary")
    st.subheader("Overall summary of the dataset")
    st.write(df.describe())

