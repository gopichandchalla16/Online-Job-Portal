import streamlit as st
import pandas as pd
from datetime import datetime
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import random

# Download NLTK data
nltk.download('punkt')
nltk.download('stopwords')

# App Configuration
st.set_page_config(page_title="CareerConnect |  Your Dream Job Awaits!", layout="wide")

# Theme Toggle
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

# Sample Job Data
jobs_data = pd.DataFrame({
    'Job ID': [1, 2, 3, 4, 5],
    'Job Title': ['Data Analyst', 'Frontend Developer', 'UI/UX Designer', 'Product Manager', 'Machine Learning Engineer'],
    'Company': ['TechCorp', 'WebSolutions', 'DesignHub', 'Innovate', 'AIWorks'],
    'Location': ['Bengaluru', 'Remote', 'Hyderabad', 'Mumbai', 'Delhi'],
    'Industry': ['IT', 'Web Development', 'Design', 'Product', 'AI'],
    'Experience': ['1-2 years', '0-1 year', '2-4 years', '3-5 years', '2-3 years'],
    'Description': ['Analyze data trends...', 'Build responsive interfaces...', 'Design user flows...', 'Lead product strategy...', 'Develop ML models...'],
    'Salary_Range': ['₹6-8 LPA', '₹4-6 LPA', '₹8-10 LPA', '₹12-15 LPA', '₹10-14 LPA'],
    'Rating': [4.5, 4.2, 4.8, 4.0, 4.7],
    'Required_Skills': ['Python, SQL, Excel', 'HTML, CSS, JavaScript', 'Figma, Adobe XD', 'Agile, Leadership', 'Python, TensorFlow']
})

# Session State Initialization
if "saved_jobs" not in st.session_state:
    st.session_state.saved_jobs = set()
if "applications" not in st.session_state:
    st.session_state.applications = {}
if "profile" not in st.session_state:
    st.session_state.profile = {}
if "alerts" not in st.session_state:
    st.session_state.alerts = []
if "portfolio" not in st.session_state:
    st.session_state.portfolio = []
if "certifications" not in st.session_state:
    st.session_state.certifications = []
if "interview_experiences" not in st.session_state:
    st.session_state.interview_experiences = []
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# App Title
st.title("🎯 CareerConnect")
st.caption("Your AI-Powered Career Companion")
st.markdown("---")

# Sidebar: Navigation and Filters
st.sidebar.header("🔍 Search & Filters")
search_query = st.sidebar.text_input("Search by Job Title or Company")
location_filter = st.sidebar.selectbox("Location", options=['All'] + list(jobs_data['Location'].unique()))
industry_filter = st.sidebar.selectbox("Industry", options=['All'] + list(jobs_data['Industry'].unique()))

# Profile Completeness Score
st.sidebar.header("👤 Your Profile")
if st.session_state.profile:
    completeness = sum(1 for key in ['name', 'email', 'experience', 'skills'] if key in st.session_state.profile and st.session_state.profile[key]) / 4 * 100
    st.sidebar.write(f"**Profile Completeness**: {int(completeness)}%")
    st.sidebar.progress(int(completeness))
else:
    st.sidebar.write("**Profile Completeness**: 0%")
    st.sidebar.progress(0)

# Job Listings with Employer Insights
st.subheader("📋 Job Listings")
filtered_jobs = jobs_data[
    (jobs_data['Job Title'].str.contains(search_query, case=False, na=False)) &
    ((jobs_data['Location'] == location_filter) | (location_filter == 'All')) &
    ((jobs_data['Industry'] == industry_filter) | (industry_filter == 'All'))
]
if filtered_jobs.empty:
    st.info("No jobs match your search. Try changing filters.")

company_reviews = {
    "TechCorp": ["Great work culture!", "Good benefits.", 4.5],
    "WebSolutions": ["Flexible hours.", "Remote-friendly.", 4.2],
    "DesignHub": ["Creative environment.", "Limited growth.", 4.8],
    "Innovate": ["Innovative projects.", "High pressure.", 4.0],
    "AIWorks": ["Cutting-edge tech.", "Fast-paced.", 4.7]
}

