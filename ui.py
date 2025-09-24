import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# -------------------
# Page Configuration
# -------------------
st.set_page_config(
    page_title="Smart Internship Allocation Platform",
    layout="wide",
    page_icon="🎯",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
    }
    
    .metric-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin: 0.5rem 0;
    }
    
    .student-card {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    .company-card {
        background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    .match-card {
        background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
</style>
""", unsafe_allow_html=True)

# -------------------
# Data Loading
# -------------------
@st.cache_data
def load_data():
    try:
        students = pd.read_csv("data/students.csv")
        internships = pd.read_csv("data/internships.csv")
        return students, internships
    except FileNotFoundError:
        st.error("CSV files not found. Please ensure 'students.csv' and 'internships.csv' are in the 'data' folder.")
        return None, None

students, internships = load_data()

if students is None or internships is None:
    st.stop()

# -------------------
# Header
# -------------------
st.markdown("""
<div class="main-header">
    <h1>🎯 Smart Internship Allocation Platform</h1>
    <p>Connecting talented students with perfect internship opportunities</p>
</div>
""", unsafe_allow_html=True)

# -------------------
# Sidebar Configuration
# -------------------
with st.sidebar:
    st.markdown("### 🔧 Platform Controls")
    
    view_mode = st.radio(
        "Select View Mode:",
        ["🎓 Student View", "🏢 Company View", "📊 Analytics Dashboard"]
    )
    
    st.markdown("---")
    
    # Filters
    st.markdown("### 🔍 Filters")
    
    if view_mode == "🎓 Student View":
        selected_student = st.selectbox("Select Student", students["name"].tolist())
        location_filter = st.multiselect("Filter by Location", internships["location"].unique())
        sector_filter = st.multiselect("Filter by Sector", internships["sector"].unique())
    
    elif view_mode == "🏢 Company View":
        selected_company = st.selectbox("Select Company", internships["company_name"].tolist())
        category_filter = st.multiselect("Filter by Student Category", students["category"].unique())
        student_location_filter = st.multiselect("Filter by Student Location", students["location"].unique())

# -------------------
# Core Functions
# -------------------
def calculate_student_company_match(student, internship):
    """Calculate comprehensive match score between student and internship"""
    
    # Skill matching
    student_skills = set([s.strip().lower() for s in student["skills"].split(",")])
    internship_skills = set([s.strip().lower() for s in internship["required_skills"].split(",")])
    skill_overlap = len(student_skills.intersection(internship_skills))
    skill_score = skill_overlap / len(internship_skills) if len(internship_skills) > 0 else 0
    
    # Location matching
    location_score = 1.0 if student["location"].lower() == internship["location"].lower() else 0.3
    
    # Category bonus (if applicable)
    category_bonus = 0.1 if hasattr(student, 'category') and student.get('category') == 'Premium' else 0
    
    # Calculate total score
    total_score = (skill_score * 0.6) + (location_score * 0.3) + (category_bonus * 0.1)
    
    return {
        'total_score': total_score,
        'skill_score': skill_score,
        'location_score': location_score,
        'skill_overlap': skill_overlap,
        'matching_skills': list(student_skills.intersection(internship_skills))
    }

def get_student_recommendations(student, top_n=5):
    """Get top internship recommendations for a student"""
    matches = []
    
    for idx, internship in internships.iterrows():
        match_info = calculate_student_company_match(student, internship)
        if match_info['skill_overlap'] > 0:  # Only include if there's skill overlap
            matches.append((match_info['total_score'], internship, match_info))
    
    matches.sort(reverse=True, key=lambda x: x[0])
    return matches[:top_n]

def get_company_recommendations(company_name, top_n=5):
    """Get top student recommendations for a company"""
    company = internships[internships["company_name"] == company_name].iloc[0]
    matches = []
    
    for idx, student in students.iterrows():
        match_info = calculate_student_company_match(student, company)
        if match_info['skill_overlap'] > 0:
            matches.append((match_info['total_score'], student, match_info))
    
    matches.sort(reverse=True, key=lambda x: x[0])
    return matches[:top_n]

# -------------------
# Student View
# -------------------
if view_mode == "🎓 Student View":
    student = students[students["name"] == selected_student].iloc[0]
    
    # Student Profile Card
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown(f"""
        <div class="student-card">
            <h3>👤 Student Profile</h3>
            <p><strong>Name:</strong> {student['name']}</p>
            <p><strong>Location:</strong> {student['location']}</p>
            <p><strong>Category:</strong> {student['category']}</p>
            <p><strong>Skills:</strong> {student['skills']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Quick Stats
        total_internships = len(internships)
        location_matches = len(internships[internships['location'] == student['location']])
        
        col2_1, col2_2, col2_3 = st.columns(3)
        with col2_1:
            st.metric("Total Internships", total_internships)
        with col2_2:
            st.metric("Location Matches", location_matches)
        with col2_3:
            st.metric("Your Category", student['category'])
    
    # Get recommendations
    recommendations = get_student_recommendations(student)
    
    # Apply filters
    filtered_internships = internships.copy()
    if location_filter:
        filtered_internships = filtered_internships[filtered_internships['location'].isin(location_filter)]
    if sector_filter:
        filtered_internships = filtered_internships[filtered_internships['sector'].isin(sector_filter)]
    
    # Recalculate recommendations with filters
    if location_filter or sector_filter:
        filtered_recommendations = []
        for idx, internship in filtered_internships.iterrows():
            match_info = calculate_student_company_match(student, internship)
            if match_info['skill_overlap'] > 0:
                filtered_recommendations.append((match_info['total_score'], internship, match_info))
        filtered_recommendations.sort(reverse=True, key=lambda x: x[0])
        recommendations = filtered_recommendations[:5]
    
    st.markdown("## 🎯 Top Internship Recommendations")
    
    if recommendations:
        for i, (score, internship, match_info) in enumerate(recommendations):
            with st.container():
                st.markdown(f"""
                <div class="match-card">
                    <h4>#{i+1} {internship['company_name']} - {internship['sector']}</h4>
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <p><strong>📍 Location:</strong> {internship['location']}</p>
                            <p><strong>🎯 Required Skills:</strong> {internship['required_skills']}</p>
                            <p><strong>👥 Capacity:</strong> {internship['capacity']}</p>
                            <p><strong>🤝 Matching Skills:</strong> {', '.join(match_info['matching_skills'])}</p>
                        </div>
                        <div style="text-align: center;">
                            <h3>{score:.2%}</h3>
                            <p>Match Score</p>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.warning("No matching internships found with current filters.")

# -------------------
# Company View
# -------------------
elif view_mode == "🏢 Company View":
    company_data = internships[internships["company_name"] == selected_company].iloc[0]
    
    # Company Profile Card
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown(f"""
        <div class="company-card">
            <h3>🏢 Company Profile</h3>
            <p><strong>Company:</strong> {company_data['company_name']}</p>
            <p><strong>Sector:</strong> {company_data['sector']}</p>
            <p><strong>Location:</strong> {company_data['location']}</p>
            <p><strong>Capacity:</strong> {company_data['capacity']}</p>
            <p><strong>Required Skills:</strong> {company_data['required_skills']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Quick Stats
        total_students = len(students)
        location_matches = len(students[students['location'] == company_data['location']])
        
        col2_1, col2_2, col2_3 = st.columns(3)
        with col2_1:
            st.metric("Total Students", total_students)
        with col2_2:
            st.metric("Location Matches", location_matches)
        with col2_3:
            st.metric("Available Positions", company_data['capacity'])
    
    # Get recommendations
    recommendations = get_company_recommendations(selected_company)
    
    # Apply filters
    filtered_students = students.copy()
    if category_filter:
        filtered_students = filtered_students[filtered_students['category'].isin(category_filter)]
    if student_location_filter:
        filtered_students = filtered_students[filtered_students['location'].isin(student_location_filter)]
    
    # Recalculate recommendations with filters
    if category_filter or student_location_filter:
        filtered_recommendations = []
        for idx, student in filtered_students.iterrows():
            match_info = calculate_student_company_match(student, company_data)
            if match_info['skill_overlap'] > 0:
                filtered_recommendations.append((match_info['total_score'], student, match_info))
        filtered_recommendations.sort(reverse=True, key=lambda x: x[0])
        recommendations = filtered_recommendations[:5]
    
    st.markdown("## 👨‍🎓 Top Student Recommendations")
    
    if recommendations:
        for i, (score, student, match_info) in enumerate(recommendations):
            with st.container():
                st.markdown(f"""
                <div class="match-card">
                    <h4>#{i+1} {student['name']} - {student['category']}</h4>
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <p><strong>📍 Location:</strong> {student['location']}</p>
                            <p><strong>🎯 Skills:</strong> {student['skills']}</p>
                            <p><strong>🤝 Matching Skills:</strong> {', '.join(match_info['matching_skills'])}</p>
                        </div>
                        <div style="text-align: center;">
                            <h3>{score:.2%}</h3>
                            <p>Match Score</p>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.warning("No matching students found with current filters.")

# -------------------
# Analytics Dashboard
# -------------------
elif view_mode == "📊 Analytics Dashboard":
    st.markdown("## 📈 Platform Analytics")
    
    # Overview Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h3>{len(students)}</h3>
            <p>Total Students</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <h3>{len(internships)}</h3>
            <p>Total Internships</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <h3>{internships['capacity'].sum()}</h3>
            <p>Total Positions</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <h3>{len(internships['sector'].unique())}</h3>
            <p>Industry Sectors</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Charts
    col1, col2 = st.columns(2)
    
    # Sector Distribution
    with col1:
        sector_count = internships['sector'].value_counts().reset_index()
        sector_count.columns = ['sector', 'count']
        fig1 = px.pie(
            sector_count, 
            names='sector', 
            values='count', 
            title='📊 Internships by Sector',
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        fig1.update_layout(showlegend=True)
        st.plotly_chart(fig1, use_container_width=True)
    
    # Student Categories
    with col2:
        category_count = students['category'].value_counts().reset_index()
        category_count.columns = ['category', 'count']
        fig2 = px.bar(
            category_count, 
            x='category', 
            y='count', 
            title='👨‍🎓 Students by Category',
            color='category',
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        st.plotly_chart(fig2, use_container_width=True)
    
    # Location Analysis
    col3, col4 = st.columns(2)
    
    with col3:
        location_count = students['location'].value_counts().reset_index()
        location_count.columns = ['location', 'count']
        fig3 = px.bar(
            location_count, 
            x='location', 
            y='count', 
            title='📍 Students by Location',
            color='location',
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        st.plotly_chart(fig3, use_container_width=True)
    
    with col4:
        intern_location_count = internships['location'].value_counts().reset_index()
        intern_location_count.columns = ['location', 'count']
        fig4 = px.bar(
            intern_location_count, 
            x='location', 
            y='count', 
            title='🏢 Internships by Location',
            color='location',
            color_discrete_sequence=px.colors.qualitative.Dark2
        )
        st.plotly_chart(fig4, use_container_width=True)
    
    # Skills Analysis
    st.markdown("## 💡 Skills Analysis")
    
    # Top Skills in Demand
    all_required_skills = []
    for skills in internships['required_skills']:
        all_required_skills.extend([skill.strip() for skill in skills.split(",")])
    
    skill_demand = pd.Series(all_required_skills).value_counts().head(10).reset_index()
    skill_demand.columns = ['skill', 'count']
    
    # Student Skills Distribution
    all_student_skills = []
    for skills in students['skills']:
        all_student_skills.extend([skill.strip() for skill in skills.split(",")])
    
    student_skill_count = pd.Series(all_student_skills).value_counts().head(10).reset_index()
    student_skill_count.columns = ['skill', 'count']
    
    col5, col6 = st.columns(2)
    
    with col5:
        fig5 = px.bar(
            skill_demand, 
            x='skill', 
            y='count', 
            title='🔥 Most In-Demand Skills',
            color='count',
            color_continuous_scale='Viridis'
        )
        fig5.update_xaxes(tickangle=45)
        st.plotly_chart(fig5, use_container_width=True)
    
    with col6:
        fig6 = px.bar(
            student_skill_count, 
            x='skill', 
            y='count', 
            title='👨‍💻 Most Common Student Skills',
            color='count',
            color_continuous_scale='Plasma'
        )
        fig6.update_xaxes(tickangle=45)
        st.plotly_chart(fig6, use_container_width=True)

# -------------------
# Footer
# -------------------
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 2rem; color: #666;">
    <p>🎯 Smart Internship Allocation Platform | Connecting Talent with Opportunity</p>
</div>
""", unsafe_allow_html=True)