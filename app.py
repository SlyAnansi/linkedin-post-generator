import streamlit as st
import requests
import json
import os
import random
from dotenv import load_dotenv
from datetime import datetime
import smtplib
from email.mime.text import MimeText
from email.mime.multipart import MimeMultipart

# Load environment variables
load_dotenv()

# Page config
st.set_page_config(
    page_title="LinkedIn Post Generator",
    page_icon="🚀",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #0066cc;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.2rem;
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    .post-container {
        background: #ffffff;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #0066cc;
        margin: 1rem 0;
        color: #212529;
        font-weight: 500;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        line-height: 1.6;
    }
    .email-button {
        background-color: #0066cc;
        color: white;
        padding: 10px 20px;
        text-decoration: none;
        border-radius: 5px;
        display: inline-block;
        margin: 5px 0;
    }
    .email-button:hover {
        background-color: #0052a3;
        color: white;
        text-decoration: none;
    }
</style>
""", unsafe_allow_html=True)

def save_email_to_file(email, name="", company=""):
    """Save email to session (in production, save to database)"""
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # In production, you'd save to a database here
        return True
    except Exception as e:
        return False

def show_email_signup():
    """Show email signup form"""
    with st.container():
        st.markdown("### 📧 Get Free Access + Updates")
        st.markdown("*Enter your email to unlock unlimited post generation and get notified about new features*")
        
        with st.form("email_signup"):
            col1, col2 = st.columns(2)
            with col1:
                name = st.text_input("Name (optional)")
            with col2:
                company = st.text_input("Company (optional)")
            
            email = st.text_input("Email Address*", placeholder="your.email@company.com")
            
            submitted = st.form_submit_button("🚀 Get Free Access", type="primary")
            
            if submitted:
                if email and "@" in email and "." in email:
                    if save_email_to_file(email, name, company):
                        st.session_state.email_collected = True
                        st.session_state.user_email = email
                        st.session_state.user_name = name
                        st.success("✅ Welcome! You now have unlimited access!")
                        st.rerun()
                    else:
                        st.error("Error saving email. Please try again.")
                else:
                    st.error("Please enter a valid email address.")

def check_email_access():
    """Check if user has provided email"""
    return st.session_state.get('email_collected', False)

def get_industry_data(industry):
    """Get industry-specific terminology"""
    
    industry_data = {
        "Technology": {
            "jargon": ["API integration", "DevOps", "scalability", "tech stack", "CI/CD pipeline"],
            "pain_points": ["technical debt", "legacy systems", "security vulnerabilities"],
            "metrics": ["uptime", "deployment frequency", "user adoption"],
            "roles": ["developers", "product managers", "engineering teams"],
            "buzzwords": ["digital transformation", "cloud-native", "microservices"]
        },
        "Healthcare": {
            "jargon": ["EHR systems", "patient outcomes", "clinical workflows", "care coordination"],
            "pain_points": ["regulatory compliance", "patient safety", "documentation burden"],
            "metrics": ["patient satisfaction", "clinical quality measures", "care efficiency"],
            "roles": ["clinicians", "healthcare administrators", "care teams"],
            "buzzwords": ["value-based care", "telehealth adoption", "population health"]
        },
        "Finance": {
            "jargon": ["portfolio optimization", "risk management", "compliance frameworks"],
            "pain_points": ["market volatility", "regulatory changes", "operational risk"],
            "metrics": ["alpha generation", "Sharpe ratio", "AUM growth"],
            "roles": ["financial advisors", "portfolio managers", "risk analysts"],
            "buzzwords": ["fintech disruption", "ESG investing", "robo-advisory"]
        },
        "Marketing": {
            "jargon": ["attribution modeling", "funnel optimization", "conversion tracking"],
            "pain_points": ["ad spend efficiency", "attribution gaps", "customer acquisition costs"],
            "metrics": ["ROAS", "LTV:CAC ratio", "engagement rates"],
            "roles": ["performance marketers", "growth teams", "brand managers"],
            "buzzwords": ["omnichannel strategy", "personalization at scale", "marketing automation"]
        },
        "Sales": {
            "jargon": ["pipeline velocity", "quota attainment", "deal progression"],
            "pain_points": ["lead quality", "sales cycle length", "quota pressure"],
            "metrics": ["win rates", "average deal size", "pipeline coverage"],
            "roles": ["sales development reps", "account executives", "sales managers"],
            "buzzwords": ["revenue intelligence", "predictive analytics", "social selling"]
        }
    }
    
    return industry_data.get(industry, {
        "jargon": ["best practices", "operational efficiency", "strategic initiatives"],
        "pain_points": ["market challenges", "competitive pressure", "operational inefficiencies"],
        "metrics": ["performance indicators", "success metrics", "ROI"],
        "roles": ["professionals", "managers", "team leaders"],
        "buzzwords": ["innovation", "transformation", "optimization"]
    })

def generate_posts(topic, industry, tone, audience, post_type):
    """Generate LinkedIn posts with industry-specific content"""
    
    # Get industry-specific data
    industry_info = get_industry_data(industry)
    
    # Random selections
    jargon = random.choice(industry_info["jargon"])
    pain_point = random.choice(industry_info["pain_points"])
    metric = random.choice(industry_info["metrics"])
    role = random.choice(industry_info["roles"])
    buzzword = random.choice(industry_info["buzzwords"])
    
    # Tone-based hooks
    tone_hooks = {
        "Professional": f"📊 Industry insight: {topic} is reshaping {industry}",
        "Conversational": f"💬 Let's talk about {topic} in {industry}",
        "Inspirational": f"🚀 The future of {topic} in {industry} starts with YOU",
        "Educational": f"📚 {topic} 101 for {industry} professionals",
        "Humorous": f"😅 {topic} in {industry}: It's complicated",
        "Thought-provoking": f"🤯 Unpopular opinion: {topic} will change {industry} forever",
        "Personal/Storytelling": f"📖 My {topic} journey in {industry}"
    }
    
    hook = tone_hooks.get(tone, tone_hooks["Professional"])
    
    # Random elements
    insights_options = ["3 key insights:", "Here's what I've learned:", "The data shows:", "My observations:"]
    insights = random.choice(insights_options)
    
    action_words = ["accelerating", "transforming", "evolving", "advancing"]
    action1 = random.choice(action_words)
    action2 = random.choice(action_words)
    
    cta_options = [
        f"What's your experience with {topic}? Share below! 👇",
        f"How is {topic} impacting your {industry} work?",
        f"What {topic} trends are you seeing in {industry}?",
        f"Thoughts on {topic} in our industry? Let's discuss! 💬"
    ]
    cta = random.choice(cta_options)
    
    emojis = random.choice([["🚀", "⭐", "💫"], ["🎯", "📊", "📈"], ["💡", "🧠", "🔍"]])
    
    # Generate posts
    posts = []
    
    # Post 1: Industry insights
    post1 = f"""{hook}

As someone working with {role}, I've been exploring how {topic} is {action1} across {industry}.

{insights}
{emojis[0]} {buzzword} is {action2} market dynamics
{emojis[1]} {jargon} requirements are evolving
{emojis[2]} {metric} optimization is accelerating

{cta}

#{industry.replace(' ', '')} #{topic.replace(' ', '')} #Innovation #Growth #Leadership"""
    
    # Post 2: Personal story
    story_starts = [
        f"Last week, I witnessed a breakthrough in {jargon} implementation",
        f"Three months ago, our {role} couldn't have predicted this shift",
        f"Yesterday's conversation about {pain_point} changed my perspective"
    ]
    story_start = random.choice(story_starts)
    
    post2 = f"""{story_start}.

The impact of {topic} on our {buzzword} initiatives was remarkable:
• {metric} improved by 40%
• {jargon} processes became more efficient
• {pain_point} resolution exceeded expectations

For {audience} in {industry}, this isn't just a trend—it's the new reality.

How is {topic} changing your {jargon} approach?

#{industry.replace(' ', '')} #{topic.replace(' ', '')} #Transformation #Success #Results"""
    
    # Post 3: Poll format
    poll_questions = [
        f"Quick poll for {role}: What's your biggest {topic} challenge?",
        f"Honest question: Is {topic} overhyped or underutilized in {industry}?",
        f"Help me settle a debate: What's the #1 {topic} benefit for {industry}?"
    ]
    poll_q = random.choice(poll_questions)
    
    post3 = f"""{poll_q}

A) Implementation complexity
B) Budget constraints
C) Skills and training gaps
D) Resistance to change

Working with {role}, I see huge variation in {topic} readiness across {industry}.

Some organizations are crushing it with {jargon}, others struggle with {pain_point}.

Drop your vote + share what's working for you! 📊

#{industry.replace(' ', '')} #{topic.replace(' ', '')} #Poll #Community #Insights"""
    
    # Post 4: Hot take
    hot_takes = [
        f"Unpopular opinion: Most {industry} companies are doing {topic} wrong",
        f"Hot take: {topic} isn't the problem in {industry}—implementation is",
        f"Bold prediction: {topic} will be standard in {industry} within 18 months"
    ]
    hot_take = random.choice(hot_takes)
    
    post4 = f"""{hot_take}.

Here's why I believe this:

→ {buzzword} adoption varies widely
→ {jargon} strategy often lacks planning
→ {pain_point} management is inconsistent

For {role}, the window of opportunity is narrowing.

Am I wrong? Prove me wrong in the comments! 🔥

#{industry.replace(' ', '')} #{topic.replace(' ', '')} #Controversial #RealTalk #ChangeManagement"""
    
    # Post 5: Data-driven
    data_hooks = [
        f"New {industry} research on {topic} is eye-opening",
        f"Latest data reveals surprising {topic} trends in {industry}",
        f"Industry report: {topic} adoption in {industry} is accelerating"
    ]
    data_hook = random.choice(data_hooks)
    
    metrics_data = [
        "73% increase in adoption rates",
        "2.3x improvement in efficiency", 
        "41% reduction in operational costs"
    ]
    
    post5 = f"""{data_hook}.

Key findings for {role}:

📊 {metrics_data[0]}
📈 {metrics_data[1]}
🎯 {metrics_data[2]}

If you're in {industry} and not tracking {metric}, you're missing critical insights.

What data points matter most in your {topic} journey?

#{industry.replace(' ', '')} #{topic.replace(' ', '')} #Data #Research #Metrics #Results"""
    
    posts = [post1, post2, post3, post4, post5]
    
    return posts

def parse_posts_from_list(posts):
    """Convert list of posts to display format"""
    return posts

# Main App Interface
def main():
    # Initialize session state
    if 'email_collected' not in st.session_state:
        st.session_state.email_collected = False
    
    # Header
    st.markdown('<div class="main-header">🚀 LinkedIn Post Generator</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Create engaging LinkedIn content in seconds</div>', unsafe_allow_html=True)
    
    # Check if user has provided email
    if not check_email_access():
        # Show preview and email signup
        st.markdown("## 👀 See What You'll Get")
        
        # Show example post
        st.markdown("### Example Generated Post:")
        example_post = """🚀 The future of AI in Technology starts with YOU

As someone working with developers, I've been exploring how AI is accelerating across Technology.

Here's what I've learned:
⭐ Digital transformation is reshaping market dynamics
💫 API integration requirements are evolving
✨ Uptime optimization is accelerating

What's your experience with AI? Share below! 👇

#Technology #AI #Innovation #Growth #Leadership"""
        
        st.markdown(f'<div class="post-container">{example_post}</div>', unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Email signup form
        show_email_signup()
        
        # Benefits below signup
        st.markdown("### 🎯 What You Get With Free Access:")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("**✅ Unlimited Posts**")
            st.markdown("Generate as many posts as you need")
        
        with col2:
            st.markdown("**✅ Industry Jargon**") 
            st.markdown("Automatically adapts to your industry")
        
        with col3:
            st.markdown("**✅ Multiple Tones**")
            st.markdown("Professional, casual, thought-provoking & more")
        
        return
    
    # Main app for users who provided email
    with st.sidebar:
        # Show user info
        if st.session_state.get('user_email'):
            st.success(f"✅ Logged in: {st.session_state.user_email}")
        
        st.header("📝 Post Configuration")
        
        # Main topic
        topic = st.text_input(
            "What topic do you want to write about?",
            placeholder="e.g., AI in healthcare, Remote work productivity..."
        )
        
        # Industry selection
        industry = st.selectbox(
            "Select your industry:",
            ["Technology", "Healthcare", "Finance", "Marketing", "Sales", "HR", 
             "Education", "Real Estate", "Consulting", "Manufacturing", "Other"]
        )
        
        # Target audience
        audience = st.selectbox(
            "Who is your target audience?",
            ["Professionals in my industry", "Business owners", "Job seekers", 
             "Students/New graduates", "C-level executives", "Entrepreneurs", "General audience"]
        )
        
        # Tone selection
        tone = st.selectbox(
            "Choose your tone:",
            ["Professional", "Conversational", "Inspirational", "Educational", 
             "Humorous", "Thought-provoking", "Personal/Storytelling"]
        )
        
        # Post type
        post_type = st.selectbox(
            "Type of post:",
            ["Industry insights", "Personal experience", "Tips/Advice", 
             "Question/Poll", "Achievement/Milestone", "Industry news commentary", "How-to guide"]
        )
        
        # Generate button
        generate_button = st.button("🎯 Generate Posts", type="primary")
        
        # Upgrade section
        st.markdown("---")
        st.markdown("### 🚀 Love this tool?")
        st.markdown("**Upgrade to Pro:**")
        st.markdown("• 50+ industry templates")
        st.markdown("• Advanced customization")
        st.markdown("• Priority support")
        st.markdown("• Export to multiple formats")
        st.markdown("**$29/month**")
        if st.button("Upgrade Now"):
            st.success("Contact us for Pro access!")
    
    # Main content area
    if generate_button:
        if not topic:
            st.warning("Please enter a topic to generate posts about.")
            return
        
        # Show loading spinner
        with st.spinner("Generating your LinkedIn posts..."):
            posts = generate_posts(topic, industry, tone, audience, post_type)
        
        if posts:
            st.success("✅ Posts generated successfully!")
            
            st.markdown("## 📱 Your Generated Posts")
            
            for i, post in enumerate(posts, 1):
                with st.expander(f"📝 Post {i}", expanded=True):
                    st.markdown(f'<div class="post-container">{post}</div>', unsafe_allow_html=True)
                    
                    # Create two columns for buttons
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        if st.button(f"📋 Copy Post {i}", key=f"copy_{i}"):
                            st.success(f"Post {i} ready to copy!")
                    
                    with col2:
                        if st.button(f"📧 Send to LinkedIn", key=f"email_{i}"):
                            # Create a mailto link that opens their email client
                            email_subject = "LinkedIn Post from Generator"
                            email_body = post.replace('\n', '%0D%0A').replace(' ', '%20')
                            mailto_link = f"mailto:anansivc.5dcz24@zapiermail.com?subject={email_subject}&body={email_body}"
                            
                            st.markdown(f'<a href="{mailto_link}" target="_blank" style="background-color: #0066cc; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; display: inline-block; margin: 10px 0;">📧 Open Email Client</a>', unsafe_allow_html=True)
                            
                            st.success("✅ Click the blue button above to open your email client with the post pre-filled!")
            
            # Download option
            st.markdown("---")
            all_posts_text = "\n\n" + "="*50 + "\n\n".join([f"POST {i+1}:\n{post}" for i, post in enumerate(posts)])
            st.download_button(
                label="📥 Download All Posts",
                data=all_posts_text,
                file_name=f"linkedin_posts_{topic.replace(' ', '_')}.txt",
                mime="text/plain"
            )
        else:
            st.error("Could not generate posts. Please try again.")
    
    else:
        # Show features for logged-in users
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("### 🎯 Targeted Content")
            st.markdown("Generate posts tailored to your industry and audience")
        
        with col2:
            st.markdown("### ⚡ Save Time")
            st.markdown("Create 5 unique posts in under 30 seconds")
        
        with col3:
            st.markdown("### 📈 Boost Engagement")
            st.markdown("AI-optimized content designed for maximum LinkedIn engagement")

    # Footer
    st.markdown("---")
    st.markdown("**Ready to dominate LinkedIn? Generate your posts above! 🚀**")
    st.markdown("*Built with ❤️ for LinkedIn professionals*")

if __name__ == "__main__":
    main()
