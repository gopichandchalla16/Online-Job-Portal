import streamlit as st
from datetime import datetime
import pandas as pd
import random
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

# Download NLTK data (no API keys needed)
nltk.download('punkt')
nltk.download('stopwords')

# Custom CSS with Job-Seeker Themes
def load_css(theme="Professional"):
    if theme == "Professional":  # Dark Blue Professional Theme
        st.markdown("""
            <style>
            .main {
                background-color: #eef2f7;
                padding: 20px;
            }
            .title {
                font-size: 40px;
                color: #1e3a8a;
                text-align: center;
            }
            .sidebar .sidebar-content {
                background-color: #1e3a8a;
                color: white;
            }
            .stButton>button {
                background-color: #3b82f6;
                color: white;
                border-radius: 5px;
            }
            .stTextInput>div>div>input {
                border-radius: 5px;
                border: 1px solid #1e3a8a;
            }
            </style>
        """, unsafe_allow_html=True)
    elif theme == "Clean Blue":  # Light Blue Modern Theme
        st.markdown("""
            <style>
            .main {
                background-color: #f0f9ff;
                padding: 20px;
            }
            .title {
                font-size: 40px;
                color: #0369a1;
                text-align: center;
            }
            .sidebar .sidebar-content {
                background-color: #0369a1;
                color: white;
            }
            .stButton>button {
                background-color: #60a5fa;
                color: white;
                border-radius: 5px;
            }
            .stTextInput>div>div>input {
                border-radius: 5px;
                border: 1px solid #0369a1;
            }
            </style>
        """, unsafe_allow_html=True)
    elif theme == "Success Green":  # Green Motivational Theme
        st.markdown("""
            <style>
            .main {
                background-color: #f0fdf4;
                padding: 20px;
            }
            .title {
                font-size: 40px;
                color: #15803d;
                text-align: center;
            }
            .sidebar .sidebar-content {
                background-color: #15803d;
                color: white;
            }
            .stButton>button {
                background-color: #4ade80;
                color: white;
                border-radius: 5px;
            }
            .stTextInput>div>div>input {
                border-radius: 5px;
                border: 1px solid #15803d;
            }
            </style>
        """, unsafe_allow_html=True)

# Initialize Session State
if "theme" not in st.session_state:
    st.session_state["theme"] = "Professional"
if "saved_jobs" not in st.session_state:
    st.session_state["saved_jobs"] = []
if "goals" not in st.session_state:
    st.session_state["goals"] = []

# Sidebar Navigation and Theme Selector
st.sidebar.title("Navigation")
theme = st.sidebar.selectbox("Choose Theme", ["Professional", "Clean Blue", "Success Green"], 
                             index=["Professional", "Clean Blue", "Success Green"].index(st.session_state["theme"]))
st.session_state["theme"] = theme
load_css(theme)
page = st.sidebar.radio("Go to", ["Home", "Profile", "Job Listings", "Resume Builder", 
                                 "Applications", "Career Resources", "Career Goals", "Mock Interview"])

# App Title
st.markdown('<p class="title">JobQuest: Your Career Journey Starts Here</p>', unsafe_allow_html=True)

# Sample Job Data
job_listings = pd.DataFrame({
    "Title": ["Software Engineer", "Data Analyst", "Product Manager", "Graphic Designer"],
    "Company": ["TechCorp", "DataWorks", "Innovate", "DesignHub"],
    "Location": ["Remote", "New York", "San Francisco", "London"],
    "Industry": ["Tech", "Analytics", "Product", "Design"],
    "Rating": [4.5, 4.2, 4.8, 4.0],
    "Required_Skills": ["Python, Java, C++", "SQL, Excel, Python", "Agile, UX, Leadership", "Photoshop, Illustrator, UI"]
})

# Home Page with Motivational Dashboard
if page == "Home":
    st.header("Welcome to JobQuest!")
    st.write("Connect with employers, build your career, and land your dream job!")
    st.image("https://via.placeholder.com/800x300.png?text=JobQuest+Banner", use_column_width=True)
    st.write("Current Date: April 08, 2025")
    st.subheader("Motivational Corner")
    quotes = ["The only way to do great work is to love what you do. – Steve Jobs", 
              "Opportunities don’t happen. You create them. – Chris Grosser"]
    st.write(random.choice(quotes))
    st.write("**Fun Fact**: Over 70% of job seekers find jobs through networking!")

# User Profile Page with Skill Extraction
elif page == "Profile":
    st.header("Your Profile")
    with st.form("profile_form"):
        name = st.text_input("Full Name")
        email = st.text_input("Email")
        experience = st.text_area("Work Experience (e.g., Job Title - Company - Years)")
        skills = st.text_input("Skills (comma-separated)")
        submitted = st.form_submit_button("Save Profile")
        if submitted:
            # NLTK Skill Extraction from Experience
            tokens = word_tokenize(experience.lower())
            stop_words = set(stopwords.words('english'))
            extracted_skills = [word for word in tokens if word not in stop_words and word.isalpha() and len(word) > 2]
            st.session_state["profile"] = {"name": name, "email": email, 
                                         "experience": experience, "skills": skills, 
                                         "extracted_skills": ", ".join(extracted_skills[:5])}
            st.success("Profile saved successfully!")

    if "profile" in st.session_state:
        st.subheader("Your Saved Profile")
        st.write(st.session_state["profile"])
        st.write(f"**Extracted Skills from Experience**: {st.session_state['profile']['extracted_skills']}")

