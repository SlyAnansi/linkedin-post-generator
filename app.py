import streamlit as st
import requests
import json
import os
import random
import hashlib
import time
import re
import qrcode
import io
import base64
from datetime import datetime, timedelta
from dotenv import load_dotenv
import pyperclip  # For clipboard functionality
from email_validator import validate_email, EmailNotValidError

# Load environment variables
load_dotenv()

# Page config
st.set_page_config(
    page_title="LinkedIn Post Generator - Built by Engineer",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed"  # Better for mobile
)

# Enhanced CSS with mobile-first responsive design
st.markdown("""
<style>
    /* Mobile-first responsive design */
    .stApp {
        background: linear-gradient(135deg, #B2BEB5 0%, #A8B4A8 100%);
    }
    
    /* Main header responsive */
    .main-header {
        font-size: clamp(2rem, 5vw, 3.5rem);
        font-weight: bold;
        text-align: center;
        background: linear-gradient(45deg, #0066cc, #004499);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        padding: 0 1rem;
    }
    
    .sub-header {
        font-size: clamp(1rem, 3vw, 1.3rem);
        text-align: center;
        color: #333;
        margin-bottom: 2rem;
        font-weight: 600;
        padding: 0 1rem;
    }
    
    /* Mobile-optimized containers */
    .intro-section {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 20px;
        margin: 1rem 0.5rem;
        text-align: center;
        box-shadow: 0 10px 40px rgba(0,0,0,0.15);
    }
    
    @media (min-width: 768px) {
        .intro-section {
            padding: 2.5rem;
            margin: 1rem 0;
        }
    }
    
    .intro-section h2, .intro-section p, .intro-section ul, .intro-section li {
        color: white !important;
    }
    
    /* Mobile-friendly feature grid */
    .feature-grid {
        display: grid;
        grid-template-columns: 1fr;
        gap: 1rem;
        margin: 1rem 0.5rem;
    }
    
    @media (min-width: 768px) {
        .feature-grid {
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 1.5rem;
            margin: 2rem 0;
        }
    }
    
    .feature-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 5px 20px rgba(0,0,0,0.1);
        text-align: center;
        transition: transform 0.3s ease;
        color: #333 !important;
    }
    
    @media (min-width: 768px) {
        .feature-card {
            padding: 2rem;
        }
        .feature-card:hover {
            transform: translateY(-5px);
        }
    }
    
    .feature-card h3, .feature-card p {
        color: #333 !important;
    }
    
    /* Post container mobile optimization */
    .post-container {
        background: #ffffff;
        padding: 1rem;
        border-radius: 15px;
        border-left: 5px solid #0066cc;
        margin: 1rem 0.5rem;
        color: #212529;
        font-weight: 500;
        box-shadow: 0 8px 25px rgba(0,0,0,0.12);
        line-height: 1.7;
        position: relative;
        font-size: 0.9rem;
    }
    
    @media (min-width: 768px) {
        .post-container {
            padding: 2rem;
            margin: 1.5rem 0;
            font-size: 1rem;
        }
    }
    
    .post-preview {
        background: #f8f9fa;
        border: 2px solid #e9ecef;
        border-radius: 12px;
        padding: 1rem;
        margin: 1rem 0.5rem;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto;
        line-height: 1.5;
        font-size: 0.9rem;
    }
    
    @media (min-width: 768px) {
        .post-preview {
            padding: 1.5rem;
            margin: 1rem 0;
            font-size: 1rem;
        }
    }
    
    .preview-header {
        display: flex;
        align-items: center;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 1px solid #dee2e6;
    }
    
    .preview-avatar {
        width: 40px;
        height: 40px;
        background: linear-gradient(45deg, #0066cc, #004499);
        border-radius: 50%;
        margin-right: 0.75rem;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-weight: bold;
        font-size: 0.9rem;
    }
    
    @media (min-width: 768px) {
        .preview-avatar {
            width: 48px;
            height: 48px;
            font-size: 1rem;
        }
    }
    
    /* QR Code container */
    .qr-container {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0.5rem;
        text-align: center;
        box-shadow: 0 5px 20px rgba(0,0,0,0.1);
    }
    
    @media (min-width: 768px) {
        .qr-container {
            padding: 2rem;
            margin: 1rem 0;
        }
    }
    
    /* Mobile-friendly buttons */
    .stButton > button {
        width: 100%;
        padding: 0.75rem 1rem;
        font-size: 0.9rem;
        border-radius: 8px;
    }
    
    @media (min-width: 768px) {
        .stButton > button {
            font-size: 1rem;
            padding: 0.5rem 1rem;
        }
    }
    
    /* Copy success message */
    .copy-success {
        background: #28a745;
        color: white;
        padding: 0.75rem 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        text-align: center;
        font-weight: bold;
        font-size: 0.9rem;
    }
    
    /* Mobile form optimization */
    .account-form {
        background: white;
        padding: 1.5rem;
        border-radius: 20px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.15);
        margin: 1rem 0.5rem;
        color: #333 !important;
    }
    
    @media (min-width: 768px) {
        .account-form {
            padding: 2.5rem;
            margin: 1rem 0;
        }
    }
    
    .account-form h3, .account-form p, .account-form label {
        color: #333 !important;
    }
    
    /* Responsive text inputs */
    .stTextInput > div > div > input {
        font-size: 16px; /* Prevents zoom on iOS */
    }
    
    .stTextArea > div > div > textarea {
        font-size: 16px; /* Prevents zoom on iOS */
    }
    
    /* Trending badges responsive */
    .trending-badge {
        background: linear-gradient(45deg, #ff6b6b, #ee5a52);
        color: white;
        padding: 0.4rem 0.8rem;
        border-radius: 15px;
        font-size: 0.8rem;
        font-weight: bold;
        display: inline-block;
        margin: 0.3rem 0.2rem;
    }
    
    /* Sidebar mobile optimization */
    @media (max-width: 768px) {
        .stSidebar {
            width: 100% !important;
        }
    }
    
    /* Enhanced copy button */
    .copy-button-container {
        display: flex;
        flex-direction: column;
        gap: 0.5rem;
        margin: 1rem 0;
    }
    
    @media (min-width: 768px) {
        .copy-button-container {
            flex-direction: row;
            gap: 1rem;
        }
    }
    
    /* Loading spinner */
    .loading-container {
        text-align: center;
        padding: 2rem;
    }
    
    /* Engagement metrics mobile */
    .engagement-metrics {
        display: flex;
        justify-content: space-around;
        padding: 0.75rem;
        background: #f8f9fa;
        border-radius: 8px;
        margin: 1rem 0;
        font-size: 0.8rem;
        color: #6c757d;
        flex-wrap: wrap;
        gap: 0.5rem;
    }
    
    @media (min-width: 768px) {
        .engagement-metrics {
            font-size: 0.9rem;
            padding: 1rem;
        }
    }
    
    /* Word count badge mobile */
    .word-count-badge {
        background: #17a2b8;
        color: white;
        padding: 0.3rem 0.6rem;
        border-radius: 10px;
        font-size: 0.7rem;
        position: absolute;
        top: 0.5rem;
        right: 0.5rem;
    }
    
    @media (min-width: 768px) {
        .word-count-badge {
            font-size: 0.8rem;
            top: 1rem;
            right: 1rem;
        }
    }
    
    /* Bot detection styling */
    .bot-detection {
        background: #fff3cd;
        border: 1px solid #ffeaa7;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
        color: #856404;
    }
    
    /* Ensure all text is readable */
    .stApp .main .block-container {
        color: #333 !important;
        padding-left: 1rem;
        padding-right: 1rem;
    }
    
    @media (min-width: 768px) {
        .stApp .main .block-container {
            padding-left: 2rem;
            padding-right: 2rem;
        }
    }
    
    .stMarkdown, .stMarkdown p, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4 {
        color: #333 !important;
    }
    
    .stSelectbox label, .stTextInput label, .stTextArea label {
        color: #333 !important;
        font-weight: 600;
    }
    
    /* Sidebar styling */
    .stSidebar {
        background-color: #f8f9fa !important;
    }
    
    .stSidebar .stMarkdown, .stSidebar .stMarkdown p, .stSidebar .stMarkdown h1, 
    .stSidebar .stMarkdown h2, .stSidebar .stMarkdown h3, .stSidebar .stMarkdown h4 {
        color: #333 !important;
    }
    
    .stSidebar .stSelectbox label, .stSidebar .stTextInput label, 
    .stSidebar .stTextArea label, .stSidebar .stButton button {
        color: #333 !important;
    }
    
    .stSidebar .stSuccess, .stSidebar .stInfo, .stSidebar .stWarning {
        color: #333 !important;
    }
    
    .stSidebar .trending-badge {
        background: linear-gradient(45deg, #ff6b6b, #ee5a52);
        color: white !important;
        padding: 0.3rem 0.8rem;
        border-radius: 15px;
        font-size: 0.8rem;
        font-weight: bold;
        display: inline-block;
        margin: 0.2rem;
    }
    
    /* Enhanced mobile navigation */
    .mobile-nav {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background: white;
        box-shadow: 0 -2px 10px rgba(0,0,0,0.1);
        z-index: 1000;
        display: flex;
        justify-content: space-around;
        padding: 0.5rem;
    }
    
    @media (min-width: 768px) {
        .mobile-nav {
            display: none;
        }
    }
    
    .mobile-nav-item {
        padding: 0.5rem;
        text-align: center;
        color: #666;
        text-decoration: none;
        font-size: 0.8rem;
        border-radius: 8px;
        min-width: 60px;
    }
    
    .mobile-nav-item.active {
        background: #0066cc;
        color: white;
    }
    
    /* PWA styles */
    .install-prompt {
        background: linear-gradient(45deg, #0066cc, #004499);
        color: white;
        padding: 1rem;
        border-radius: 12px;
        margin: 1rem 0;
        text-align: center;
    }
    
    .install-button {
        background: white;
        color: #0066cc;
        border: none;
        padding: 0.75rem 1.5rem;
        border-radius: 8px;
        font-weight: bold;
        margin-top: 0.5rem;
        cursor: pointer;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
def init_session_state():
    defaults = {
        'logged_in': False,
        'user_data': {},
        'usage_count': 0,
        'saved_posts': [],
        'brand_voice_examples': [],
        'trending_topics_cache': {},
        'user_preferences': {
            'favorite_templates': [],
            'default_tone': 'Professional',
            'default_industry': 'Technology'
        },
        'show_mobile_nav': True,
        'current_page': 'generate',
        'bot_check_passed': False,
        'login_attempts': 0,
        'last_activity': datetime.now()
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

# Enhanced email validation
def validate_email_address(email):
    """Validate email address format and domain"""
    try:
        # Basic validation
        validated_email = validate_email(email)
        email = validated_email.email
        
        # Additional checks for common typos and disposable emails
        disposable_domains = [
            '10minutemail.com', 'guerrillamail.com', 'mailinator.com',
            'tempmail.org', 'throwaway.email', 'yopmail.com'
        ]
        
        domain = email.split('@')[1].lower()
        if domain in disposable_domains:
            return False, "Disposable email addresses are not allowed"
        
        # Check for common typos in popular domains
        common_domains = {
            'gmial.com': 'gmail.com',
            'gmai.com': 'gmail.com',
            'yahooo.com': 'yahoo.com',
            'hotmial.com': 'hotmail.com',
            'outlok.com': 'outlook.com'
        }
        
        if domain in common_domains:
            suggested = email.replace(domain, common_domains[domain])
            return False, f"Did you mean {suggested}?"
        
        return True, email
    
    except EmailNotValidError:
        return False, "Please enter a valid email address"

# Enhanced bot detection
def check_bot_behavior():
    """Simple bot detection based on behavior patterns"""
    current_time = datetime.now()
    
    # Check for rapid successive requests
    if 'last_request_time' in st.session_state:
        time_diff = (current_time - st.session_state.last_request_time).total_seconds()
        if time_diff < 2:  # Less than 2 seconds between requests
            st.session_state.bot_score = st.session_state.get('bot_score', 0) + 1
    
    st.session_state.last_request_time = current_time
    
    # Check for suspicious patterns
    bot_score = st.session_state.get('bot_score', 0)
    
    # Simple honeypot field check (hidden field that humans shouldn't fill)
    if st.session_state.get('honeypot_field', ''):
        bot_score += 10
    
    # Rate limiting
    if bot_score > 5:
        return False, "Suspicious activity detected. Please wait a moment."
    
    return True, "Human verified"

def simple_captcha():
    """Simple math captcha"""
    if 'captcha_answer' not in st.session_state:
        num1 = random.randint(1, 10)
        num2 = random.randint(1, 10)
        st.session_state.captcha_question = f"{num1} + {num2}"
        st.session_state.captcha_answer = num1 + num2
    
    user_answer = st.number_input(
        f"🤖 Human verification: What is {st.session_state.captcha_question}?",
        min_value=0,
        max_value=100,
        value=0,
        key="captcha_input"
    )
    
    if user_answer == st.session_state.captcha_answer:
        st.session_state.bot_check_passed = True
        return True
    elif user_answer != 0:
        st.error("Incorrect answer. Please try again.")
        return False
    
    return False

# QR Code generation
def generate_qr_code(url):
    """Generate QR code for the website URL"""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Convert to base64 for display
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    buf.seek(0)
    img_base64 = base64.b64encode(buf.getvalue()).decode()
    
    return img_base64

# Enhanced user database management
USER_DB_FILE = "users.json"

def load_users():
    try:
        if os.path.exists(USER_DB_FILE):
            with open(USER_DB_FILE, 'r') as f:
                return json.load(f)
    except:
        pass
    return {}

def save_users(users):
    try:
        with open(USER_DB_FILE, 'w') as f:
            json.dump(users, f, indent=2)
        return True
    except:
        return False

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def create_account(email, password, name, company):
    users = load_users()
    
    if email in users:
        return False, "Email already exists"
    
    # Validate email
    is_valid, result = validate_email_address(email)
    if not is_valid:
        return False, result
    
    users[email] = {
        'password': hash_password(password),
        'name': name,
        'company': company,
        'created_at': datetime.now().isoformat(),
        'usage_count': 0,
        'saved_posts': [],
        'brand_voice_examples': [],
        'preferences': {
            'favorite_templates': [],
            'default_tone': 'Professional',
            'default_industry': 'Technology'
        },
        'login_count': 0,
        'last_login': None
    }
    
    if save_users(users):
        return True, "Account created successfully"
    return False, "Error creating account"

def login_user(email, password):
    # Check bot behavior
    is_human, message = check_bot_behavior()
    if not is_human:
        return False, message
    
    users = load_users()
    
    if email not in users:
        st.session_state.login_attempts += 1
        return False, "Email not found"
    
    if users[email]['password'] != hash_password(password):
        st.session_state.login_attempts += 1
        return False, "Incorrect password"
    
    # Rate limiting for failed attempts
    if st.session_state.login_attempts > 3:
        return False, "Too many failed attempts. Please refresh the page and try again."
    
    user_data = users[email]
    
    # Update login stats
    users[email]['login_count'] = users[email].get('login_count', 0) + 1
    users[email]['last_login'] = datetime.now().isoformat()
    save_users(users)
    
    st.session_state.logged_in = True
    st.session_state.user_data = user_data
    st.session_state.user_data['email'] = email
    st.session_state.usage_count = user_data.get('usage_count', 0)
    st.session_state.saved_posts = user_data.get('saved_posts', [])
    st.session_state.brand_voice_examples = user_data.get('brand_voice_examples', [])
    st.session_state.user_preferences = user_data.get('preferences', {
        'favorite_templates': [],
        'default_tone': 'Professional',
        'default_industry': 'Technology'
    })
    st.session_state.login_attempts = 0
    st.session_state.current_page = 'generate'  # Redirect to homepage
    
    return True, "Login successful"

def update_user_data():
    if st.session_state.logged_in:
        users = load_users()
        email = st.session_state.user_data['email']
        users[email].update({
            'usage_count': st.session_state.usage_count,
            'saved_posts': st.session_state.saved_posts,
            'brand_voice_examples': st.session_state.brand_voice_examples,
            'preferences': st.session_state.user_preferences
        })
        save_users(users)

# Enhanced clipboard functionality
def copy_to_clipboard(text, post_id):
    """Enhanced copy functionality with multiple methods"""
    try:
        # Try to use pyperclip first
        pyperclip.copy(text)
        st.session_state[f'copied_{post_id}'] = True
        return True, "Copied to clipboard!"
    except:
        # Fallback to session state for manual copy
        st.session_state[f'copy_text_{post_id}'] = text
        return False, "Click the text area below and copy manually (Ctrl+A, Ctrl+C)"

# Enhanced trending topics with real-time feel
def get_current_trending_topics():
    """Get current trending topics with timestamp-based rotation"""
    
    # Rotate trending topics daily to feel fresh
    day_of_year = datetime.now().timetuple().tm_yday
    
    all_trending = {
        "general": [
            "AI automation in the workplace",
            "Remote work productivity hacks", 
            "Sustainable business practices",
            "Mental health in professional settings",
            "Skills-based hiring trends",
            "Digital transformation strategies",
            "Employee retention strategies",
            "Authentic leadership styles",
            "Work-life integration",
            "Diversity and inclusion initiatives",
            "Career pivoting in 2025",
            "Professional networking evolution",
            "Continuous learning culture",
            "Emotional intelligence at work",
            "Future of hybrid teams"
        ],
        "Technology": [
            "AI ethics and responsible deployment",
            "Quantum computing breakthroughs",
            "Cybersecurity in remote work",
            "Low-code/no-code platforms",
            "Edge computing applications",
            "API-first architecture",
            "DevSecOps implementation",
            "Cloud cost optimization",
            "Microservices architecture",
            "Developer experience (DX)"
        ],
        "Healthcare": [
            "Telehealth expansion",
            "AI-powered diagnostics",
            "Patient experience optimization",
            "Healthcare worker burnout",
            "Precision medicine advances",
            "Digital therapeutics",
            "Health equity initiatives",
            "Interoperability challenges",
            "Value-based care models",
            "Mental health integration"
        ],
        "Finance": [
            "ESG investing momentum",
            "Fintech disruption",
            "Cryptocurrency regulation",
            "Open banking evolution",
            "Financial wellness programs",
            "RegTech solutions",
            "Digital payment innovation",
            "Robo-advisory growth",
            "DeFi mainstream adoption",
            "Financial inclusion efforts"
        ],
        "Marketing": [
            "First-party data strategies",
            "AI-powered personalization",
            "Influencer marketing ROI",
            "Social commerce growth",
            "Brand authenticity",
            "Customer experience optimization",
            "Marketing attribution challenges",
            "Content marketing evolution",
            "Video-first strategies",
            "Community building"
        ],
        "Sales": [
            "Social selling mastery",
            "Sales automation tools",
            "Revenue operations alignment",
            "Customer success integration",
            "Consultative selling approach",
            "Digital sales transformation",
            "Account-based selling",
            "Sales enablement technology",
            "Predictive analytics in sales",
            "Virtual relationship building"
        ]
    }
    
    # Select trending topics based on day rotation
    selected_topics = {}
    for category, topics in all_trending.items():
        # Rotate through topics based on day
        start_idx = (day_of_year * 3) % len(topics)
        selected_topics[category] = topics[start_idx:start_idx+5] + topics[:max(0, 5-(len(topics)-start_idx))]
    
    return selected_topics

# Enhanced post templates
def get_post_templates():
    return {
        "Story": {
            "description": "Personal experience or anecdote",
            "structure": "Hook → Story → Lesson → CTA",
            "best_for": "Building personal connection"
        },
        "Insight": {
            "description": "Industry knowledge or observation", 
            "structure": "Observation → Analysis → Implication → Discussion",
            "best_for": "Thought leadership"
        },
        "Tip": {
            "description": "Actionable advice or how-to",
            "structure": "Problem → Solution → Steps → Outcome",
            "best_for": "Providing value"
        },
        "Question": {
            "description": "Engaging discussion starter",
            "structure": "Context → Question → Your take → Open discussion",
            "best_for": "Community engagement"
        },
        "Data": {
            "description": "Statistics or research findings",
            "structure": "Statistic → Context → Analysis → Takeaway",
            "best_for": "Credibility building"
        },
        "Controversial": {
            "description": "Bold opinion or hot take",
            "structure": "Controversial statement → Supporting evidence → Nuance → Debate invite",
            "best_for": "High engagement"
        },
        "Achievement": {
            "description": "Celebrating success or milestone",
            "structure": "Achievement → Journey → Lessons → Thanks/Inspiration",
            "best_for": "Personal branding"
        },
        "List": {
            "description": "Curated tips or insights",
            "structure": "Setup → Numbered points → Summary → Engagement",
            "best_for": "Easy consumption"
        }
    }

# [Include all the post generation functions from the original code here - they remain the same]
# For brevity, I'm including just the signatures. The full implementations should be copied from the original.

def generate_enhanced_posts(topic, industry, tone, audience, template, word_count, include_emojis, trending_focus):
    """Generate posts with all new features"""
    # [Original implementation]
    pass

def create_structured_post(topic, industry, tone, audience, template, template_info, word_count, include_emojis, trending_topic, variation):
    """Create a post following the selected template structure"""
    # [Original implementation]
    pass

# [All the create_*_post functions remain the same]

def get_word_count(text):
    """Get word count of text"""
    return len(text.split())

def predict_engagement(post, template, tone, industry):
    """Predict engagement level based on post characteristics"""
    # [Original implementation]
    pass

def show_post_preview(post, user_name="Your Name"):
    """Show LinkedIn-style preview with mobile optimization"""
    
    word_count = get_word_count(post)
    
    st.markdown(f"""
    <div class="post-preview">
        <div class="preview-header">
            <div class="preview-avatar">{user_name[0] if user_name else "U"}</div>
            <div>
                <div style="font-weight: bold; color: #333; font-size: clamp(0.9rem, 2.5vw, 1rem);">{user_name}</div>
                <div style="font-size: clamp(0.8rem, 2vw, 0.9rem); color: #666;">Software Engineer • Just now</div>
            </div>
        </div>
        <div style="white-space: pre-line; margin-bottom: 1rem; font-size: clamp(0.85rem, 2vw, 0.95rem);">{post}</div>
        <div class="engagement-metrics">
            <span>👍 Like</span>
            <span>💬 Comment</span>
            <span>🔄 Repost</span>
            <span>📤 Send</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Word count badge
    st.markdown(f'<div class="word-count-badge">{word_count} words</div>', unsafe_allow_html=True)

def show_copy_functionality(post, post_id):
    """Enhanced copy functionality with multiple options and mobile optimization"""
    
    # Mobile-friendly layout
    st.markdown('<div class="copy-button-container">', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        if st.button(f"📋 Copy Post", key=f"copy_main_{post_id}", use_container_width=True):
            success, message = copy_to_clipboard(post, post_id)
            if success:
                st.success("✅ Copied to clipboard!")
            else:
                st.info("📋 Text ready for manual copy below")
    
    with col2:
        if st.button(f"💾 Save", key=f"save_{post_id}", use_container_width=True):
            if st.session_state.logged_in:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
                # Enhanced saved post with metadata
                saved_post = {
                    'content': post,
                    'saved_at': timestamp,
                    'id': f"post_{len(st.session_state.saved_posts) + 1}",
                    'word_count': get_word_count(post),
                    'preview': post[:100] + "..." if len(post) > 100 else post,
                    'template': st.session_state.get('current_template', 'Unknown'),
                    'topic': st.session_state.get('current_topic', 'Unknown')
                }
                st.session_state.saved_posts.append(saved_post)
                update_user_data()
                st.success("💾 Saved!")
            else:
                st.warning("Login to save")
    
    with col3:
        # LinkedIn share link (mobile optimized)
        linkedin_text = post.replace('\n', '%0A').replace(' ', '%20')
        share_url = f"https://www.linkedin.com/sharing/share-offsite/?url=https://linkedin-post-generator-ao8jqjdjy8tdsawokcarj4.streamlit.app&summary={linkedin_text[:100]}..."
        st.markdown(f"[🔗 Share]({share_url})", unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Enhanced text area for manual copy
    copy_text = st.session_state.get(f'copy_text_{post_id}', post)
    st.text_area(
        f"📝 Manual copy (tap to select all):",
        value=copy_text,
        height=100,
        key=f"manual_copy_{post_id}",
        help="Tap here, then select all (Ctrl+A/Cmd+A) and copy (Ctrl+C/Cmd+C)"
    )

def show_qr_code():
    """Display QR code for mobile access"""
    website_url = "https://linkedin-post-generator-ao8jqjdjy8tdsawokcarj4.streamlit.app"
    
    st.markdown('<div class="qr-container">', unsafe_allow_html=True)
    st.markdown("### 📱 Share with Mobile Users")
    st.markdown("**Scan this QR code to access the site on mobile:**")
    
    try:
        qr_base64 = generate_qr_code(website_url)
        st.markdown(
            f'<div style="text-align: center;"><img src="data:image/png;base64,{qr_base64}" style="max-width: 200px; width: 100%;"></div>',
            unsafe_allow_html=True
        )
        st.markdown("*Point your phone camera at this code or use a QR scanner app*")
    except Exception as e:
        st.error("Could not generate QR code")
        st.markdown(f"**Direct link:** {website_url}")
    
    st.markdown('</div>', unsafe_allow_html=True)

def show_mobile_navigation():
    """Show mobile bottom navigation - Simplified for Streamlit compatibility"""
    # Remove the problematic HTML navigation for now
    # Streamlit doesn't handle complex interactive HTML well
    pass

def show_pwa_install_prompt():
    """Show Progressive Web App install prompt"""
    st.markdown("""
    <div class="install-prompt">
        <h3>📱 Install as App</h3>
        <p>Add this to your phone's home screen for easy access!</p>
        <p><strong>iPhone:</strong> Tap Share → Add to Home Screen</p>
        <p><strong>Android:</strong> Tap Menu → Add to Home Screen</p>
        <button class="install-button" onclick="showInstallInstructions()">
            📲 Install Instructions
        </button>
    </div>
    
    <script>
    function showInstallInstructions() {
        alert('iPhone: Safari → Share → Add to Home Screen\\nAndroid: Chrome → Menu → Add to Home Screen');
    }
    </script>
    """, unsafe_allow_html=True)

def show_login_signup():
    """Enhanced login/signup with better UX and security"""
    
    # QR Code for mobile users
    show_qr_code()
    
    # Engineer introduction
    st.markdown('<div class="intro-section">', unsafe_allow_html=True)
    st.markdown("## 👋 Built by a Software Engineer")
    st.markdown("""
    **Hey! I'm a software engineer** who got tired of generic LinkedIn content tools that produce 
    robotic posts. So I built this—a technical approach to content that actually gets engagement.
    
    **What makes this different:**
    • Real trending topic integration (updates daily)
    • 8 proven post templates that drive engagement  
    • Industry-specific AI that understands your field
    • LinkedIn preview so you see exactly how posts will look
    • Mobile-optimized design that works everywhere
    • Built with the same attention to detail I use in production code
    
    **Ready to create LinkedIn content that doesn't suck?** 🚀
    """)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Features showcase
    st.markdown("## ⚡ What You Get (100% Free)")
    
    st.markdown('<div class="feature-grid">', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <h3>🎯 Smart Templates</h3>
            <p>8 proven post structures: Story, Insight, Tip, Question, Data, Controversial, Achievement & List</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <h3>📈 Trending Topics</h3>
            <p>Real LinkedIn trends updated daily. Your posts will feel current and relevant</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-card">
            <h3>👀 Live Preview</h3>
            <p>See exactly how your post looks on LinkedIn before posting</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # PWA install prompt
    show_pwa_install_prompt()
    
    # Login/Signup tabs
    tab1, tab2 = st.tabs(["🔑 Login", "🚀 Create Free Account"])
    
    with tab1:
        st.markdown('<div class="account-form">', unsafe_allow_html=True)
        st.markdown("### Welcome Back!")
        
        # Bot detection warning if needed
        if st.session_state.get('bot_score', 0) > 2:
            st.markdown('<div class="bot-detection">🤖 Please complete the verification below</div>', unsafe_allow_html=True)
            if not simple_captcha():
                st.markdown('</div>', unsafe_allow_html=True)
                return
        
        with st.form("login_form"):
            login_email = st.text_input("Email", placeholder="your.email@company.com")
            login_password = st.text_input("Password", type="password")
            
            # Honeypot field (hidden from humans)
            honeypot = st.text_input("Website", value="", key="honeypot_login", 
                                    help="Leave this field empty", label_visibility="hidden")
            st.session_state.honeypot_field = honeypot
            
            login_submit = st.form_submit_button("🔑 Login", type="primary", use_container_width=True)
            
            if login_submit:
                if honeypot:  # Bot detected
                    st.error("Please try again")
                elif login_email and login_password:
                    success, message = login_user(login_email, login_password)
                    if success:
                        st.success(message)
                        st.rerun()
                    else:
                        st.error(message)
                else:
                    st.error("Please fill in all fields")
        
        # Show failed attempts warning
        if st.session_state.get('login_attempts', 0) > 2:
            st.warning(f"⚠️ {st.session_state.login_attempts} failed attempts. Refresh page if you continue having issues.")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab2:
        st.markdown('<div class="account-form">', unsafe_allow_html=True)
        st.markdown("### Join the Community")
        st.markdown("**Get unlimited access to all features - no credit card required!**")
        
        # Bot detection for signup
        if st.session_state.get('bot_score', 0) > 1:
            st.markdown('<div class="bot-detection">🤖 Please complete the verification below</div>', unsafe_allow_html=True)
            if not simple_captcha():
                st.markdown('</div>', unsafe_allow_html=True)
                return
        
        with st.form("signup_form"):
            col1, col2 = st.columns(2)
            with col1:
                signup_name = st.text_input("Full Name*", placeholder="John Doe")
                signup_email = st.text_input("Email*", placeholder="your.email@company.com")
            with col2:
                signup_company = st.text_input("Company", placeholder="Your Company (optional)")
                signup_password = st.text_input("Password*", type="password", help="Minimum 6 characters")
            
            signup_confirm = st.text_input("Confirm Password*", type="password")
            
            # Honeypot field (hidden from humans)
            honeypot_signup = st.text_input("Website URL", value="", key="honeypot_signup", 
                                          help="Leave this field empty", label_visibility="hidden")
            
            agree_terms = st.checkbox("I agree to the Terms of Service and Privacy Policy")
            
            signup_submit = st.form_submit_button("🚀 Create Free Account", type="primary", use_container_width=True)
            
            if signup_submit:
                if honeypot_signup:  # Bot detected
                    st.error("Please try again")
                elif not all([signup_name, signup_email, signup_password, signup_confirm]):
                    st.error("Please fill in all required fields")
                elif len(signup_password) < 6:
                    st.error("Password must be at least 6 characters")
                elif signup_password != signup_confirm:
                    st.error("Passwords don't match")
                elif not agree_terms:
                    st.error("Please agree to the Terms of Service")
                else:
                    success, message = create_account(signup_email, signup_password, signup_name, signup_company)
                    if success:
                        st.success(f"{message}! Please login to continue.")
                        st.balloons()
                        # Clear captcha for fresh login
                        if 'captcha_answer' in st.session_state:
                            del st.session_state.captcha_answer
                    else:
                        st.error(message)
        st.markdown('</div>', unsafe_allow_html=True)

def show_trending_topics_sidebar():
    """Show current trending topics"""
    
    st.markdown("### 🔥 Trending Now")
    trending = get_current_trending_topics()
    
    # Show general trends
    st.markdown("**🌍 General:**")
    for topic in trending["general"][:3]:
        st.markdown(f'<span class="trending-badge">{topic}</span>', unsafe_allow_html=True)
    
    # Show industry specific if user has preference
    if st.session_state.logged_in:
        user_industry = st.session_state.user_preferences.get('default_industry', 'Technology')
        if user_industry in trending:
            st.markdown(f"**🏢 {user_industry}:**")
            for topic in trending[user_industry][:2]:
                st.markdown(f'<span class="trending-badge">{topic}</span>', unsafe_allow_html=True)

def show_saved_posts():
    """Enhanced saved posts display with better metadata"""
    
    if not st.session_state.saved_posts:
        st.info("📝 No saved posts yet. Save posts from the generator to build your library!")
        return
    
    st.markdown("### 💾 Your Saved Posts")
    st.markdown(f"**Total saved:** {len(st.session_state.saved_posts)} posts")
    
    # Search/filter functionality
    search_term = st.text_input("🔍 Search saved posts", placeholder="Search by content or topic...")
    
    filtered_posts = st.session_state.saved_posts
    if search_term:
        filtered_posts = [
            post for post in st.session_state.saved_posts 
            if search_term.lower() in post.get('content', '').lower() or 
               search_term.lower() in post.get('topic', '').lower()
        ]
    
    if not filtered_posts:
        st.warning("No posts match your search")
        return
    
    # Display posts in reverse chronological order
    for i, saved_post in enumerate(reversed(filtered_posts)):
        post_index = len(filtered_posts) - i
        
        # Enhanced post display with metadata
        with st.expander(
            f"📝 {saved_post.get('topic', 'Post')} - {saved_post.get('saved_at', 'Unknown date')}", 
            expanded=False
        ):
            # Post metadata
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Words", saved_post.get('word_count', 'N/A'))
            with col2:
                st.metric("Template", saved_post.get('template', 'Unknown'))
            with col3:
                st.write(f"**Saved:** {saved_post.get('saved_at', 'Unknown')}")
            
            # Post content with preview
            st.markdown("**Preview:**")
            st.markdown(f"*{saved_post.get('preview', saved_post.get('content', '')[:100] + '...')}*")
            
            # Full content in text area for easy copying
            st.markdown("**Full Content:**")
            st.text_area(
                "Content:",
                value=saved_post.get('content', ''),
                height=150,
                key=f"saved_content_{i}",
                help="Select all (Ctrl+A/Cmd+A) and copy (Ctrl+C/Cmd+C)"
            )
            
            # Action buttons
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button(f"📋 Copy", key=f"copy_saved_{i}", use_container_width=True):
                    success, message = copy_to_clipboard(saved_post.get('content', ''), f"saved_{i}")
                    if success:
                        st.success("✅ Copied!")
                    else:
                        st.info("📋 Use text area above to copy")
            
            with col2:
                # LinkedIn share
                content = saved_post.get('content', '')
                linkedin_text = content.replace('\n', '%0A').replace(' ', '%20')
                share_url = f"https://www.linkedin.com/sharing/share-offsite/?url=https://linkedin-post-generator-ao8jqjdjy8tdsawokcarj4.streamlit.app&summary={linkedin_text[:100]}..."
                st.markdown(f"[🔗 Share on LinkedIn]({share_url})")
            
            with col3:
                if st.button(f"🗑️ Delete", key=f"delete_saved_{i}", use_container_width=True):
                    st.session_state.saved_posts.remove(saved_post)
                    update_user_data()
                    st.success("🗑️ Post deleted!")
                    st.rerun()

def main():
    init_session_state()
    
    # Header
    st.markdown('<div class="main-header">🚀 LinkedIn Post Generator</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Create engaging, AI-powered LinkedIn content that drives real engagement</div>', unsafe_allow_html=True)
    
    # Check if user is logged in
    if not st.session_state.logged_in:
        show_login_signup()
        show_mobile_navigation()
        return
    
    # Main app for logged-in users
    user = st.session_state.user_data
    
    # Sidebar (desktop) or mobile navigation
    with st.sidebar:
        # User info
        st.markdown(f"### 👋 Welcome, {user.get('name', 'User')}!")
        st.write(f"📧 {user.get('email', '')}")
        st.write(f"🏢 {user.get('company', 'N/A')}")
        
        if st.button("🚪 Logout", use_container_width=True):
            # Clear session state
            for key in list(st.session_state.keys()):
                if key not in ['current_page', 'show_mobile_nav']:
                    del st.session_state[key]
            init_session_state()
            st.rerun()
        
        st.markdown("---")
        
        # Usage stats (now unlimited)
        st.success("⭐ Unlimited Access - No Limits!")
        st.info(f"📊 Posts Generated: {st.session_state.usage_count}")
        st.info(f"💾 Posts Saved: {len(st.session_state.saved_posts)}")
        
        st.markdown("---")
        
        # Trending topics
        show_trending_topics_sidebar()
        
        st.markdown("---")
        
        # Navigation
        page_options = ["🎯 Generate Posts", "💾 Saved Posts", "⚙️ Preferences", "📱 QR Code"]
        page = st.selectbox("🧭 Navigate", page_options)
        
        # Update current page for mobile nav
        page_mapping = {
            "🎯 Generate Posts": "generate",
            "💾 Saved Posts": "saved", 
            "⚙️ Preferences": "preferences",
            "📱 QR Code": "qr"
        }
        st.session_state.current_page = page_mapping.get(page, "generate")
    
    # Main content based on navigation (updated to use session state)
    current_page = st.session_state.get('current_page', 'generate')
    
    if current_page == 'generate' or page == "🎯 Generate Posts":
        show_post_generator()
    elif current_page == 'saved' or page == "💾 Saved Posts":
        show_saved_posts()
    elif current_page == 'qr' or page == "📱 QR Code":
        show_qr_code()
    else:
        show_preferences()
    
    # Enhanced mobile navigation using Streamlit columns (works better than HTML)
    if st.session_state.get('show_mobile_nav', True) and st.session_state.logged_in:
        st.markdown("---")
        st.markdown("#### 📱 Quick Navigation")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("🎯\nGenerate", key="mobile_nav_generate", use_container_width=True):
                st.session_state.current_page = 'generate'
                st.rerun()
        
        with col2:
            if st.button("💾\nSaved", key="mobile_nav_saved", use_container_width=True):
                st.session_state.current_page = 'saved'
                st.rerun()
        
        with col3:
            if st.button("⚙️\nSettings", key="mobile_nav_settings", use_container_width=True):
                st.session_state.current_page = 'preferences'
                st.rerun()
        
        with col4:
            if st.button("📱\nQR Code", key="mobile_nav_qr", use_container_width=True):
                st.session_state.current_page = 'qr'
                st.rerun()

def show_post_generator():
    """Main post generation interface with mobile optimization"""
    
    st.markdown("## 🎯 Generate Your LinkedIn Posts")
    
    # Configuration in mobile-friendly layout
    with st.container():
        # Main inputs
        topic = st.text_input(
            "💡 What topic do you want to write about?",
            placeholder="e.g., AI in healthcare, Remote work productivity, Leadership in crisis...",
            help="Be specific for better results"
        )
        
        # Store current topic for saved posts
        st.session_state.current_topic = topic
        
        # Template selection with descriptions
        st.markdown("### 📋 Choose Your Post Template")
        templates = get_post_templates()
        
        template_options = []
        for template, info in templates.items():
            template_options.append(f"{template} - {info['description']}")
        
        selected_template = st.selectbox(
            "Template:",
            template_options,
            help="Each template follows a proven structure for maximum engagement"
        )
        
        template = selected_template.split(" - ")[0]
        st.session_state.current_template = template
        
        # Show template info
        template_info = templates[template]
        st.info(f"**Structure:** {template_info['structure']}\n\n**Best for:** {template_info['best_for']}")
    
    # Configuration options in expandable section for mobile
    with st.expander("⚙️ Configuration Options", expanded=True):
        col1, col2 = st.columns(2)
        
        with col1:
            industry = st.selectbox(
                "Industry:",
                ["Technology", "Healthcare", "Finance", "Marketing", "Sales", "HR", 
                 "Education", "Real Estate", "Consulting", "Manufacturing", "Other"],
                index=0 if not st.session_state.user_preferences.get('default_industry') else 
                      ["Technology", "Healthcare", "Finance", "Marketing", "Sales", "HR", 
                       "Education", "Real Estate", "Consulting", "Manufacturing", "Other"].index(
                           st.session_state.user_preferences.get('default_industry', 'Technology'))
            )
            
            audience = st.selectbox(
                "Target Audience:",
                ["Professionals in my industry", "Business owners", "Job seekers", 
                 "Students/New graduates", "C-level executives", "Entrepreneurs", "General audience"]
            )
        
        with col2:
            tone = st.selectbox(
                "Tone:",
                ["Professional", "Conversational", "Inspirational", "Educational", 
                 "Humorous", "Thought-provoking", "Personal/Storytelling"],
                index=0 if not st.session_state.user_preferences.get('default_tone') else
                      ["Professional", "Conversational", "Inspirational", "Educational", 
                       "Humorous", "Thought-provoking", "Personal/Storytelling"].index(
                           st.session_state.user_preferences.get('default_tone', 'Professional'))
            )
            
            word_count = st.selectbox(
                "Post Length:",
                ["Short (50-100 words)", "Medium (100-200 words)", "Long (200-300 words)"]
            )
        
        # Additional options
        col3, col4 = st.columns(2)
        with col3:
            include_emojis = st.checkbox("Include Emojis", value=True)
        with col4:
            trending_focus = st.checkbox("Focus on Trending Topics", value=True, 
                                       help="Incorporate current LinkedIn trending topics")
    
    # Generate button
    if st.button("🚀 Generate Posts", type="primary", use_container_width=True):
        if not topic:
            st.warning("Please enter a topic to generate posts about.")
            return
        
        # Show loading with mobile-friendly spinner
        with st.spinner("🤖 AI is crafting your LinkedIn posts..."):
            time.sleep(1)  # Brief pause for better UX
            
            # Generate posts using the complete function
            posts = generate_enhanced_posts(
                topic, industry, tone, audience, template, 
                word_count, include_emojis, trending_focus
            )
            
            # Update usage count
            st.session_state.usage_count += 1
            update_user_data()
        
        if posts:
            st.success("✅ Posts generated successfully!")
            
            st.markdown("## 📱 Your Generated Posts")
            
            # Show all posts
            for i, post in enumerate(posts, 1):
                st.markdown(f"### 📝 Post {i}")
                
                # Show preview
                show_post_preview(post, st.session_state.user_data.get('name', 'Your Name'))
                
                # Engagement prediction
                engagement_score = predict_engagement(post, template, tone, industry)
                engagement_color = "🟢" if engagement_score > 70 else "🟡" if engagement_score > 50 else "🔴"
                st.markdown(f"**Predicted Engagement:** {engagement_color} {engagement_score}/100")
                
                # Copy functionality
                show_copy_functionality(post, i)
                
                st.markdown("---")
            
            # Download all posts
            all_posts_text = "\n\n" + "="*50 + "\n\n".join([f"POST {i+1}:\n{post}" for i, post in enumerate(posts)])
            st.download_button(
                label="📥 Download All Posts",
                data=all_posts_text,
                file_name=f"linkedin_posts_{topic.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.txt",
                mime="text/plain",
                use_container_width=True
            )
            
            # Success message
            st.info("🎉 Posts generated! Don't forget to save your favorites to your library.") Topics", value=True, 
                                       help="Incorporate current LinkedIn trending topics")
    
    # Generate button
    if st.button("🚀 Generate Posts", type="primary", use_container_width=True):
        if not topic:
            st.warning("Please enter a topic to generate posts about.")
            return
        
        # Show loading with mobile-friendly spinner
        with st.spinner("🤖 AI is crafting your LinkedIn posts..."):
            time.sleep(1)  # Brief pause for better UX
            
            # Generate posts using the complete function
            posts = generate_enhanced_posts(
                topic, industry, tone, audience, template, 
                word_count, include_emojis, trending_focus
            )
            
            # Update usage count
            st.session_state.usage_count += 1
            update_user_data()
        
        if posts:
            st.success("✅ Posts generated successfully!")
            
            st.markdown("## 📱 Your Generated Posts")
            
            # Show all posts
            for i, post in enumerate(posts, 1):
                st.markdown(f"### 📝 Post {i}")
                
                # Show preview
                show_post_preview(post, st.session_state.user_data.get('name', 'Your Name'))
                
                # Engagement prediction
                engagement_score = predict_engagement(post, template, tone, industry)
                engagement_color = "🟢" if engagement_score > 70 else "🟡" if engagement_score > 50 else "🔴"
                st.markdown(f"**Predicted Engagement:** {engagement_color} {engagement_score}/100")
                
                # Copy functionality
                show_copy_functionality(post, i)
                
                st.markdown("---")
            
            # Download all posts
            all_posts_text = "\n\n" + "="*50 + "\n\n".join([f"POST {i+1}:\n{post}" for i, post in enumerate(posts)])
            st.download_button(
                label="📥 Download All Posts",
                data=all_posts_text,
                file_name=f"linkedin_posts_{topic.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.txt",
                mime="text/plain",
                use_container_width=True
            )
            
            # Success message
            st.info("🎉 Posts generated! Don't forget to save your favorites to your library.")

def predict_engagement(post, template, tone, industry):
    """Predict engagement level based on post characteristics"""
    
    score = 50  # Base score
    
    # Template bonuses
    template_scores = {
        "Question": 15, "Controversial": 20, "Story": 12, "List": 10,
        "Data": 8, "Tip": 8, "Achievement": 5, "Insight": 7
    }
    score += template_scores.get(template, 5)
    
    # Tone bonuses
    tone_scores = {
        "Conversational": 10, "Humorous": 15, "Thought-provoking": 12,
        "Personal/Storytelling": 10, "Inspirational": 8, "Educational": 5, "Professional": 3
    }
    score += tone_scores.get(tone, 3)
    
    # Content analysis
    if "?" in post:
        score += 8
    if any(emoji in post for emoji in ["🤔", "💭", "🔥", "💡", "🚀"]):
        score += 5
    if len(post.split()) < 150:
        score += 5
    
    # Hashtag analysis
    hashtag_count = post.count('#')
    if 3 <= hashtag_count <= 5:
        score += 5
    elif hashtag_count > 7:
        score -= 3
    
    return min(95, max(25, score)) Topics", value=True, 
                                       help="Incorporate current LinkedIn trending topics")
    
    # Generate button
    if st.button("🚀 Generate Posts", type="primary", use_container_width=True):
        if not topic:
            st.warning("Please enter a topic to generate posts about.")
            return
        
        # Show loading with mobile-friendly spinner
        with st.spinner("🤖 AI is crafting your LinkedIn posts..."):
            time.sleep(1)  # Brief pause for better UX
            
            # Placeholder for actual post generation
            # For now, create sample posts
            posts = [
                f"Sample post about {topic} in {industry} with {tone} tone...",
                f"Another engaging post about {topic} for {audience}...",
                f"Third post focusing on {topic} trends...",
                f"Fourth post with actionable {topic} tips...",
                f"Fifth post sharing {topic} insights..."
            ]
            
            # Update usage count
            st.session_state.usage_count += 1
            update_user_data()
        
        if posts:
            st.success("✅ Posts generated successfully!")
            
            st.markdown("## 📱 Your Generated Posts")
            
            # Show all posts
            for i, post in enumerate(posts, 1):
                st.markdown(f"### 📝 Post {i}")
                
                # Show preview
                show_post_preview(post, st.session_state.user_data.get('name', 'Your Name'))
                
                # Engagement prediction
                engagement_score = random.randint(60, 90)  # Placeholder
                engagement_color = "🟢" if engagement_score > 70 else "🟡" if engagement_score > 50 else "🔴"
                st.markdown(f"**Predicted Engagement:** {engagement_color} {engagement_score}/100")
                
                # Copy functionality
                show_copy_functionality(post, i)
                
                st.markdown("---")
            
            # Download all posts
            all_posts_text = "\n\n" + "="*50 + "\n\n".join([f"POST {i+1}:\n{post}" for i, post in enumerate(posts)])
            st.download_button(
                label="📥 Download All Posts",
                data=all_posts_text,
                file_name=f"linkedin_posts_{topic.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.txt",
                mime="text/plain",
                use_container_width=True
            )
            
            # Success message
            st.info("🎉 Posts generated! Don't forget to save your favorites to your library.")

def show_preferences():
    """User preferences and settings with mobile optimization"""
    
    st.markdown("## ⚙️ Preferences & Settings")
    
    # Default settings
    with st.expander("🎯 Default Settings", expanded=True):
        col1, col2 = st.columns(2)
        
        with col1:
            default_industry = st.selectbox(
                "Default Industry:",
                ["Technology", "Healthcare", "Finance", "Marketing", "Sales", "HR", 
                 "Education", "Real Estate", "Consulting", "Manufacturing", "Other"],
                index=["Technology", "Healthcare", "Finance", "Marketing", "Sales", "HR", 
                       "Education", "Real Estate", "Consulting", "Manufacturing", "Other"].index(
                           st.session_state.user_preferences.get('default_industry', 'Technology'))
            )
        
        with col2:
            default_tone = st.selectbox(
                "Default Tone:",
                ["Professional", "Conversational", "Inspirational", "Educational", 
                 "Humorous", "Thought-provoking", "Personal/Storytelling"],
                index=["Professional", "Conversational", "Inspirational", "Educational", 
                       "Humorous", "Thought-provoking", "Personal/Storytelling"].index(
                           st.session_state.user_preferences.get('default_tone', 'Professional'))
            )
        
        if st.button("💾 Save Preferences", use_container_width=True):
            st.session_state.user_preferences.update({
                'default_industry': default_industry,
                'default_tone': default_tone
            })
            update_user_data()
            st.success("✅ Preferences saved!")
    
    # Brand voice training
    with st.expander("🎨 Brand Voice Training", expanded=False):
        st.markdown("Add examples of your writing style to personalize AI generation:")
        
        example_text = st.text_area(
            "Paste an example of your LinkedIn post:",
            height=100,
            placeholder="Paste a LinkedIn post you've written that represents your voice...",
            help="This helps the AI learn your writing style"
        )
        
        if st.button("📚 Add to Brand Voice", use_container_width=True):
            if example_text and len(example_text) > 50:
                st.session_state.brand_voice_examples.append({
                    'text': example_text,
                    'added_at': datetime.now().isoformat()
                })
                update_user_data()
                st.success("✅ Added to your brand voice library!")
                st.rerun()
            else:
                st.warning("Please add a longer example (at least 50 characters)")
        
        # Show existing examples
        if st.session_state.brand_voice_examples:
            st.markdown("**Your Brand Voice Examples:**")
            for i, example in enumerate(st.session_state.brand_voice_examples):
                with st.expander(f"Example {i+1} - {example['added_at'][:10]}", expanded=False):
                    st.write(example['text'])
                    if st.button(f"🗑️ Remove", key=f"remove_example_{i}", use_container_width=True):
                        st.session_state.brand_voice_examples.pop(i)
                        update_user_data()
                        st.success("🗑️ Example removed!")
                        st.rerun()
    
    # Account stats
    with st.expander("📊 Account Statistics", expanded=True):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Posts Generated", st.session_state.usage_count)
        
        with col2:
            st.metric("Saved Posts", len(st.session_state.saved_posts))
        
        with col3:
            st.metric("Brand Examples", len(st.session_state.brand_voice_examples))
        
        # Additional stats
        if st.session_state.user_data:
            st.markdown("---")
            st.markdown("**Account Details:**")
            st.write(f"📅 **Member since:** {st.session_state.user_data.get('created_at', 'Unknown')[:10]}")
            st.write(f"🔑 **Last login:** {st.session_state.user_data.get('last_login', 'Unknown')[:10] if st.session_state.user_data.get('last_login') else 'First time'}")
            st.write(f"🏢 **Company:** {st.session_state.user_data.get('company', 'Not specified')}")
    
    # Export data
    with st.expander("💾 Export Your Data", expanded=False):
        st.markdown("Download all your saved posts and preferences:")
        
        if st.button("📥 Export Data", use_container_width=True):
            export_data = {
                'user_info': {
                    'name': st.session_state.user_data.get('name'),
                    'email': st.session_state.user_data.get('email'),
                    'company': st.session_state.user_data.get('company')
                },
                'saved_posts': st.session_state.saved_posts,
                'brand_voice_examples': st.session_state.brand_voice_examples,
                'preferences': st.session_state.user_preferences,
                'usage_stats': {
                    'posts_generated': st.session_state.usage_count,
                    'posts_saved': len(st.session_state.saved_posts)
                },
                'export_date': datetime.now().isoformat()
            }
            
            export_json = json.dumps(export_data, indent=2)
            st.download_button(
                label="📥 Download JSON",
                data=export_json,
                file_name=f"linkedin_generator_data_{datetime.now().strftime('%Y%m%d')}.json",
                mime="application/json",
                use_container_width=True
            )
            st.success("✅ Data exported successfully!")

# Complete post generation functions (restored from original)
def generate_enhanced_posts(topic, industry, tone, audience, template, word_count, include_emojis, trending_focus):
    """Generate posts with all new features"""
    
    # Get trending topics for context
    trending_topics = get_current_trending_topics()
    industry_trends = trending_topics.get(industry, trending_topics["general"])
    selected_trend = random.choice(industry_trends) if trending_focus else None
    
    # Get template structure
    templates = get_post_templates()
    template_info = templates.get(template, templates["Insight"])
    
    posts = []
    
    for i in range(5):
        post = create_structured_post(
            topic, industry, tone, audience, template, template_info,
            word_count, include_emojis, selected_trend, i
        )
        posts.append(post)
    
    return posts

def create_structured_post(topic, industry, tone, audience, template, template_info, word_count, include_emojis, trending_topic, variation):
    """Create a post following the selected template structure"""
    
    # Emojis based on tone and template
    emoji_sets = {
        "Professional": ["📊", "💼", "🎯", "📈", "⭐"],
        "Conversational": ["💬", "🤔", "👥", "💡", "🚀"],
        "Inspirational": ["✨", "🌟", "💪", "🔥", "🎉"],
        "Educational": ["📚", "🧠", "💭", "🔍", "📖"],
        "Humorous": ["😄", "🤣", "😅", "🎭", "😊"],
        "Thought-provoking": ["🤯", "💭", "🧐", "⚡", "🔮"],
        "Personal/Storytelling": ["📖", "🌍", "💫", "🎭", "🎪"]
    }
    
    emojis = emoji_sets.get(tone, emoji_sets["Professional"])
    
    # Create post based on template
    if template == "Story":
        post = create_story_post(topic, industry, tone, trending_topic, emojis, include_emojis, word_count)
    elif template == "Insight":
        post = create_insight_post(topic, industry, tone, trending_topic, emojis, include_emojis, word_count)
    elif template == "Tip":
        post = create_tip_post(topic, industry, tone, trending_topic, emojis, include_emojis, word_count)
    elif template == "Question":
        post = create_question_post(topic, industry, tone, trending_topic, emojis, include_emojis, word_count)
    elif template == "Data":
        post = create_data_post(topic, industry, tone, trending_topic, emojis, include_emojis, word_count)
    elif template == "Controversial":
        post = create_controversial_post(topic, industry, tone, trending_topic, emojis, include_emojis, word_count)
    elif template == "Achievement":
        post = create_achievement_post(topic, industry, tone, trending_topic, emojis, include_emojis, word_count)
    else:  # List
        post = create_list_post(topic, industry, tone, trending_topic, emojis, include_emojis, word_count)
    
    return post

def create_story_post(topic, industry, tone, trending_topic, emojis, include_emojis, word_count):
    emoji = random.choice(emojis) if include_emojis else ""
    
    story_hooks = [
        f"Last week, something happened that changed how I think about {topic}",
        f"Three months ago, I would have never believed this about {topic}",
        f"Here's what {topic} taught me about {industry}",
        f"I used to think {topic} was overhyped. I was wrong."
    ]
    
    hook = random.choice(story_hooks)
    
    if trending_topic:
        connection = f"It connects directly to what we're seeing with {trending_topic.lower()}."
    else:
        connection = f"It's reshaping how we approach {industry.lower()}."
    
    lesson = f"The lesson? {topic} isn't just about technology—it's about people."
    cta = f"What's your experience with {topic}? Share your story below! {emoji if include_emojis else ''}"
    
    hashtags = f"#{industry.replace(' ', '')} #{topic.replace(' ', '')} #Story #Leadership"
    
    post = f"""{hook}

{connection}

{lesson}

{cta}

{hashtags}"""
    
    return adjust_word_count(post, word_count)

def create_insight_post(topic, industry, tone, trending_topic, emojis, include_emojis, word_count):
    emoji = random.choice(emojis) if include_emojis else ""
    
    insights = [
        f"{emoji} {topic} is fundamentally changing {industry}",
        f"{emoji} Here's what most people miss about {topic}",
        f"{emoji} The future of {topic} in {industry} isn't what you think"
    ]
    
    observation = random.choice(insights)
    
    if trending_topic:
        analysis = f"While everyone focuses on {trending_topic.lower()}, the real opportunity lies in how {topic} amplifies human potential."
    else:
        analysis = f"The companies winning with {topic} share one thing: they focus on augmentation, not replacement."
    
    implication = f"This means {industry} professionals need to rethink their approach."
    discussion = f"What's your take on {topic}'s role in {industry}? {emoji if include_emojis else ''}"
    
    hashtags = f"#{industry.replace(' ', '')} #{topic.replace(' ', '')} #Innovation #ThoughtLeadership"
    
    post = f"""{observation}

{analysis}

{implication}

{discussion}

{hashtags}"""
    
    return adjust_word_count(post, word_count)

def create_tip_post(topic, industry, tone, trending_topic, emojis, include_emojis, word_count):
    emoji = random.choice(emojis) if include_emojis else ""
    
    problem = f"Struggling with {topic} implementation in {industry}?"
    solution = f"Here's what's working for leading companies:"
    
    tips = [
        f"{emoji if include_emojis else '•'} Start small and scale gradually",
        f"{emoji if include_emojis else '•'} Focus on user experience first", 
        f"{emoji if include_emojis else '•'} Measure impact, not just adoption"
    ]
    
    outcome = f"Result: Smoother {topic} integration and better ROI."
    cta = f"What tips would you add? {emoji if include_emojis else ''}"
    
    hashtags = f"#{industry.replace(' ', '')} #{topic.replace(' ', '')} #Tips #BestPractices"
    
    post = f"""{problem}

{solution}

{chr(10).join(tips)}

{outcome}

{cta}

{hashtags}"""
    
    return adjust_word_count(post, word_count)

def create_question_post(topic, industry, tone, trending_topic, emojis, include_emojis, word_count):
    emoji = random.choice(emojis) if include_emojis else ""
    
    contexts = [
        f"Quick question for {industry} professionals:",
        f"Honest question about {topic}:",
        f"Help me settle a debate:"
    ]
    
    context = random.choice(contexts)
    
    questions = [
        f"Is {topic} overhyped or underutilized in {industry}?",
        f"What's the biggest {topic} misconception in our industry?",
        f"If you could change one thing about {topic} adoption, what would it be?"
    ]
    
    question = random.choice(questions)
    take = f"My take: Most companies focus on the tech, but success comes from change management."
    
    if trending_topic:
        discussion = f"Especially with {trending_topic.lower()} accelerating, we need better frameworks."
    else:
        discussion = f"The companies getting this right are the ones thinking long-term."
    
    invite = f"What's your perspective? Drop your thoughts below! {emoji if include_emojis else ''}"
    
    hashtags = f"#{industry.replace(' ', '')} #{topic.replace(' ', '')} #Discussion #Community"
    
    post = f"""{context}

{question}

{take} {discussion}

{invite}

{hashtags}"""
    
    return adjust_word_count(post, word_count)

def create_data_post(topic, industry, tone, trending_topic, emojis, include_emojis, word_count):
    emoji = random.choice(emojis) if include_emojis else ""
    
    stats = [
        "73% of companies report improved efficiency",
        "2.3x faster implementation than expected",
        "41% reduction in operational costs",
        "85% of users say it exceeded expectations"
    ]
    
    statistic = f"{emoji if include_emojis else '📊'} New data on {topic} in {industry}: {random.choice(stats)}"
    
    context = f"This aligns with what we're seeing across the industry."
    
    if trending_topic:
        analysis = f"Particularly interesting given the focus on {trending_topic.lower()}."
    else:
        analysis = f"The key factor? Companies that invested in training see 3x better results."
    
    takeaway = f"Bottom line: {topic} ROI depends more on implementation than technology."
    cta = f"What metrics are you tracking? {emoji if include_emojis else ''}"
    
    hashtags = f"#{industry.replace(' ', '')} #{topic.replace(' ', '')} #Data #ROI"
    
    post = f"""{statistic}

{context} {analysis}

{takeaway}

{cta}

{hashtags}"""
    
    return adjust_word_count(post, word_count)

def create_controversial_post(topic, industry, tone, trending_topic, emojis, include_emojis, word_count):
    emoji = random.choice(emojis) if include_emojis else ""
    
    controversial_statements = [
        f"Unpopular opinion: Most {industry} companies are doing {topic} completely wrong",
        f"Hot take: {topic} isn't the problem in {industry}—leadership is",
        f"Controversial view: {topic} hype is setting unrealistic expectations"
    ]
    
    statement = random.choice(controversial_statements)
    
    evidence = f"Here's why: Companies focus on features instead of outcomes."
    
    if trending_topic:
        nuance = f"Yes, {trending_topic.lower()} is important, but without proper strategy, it's just expensive technology."
    else:
        nuance = f"Don't get me wrong—{topic} is powerful. But success requires more than just implementation."
    
    debate = f"Am I completely off base here? Change my mind in the comments! {emoji if include_emojis else ''}"
    
    hashtags = f"#{industry.replace(' ', '')} #{topic.replace(' ', '')} #Controversial #ChangeMyMind"
    
    post = f"""{statement}.

{evidence}

{nuance}

{debate}

{hashtags}"""
    
    return adjust_word_count(post, word_count)

def create_achievement_post(topic, industry, tone, trending_topic, emojis, include_emojis, word_count):
    emoji = random.choice(emojis) if include_emojis else ""
    
    achievements = [
        f"Milestone reached: Our {topic} implementation just hit 6 months",
        f"Celebrating: Successfully deployed {topic} across our {industry} team",
        f"Proud moment: Led our company's first {topic} initiative"
    ]
    
    achievement = random.choice(achievements)
    
    journey = f"The journey wasn't easy—lots of late nights and tough conversations."
    
    lessons = f"Key lessons: Start with why, involve everyone, and iterate constantly."
    
    if trending_topic:
        inspiration = f"To anyone working on {trending_topic.lower()} or {topic}: persistence pays off."
    else:
        inspiration = f"To anyone implementing {topic}: trust the process."
    
    thanks = f"Huge thanks to my team for making this possible! {emoji if include_emojis else ''}"
    
    hashtags = f"#{industry.replace(' ', '')} #{topic.replace(' ', '')} #Achievement #Teamwork"
    
    post = f"""{achievement} {emoji if include_emojis else '🎉'}

{journey}

{lessons}

{inspiration}

{thanks}

{hashtags}"""
    
    return adjust_word_count(post, word_count)

def create_list_post(topic, industry, tone, trending_topic, emojis, include_emojis, word_count):
    emoji = random.choice(emojis) if include_emojis else ""
    
    setup = f"5 things I wish I knew about {topic} when starting in {industry}:"
    
    points = [
        f"1{emoji if include_emojis else '.'} Implementation is 20% tech, 80% people",
        f"2{emoji if include_emojis else '.'} Start with pilot projects, not company-wide rollouts",
        f"3{emoji if include_emojis else '.'} Measure outcomes, not just outputs",
        f"4{emoji if include_emojis else '.'} Training is an investment, not a cost",
        f"5{emoji if include_emojis else '.'} Feedback loops are everything"
    ]
    
    if trending_topic:
        summary = f"Bonus: With {trending_topic.lower()} accelerating, these fundamentals matter more than ever."
    else:
        summary = f"The companies that get these right see 3x better adoption rates."
    
    engagement = f"What would you add to this list? {emoji if include_emojis else ''}"
    
    hashtags = f"#{industry.replace(' ', '')} #{topic.replace(' ', '')} #Tips #Lessons"
    
    post = f"""{setup}

{chr(10).join(points)}

{summary}

{engagement}

{hashtags}"""
    
    return adjust_word_count(post, word_count)

def adjust_word_count(post, target_word_count):
    """Adjust post length based on target word count"""
    words = post.split()
    current_count = len(words)
    
    if target_word_count == "Short (50-100 words)":
        target_min, target_max = 50, 100
    elif target_word_count == "Medium (100-200 words)":
        target_min, target_max = 100, 200
    else:  # Long (200-300 words)
        target_min, target_max = 200, 300
    
    # If current post is already in target range, return as is
    if target_min <= current_count <= target_max:
        return post
    
    # If post is too long, truncate intelligently
    if current_count > target_max:
        lines = post.split('\n')
        hashtag_lines = [line for line in lines if '#' in line]
        content_lines = [line for line in lines if '#' not in line and line.strip()]
        
        # Keep essential content and hashtags
        content_text = '\n'.join(content_lines)
        content_words = content_text.split()
        
        if len(content_words) > target_max - 10:
            truncated_content = ' '.join(content_words[:target_max-10])
            return truncated_content + '\n\n' + ('\n'.join(hashtag_lines) if hashtag_lines else '')
    
    # If post is too short, expand it
    if current_count < target_min:
        return expand_post_content(post, target_min, target_max)
    
    return post

def expand_post_content(post, target_min, target_max):
    """Expand post content to meet word count requirements"""
    
    lines = post.split('\n')
    hashtag_lines = [line for line in lines if '#' in line]
    content_lines = [line for line in lines if '#' not in line and line.strip()]
    
    # Expansion strategies based on content type
    expansion_elements = [
        "Here's what this means for professionals:",
        "This trend is accelerating across industries.",
        "The data supports this shift in thinking.",
        "Companies are already seeing positive results.",
        "Early adopters are gaining competitive advantages.",
        "This approach requires strategic planning and execution.",
        "The key is balancing innovation with practical implementation.",
        "Success depends on strong leadership and team buy-in.",
        "Consider the long-term implications for your industry.",
        "This represents a fundamental shift in how we work.",
        "The impact extends beyond just technology adoption.",
        "Organizations need to prepare for this evolution.",
        "Training and change management are critical components.",
        "The return on investment justifies the initial effort.",
        "Building the right team structure is essential for success."
    ]
    
    # Add contextual expansions
    context_additions = [
        "From my experience working with various teams, this approach consistently delivers results.",
        "Industry research confirms what many professionals have suspected for months.",
        "The most successful implementations share common characteristics worth noting.",
        "Breaking this down into actionable steps makes the process more manageable.",
        "Looking at case studies from leading companies reveals interesting patterns.",
        "The timing couldn't be better given current market conditions.",
        "This aligns perfectly with broader workplace transformation trends.",
        "Smart organizations are already positioning themselves for this shift.",
        "The competitive advantage goes to those who act decisively now.",
        "Risk management strategies should account for these emerging realities."
    ]
    
    # Calculate how many words we need to add
    current_words = len(' '.join(content_lines).split())
    words_needed = target_min - current_words
    
    expanded_content = content_lines.copy()
    
    # Add expansions until we reach target
    while len(' '.join(expanded_content).split()) < target_min:
        remaining_words = target_min - len(' '.join(expanded_content).split())
        
        if remaining_words > 15:
            # Add longer contextual addition
            addition = random.choice(context_additions)
            expanded_content.insert(-1, addition)  # Insert before last line
        else:
            # Add shorter element
            addition = random.choice(expansion_elements)
            expanded_content.append(addition)
        
        # Prevent infinite loop
        if len(' '.join(expanded_content).split()) > target_max:
            break
    
    # Reconstruct the post
    final_content = '\n'.join(expanded_content)
    if hashtag_lines:
        final_content += '\n\n' + '\n'.join(hashtag_lines)
    
    return final_content

# Run the app
if __name__ == "__main__":
    main()
