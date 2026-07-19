import streamlit as st

st.title("Talk to Agent")
st.write("This app demonstrates a conversational agent.")   

# Take Obtained Marks
obtMarks=st.number_input("Enter Obtained Marks:", min_value=0, max_value=1100, step=1)
totalMarks=st.number_input("Enter Total Marks:", min_value=0, max_value=1100, step=1)

# File Input
uploaded_file = st.file_uploader("Choose a file")
# User name
user_name = st.text_input("Enter your name:")
# Dropdown for selecting a course
course = st.selectbox("Select a course:", ["Web with Agentic AI", "Data Science"])

# Calculate Percentage
if st.button("Calculate Percentage"):
    if totalMarks > 0:
        percentage = (obtMarks / totalMarks) * 100
        st.write(f"Percentage: {percentage:.2f}%")
    else:
        st.write("Total Marks must be greater than 0.")