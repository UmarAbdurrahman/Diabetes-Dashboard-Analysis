import streamlit as st
import pandas as pd
import plotly.express as px

# Step 1: Load the data
@st.cache_data  # Cache for performance
def load_data():
    df = pd.read_csv('Data/diabetes.csv')
    # Clean data: Map SEX to readable labels (assuming 1=Female, 2=Male based on common datasets)
    df['SEX'] = df['SEX'].map({1: 'Female', 2: 'Male'})
    # Handle any NaNs
    df.fillna(0, inplace=True)
    return df

df = load_data()

# Step 2: Basic Streamlit Components
st.title("Diabetes Dataset Analysis Dashboard")
st.header("Overview of Diabetes Data")
st.text("This dashboard analyzes diabetes progression data using interactive visualizations.")
st.text(f"Dataset shape: {df.shape[0]} rows, {df.shape[1]} columns")

# Show raw data with a button (interactive component)
if st.button("Show Raw Data"):
    st.dataframe(df.head(10))  # Display first 10 rows

# Step 3: Interactive Widgets for Filtering
st.sidebar.header("Filter Options")
age_min, age_max = st.sidebar.slider("Select Age Range", min_value=int(df['AGE'].min()), max_value=int(df['AGE'].max()), value=(int(df['AGE'].min()), int(df['AGE'].max())))
bmi_min, bmi_max = st.sidebar.slider("Select BMI Range", min_value=float(df['BMI'].min()), max_value=float(df['BMI'].max()), value=(float(df['BMI'].min()), float(df['BMI'].max())))
sex_filter = st.sidebar.selectbox("Select Sex", options=["All"] + list(df['SEX'].unique()), index=0)

# Apply filters
filtered_df = df[(df['AGE'] >= age_min) & (df['AGE'] <= age_max) &
                 (df['BMI'] >= bmi_min) & (df['BMI'] <= bmi_max)]
if sex_filter != "All":
    filtered_df = filtered_df[filtered_df['SEX'] == sex_filter]

st.text(f"Filtered data: {filtered_df.shape[0]} rows")

# Step 4: Interactive Visualizations
st.header("Interactive Visualizations")

# Visualization 1: Histogram of Disease Progression (Y)
fig1 = px.histogram(filtered_df, x='Y', color='SEX', title="Distribution of Disease Progression (Y) by Sex",
                    labels={'Y': 'Disease Progression'}, barmode='overlay')
fig1.update_layout(xaxis_title="Disease Progression (Y)", yaxis_title="Count")
st.plotly_chart(fig1)

# Visualization 2: Scatter Plot of BMI vs Disease Progression (Colored by Sex)
fig2 = px.scatter(filtered_df, x='BMI', y='Y', color='SEX',
                  title="BMI vs Disease Progression by Sex",
                  labels={'BMI': 'Body Mass Index', 'Y': 'Disease Progression'},
                  hover_data=['AGE', 'BP', 'S1'])
st.plotly_chart(fig2)

# Visualization 3: Box Plot of Key Features by Sex
fig3 = px.box(filtered_df, x='SEX', y=['BMI', 'BP', 'S3', 'S4'], title="Box Plot of Features by Sex",
              labels={'value': 'Feature Value', 'variable': 'Feature'})
st.plotly_chart(fig3)

# Visualization 4: Correlation Heatmap
corr_matrix = filtered_df[['AGE', 'BMI', 'BP', 'S1', 'S2', 'S3', 'S4', 'S5', 'S6', 'Y']].corr()
fig4 = px.imshow(corr_matrix.values, x=corr_matrix.columns, y=corr_matrix.columns,
                 title="Correlation Heatmap of Features",
                 color_continuous_scale='RdBu_r', text_auto=True)
st.plotly_chart(fig4)