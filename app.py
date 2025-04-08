import streamlit as st
import pandas as pd
import os
from datetime import datetime

# App Configuration
st.set_page_config(page_title="CareerConnect | Your Dream Job Awaits!", layout="wide")

# Theme Toggle (Dark Mode Switch)
if "theme" not in st.session_state:
    st.session_state.theme = "Light"

selected_theme = st.sidebar.selectbox("🌓 Theme", ["Light", "Dark"], index=0 if st.session_state.theme == "Light" else 1)
if selected_theme != st.session_state.theme:
    st.session_state.theme = selected_theme
    st.sidebar.success("Theme updated! Please refresh the app manually.")

if st.session_state.theme == "Dark":
    st.markdown("""
        <style>
            body { background-color: #1e1e1e; color: white; }
            .stApp { background-color: #2c2c2c; }
        </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
        <style>
            body { background-color: #f0f2f6; }
        </style>
    """, unsafe_allow_html=True)

# Sample Job Data (Can be replaced with CSV/database)
jobs_data = pd.DataFrame({
    'Job ID': [1, 2, 3],
    'Job Title': ['Data Analyst', 'Frontend Developer', 'UI/UX Designer'],
    'Company': ['TechCorp', 'WebSolutions', 'DesignHub'],
    'Location': ['Bengaluru', 'Remote', 'Hyderabad'],
    'Industry': ['IT', 'Web Development', 'Design'],
    'Experience': ['1-2 years', '0-1 year', '2-4 years'],
    'Description': ['Analyze data...', 'Build interfaces...', 'Design user flows...']
})

# Session state for saved jobs and applications
if "saved_jobs" not in st.session_state:
    st.session_state.saved_jobs = set()
if "applications" not in st.session_state:
    st.session_state.applications = {}

# App Title
st.title("🎯 CareerConnect")
st.caption("Empowering Careers, One Job at a Time")
st.markdown("---")

# Sidebar: Navigation
st.sidebar.header("🔍 Search & Filters")
search_query = st.sidebar.text_input("Search by Job Title or Company")
location_filter = st.sidebar.selectbox("Location", options=['All'] + list(jobs_data['Location'].unique()))
industry_filter = st.sidebar.selectbox("Industry", options=['All'] + list(jobs_data['Industry'].unique()))

# Filter jobs
filtered_jobs = jobs_data[
    (jobs_data['Job Title'].str.contains(search_query, case=False)) &
    ((jobs_data['Location'] == location_filter) | (location_filter == 'All')) &
    ((jobs_data['Industry'] == industry_filter) | (industry_filter == 'All'))
]

# Main Area: Job Listings
st.subheader("📋 Job Listings")
if filtered_jobs.empty:
    st.info("No jobs match your search. Try changing filters.")

for idx, row in filtered_jobs.iterrows():
    with st.expander(f"{row['Job Title']} at {row['Company']} ({row['Location']})"):
        st.write(f"**Industry:** {row['Industry']}")
        st.write(f"**Experience:** {row['Experience']}")
        st.write(f"**Description:** {row['Description']}")
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("💾 Save Job", key=f"save_{row['Job ID']}"):
                st.session_state.saved_jobs.add(row['Job ID'])
                st.success("Job saved!")
        with col2:
            if st.button("✅ Mark as Applied", key=f"apply_{row['Job ID']}"):
                st.session_state.applications[row['Job ID']] = "Applied"
                st.success("Marked as Applied")

# Saved Jobs Tracker
st.markdown("---")
st.subheader("⭐ Saved Jobs")
saved_jobs = jobs_data[jobs_data['Job ID'].isin(st.session_state.saved_jobs)]
if saved_jobs.empty:
    st.info("No saved jobs.")
else:
    st.table(saved_jobs[['Job Title', 'Company', 'Location']])

# Resume Builder and Upload
st.markdown("---")
st.subheader("📄 Resume Builder & Upload")
with st.form("resume_form"):
    name = st.text_input("Full Name")
    email = st.text_input("Email")
    experience = st.text_area("Experience Summary")
    skills = st.text_input("Key Skills (comma-separated)")
    resume_file = st.file_uploader("Upload Your Resume (PDF)", type=['pdf'])
    cover_letter_file = st.file_uploader("Upload Cover Letter (Optional)", type=['pdf'])
    submitted = st.form_submit_button("Submit Resume")
    if submitted:
        if resume_file:
            st.success("✅ Resume submitted successfully!")
            st.write(f"**Name:** {name}")
            st.write(f"**Email:** {email}")
            st.write(f"**Experience:** {experience}")
            st.write(f"**Skills:** {skills}")
            st.write("**Resume Uploaded:** ✅")
            if cover_letter_file:
                st.write("**Cover Letter Uploaded:** ✅")
        else:
            st.warning("⚠️ Please upload your resume before submitting.")

# Job Posting (for Employers)
st.markdown("---")
st.subheader("📢 Post a Job (Employers)")
with st.form("post_job"):
    job_title = st.text_input("Job Title")
    company = st.text_input("Company")
    location = st.text_input("Location")
    industry = st.text_input("Industry")
    exp = st.text_input("Experience Required")
    desc = st.text_area("Job Description")
    post = st.form_submit_button("Post Job")
    if post:
        st.success("🚀 Job Posted (Demo only — not saved)")

# Application Tracker
st.markdown("---")
st.subheader("📌 Application Status")
if st.session_state.applications:
    for job_id, status in st.session_state.applications.items():
        job = jobs_data[jobs_data['Job ID'] == job_id].iloc[0]
        st.write(f"{job['Job Title']} at {job['Company']} — **Status:** {status}")
else:
    st.info("No job applications yet.")

# Career Resources
st.markdown("---")
st.subheader("🎯 Career Resources")
st.markdown("- 💡 [Resume Writing Tips](https://www.linkedin.com/learning/)")
st.markdown("- 🎤 [Interview Guidance](https://www.indeed.com/career-advice/interviewing)")
st.markdown("- 📚 [Free Courses](https://www.coursera.org/)")

# Feedback Section
st.markdown("---")
st.subheader("💬 Feedback")
with st.form("feedback_form"):
    user_feedback = st.text_area("Let us know how we can improve!")
    send = st.form_submit_button("Submit Feedback")
    if send:
        st.success("🙏 Thank you for your feedback!")

# Footer
st.markdown("---")
st.markdown("<div style='text-align: center; color: gray;'>© 2025 CareerConnect — Designed to Connect Talent with Opportunity</div>", unsafe_allow_html=True)
