#!/usr/bin/env python3
"""
LinkedIn Post Generator - Professional Version
A streamlined tool for creating engaging LinkedIn content
Built with modern Python practices and clean architecture
"""

import hashlib
import json
import os
import random
import re
import time
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
import base64
import io

import streamlit as st
import qrcode
from PIL import Image

# Configuration
st.set_page_config(
    page_title="LinkedIn Post Generator Pro",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Constants
USER_DB_FILE = "users.json"
SESSION_TIMEOUT = 3600  # 1 hour

# Custom CSS
def render_css():
    """Render custom CSS styles"""
    st.markdown("""
    <style>
        .stApp {
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        }
        
        .main-header {
            font-size: clamp(2rem, 5vw, 3.5rem);
            font-weight: bold;
            text-align: center;
            background: linear-gradient(45deg, #0066cc, #004499);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 1rem;
        }
        
        .post-preview {
            background: white;
            border: 1px solid #e1e5e9;
            border-radius: 12px;
            padding: 1.5rem;
            margin: 1rem 0;
            box-shadow: 0 2px 12px rgba(0,0,0,0.08);
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto;
            position: relative;
        }
        
        .preview-header {
            display: flex;
            align-items: center;
            margin-bottom: 1rem;
            padding-bottom: 0.5rem;
            border-bottom: 1px solid #e1e5e9;
        }
        
        .preview-avatar {
            width: 48px;
            height: 48px;
            background: linear-gradient(45deg, #0066cc, #004499);
            border-radius: 50%;
            margin-right: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: bold;
        }
        
        .engagement-actions {
            display: flex;
            justify-content: space-between;
            padding: 1rem 0;
            border-top: 1px solid #e1e5e9;
            margin-top: 1rem;
            color: #65676b;
            font-size: 0.9rem;
        }
        
        .word-count {
            position: absolute;
            top: 10px;
            right: 10px;
            background: #42a5f5;
            color: white;
            padding: 4px 8px;
            border-radius: 12px;
            font-size: 0.75rem;
            font-weight: bold;
        }
        
        .feature-card {
            background: white;
            padding: 2rem;
            border-radius: 12px;
            box-shadow: 0 4px 16px rgba(0,0,0,0.08);
            text-align: center;
            transition: transform 0.2s ease;
        }
        
        .feature-card:hover {
            transform: translateY(-4px);
        }
        
        .trending-badge {
            background: linear-gradient(45deg, #ff6b6b, #ee5a52);
            color: white;
            padding: 0.25rem 0.75rem;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: 500;
            display: inline-block;
            margin: 0.25rem;
        }
        
        .stButton > button {
            width: 100%;
            border-radius: 8px;
            font-weight: 500;
            transition: all 0.2s ease;
        }
        
        .stButton > button:hover {
            transform: translateY(-1px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        }
    </style>
    """, unsafe_allow_html=True)


class SessionManager:
    """Handle session state management"""
    
    @staticmethod
    def init_session_state():
        """Initialize session state with default values"""
        defaults = {
            'logged_in': False,
            'user_data': {},
            'usage_count': 0,
            'saved_posts': [],
            'brand_voice_examples': [],
            'user_preferences': {
                'default_tone': 'Professional',
                'default_industry': 'Technology',
                'default_length': 'Medium (100-200 words)'
            },
            'current_page': 'generate',
            'login_attempts': 0,
            'last_activity': datetime.now(),
            'bot_score': 0
        }
        
        for key, value in defaults.items():
            if key not in st.session_state:
                st.session_state[key] = value


class UserManager:
    """Handle user authentication and data management"""
    
    @staticmethod
    def load_users() -> Dict:
        """Load users from JSON file"""
        try:
            if os.path.exists(USER_DB_FILE):
                with open(USER_DB_FILE, 'r') as f:
                    return json.load(f)
        except Exception as e:
            st.error(f"Error loading users: {e}")
        return {}
    
    @staticmethod
    def save_users(users: Dict) -> bool:
        """Save users to JSON file"""
        try:
            with open(USER_DB_FILE, 'w') as f:
                json.dump(users, f, indent=2)
            return True
        except Exception as e:
            st.error(f"Error saving users: {e}")
            return False
    
    @staticmethod
    def hash_password(password: str) -> str:
        """Hash password using SHA256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    @staticmethod
    def validate_email(email: str) -> Tuple[bool, str]:
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(pattern, email):
            return False, "Please enter a valid email address"
        
        # Check for common disposable email domains
        disposable_domains = {
            '10minutemail.com', 'guerrillamail.com', 'mailinator.com',
            'tempmail.org', 'throwaway.email', 'yopmail.com'
        }
        
        domain = email.split('@')[1].lower()
        if domain in disposable_domains:
            return False, "Disposable email addresses are not allowed"
        
        return True, "Valid email"
    
    @classmethod
    def create_account(cls, email: str, password: str, name: str, company: str = "") -> Tuple[bool, str]:
        """Create a new user account"""
        users = cls.load_users()
        
        if email in users:
            return False, "Email already exists"
        
        is_valid, message = cls.validate_email(email)
        if not is_valid:
            return False, message
        
        users[email] = {
            'password': cls.hash_password(password),
            'name': name,
            'company': company,
            'created_at': datetime.now().isoformat(),
            'usage_count': 0,
            'saved_posts': [],
            'brand_voice_examples': [],
            'preferences': {
                'default_tone': 'Professional',
                'default_industry': 'Technology',
                'default_length': 'Medium (100-200 words)'
            },
            'login_count': 0,
            'last_login': None
        }
        
        if cls.save_users(users):
            return True, "Account created successfully"
        return False, "Error creating account"
    
    @classmethod
    def login_user(cls, email: str, password: str) -> Tuple[bool, str]:
        """Authenticate user login"""
        users = cls.load_users()
        
        if email not in users:
            st.session_state.login_attempts += 1
            return False, "Email not found"
        
        if users[email]['password'] != cls.hash_password(password):
            st.session_state.login_attempts += 1
            return False, "Incorrect password"
        
        if st.session_state.login_attempts > 5:
            return False, "Too many failed attempts. Please refresh and try again."
        
        # Update user data
        user_data = users[email]
        users[email]['login_count'] = users[email].get('login_count', 0) + 1
        users[email]['last_login'] = datetime.now().isoformat()
        cls.save_users(users)
        
        # Set session data
        st.session_state.logged_in = True
        st.session_state.user_data = user_data
        st.session_state.user_data['email'] = email
        st.session_state.usage_count = user_data.get('usage_count', 0)
        st.session_state.saved_posts = user_data.get('saved_posts', [])
        st.session_state.brand_voice_examples = user_data.get('brand_voice_examples', [])
        st.session_state.user_preferences = user_data.get('preferences', {})
        st.session_state.login_attempts = 0
        
        return True, "Login successful"
    
    @classmethod
    def update_user_data(cls):
        """Update user data in database"""
        if st.session_state.logged_in and st.session_state.user_data:
            users = cls.load_users()
            email = st.session_state.user_data['email']
            
            if email in users:
                users[email].update({
                    'usage_count': st.session_state.usage_count,
                    'saved_posts': st.session_state.saved_posts,
                    'brand_voice_examples': st.session_state.brand_voice_examples,
                    'preferences': st.session_state.user_preferences,
                    'last_activity': datetime.now().isoformat()
                })
                cls.save_users(users)


class TrendingTopics:
    """Manage trending topics for different industries"""
    
    @staticmethod
    def get_trending_topics() -> Dict[str, List[str]]:
        """Get current trending topics"""
        # Rotate topics based on day of year for variety
        day_of_year = datetime.now().timetuple().tm_yday
        
        topics = {
            "general": [
                "AI automation in workplace",
                "Remote work productivity",
                "Sustainable business practices",
                "Mental health at work",
                "Skills-based hiring",
                "Digital transformation",
                "Employee retention",
                "Authentic leadership",
                "Work-life balance",
                "Diversity and inclusion",
                "Career development",
                "Professional networking",
                "Continuous learning",
                "Emotional intelligence",
                "Future of work"
            ],
            "Technology": [
                "AI ethics and deployment",
                "Quantum computing",
                "Cybersecurity trends",
                "Low-code platforms",
                "Cloud optimization",
                "DevOps practices",
                "API architecture",
                "Machine learning",
                "Data privacy",
                "Tech leadership"
            ],
            "Healthcare": [
                "Telehealth expansion",
                "AI diagnostics",
                "Patient experience",
                "Healthcare innovation",
                "Digital therapeutics",
                "Health equity",
                "Medical technology",
                "Care coordination",
                "Health data",
                "Preventive care"
            ],
            "Finance": [
                "ESG investing",
                "Fintech innovation",
                "Digital payments",
                "Financial inclusion",
                "Blockchain technology",
                "RegTech solutions",
                "Investment strategies",
                "Risk management",
                "Banking transformation",
                "Wealth management"
            ],
            "Marketing": [
                "Content marketing",
                "Social media strategy",
                "Brand authenticity",
                "Customer experience",
                "Marketing automation",
                "Influencer marketing",
                "Data-driven marketing",
                "Personalization",
                "Video marketing",
                "Community building"
            ]
        }
        
        # Rotate selection based on day
        rotated_topics = {}
        for category, topic_list in topics.items():
            start_idx = (day_of_year * 2) % len(topic_list)
            rotated_topics[category] = topic_list[start_idx:start_idx+8] + topic_list[:max(0, 8-(len(topic_list)-start_idx))]
        
        return rotated_topics


class PostGenerator:
    """Generate LinkedIn posts using various templates"""
    
    TEMPLATES = {
        "Story": {
            "description": "Personal experience or anecdote",
            "structure": "Hook → Story → Lesson → Call-to-Action",
            "best_for": "Building personal connection and relatability"
        },
        "Insight": {
            "description": "Industry knowledge or observation",
            "structure": "Observation → Analysis → Implication → Discussion",
            "best_for": "Establishing thought leadership"
        },
        "Tips": {
            "description": "Actionable advice or how-to",
            "structure": "Problem → Solution → Steps → Outcome",
            "best_for": "Providing practical value"
        },
        "Question": {
            "description": "Engaging discussion starter",
            "structure": "Context → Question → Your Take → Open Discussion",
            "best_for": "Community engagement and comments"
        },
        "Data": {
            "description": "Statistics or research findings",
            "structure": "Statistic → Context → Analysis → Takeaway",
            "best_for": "Building credibility with facts"
        },
        "Opinion": {
            "description": "Thought-provoking viewpoint",
            "structure": "Statement → Evidence → Nuance → Discussion",
            "best_for": "Generating engagement and debate"
        },
        "Achievement": {
            "description": "Celebrating success or milestone",
            "structure": "Achievement → Journey → Lessons → Inspiration",
            "best_for": "Personal branding and inspiration"
        },
        "List": {
            "description": "Curated tips or insights",
            "structure": "Setup → Numbered Points → Summary → Engagement",
            "best_for": "Easy consumption and sharing"
        }
    }
    
    EMOJI_SETS = {
        "Professional": ["📊", "💼", "🎯", "📈", "⭐", "💡", "🔍"],
        "Conversational": ["💬", "🤔", "👥", "💭", "🚀", "✨", "🌟"],
        "Inspirational": ["✨", "🌟", "💪", "🔥", "🎉", "🌈", "⚡"],
        "Educational": ["📚", "🧠", "💭", "🔍", "📖", "🎓", "💡"],
        "Humorous": ["😄", "🤣", "😅", "🎭", "😊", "🙃", "😉"],
        "Thought-provoking": ["🤯", "💭", "🧐", "⚡", "🔮", "🎯", "💫"]
    }
    
    @classmethod
    def generate_posts(cls, topic: str, industry: str, tone: str, template: str, 
                      word_count: str, include_emojis: bool, use_trending: bool) -> List[str]:
        """Generate multiple posts based on parameters"""
        posts = []
        trending_topics = TrendingTopics.get_trending_topics() if use_trending else {}
        selected_trend = None
        
        if use_trending and industry in trending_topics:
            selected_trend = random.choice(trending_topics[industry])
        
        # Generate 3 variations
        for i in range(3):
            post = cls._create_post(topic, industry, tone, template, word_count, 
                                  include_emojis, selected_trend, i)
            posts.append(post)
        
        return posts
    
    @classmethod
    def _create_post(cls, topic: str, industry: str, tone: str, template: str,
                    word_count: str, include_emojis: bool, trending_topic: Optional[str], 
                    variation: int) -> str:
        """Create a single post based on template"""
        emojis = cls.EMOJI_SETS.get(tone, cls.EMOJI_SETS["Professional"])
        emoji = random.choice(emojis) if include_emojis else ""
        
        if template == "Story":
            return cls._create_story_post(topic, industry, trending_topic, emoji, word_count)
        elif template == "Insight":
            return cls._create_insight_post(topic, industry, trending_topic, emoji, word_count)
        elif template == "Tips":
            return cls._create_tips_post(topic, industry, trending_topic, emoji, word_count)
        elif template == "Question":
            return cls._create_question_post(topic, industry, trending_topic, emoji, word_count)
        elif template == "Data":
            return cls._create_data_post(topic, industry, trending_topic, emoji, word_count)
        elif template == "Opinion":
            return cls._create_opinion_post(topic, industry, trending_topic, emoji, word_count)
        elif template == "Achievement":
            return cls._create_achievement_post(topic, industry, trending_topic, emoji, word_count)
        else:  # List
            return cls._create_list_post(topic, industry, trending_topic, emoji, word_count)
    
    @classmethod
    def _create_story_post(cls, topic: str, industry: str, trending_topic: Optional[str], 
                          emoji: str, word_count: str) -> str:
        """Create a story-style post"""
        hooks = [
            f"Last week changed how I think about {topic}",
            f"Here's what {topic} taught me about {industry}",
            f"A conversation about {topic} opened my eyes",
            f"My biggest misconception about {topic}? Let me tell you..."
        ]
        
        hook = random.choice(hooks)
        story = f"The situation forced me to reconsider everything I thought I knew."
        
        if trending_topic:
            connection = f"It connects to what we're seeing with {trending_topic.lower()}."
        else:
            connection = f"It's reshaping how we approach {industry.lower()}."
        
        lesson = f"The key insight: {topic} is about empowering people, not replacing them."
        cta = f"What's your experience with {topic}? {emoji}"
        
        hashtags = f"#{industry.replace(' ', '')} #{topic.replace(' ', '')} #Story #Leadership"
        
        post = f"{hook}\n\n{story} {connection}\n\n{lesson}\n\n{cta}\n\n{hashtags}"
        return cls._adjust_length(post, word_count)
    
    @classmethod
    def _create_insight_post(cls, topic: str, industry: str, trending_topic: Optional[str], 
                           emoji: str, word_count: str) -> str:
        """Create an insight-style post"""
        observations = [
            f"{emoji} {topic} is fundamentally changing {industry}",
            f"{emoji} The future of {topic} isn't what you think",
            f"{emoji} Here's what most people miss about {topic}"
        ]
        
        observation = random.choice(observations)
        
        if trending_topic:
            analysis = f"While everyone focuses on {trending_topic.lower()}, the real opportunity is in human-AI collaboration."
        else:
            analysis = f"The companies winning focus on augmentation, not automation."
        
        implication = f"This means {industry} professionals need to rethink their approach."
        discussion = f"What's your take on {topic}'s impact? {emoji}"
        
        hashtags = f"#{industry.replace(' ', '')} #{topic.replace(' ', '')} #Innovation #ThoughtLeadership"
        
        post = f"{observation}\n\n{analysis}\n\n{implication}\n\n{discussion}\n\n{hashtags}"
        return cls._adjust_length(post, word_count)
    
    @classmethod
    def _create_tips_post(cls, topic: str, industry: str, trending_topic: Optional[str], 
                         emoji: str, word_count: str) -> str:
        """Create a tips-style post"""
        problem = f"Struggling with {topic} implementation?"
        solution = f"Here's what's working:"
        
        tips = [
            f"{emoji} Start with pilot projects",
            f"{emoji} Focus on user experience first",
            f"{emoji} Measure outcomes, not just outputs",
            f"{emoji} Invest in training and change management"
        ]
        
        outcome = f"Result: Smoother adoption and better ROI."
        cta = f"What would you add to this list? {emoji}"
        
        hashtags = f"#{industry.replace(' ', '')} #{topic.replace(' ', '')} #Tips #BestPractices"
        
        post = f"{problem}\n\n{solution}\n\n" + "\n".join(tips[:3]) + f"\n\n{outcome}\n\n{cta}\n\n{hashtags}"
        return cls._adjust_length(post, word_count)
    
    @classmethod
    def _create_question_post(cls, topic: str, industry: str, trending_topic: Optional[str], 
                             emoji: str, word_count: str) -> str:
        """Create a question-style post"""
        contexts = [
            f"Quick question for {industry} professionals:",
            f"Honest question about {topic}:",
            f"Help me understand this better:"
        ]
        
        questions = [
            f"Is {topic} overhyped or underutilized?",
            f"What's the biggest {topic} misconception?",
            f"How do you measure {topic} success?"
        ]
        
        context = random.choice(contexts)
        question = random.choice(questions)
        take = f"My take: Success comes from focusing on people, not just technology."
        
        if trending_topic:
            connection = f"Especially with {trending_topic.lower()} evolving rapidly."
        else:
            connection = f"The landscape is changing fast."
        
        invite = f"What's your perspective? {emoji}"
        hashtags = f"#{industry.replace(' ', '')} #{topic.replace(' ', '')} #Discussion #Community"
        
        post = f"{context}\n\n{question}\n\n{take} {connection}\n\n{invite}\n\n{hashtags}"
        return cls._adjust_length(post, word_count)
    
    @classmethod
    def _create_data_post(cls, topic: str, industry: str, trending_topic: Optional[str], 
                         emoji: str, word_count: str) -> str:
        """Create a data-driven post"""
        stats = [
            "73% of companies report improved efficiency",
            "2.5x faster implementation than expected", 
            "45% reduction in operational costs",
            "89% of users exceed initial expectations"
        ]
        
        statistic = f"📊 New data on {topic}: {random.choice(stats)}"
        context = f"This aligns with industry-wide trends."
        
        if trending_topic:
            analysis = f"Particularly relevant given the focus on {trending_topic.lower()}."
        else:
            analysis = f"The key differentiator? Investment in training and change management."
        
        takeaway = f"Bottom line: {topic} ROI depends on implementation strategy."
        cta = f"What metrics are you tracking? {emoji}"
        
        hashtags = f"#{industry.replace(' ', '')} #{topic.replace(' ', '')} #Data #ROI"
        
        post = f"{statistic}\n\n{context} {analysis}\n\n{takeaway}\n\n{cta}\n\n{hashtags}"
        return cls._adjust_length(post, word_count)
    
    @classmethod
    def _create_opinion_post(cls, topic: str, industry: str, trending_topic: Optional[str], 
                           emoji: str, word_count: str) -> str:
        """Create an opinion/controversial post"""
        statements = [
            f"Unpopular opinion: Most {industry} companies are approaching {topic} wrong",
            f"Hot take: {topic} isn't the problem—leadership mindset is",
            f"Controversial view: {topic} hype is creating unrealistic expectations"
        ]
        
        statement = random.choice(statements)
        evidence = f"Here's why: Focus on technology over people strategy."
        
        if trending_topic:
            nuance = f"Don't get me wrong—{trending_topic.lower()} is important. But without proper change management, it's just expensive technology."
        else:
            nuance = f"I'm not anti-{topic}. But success requires more than just implementation."
        
        debate = f"Am I off base here? Change my mind! {emoji}"
        hashtags = f"#{industry.replace(' ', '')} #{topic.replace(' ', '')} #Opinion #ChangeMyMind"
        
        post = f"{statement}\n\n{evidence}\n\n{nuance}\n\n{debate}\n\n{hashtags}"
        return cls._adjust_length(post, word_count)
    
    @classmethod
    def _create_achievement_post(cls, topic: str, industry: str, trending_topic: Optional[str], 
                                emoji: str, word_count: str) -> str:
        """Create an achievement post"""
        achievements = [
            f"Milestone: Our {topic} initiative just hit 6 months! 🎉",
            f"Celebrating: Successfully implemented {topic} across our team",
            f"Proud moment: Led our first {topic} transformation"
        ]
        
        achievement = random.choice(achievements)
        journey = f"The journey wasn't easy—lots of learning and iteration."
        lessons = f"Key lessons: Start with why, involve everyone, measure impact."
        
        if trending_topic:
            inspiration = f"To anyone working on {trending_topic.lower()}: persistence pays off."
        else:
            inspiration = f"To anyone implementing {topic}: trust the process."
        
        thanks = f"Huge thanks to my team! {emoji}"
        hashtags = f"#{industry.replace(' ', '')} #{topic.replace(' ', '')} #Achievement #Teamwork"
        
        post = f"{achievement}\n\n{journey}\n\n{lessons}\n\n{inspiration}\n\n{thanks}\n\n{hashtags}"
        return cls._adjust_length(post, word_count)
    
    @classmethod
    def _create_list_post(cls, topic: str, industry: str, trending_topic: Optional[str], 
                         emoji: str, word_count: str) -> str:
        """Create a list-style post"""
        setup = f"5 things I wish I knew about {topic}:"
        
        points = [
            f"1{emoji} Implementation is 20% tech, 80% people",
            f"2{emoji} Start with pilots, not company-wide rollouts", 
            f"3{emoji} Measure outcomes, not just outputs",
            f"4{emoji} Training is investment, not cost",
            f"5{emoji} Feedback loops are everything"
        ]
        
        if trending_topic:
            summary = f"With {trending_topic.lower()} accelerating, these fundamentals matter more than ever."
        else:
            summary = f"Companies that nail these see 3x better adoption rates."
        
        engagement = f"What would you add? {emoji}"
        hashtags = f"#{industry.replace(' ', '')} #{topic.replace(' ', '')} #Tips #Lessons"
        
        post = f"{setup}\n\n" + "\n".join(points) + f"\n\n{summary}\n\n{engagement}\n\n{hashtags}"
        return cls._adjust_length(post, word_count)
    
    @classmethod
    def _adjust_length(cls, post: str, target_length: str) -> str:
        """Adjust post length to meet word count requirements"""
        words = post.split()
        current_count = len(words)
        
        if target_length == "Short (50-100 words)":
            target_min, target_max = 50, 100
        elif target_length == "Medium (100-200 words)":
            target_min, target_max = 100, 200
        else:  # Long
            target_min, target_max = 200, 300
        
        if target_min <= current_count <= target_max:
            return post
        
        # If too long, trim content
        if current_count > target_max:
            lines = post.split('\n')
            hashtag_lines = [line for line in lines if '#' in line]
            content_lines = [line for line in lines if '#' not in line and line.strip()]
            
            content_text = '\n'.join(content_lines)
            content_words = content_text.split()
            
            if len(content_words) > target_max - 10:
                truncated_content = ' '.join(content_words[:target_max-10])
                return truncated_content + '\n\n' + ('\n'.join(hashtag_lines) if hashtag_lines else '')
        
        # If too short, add expansion
        if current_count < target_min:
            expansions = [
                "This shift is happening across industries.",
                "The timing couldn't be better for professionals.",
                "Early adopters are seeing competitive advantages.",
                "Success requires strategic thinking and execution.",
                "The impact extends beyond just operational efficiency."
            ]
            
            lines = post.split('\n')
            hashtag_idx = next((i for i, line in enumerate(lines) if '#' in line), len(lines))
            
            addition = random.choice(expansions)
            lines.insert(hashtag_idx, addition)
            
            return '\n'.join(lines)
        
        return post


def show_post_preview(post: str, user_name: str = "Your Name"):
    """Display LinkedIn-style post preview"""
    word_count = len(post.split())
    
    # Escape HTML in post content and user_name to prevent injection
    escaped_post = post.replace('<', '&lt;').replace('>', '&gt;')
    escaped_user_name = user_name.replace('<', '&lt;').replace('>', '&gt;')
    
    st.markdown(f"""
    <div class="post-preview">
        <div class="preview-header">
            <div class="preview-avatar">{escaped_user_name[0] if escaped_user_name else "U"}</div>
            <div>
                <div style="font-weight: bold; color: #1d2129;">{escaped_user_name}</div>
                <div style="color: #65676b; font-size: 0.9rem;">Professional • Just now</div>
            </div>
        </div>
        <div style="color: #1d2129; white-space: pre-line; line-height: 1.5; margin: 1rem 0;">{escaped_post}</div>
        <div class="engagement-actions">
            <span>👍 Like</span>
            <span>💬 Comment</span>
            <span>🔄 Repost</span>
            <span>📤 Send</span>
        </div>
        <div class="word-count">{word_count} words</div>
    </div>
    """, unsafe_allow_html=True)


def generate_qr_code(url: str) -> Optional[str]:
    """Generate QR code for URL"""
    try:
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_M,
            box_size=10,
            border=4,
        )
        qr.add_data(url)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        buf = io.BytesIO()
        img.save(buf, format='PNG')
        buf.seek(0)
        
        return base64.b64encode(buf.getvalue()).decode()
    except Exception as e:
        st.error(f"QR Code generation failed: {e}")
        return None


class LinkedInPostApp:
    """Main application class"""
    
    def __init__(self):
        SessionManager.init_session_state()
        render_css()
    
    def run(self):
        """Main application entry point"""
        st.markdown('<div class="main-header">🚀 LinkedIn Post Generator Pro</div>', unsafe_allow_html=True)
        st.markdown('<div style="text-align: center; color: #666; margin-bottom: 2rem; font-size: 1.1rem;">Create engaging, professional LinkedIn content that drives real engagement</div>', unsafe_allow_html=True)
        
        if not st.session_state.logged_in:
            self._show_auth_page()
        else:
            self._show_main_app()
    
    def _show_auth_page(self):
        """Show authentication page"""
        # Introduction section
        st.markdown("""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    color: white; padding: 2rem; border-radius: 16px; text-align: center; margin: 2rem 0;">
            <h2 style="color: white; margin-bottom: 1rem;">Built for Professionals Who Value Quality Content</h2>
            <p style="color: white; font-size: 1.1rem; margin-bottom: 1.5rem;">
                Stop posting generic LinkedIn content. This tool creates engaging posts that actually get noticed.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Features showcase
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div class="feature-card">
                <h3>🎯 Smart Templates</h3>
                <p>8 proven post structures designed for maximum engagement</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="feature-card">
                <h3>📈 Trending Topics</h3>
                <p>AI-powered integration of current industry trends</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="feature-card">
                <h3>👀 Live Preview</h3>
                <p>See exactly how your post looks before publishing</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Authentication tabs
        tab1, tab2 = st.tabs(["🔑 Login", "🚀 Create Account"])
        
        with tab1:
            self._show_login_form()
        
        with tab2:
            self._show_signup_form()
    
    def _show_login_form(self):
        """Show login form"""
        st.markdown("### Welcome Back!")
        
        with st.form("login_form"):
            email = st.text_input("Email", placeholder="your.email@company.com")
            password = st.text_input("Password", type="password")
            submit = st.form_submit_button("🔑 Login", type="primary", use_container_width=True)
            
            if submit:
                if email and password:
                    success, message = UserManager.login_user(email, password)
                    if success:
                        st.success(message)
                        st.rerun()
                    else:
                        st.error(message)
                else:
                    st.error("Please fill in all fields")
    
    def _show_signup_form(self):
        """Show signup form"""
        st.markdown("### Join the Community")
        st.markdown("**Create your free account - no credit card required**")
        
        with st.form("signup_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                name = st.text_input("Full Name*", placeholder="John Doe")
                email = st.text_input("Email*", placeholder="your.email@company.com")
            
            with col2:
                company = st.text_input("Company", placeholder="Your Company (optional)")
                password = st.text_input("Password*", type="password", help="Minimum 6 characters")
            
            confirm_password = st.text_input("Confirm Password*", type="password")
            agree_terms = st.checkbox("I agree to the Terms of Service and Privacy Policy")
            
            submit = st.form_submit_button("🚀 Create Free Account", type="primary", use_container_width=True)
            
            if submit:
                if not all([name, email, password, confirm_password]):
                    st.error("Please fill in all required fields")
                elif len(password) < 6:
                    st.error("Password must be at least 6 characters")
                elif password != confirm_password:
                    st.error("Passwords don't match")
                elif not agree_terms:
                    st.error("Please agree to the Terms of Service")
                else:
                    success, message = UserManager.create_account(email, password, name, company)
                    if success:
                        st.success(f"{message}! Please login to continue.")
                        st.balloons()
                    else:
                        st.error(message)
    
    def _show_main_app(self):
        """Show main application for logged-in users"""
        # Sidebar
        with st.sidebar:
            user = st.session_state.user_data
            st.markdown(f"### 👋 Welcome, {user.get('name', 'User')}!")
            st.write(f"📧 {user.get('email', '')}")
            if user.get('company'):
                st.write(f"🏢 {user.get('company')}")
            
            if st.button("🚪 Logout", use_container_width=True):
                self._logout()
            
            st.markdown("---")
            
            # Stats
            st.markdown("### 📊 Your Stats")
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Posts Generated", st.session_state.usage_count)
            with col2:
                st.metric("Posts Saved", len(st.session_state.saved_posts))
            
            st.markdown("---")
            
            # Trending topics
            st.markdown("### 🔥 Trending Now")
            trending = TrendingTopics.get_trending_topics()
            for topic in trending["general"][:3]:
                st.markdown(f'<span class="trending-badge">{topic}</span>', unsafe_allow_html=True)
            
            st.markdown("---")
            
            # Navigation
            page = st.selectbox(
                "Navigate",
                ["🎯 Generate Posts", "💾 Saved Posts", "⚙️ Settings", "📱 Mobile QR"],
                key="nav_select"
            )
            
            page_map = {
                "🎯 Generate Posts": "generate",
                "💾 Saved Posts": "saved", 
                "⚙️ Settings": "settings",
                "📱 Mobile QR": "qr"
            }
            st.session_state.current_page = page_map.get(page, "generate")
        
        # Main content
        if st.session_state.current_page == "generate":
            self._show_post_generator()
        elif st.session_state.current_page == "saved":
            self._show_saved_posts()
        elif st.session_state.current_page == "settings":
            self._show_settings()
        elif st.session_state.current_page == "qr":
            self._show_qr_code()
    
    def _show_post_generator(self):
        """Show the main post generation interface"""
        st.markdown("## 🎯 Generate Your LinkedIn Posts")
        
        # Input form
        with st.container():
            topic = st.text_input(
                "💡 What topic do you want to write about?",
                placeholder="e.g., AI in healthcare, Remote work tips, Leadership strategies...",
                help="Be specific for better results"
            )
            
            if not topic:
                st.info("👆 Enter a topic above to get started!")
                return
        
        # Configuration
        with st.expander("⚙️ Post Configuration", expanded=True):
            col1, col2 = st.columns(2)
            
            with col1:
                template = st.selectbox(
                    "Post Template:",
                    list(PostGenerator.TEMPLATES.keys()),
                    help="Choose the structure that fits your content"
                )
                
                industry = st.selectbox(
                    "Industry:",
                    ["Technology", "Healthcare", "Finance", "Marketing", "Sales", 
                     "HR", "Education", "Consulting", "Manufacturing", "Other"],
                    index=["Technology", "Healthcare", "Finance", "Marketing", "Sales", 
                           "HR", "Education", "Consulting", "Manufacturing", "Other"].index(
                               st.session_state.user_preferences.get('default_industry', 'Technology'))
                )
            
            with col2:
                tone = st.selectbox(
                    "Tone:",
                    ["Professional", "Conversational", "Inspirational", "Educational", 
                     "Humorous", "Thought-provoking"],
                    index=["Professional", "Conversational", "Inspirational", "Educational", 
                           "Humorous", "Thought-provoking"].index(
                               st.session_state.user_preferences.get('default_tone', 'Professional'))
                )
                
                word_count = st.selectbox(
                    "Post Length:",
                    ["Short (50-100 words)", "Medium (100-200 words)", "Long (200-300 words)"],
                    index=["Short (50-100 words)", "Medium (100-200 words)", "Long (200-300 words)"].index(
                        st.session_state.user_preferences.get('default_length', 'Medium (100-200 words)'))
                )
            
            col3, col4 = st.columns(2)
            with col3:
                include_emojis = st.checkbox("Include Emojis", value=True)
            with col4:
                use_trending = st.checkbox("Include Trending Topics", value=True)
        
        # Template info
        template_info = PostGenerator.TEMPLATES[template]
        st.info(f"**{template} Template:** {template_info['description']}\n\n"
               f"**Structure:** {template_info['structure']}\n\n"
               f"**Best for:** {template_info['best_for']}")
        
        # Generate button
        if st.button("🚀 Generate Posts", type="primary", use_container_width=True):
            with st.spinner("🤖 Creating your LinkedIn posts..."):
                posts = PostGenerator.generate_posts(
                    topic, industry, tone, template, word_count, include_emojis, use_trending
                )
                
                st.session_state.usage_count += 1
                UserManager.update_user_data()
            
            if posts:
                st.success("✅ Posts generated successfully!")
                
                # Display posts
                for i, post in enumerate(posts, 1):
                    st.markdown(f"### 📝 Post Variation {i}")
                    
                    # Preview
                    show_post_preview(post, st.session_state.user_data.get('name', 'Your Name'))
                    
                    # Engagement prediction
                    engagement_score = self._predict_engagement(post, template, tone)
                    color = "🟢" if engagement_score > 70 else "🟡" if engagement_score > 50 else "🔴"
                    st.markdown(f"**Predicted Engagement:** {color} {engagement_score}/100")
                    
                    # Action buttons
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        if st.button(f"📋 Copy Post {i}", key=f"copy_{i}", use_container_width=True):
                            st.success("✅ Post ready to copy from text area below!")
                    
                    with col2:
                        if st.button(f"💾 Save Post {i}", key=f"save_{i}", use_container_width=True):
                            saved_post = {
                                'content': post,
                                'saved_at': datetime.now().isoformat(),
                                'topic': topic,
                                'template': template,
                                'word_count': len(post.split()),
                                'preview': post[:100] + "..." if len(post) > 100 else post
                            }
                            st.session_state.saved_posts.append(saved_post)
                            UserManager.update_user_data()
                            st.success("💾 Post saved!")
                    
                    with col3:
                        linkedin_url = f"https://www.linkedin.com/sharing/share-offsite/?url=https://linkedin-post-generator.com"
                        st.markdown(f"[🔗 Share on LinkedIn]({linkedin_url})")
                    
                    # Text area for manual copying
                    st.text_area(
                        f"📝 Post {i} (click to select all):",
                        value=post,
                        height=150,
                        key=f"post_text_{i}",
                        help="Click here, then Ctrl+A (Cmd+A) to select all, Ctrl+C (Cmd+C) to copy"
                    )
                    
                    st.markdown("---")
                
                # Download all posts
                all_posts_text = "\n\n" + "="*50 + "\n\n".join([f"POST {i}:\n{post}" for i, post in enumerate(posts, 1)])
                st.download_button(
                    label="📥 Download All Posts as Text File",
                    data=all_posts_text,
                    file_name=f"linkedin_posts_{topic.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.txt",
                    mime="text/plain",
                    use_container_width=True
                )
    
    def _show_saved_posts(self):
        """Show saved posts management"""
        st.markdown("### 💾 Your Saved Posts")
        
        if not st.session_state.saved_posts:
            st.info("📝 No saved posts yet. Generate and save posts to build your content library!")
            return
        
        st.markdown(f"**Total saved:** {len(st.session_state.saved_posts)} posts")
        
        # Search functionality
        search_term = st.text_input("🔍 Search saved posts", placeholder="Search by content or topic...")
        
        # Filter posts
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
        
        # Display posts
        for i, saved_post in enumerate(reversed(filtered_posts)):
            with st.expander(
                f"📝 {saved_post.get('topic', 'Post')} - {saved_post.get('saved_at', 'Unknown date')[:10]}", 
                expanded=False
            ):
                # Metadata
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Words", saved_post.get('word_count', 'N/A'))
                with col2:
                    st.metric("Template", saved_post.get('template', 'Unknown'))
                with col3:
                    st.write(f"**Saved:** {saved_post.get('saved_at', 'Unknown')[:16]}")
                
                # Preview
                st.markdown("**Preview:**")
                st.markdown(f"*{saved_post.get('preview', saved_post.get('content', '')[:100] + '...')}*")
                
                # Full content
                st.text_area(
                    "Full Content:",
                    value=saved_post.get('content', ''),
                    height=150,
                    key=f"saved_content_{i}",
                    help="Click to select all and copy"
                )
                
                # Actions
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    if st.button(f"📋 Copy", key=f"copy_saved_{i}", use_container_width=True):
                        st.success("✅ Ready to copy from text area above!")
                
                with col2:
                    linkedin_url = f"https://www.linkedin.com/sharing/share-offsite/?url=https://linkedin-post-generator.com"
                    st.markdown(f"[🔗 Share]({linkedin_url})")
                
                with col3:
                    if st.button(f"🗑️ Delete", key=f"delete_saved_{i}", use_container_width=True):
                        st.session_state.saved_posts.remove(saved_post)
                        UserManager.update_user_data()
                        st.success("🗑️ Post deleted!")
                        st.rerun()
    
    def _show_settings(self):
        """Show user settings and preferences"""
        st.markdown("## ⚙️ Settings & Preferences")
        
        # Default preferences
        with st.expander("🎯 Default Preferences", expanded=True):
            col1, col2 = st.columns(2)
            
            with col1:
                default_industry = st.selectbox(
                    "Default Industry:",
                    ["Technology", "Healthcare", "Finance", "Marketing", "Sales", 
                     "HR", "Education", "Consulting", "Manufacturing", "Other"],
                    index=["Technology", "Healthcare", "Finance", "Marketing", "Sales", 
                           "HR", "Education", "Consulting", "Manufacturing", "Other"].index(
                               st.session_state.user_preferences.get('default_industry', 'Technology'))
                )
                
                default_tone = st.selectbox(
                    "Default Tone:",
                    ["Professional", "Conversational", "Inspirational", "Educational", 
                     "Humorous", "Thought-provoking"],
                    index=["Professional", "Conversational", "Inspirational", "Educational", 
                           "Humorous", "Thought-provoking"].index(
                               st.session_state.user_preferences.get('default_tone', 'Professional'))
                )
            
            with col2:
                default_length = st.selectbox(
                    "Default Post Length:",
                    ["Short (50-100 words)", "Medium (100-200 words)", "Long (200-300 words)"],
                    index=["Short (50-100 words)", "Medium (100-200 words)", "Long (200-300 words)"].index(
                        st.session_state.user_preferences.get('default_length', 'Medium (100-200 words)'))
                )
            
            if st.button("💾 Save Preferences", use_container_width=True):
                st.session_state.user_preferences.update({
                    'default_industry': default_industry,
                    'default_tone': default_tone,
                    'default_length': default_length
                })
                UserManager.update_user_data()
                st.success("✅ Preferences saved!")
        
        # Account statistics
        with st.expander("📊 Account Statistics", expanded=True):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Posts Generated", st.session_state.usage_count)
            with col2:
                st.metric("Posts Saved", len(st.session_state.saved_posts))
            with col3:
                st.metric("Brand Examples", len(st.session_state.brand_voice_examples))
            
            if st.session_state.user_data:
                st.markdown("---")
                st.markdown("**Account Details:**")
                user = st.session_state.user_data
                st.write(f"📅 **Member since:** {user.get('created_at', 'Unknown')[:10]}")
                st.write(f"🔑 **Last login:** {user.get('last_login', 'Unknown')[:10] if user.get('last_login') else 'First time'}")
                st.write(f"🏢 **Company:** {user.get('company', 'Not specified')}")
        
        # Export data
        with st.expander("💾 Export Your Data", expanded=False):
            st.markdown("Download all your saved posts and preferences as JSON:")
            
            if st.button("📥 Export Data", use_container_width=True):
                export_data = {
                    'user_info': {
                        'name': st.session_state.user_data.get('name'),
                        'email': st.session_state.user_data.get('email'),
                        'company': st.session_state.user_data.get('company')
                    },
                    'saved_posts': st.session_state.saved_posts,
                    'preferences': st.session_state.user_preferences,
                    'usage_stats': {
                        'posts_generated': st.session_state.usage_count,
                        'posts_saved': len(st.session_state.saved_posts)
                    },
                    'export_date': datetime.now().isoformat()
                }
                
                export_json = json.dumps(export_data, indent=2)
                st.download_button(
                    label="📥 Download JSON File",
                    data=export_json,
                    file_name=f"linkedin_generator_data_{datetime.now().strftime('%Y%m%d')}.json",
                    mime="application/json",
                    use_container_width=True
                )
                st.success("✅ Data export ready!")
    
    def _show_qr_code(self):
        """Show QR code for mobile access"""
        st.markdown("### 📱 Mobile Access")
        st.markdown("**Share this tool with mobile users:**")
        
        website_url = "https://linkedin-post-generator.streamlit.app"
        
        qr_base64 = generate_qr_code(website_url)
        if qr_base64:
            st.markdown(
                f'''
                <div style="text-align: center; padding: 20px;">
                    <img src="data:image/png;base64,{qr_base64}" 
                         style="max-width: 250px; width: 100%; height: auto; border: 2px solid #ccc; border-radius: 10px;">
                </div>
                ''',
                unsafe_allow_html=True
            )
            st.markdown("*Point your phone camera at this code or use a QR scanner app*")
        else:
            st.error("Could not generate QR code")
        
        st.markdown(f"**Direct link:** {website_url}")
        st.info("💡 Bookmark this page on your phone for easy access!")
    
    def _predict_engagement(self, post: str, template: str, tone: str) -> int:
        """Predict engagement score for a post"""
        score = 50  # Base score
        
        # Template scoring
        template_scores = {
            "Question": 15, "Opinion": 18, "Story": 12, "List": 10,
            "Data": 8, "Tips": 8, "Achievement": 6, "Insight": 7
        }
        score += template_scores.get(template, 5)
        
        # Tone scoring
        tone_scores = {
            "Conversational": 10, "Humorous": 15, "Thought-provoking": 12,
            "Inspirational": 8, "Educational": 6, "Professional": 4
        }
        score += tone_scores.get(tone, 3)
        
        # Content analysis
        if "?" in post:
            score += 8  # Questions drive engagement
        if any(emoji in post for emoji in ["🤔", "💭", "🔥", "💡", "🚀"]):
            score += 5  # Engaging emojis
        if len(post.split()) < 150:
            score += 5  # Shorter posts often perform better
        
        # Hashtag analysis
        hashtag_count = post.count('#')
        if 3 <= hashtag_count <= 5:
            score += 5
        elif hashtag_count > 7:
            score -= 3
        
        return min(95, max(25, score))
    
    def _logout(self):
        """Handle user logout"""
        # Clear session state
        for key in list(st.session_state.keys()):
            if key not in ['current_page']:
                del st.session_state[key]
        
        SessionManager.init_session_state()
        st.rerun()


# Main execution
if __name__ == "__main__":
    app = LinkedInPostApp()
    app.run()
