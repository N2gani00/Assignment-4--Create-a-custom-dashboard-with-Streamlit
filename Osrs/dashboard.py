import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('OSRS Skill XP DATA Jan 2023.csv')

# Streamlit title
st.title('OSRS Level 99 Skills Dashboard')

# Display introductory text
st.markdown("""
    Welcome to the **OSRS Level 99 Skills Dashboard**! This dashboard visualizes the number of users
    who have achieved level 99 in each of the 23 skills in Old School RuneScape (OSRS). You can interact 
    with the data using the controls below.
""")

# Show the first few rows of the dataset
st.write("### Dataset Overview")
st.write(df.head(10))  # Display the first 10 rows of the data

# Show summary statistics of the data
st.write("### Summary Statistics")
st.write(df.describe())

# Clean up the 'lvl_99_users' column (remove commas and convert to numeric)
df['lvl_99_users'] = df['lvl_99_users'].replace({',': ''}, regex=True).astype(float)

# --- Streamlit Input Widgets ---
st.sidebar.header('Filters')
min_users = st.sidebar.slider('Minimum number of users with Level 99', 
                              int(df['lvl_99_users'].min()), 
                              int(df['lvl_99_users'].max()), 
                              int(df['lvl_99_users'].min()))
# Filter the data based on user input
df_filtered = df[df['lvl_99_users'] >= min_users]

# --- Layout and Containers ---
# Create two columns for displaying charts and data side-by-side
col1, col2 = st.columns(2)

with col1:
    # Bar chart for the number of users with level 99 for each skill
    st.write("### Number of Users with Level 99 (Filtered)")
    plt.figure(figsize=(10, 6))
    plt.bar(df_filtered['Skill'], df_filtered['lvl_99_users'], color='lightcoral')
    plt.xlabel('Skill')
    plt.ylabel('Number of Users with Level 99')
    plt.title('Number of Users with Level 99 in OSRS Skills')
    plt.xticks(rotation=90)
    st.pyplot(plt)

with col2:
    # Display a table with the filtered data
    st.write("### Filtered Data")
    st.write(df_filtered[['Skill', 'lvl_99_users']])

# --- Sort Data to Get Top 5 Skills ---
df_sorted = df.sort_values('lvl_99_users', ascending=False)

# Display a pie chart of skills with the highest level 99 user count
st.write("### Pie Chart of Top Skills with Most Users")
top_skills = df_sorted.head(5)  # Take the top 5 skills with most level 99 users
plt.figure(figsize=(8, 8))
plt.pie(top_skills['lvl_99_users'], labels=top_skills['Skill'], autopct='%1.1f%%', colors=['#ff9999','#66b3ff','#99ff99','#ffcc99','#c2c2f0'])
plt.title('Top 5 Skills with Most Users at Level 99')
st.pyplot(plt)

# Show some additional information and user guidance
st.markdown("""
    ## How to Use This Dashboard
    - **Sidebar**: Use the slider to filter the dataset by the minimum number of users with level 99.
    - **Bar Chart**: View the number of users who have achieved level 99 in each skill.
    - **Pie Chart**: See a visual representation of the top 5 skills with the highest number of level 99 users.
""")
