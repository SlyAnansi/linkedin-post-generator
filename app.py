import streamlit as st
import requests
import json
import os
import random
import hashlib
import time
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()

# Page config
st.set_page_config(
    page_title="LinkedIn Post Generator",
    page_icon="🚀",
    layout="wide"
)

# Custom CSS with Ash Gray background
st.markdown("""
<style>
    .stApp {
        background-color: #B2BEB5;
    }
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #0066cc;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    .sub-header {
        font-size: 1.2rem;
        text-align: center;
        color: #333;
        margin-bottom: 2rem;
        font-weight: 500;
    }
    .intro-section {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        margin: 1rem 0;
        text-align: center;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
    }
    .post-container {
        background: #ffffff;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #0066cc;
        margin: 1rem 0;
        color: #212529;
        font-weight: 500;
        box-shadow: 0 4px 16px rgba(0,0,0,0.1);
        line-height: 1.6;
    }
    .copy-button {
        background: linear-gradient(45deg, #0066cc, #004499);
        color: white;
        border: none;
        padding: 8px 16px;
        border-radius: 5px;
        cursor: pointer;
        font-weight: bold;
        transition: all 0.3s ease;
        margin: 5px;
    }
    .copy-button:hover {
        background: linear-gradient(45deg, #004499, #0066cc);
        transform: translateY(-1px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    .usage-counter {
        background: linear-gradient(135deg, #ff6b6b, #ee5a52);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        text-align: center;
        font-weight: bold;
        box-shadow: 0 4px 16px rgba(0,0,0,0.1);
    }
    .premium-box {
        background: linear-gradient(135deg, #ffeaa7, #fdcb6e);
        color: #2d3436;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        text-align: center;
        font-weight: bold;
        box-shadow: 0 4px 16px rgba(0,0,0,0.1);
    }
    .account-form {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }
    .sidebar .stSelectbox, .sidebar .stTextInput {
        background-color: white;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
def init_session_state():
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'user_data' not in st.session_state:
        st.session_state.user_data = {}
    if 'usage_count' not in st.session_state:
        st.session_state.usage_count = 0
    if 'is_premium' not in st.session_state:
        st.session_state.is_premium = False

# Simple user database (in production, use a real database)
USER_DB_FILE = "users.json"

def load_users():
    """Load users from JSON file"""
    try:
        if os.path.exists(USER_DB_FILE):
            with open(USER_DB_FILE, 'r') as f:
                return json.load(f)
    except:
        pass
    return {}

def save_users(users):
    """Save users to JSON file"""
    try:
        with open(USER_DB_FILE, 'w') as f:
            json.dump(users, f, indent=2)
        return True
    except:
        return False

def hash_password(password):
    """Hash password for security"""
    return hashlib.sha256(password.encode()).hexdigest()

def create_account(email, password, name, company):
    """Create new user account"""
    users = load_users()
    
    if email in users:
        return False, "Email already exists"
    
    users[email] = {
        'password': hash_password(password),
        'name': name,
        'company': company,
        'created_at': datetime.now().isoformat(),
        'usage_count': 0,
        'is_premium': False
    }
    
    if save_users(users):
        return True, "Account created successfully"
    return False, "Error creating account"

def login_user(email, password):
    """Login user"""
    users = load_users()
    
    if email not in users:
        return False, "Email not found"
    
    if users[email]['password'] != hash_password(password):
        return False, "Incorrect password"
    
    st.session_state.logged_in = True
    st.session_state.user_data = users[email]
    st.session_state.user_data['email'] = email
    st.session_state.usage_count = users[email]['usage_count']
    st.session_state.is_premium = users[email]['is_premium']
    
    return True, "Login successful"

def update_usage():
    """Update user usage count"""
    if st.session_state.logged_in:
        users = load_users()
        email = st.session_state.user_data['email']
        users[email]['usage_count'] = st.session_state.usage_count + 1
        st.session_state.usage_count += 1
        save_users(users)

def show_login_signup():
    """Show login/signup form"""
    st.markdown('<div class="intro-section">', unsafe_allow_html=True)
    st.markdown("## 👋 Hey there! I'm a Software Engineer")
    st.markdown("""
    I built this LinkedIn Post Generator to help professionals like you create engaging content effortlessly. 
    As someone who understands the struggle of consistent posting, I wanted to make a tool that generates 
    authentic, industry-specific posts that actually get engagement.
    
    **Ready to level up your LinkedIn game?** 🚀
    """)
    st.markdown('</div>', unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["🔑 Login", "📝 Create Account"])
    
    with tab1:
        st.markdown('<div class="account-form">', unsafe_allow_html=True)
        st.markdown("### Login to Your Account")
        
        with st.form("login_form"):
            login_email = st.text_input("Email", placeholder="your.email@company.com")
            login_password = st.text_input("Password", type="password")
            login_submit = st.form_submit_button("🔑 Login", type="primary")
            
            if login_submit:
                if login_email and login_password:
                    success, message = login_user(login_email, login_password)
                    if success:
                        st.success(message)
                        st.rerun()
                    else:
                        st.error(message)
                else:
                    st.error("Please fill in all fields")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab2:
        st.markdown('<div class="account-form">', unsafe_allow_html=True)
        st.markdown("### Create Your Free Account")
        st.markdown("**Get 3 free generations (15 posts total)!**")
        
        with st.form("signup_form"):
            signup_name = st.text_input("Full Name*", placeholder="John Doe")
            signup_email = st.text_input("Email*", placeholder="your.email@company.com")
            signup_company = st.text_input("Company", placeholder="Your Company (optional)")
            signup_password = st.text_input("Password*", type="password", help="Minimum 6 characters")
            signup_confirm = st.text_input("Confirm Password*", type="password")
            
            agree_terms = st.checkbox("I agree to the Terms of Service and Privacy Policy")
            
            signup_submit = st.form_submit_button("🚀 Create Free Account", type="primary")
            
            if signup_submit:
                if not all([signup_name, signup_email, signup_password, signup_confirm]):
                    st.error("Please fill in all required fields")
                elif len(signup_password) < 6:
                    st.error("Password must be at least 6 characters")
                elif signup_password != signup_confirm:
                    st.error("Passwords don't match")
                elif not agree_terms:
                    st.error("Please agree to the Terms of Service")
                elif "@" not in signup_email or "." not in signup_email:
                    st.error("Please enter a valid email address")
                else:
                    success, message = create_account(signup_email, signup_password, signup_name, signup_company)
                    if success:
                        st.success(f"{message}! Please login to continue.")
                    else:
                        st.error(message)
        st.markdown('</div>', unsafe_allow_html=True)

def generate_with_llm(topic, industry, tone, audience, post_type, user_history=""):
    """Generate posts using Hugging Face LLM"""
    
    # Get your Hugging Face API key from Streamlit secrets
    try:
        HF_API_TOKEN = st.secrets["HUGGINGFACE_API_KEY"]
    except:
        st.error("Hugging Face API key not found. Please set HUGGINGFACE_API_KEY in your Streamlit secrets.")
        return generate_fallback_posts(topic, industry, tone, audience, post_type)
    
    # Use a free model like microsoft/DialoGPT-large or facebook/blenderbot-3B
    API_URL = "https://api-inference.huggingface.co/models/microsoft/DialoGPT-large"
    
    headers = {"Authorization": f"Bearer {HF_API_TOKEN}"}
    
    # Create a detailed prompt
    prompt = f"""Create a professional LinkedIn post about {topic} for {industry} professionals. 
    Tone: {tone}
    Audience: {audience}
    Post type: {post_type}
    
    Requirements:
    - 150-200 words
    - Include relevant hashtags
    - Use engaging hook
    - Include call-to-action
    - Professional and authentic
    - Industry-specific terminology
    
    Post:"""
    
    try:
        payload = {
            "inputs": prompt,
            "parameters": {
                "max_length": 300,
                "temperature": 0.7,
                "do_sample": True,
                "top_p": 0.9
            }
        }
        
        response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            if result and len(result) > 0:
                generated_text = result[0].get('generated_text', '')
                # Clean up the response
                if 'Post:' in generated_text:
                    post_content = generated_text.split('Post:')[1].strip()
                else:
                    post_content = generated_text.strip()
                
                # Generate 5 variations
                posts = []
                for i in range(5):
                    # Make slight variations for each post
                    variation_prompt = f"{prompt}\n\nVariation {i+1} - Make this unique:"
                    var_response = requests.post(API_URL, headers=headers, json={
                        "inputs": variation_prompt,
                        "parameters": {"max_length": 300, "temperature": 0.8}
                    }, timeout=20)
                    
                    if var_response.status_code == 200:
                        var_result = var_response.json()
                        if var_result and len(var_result) > 0:
                            var_text = var_result[0].get('generated_text', post_content)
                            if 'Post:' in var_text:
                                var_text = var_text.split('Post:')[1].strip()
                            posts.append(var_text.strip())
                        else:
                            posts.append(post_content)
                    else:
                        posts.append(post_content)
                    
                    time.sleep(1)  # Rate limiting
                
                return posts if posts else generate_fallback_posts(topic, industry, tone, audience, post_type)
            
    except Exception as e:
        st.warning(f"LLM service temporarily unavailable. Using fallback generator.")
        return generate_fallback_posts(topic, industry, tone, audience, post_type)
    
    # Fallback to original method
    return generate_fallback_posts(topic, industry, tone, audience, post_type)

def generate_fallback_posts(topic, industry, tone, audience, post_type):
    """Fallback post generation (your original method)"""
    # Your original generate_posts logic here (shortened for brevity)
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
        }
        # Add other industries...
    }
    
    info = industry_data.get(industry, {
        "jargon": ["best practices"], "pain_points": ["challenges"], 
        "metrics": ["performance"], "roles": ["professionals"], 
        "buzzwords": ["innovation"]
    })
    
    posts = []
    for i in range(5):
        post = f"""🚀 {topic} is transforming {industry}

As someone working with {random.choice(info['roles'])}, I've been exploring how {topic} impacts our industry.

Key insights:
• {random.choice(info['buzzwords'])} is reshaping workflows
• {random.choice(info['jargon'])} requirements are evolving  
• {random.choice(info['metrics'])} optimization is accelerating

What's your experience with {topic}? Share below! 👇

#{industry.replace(' ', '')} #{topic.replace(' ', '')} #Innovation #Growth #Leadership"""
        
        posts.append(post)
    
    return posts

def copy_to_clipboard_js(text, button_id):
    """Generate JavaScript for copy to clipboard functionality"""
    return f"""
    <script>
    function copyToClipboard{button_id}() {{
        const text = `{text.replace('`', '\\`').replace('"', '\\"')}`;
        navigator.clipboard.writeText(text).then(function() {{
            const button = document.getElementById('copy-btn-{button_id}');
            const originalText = button.innerHTML;
            button.innerHTML = '✅ Copied!';
            button.style.backgroundColor = '#28a745';
            setTimeout(function() {{
                button.innerHTML = originalText;
                button.style.backgroundColor = '#0066cc';
            }}, 2000);
        }}).catch(function(err) {{
            console.error('Could not copy text: ', err);
            alert('Copy failed. Please select and copy manually.');
        }});
    }}
    </script>
    <button id="copy-btn-{button_id}" class="copy-button" onclick="copyToClipboard{button_id}()">
        📋 Copy Post
    </button>
    """

def main():
    init_session_state()
    
    # Header
    st.markdown('<div class="main-header">🚀 LinkedIn Post Generator</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Create engaging, AI-powered LinkedIn content in seconds</div>', unsafe_allow_html=True)
    
    # Check if user is logged in
    if not st.session_state.logged_in:
        show_login_signup()
        return
    
    # User is logged in - show main app
    user = st.session_state.user_data
    
    # Sidebar with user info and logout
    with st.sidebar:
        st.success(f"✅ Welcome, {user.get('name', 'User')}!")
        st.write(f"📧 {user.get('email', '')}")
        
        if st.button("🚪 Logout"):
            st.session_state.logged_in = False
            st.session_state.user_data = {}
            st.rerun()
        
        st.markdown("---")
        
        # Usage counter
        free_limit = 3
        remaining = max(0, free_limit - st.session_state.usage_count)
        
        if not st.session_state.is_premium:
            st.markdown(f"""
            <div class="usage-counter">
                📊 Free Uses Remaining: {remaining}/{free_limit}<br>
                <small>Each use generates 5 posts</small>
            </div>
            """, unsafe_allow_html=True)
            
            if remaining == 0:
                st.markdown("""
                <div class="premium-box">
                    🔥 Upgrade to Premium<br>
                    Unlimited posts + Advanced features<br>
                    <strong>$29/month</strong>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button("💳 Upgrade Now", type="primary"):
                    st.info("Contact support@yourapp.com for premium access!")
        else:
            st.success("⭐ Premium User - Unlimited Access!")
        
        st.markdown("---")
        
        # Post configuration
        st.header("📝 Post Configuration")
        
        topic = st.text_input(
            "What topic do you want to write about?",
            placeholder="e.g., AI in healthcare, Remote work productivity..."
        )
        
        industry = st.selectbox(
            "Select your industry:",
            ["Technology", "Healthcare", "Finance", "Marketing", "Sales", "HR", 
             "Education", "Real Estate", "Consulting", "Manufacturing", "Other"]
        )
        
        audience = st.selectbox(
            "Who is your target audience?",
            ["Professionals in my industry", "Business owners", "Job seekers", 
             "Students/New graduates", "C-level executives", "Entrepreneurs", "General audience"]
        )
        
        tone = st.selectbox(
            "Choose your tone:",
            ["Professional", "Conversational", "Inspirational", "Educational", 
             "Humorous", "Thought-provoking", "Personal/Storytelling"]
        )
        
        post_type = st.selectbox(
            "Type of post:",
            ["Industry insights", "Personal experience", "Tips/Advice", 
             "Question/Poll", "Achievement/Milestone", "Industry news commentary", "How-to guide"]
        )
        
        # Generate button - check limits
        can_generate = st.session_state.is_premium or remaining > 0
        
        if can_generate:
            generate_button = st.button("🎯 Generate Posts", type="primary")
        else:
            st.button("🎯 Generate Posts", type="primary", disabled=True)
            st.error("No free uses remaining. Please upgrade to premium.")
            generate_button = False
    
    # Main content area
    if 'generate_button' in locals() and generate_button:
        if not topic:
            st.warning("Please enter a topic to generate posts about.")
            return
        
        # Check usage limits again
        if not st.session_state.is_premium and st.session_state.usage_count >= 3:
            st.error("You've reached your free usage limit. Please upgrade to premium.")
            return
        
        # Show loading spinner
        with st.spinner("🤖 AI is crafting your LinkedIn posts..."):
            posts = generate_with_llm(topic, industry, tone, audience, post_type)
            
            # Update usage count
            update_usage()
        
        if posts:
            st.success("✅ Posts generated successfully!")
            
            st.markdown("## 📱 Your AI-Generated Posts")
            
            for i, post in enumerate(posts, 1):
                with st.expander(f"📝 Post {i}", expanded=True):
                    st.markdown(f'<div class="post-container">{post}</div>', unsafe_allow_html=True)
                    
                    # Copy button with JavaScript
                    st.markdown(copy_to_clipboard_js(post, i), unsafe_allow_html=True)
                    
                    # Alternative manual copy
                    st.code(post, language=None)
                    st.caption("👆 Alternative: Select all text above and copy manually")
            
            # Download option
            st.markdown("---")
            all_posts_text = "\n\n" + "="*50 + "\n\n".join([f"POST {i+1}:\n{post}" for i, post in enumerate(posts)])
            st.download_button(
                label="📥 Download All Posts",
                data=all_posts_text,
                file_name=f"linkedin_posts_{topic.replace(' ', '_')}.txt",
                mime="text/plain"
            )
            
            # Success message
            remaining_after = max(0, 3 - st.session_state.usage_count)
            if not st.session_state.is_premium:
                if remaining_after > 0:
                    st.info(f"🎉 Great! You have {remaining_after} free generations remaining.")
                else:
                    st.warning("🔥 You've used all free generations! Upgrade to premium for unlimited access.")
        else:
            st.error("Could not generate posts. Please try again.")
    
    else:
        # Show welcome message for logged-in users
        st.markdown(f"## 👋 Welcome back, {user.get('name', 'User')}!")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("### 🎯 AI-Powered Content")
            st.markdown("Advanced LLM generates unique, engaging posts tailored to your industry")
        
        with col2:
            st.markdown("### ⚡ Lightning Fast")
            st.markdown("Create 5 unique posts in under 30 seconds with one click")
        
        with col3:
            st.markdown("### 📈 Boost Engagement")
            st.markdown("Optimized content designed for maximum LinkedIn engagement and reach")
        
        # Usage stats
        if not st.session_state.is_premium:
            remaining = max(0, 3 - st.session_state.usage_count)
            st.info(f"💡 You have {remaining} free generations remaining. Each generation creates 5 unique posts!")

    # Footer
    st.markdown("---")
    st.markdown("**Built with ❤️ by a Software Engineer | Powered by AI | Ready to dominate LinkedIn? 🚀**")

if __name__ == "__main__":
    main()