for idx, row in filtered_jobs.iterrows():
    with st.expander(f"{row['Job Title']} at {row['Company']} ({row['Location']})"):
        st.write(f"**Industry:** {row['Industry']}")
        st.write(f"**Experience:** {row['Experience']}")
        st.write(f"**Salary Range:** {row['Salary_Range']}")
        st.write(f"**Company Rating:** {row['Rating']}/5")
        if row['Company'] in company_reviews:
            st.write(f"**Employer Insight**: {company_reviews[row['Company']][0]}")
        st.write(f"**Required Skills:** {row['Required_Skills']}")
        st.write(f"**Description:** {row['Description']}")
        if "profile" in st.session_state and "skills" in st.session_state.profile:
            user_skills = set(st.session_state.profile["skills"].lower().split(", "))
            req_skills = set(row['Required_Skills'].lower().split(", "))
            fit_score = len(user_skills.intersection(req_skills)) / len(req_skills) * 100 if req_skills else 0
            st.write(f"**Job Fit Score**: {int(fit_score)}%")
            success_score = (fit_score * 0.7) + (completeness * 0.3)  # Weighted score
            st.write(f"**Application Success Predictor**: {int(success_score)}% chance of success")
        col1, col2, col3 = st.columns([1, 1, 1])
        with col1:
            if st.button("💾 Save Job", key=f"save_{row['Job ID']}"):
                st.session_state.saved_jobs.add(row['Job ID'])
                st.success("Job saved!")
        with col2:
            if st.button("✅ Mark as Applied", key=f"apply_{row['Job ID']}"):
                st.session_state.applications[row['Job ID']] = {"status": "Applied", "date": datetime.now().strftime("%Y-%m-%d")}
                st.success("Marked as Applied")
        with col3:
            if st.button("🚀 Quick Apply", key=f"quick_{row['Job ID']}") and "profile" in st.session_state:
                st.session_state.applications[row['Job ID']] = {"status": "Applied (Quick)", "date": datetime.now().strftime("%Y-%m-%d")}
                st.success("Quick Applied with your profile!")

# Saved Jobs Tracker
st.markdown("---")
st.subheader("⭐ Saved Jobs")
saved_jobs = jobs_data[jobs_data['Job ID'].isin(st.session_state.saved_jobs)]
if saved_jobs.empty:
    st.info("No saved jobs.")
else:
    st.table(saved_jobs[['Job Title', 'Company', 'Location', 'Salary_Range']])

# User Profiles & Resume Builder with Templates
st.markdown("---")
st.subheader("📄 User Profile & Resume Builder")
with st.form("resume_form"):
    name = st.text_input("Full Name")
    email = st.text_input("Email")
    experience = st.text_area("Experience Summary (e.g., Job Title - Company - Years)")
    skills = st.text_input("Key Skills (comma-separated)")
    resume_file = st.file_uploader("Upload Your Resume (PDF)", type=['pdf'])
    cover_letter_file = st.file_uploader("Upload Cover Letter (Optional)", type=['pdf'])
    template = st.selectbox("Resume Template", ["Modern", "Creative", "Professional"])
    submitted = st.form_submit_button("Save Profile & Generate Resume")
    if submitted:
        if name and email and experience and skills:
            st.session_state.profile = {"name": name, "email": email, "experience": experience, "skills": skills}
            st.success("✅ Profile saved successfully!")
            if template == "Modern":
                resume_text = f"**{name}**\n{email}\n\n**Skills**: {skills}\n\n**Experience**: {experience}"
            elif template == "Creative":
                resume_text = f"✨ {name} ✨\n📧 {email}\n\n🎨 **Skills**: {skills}\n\n🌟 **Experience**: {experience}"
            else:  # Professional
                resume_text = f"{name}\n{email}\n\nSkills:\n{skills}\n\nProfessional Experience:\n{experience}"
            st.text_area("Generated Resume Preview", resume_text, height=300)
            if resume_file:
                st.write("**Resume Uploaded:** ✅")
                resume_content = experience + " " + skills
                tokens = word_tokenize(resume_content.lower())
                stop_words = set(stopwords.words('english'))
                keywords = [word for word in tokens if word not in stop_words and word.isalpha()]
                job_keywords = "python, sql, javascript, leadership, design, communication"
                missing = [kw for kw in job_keywords.split(", ") if kw not in keywords]
                st.write("**AI Resume Analysis**:")
                if missing:
                    st.write(f"- **Missing Keywords**: {', '.join(missing)}")
                else:
                    st.write("- **Analysis**: Your resume is well-optimized!")
            if cover_letter_file:
                st.write("**Cover Letter Uploaded:** ✅")
        else:
            st.warning("⚠️ Please fill all required fields.")

# Applicant Tracking
st.markdown("---")
st.subheader("📌 Applicant Tracking")
if st.session_state.applications:
    app_data = []
    for job_id, details in st.session_state.applications.items():
        job = jobs_data[jobs_data['Job ID'] == job_id].iloc[0]
        app_data.append({
            "Job Title": job['Job Title'],
            "Company": job['Company'],
            "Status": details["status"],
            "Date Applied": details["date"]
        })
    st.table(pd.DataFrame(app_data))
else:
    st.info("No job applications yet.")