# Job Listings Page with Enhanced Recommendations
elif page == "Job Listings":
    st.header("Explore Job Listings")
    location_filter = st.multiselect("Filter by Location", job_listings["Location"].unique())
    industry_filter = st.multiselect("Filter by Industry", job_listings["Industry"].unique())

    filtered_jobs = job_listings
    if location_filter:
        filtered_jobs = filtered_jobs[filtered_jobs["Location"].isin(location_filter)]
    if industry_filter:
        filtered_jobs = filtered_jobs[filtered_jobs["Industry"].isin(industry_filter)]

    if "profile" in st.session_state and "skills" in st.session_state["profile"]:
        user_skills = [skill.strip().lower() for skill in st.session_state["profile"]["skills"].split(",")]
        filtered_jobs["Match_Score"] = filtered_jobs["Required_Skills"].apply(
            lambda req: sum(1 for skill in user_skills if skill in req.lower()) / len(req.split(",")) * 100
        )
    else:
        filtered_jobs["Match_Score"] = 0

    st.dataframe(filtered_jobs)

    selected_job = st.selectbox("View Employer Insights or Save Job", filtered_jobs["Title"])
    job_details = filtered_jobs[filtered_jobs["Title"] == selected_job].iloc[0]
    st.subheader(f"{job_details['Company']} Insights")
    st.write(f"Rating: {job_details['Rating']}/5")
    st.write(f"Location: {job_details['Location']}")
    st.write(f"Industry: {job_details['Industry']}")
    st.write(f"Required Skills: {job_details['Required_Skills']}")
    st.write(f"Match Score: {job_details['Match_Score']:.1f}%")
    if st.button("Save Job"):
        if selected_job not in st.session_state["saved_jobs"]:
            st.session_state["saved_jobs"].append(selected_job)
            st.success(f"Saved {selected_job}!")
        else:
            st.warning("Job already saved!")

    if st.session_state["saved_jobs"]:
        st.subheader("Saved Jobs")
        st.write(st.session_state["saved_jobs"])

# Resume Builder Page with Keyword Optimizer
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
        
        # Keyword Optimizer with NLTK
        st.subheader("Keyword Optimizer")
        job_keywords = "python, sql, leadership, design, communication, teamwork"
        resume_text = f"{profile['skills']} {profile['experience']}".lower()
        tokens = word_tokenize(resume_text)
        stop_words = set(stopwords.words('english'))
        resume_keywords = [word for word in tokens if word not in stop_words and word.isalpha()]
        missing_keywords = [kw for kw in job_keywords.split(", ") if kw not in resume_keywords]
        if missing_keywords:
            st.write(f"**Suggested Keywords to Add**: {', '.join(missing_keywords)}")
        else:
            st.write("Your resume is well-optimized!")
        
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

# Career Goals Page
elif page == "Career Goals":
    st.header("Career Goal Tracker")
    with st.form("goal_form"):
        goal = st.text_input("Enter a Career Goal (e.g., Get a Tech Job)")
        progress = st.slider("Progress (%)", 0, 100, 0)
        submitted = st.form_submit_button("Add Goal")
        if submitted:
            st.session_state["goals"].append({"Goal": goal, "Progress": progress})
            st.success("Goal added!")

    if st.session_state["goals"]:
        st.subheader("Your Goals")
        for i, g in enumerate(st.session_state["goals"]):
            st.write(f"{g['Goal']} - Progress: {g['Progress']}%")
            st.progress(g["Progress"] / 100)

# Mock Interview Simulator
elif page == "Mock Interview":
    st.header("Mock Interview Simulator")
    questions = ["Tell me about yourself.", "What’s your greatest strength?", 
                 "Why do you want this job?", "Describe a challenge you faced."]
    if "current_question" not in st.session_state:
        st.session_state["current_question"] = random.choice(questions)

    st.write(f"**Question**: {st.session_state['current_question']}")
    answer = st.text_area("Your Answer")
    if st.button("Submit Answer"):
        feedback = random.choice(["Great response! You highlighted your skills well.", 
                                  "Good, but try to be more concise.", 
                                  "Nice effort! Add more specific examples."])
        st.write(f"**Feedback**: {feedback}")
    if st.button("Next Question"):
        st.session_state["current_question"] = random.choice(questions)
        st.experimental_rerun()

# Footer
st.markdown("---")
st.write("© 2025 JobQuest | Built for Job Seekers | Inspired by LinkedIn & Indeed")
