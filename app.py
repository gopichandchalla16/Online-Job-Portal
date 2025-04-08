import streamlit as st
from datetime import datetime
import pandas as pd
import random

# Custom CSS for enhanced UI
st.markdown("""
    <style>
    .main {
        background-color: #f0f2f6;
        padding: 20px;
    }
    .title {
        font-size: 40px;
        color: #2c3e50;
        text-align: center;
    }
    .sidebar .sidebar-content {
        background-color: #34495e;
        color: white;
    }
    .stButton>button {
        background-color: #3498db;
        color: white;
        border-radius: 5px;
    }
    .stTextInput>div>div>input {
        border-radius: 5px;
    }
    </style>
""", unsafe_allow_html=True)

# App Title
st.markdown('<p class="title">JobQuest: Your Career Journey Starts Here</p>', unsafe_allow_html=True)

# Sidebar Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "Profile", "Job Listings", "Resume Builder", 
                                 "Applications", "Career Resources"])

# Sample Data (No API keys, so using static data)
job_listings = pd.DataFrame({
    "Title": ["Software Engineer", "Data Analyst", "Product Manager", "Graphic Designer"],
    "Company": ["TechCorp", "DataWorks", "Innovate", "DesignHub"],
    "Location": ["Remote", "New York", "San Francisco", "London"],
    "Industry": ["Tech", "Analytics", "Product", "Design"],
    "Rating": [4.5, 4.2, 4.8, 4.0]
})

# Home Page
if page == "Home":
    st.header("Welcome to JobQuest!")
    st.write("Find your dream job, build a standout resume, and track your applications all in one place.")
    st.image("https://via.placeholder.com/800x300.png?text=JobQuest+Banner", use_column_width=True)
    st.write("Current Date: April 08, 2025")  # Static date as per prompt

# User Profile Page
elif page == "Profile":
    st.header("Your Profile")
    with st.form("profile_form"):
        name = st.text_input("Full Name")
        email = st.text_input("Email")
        experience = st.text_area("Work Experience (e.g., Job Title - Company - Years)")
        skills = st.text_input("Skills (comma-separated)")
        submitted = st.form_submit_button("Save Profile")
        if submitted:
            st.session_state["profile"] = {"name": name, "email": email, 
                                         "experience": experience, "skills": skills}
            st.success("Profile saved successfully!")

    if "profile" in st.session_state:
        st.subheader("Your Saved Profile")
        st.write(st.session_state["profile"])

# Job Listings Page
elif page == "Job Listings":
    st.header("Explore Job Listings")
    location_filter = st.multiselect("Filter by Location", job_listings["Location"].unique())
    industry_filter = st.multiselect("Filter by Industry", job_listings["Industry"].unique())

    filtered_jobs = job_listings
    if location_filter:
        filtered_jobs = filtered_jobs[filtered_jobs["Location"].isin(location_filter)]
    if industry_filter:
        filtered_jobs = filtered_jobs[filtered_jobs["Industry"].isin(industry_filter)]

    st.dataframe(filtered_jobs)

    selected_job = st.selectbox("View Employer Insights", filtered_jobs["Title"])
    job_details = filtered_jobs[filtered_jobs["Title"] == selected_job].iloc[0]
    st.subheader(f"{job_details['Company']} Insights")
    st.write(f"Rating: {job_details['Rating']}/5")
    st.write(f"Location: {job_details['Location']}")
    st.write(f"Industry: {job_details['Industry']}")

# Resume Builder Page
elif page == "Resume Builder":
    st.header("Build Your Resume")
    template = st.selectbox("Choose a Template", ["Modern", "Classic", "Creative"])
    if "profile" in st.session_state:
        profile = st.session_state["profile"]
        st.subheader(f"{template} Resume Preview")
        st.write(f"**Name**: {profile['name']}")
        st.write(f"**Email**: {profile['email']}")
        st.write(f"**Skills**: {profile['skills']}")
        st.write(f"**Experience**:")
        st.write(profile['experience'])
        if st.button("Download Resume"):
            st.write("Download functionality placeholder (requires local deployment)")
    else:
        st.warning("Please create a profile first!")

# Applicant Tracking Page
elif page == "Applications":
    st.header("Track Your Applications")
    if "applications" not in st.session_state:
        st.session_state["applications"] = []

    with st.form("application_form"):
        job_title = st.text_input("Job Title")
        company = st.text_input("Company")
        status = st.selectbox("Status", ["Applied", "Interview", "Offer", "Rejected"])
        submitted = st.form_submit_button("Add Application")
        if submitted:
            st.session_state["applications"].append({"Job Title": job_title, 
                                                    "Company": company, 
                                                    "Status": status, 
                                                    "Date": datetime.now().strftime("%Y-%m-%d")})
            st.success("Application added!")

    if st.session_state["applications"]:
        st.subheader("Your Applications")
        st.dataframe(pd.DataFrame(st.session_state["applications"]))

# Career Resources Page
elif page == "Career Resources":
    st.header("Career Resources")
    st.subheader("Resume Tips")
    st.write("- Keep it concise (1-2 pages).")
    st.write("- Use action verbs (e.g., 'Developed', 'Led').")
    st.subheader("Interview Guidance")
    st.write("- Research the company beforehand.")
    st.write("- Practice common questions.")
    st.button("Generate Random Interview Question", 
              on_click=lambda: st.write(f"Q: {random.choice(['Tell me about yourself.', 'Why this role?', 'What’s your strength?'])}"))

# Footer
st.markdown("---")
st.write("© 2025 JobQuest | Built for Job seekers