# Employer Insights
st.markdown("---")
st.subheader("🏢 Employer Insights")
for company, (review1, review2, rating) in company_reviews.items():
    with st.expander(f"{company} ({rating}/5)"):
        st.write(f"- {review1}")
        st.write(f"- {review2}")

# Career Resources
st.markdown("---")
st.subheader("🎯 Career Resources")
st.markdown("- 💡 [Resume Writing Tips](https://www.linkedin.com/learning/) - Keep it concise, use action verbs.")
st.markdown("- 🎤 [Interview Guidance](https://www.indeed.com/career-advice/interviewing) - Practice common questions.")
st.markdown("- 📚 [Free Courses](https://www.coursera.org/) - Upskill with free resources.")

# Interactive Chatbot
st.markdown("---")
st.subheader("🤖 CareerConnect Chatbot")
with st.form("chat_form"):
    user_query = st.text_input("Ask me anything (e.g., 'How to improve my resume?')")
    submitted = st.form_submit_button("Send")
    if submitted and user_query:
        st.session_state.chat_history.append({"user": user_query, "bot": ""})
        query_lower = user_query.lower()
        if "resume" in query_lower:
            st.session_state.chat_history[-1]["bot"] = "To improve your resume, add keywords like 'Python' or 'SQL' from job descriptions, keep it to 1-2 pages, and use action verbs like 'developed' or 'led'."
        elif "interview" in query_lower:
            st.session_state.chat_history[-1]["bot"] = "Prepare for interviews by researching the company, practicing STAR method answers (Situation, Task, Action, Result), and dressing professionally."
        elif "job search" in query_lower:
            st.session_state.chat_history[-1]["bot"] = "For a better job search, use specific keywords in filters, set alerts, and network with employers via messages."
        else:
            st.session_state.chat_history[-1]["bot"] = "I’m here to help! Try asking about resumes, interviews, or job search strategies."
for chat in st.session_state.chat_history:
    st.write(f"**You**: {chat['user']}")
    st.write(f"**Bot**: {chat['bot']}")

# Job Application Success Predictor (Moved to Job Listings)

# Employer Contact Simulator
st.markdown("---")
st.subheader("📩 Employer Contact Simulator")
selected_company = st.selectbox("Select Employer", jobs_data["Company"].unique())
message = st.text_area("Message to Employer")
if st.button("Send Message"):
    st.success(f"Message sent to {selected_company}! (Simulated)")

# Resume Visibility Booster
st.markdown("---")
st.subheader("✨ Resume Visibility Booster")
if "profile" in st.session_state:
    st.write("**Current Profile Strength**:")
    if len(st.session_state.profile.get("skills", "").split(", ")) < 5:
        st.write("- Add more skills (aim for 5+) to stand out.")
    if not st.session_state.portfolio:
        st.write("- Add projects to your portfolio for visibility.")
    if not resume_file:
        st.write("- Upload a resume file to boost employer interest.")
else:
    st.info("Complete your profile to boost visibility!")

# Job Seeker Dashboard
st.markdown("---")
st.subheader("📊 Job Seeker Dashboard")
apps_count = len(st.session_state.applications)
alerts_count = len(st.session_state.alerts)
profile_views = random.randint(0, 50)  # Simulated
st.write(f"**Applications Submitted**: {apps_count}")
st.write(f"**Active Alerts**: {alerts_count}")
st.write(f"**Profile Views (Simulated)**: {profile_views}")
st.bar_chart({"Applications": [apps_count], "Alerts": [alerts_count], "Views": [profile_views]})

# Interview Experience Sharing
st.markdown("---")
st.subheader("🎤 Interview Experience Sharing")
with st.form("interview_exp_form"):
    company = st.text_input("Company Name")
    exp = st.text_area("Your Interview Experience")
    submitted = st.form_submit_button("Share Experience")
    if submitted:
        st.session_state.interview_experiences.append({"company": company, "exp": exp})
        st.success("Experience shared!")
if st.session_state.interview_experiences:
    for exp in st.session_state.interview_experiences:
        st.write(f"**{exp['company']}**: {exp['exp']}")

# Skill Certification Tracker
st.markdown("---")
st.subheader("🏆 Skill Certification Tracker")
with st.form("cert_form"):
    cert_name = st.text_input("Certification Name")
    date = st.date_input("Completion Date")
    submitted = st.form_submit_button("Add Certification")
    if submitted:
        st.session_state.certifications.append({"name": cert_name, "date": date.strftime("%Y-%m-%d")})
        st.success("Certification added!")
if st.session_state.certifications:
    st.table(pd.DataFrame(st.session_state.certifications))

# Footer
st.markdown("---")
st.markdown("<div style='text-align: center; color: gray;'>© 2025 CareerConnect — Inspired by LinkedIn, Indeed, and Naukri</div>", unsafe_allow_html=True)
