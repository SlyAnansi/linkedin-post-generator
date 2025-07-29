import streamlit as st
import requests
import json
import os
import random
from dotenv import load_dotenv

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
</style>
""", unsafe_allow_html=True)

def generate_simple_posts(topic, industry, tone, audience, post_type):
    """Simple function with variations that works reliably"""
    
    # Different hooks based on tone
    if tone == "Professional":
        hook = f"📊 Industry insight: {topic} is reshaping {industry}"
    elif tone == "Conversational":
        hook = f"💬 Let's talk about {topic} in {industry}"
    elif tone == "Inspirational":
        hook = f"🚀 The future of {topic} in {industry} starts with YOU"
    elif tone == "Educational":
        hook = f"📚 {topic} 101 for {industry} professionals"
    elif tone == "Humorous":
        hook = f"😅 {topic} in {industry}: It's complicated"
    elif tone == "Thought-provoking":
        hook = f"🤯 Unpopular opinion: {topic} will change {industry} forever"
    else:  # Personal/Storytelling
        hook = f"📖 My {topic} journey in {industry}"
    
    # Random elements
    import random
    
    insights_options = ["3 key insights:", "Here's what I've learned:", "The data shows:", "My observations:"]
    insights = random.choice(insights_options)
    
    action1 = random.choice(["accelerating", "advancing", "evolving"])
    action2 = random.choice(["transforming", "reshaping", "revolutionizing"])
    action3 = random.choice(["emerging", "developing", "expanding"])
    
    cta_options = [
        f"What's your experience with {topic}? Share below! 👇",
        f"How is {topic} impacting your {industry} work?",
        f"What {topic} trends are you seeing in {industry}?",
        f"Thoughts on {topic} in our industry? Let's discuss! 💬"
    ]
    cta = random.choice(cta_options)
    
    emoji_set = random.choice([
        ["🚀", "⭐", "💫"],
        ["🎯", "📊", "📈"],
        ["💡", "🧠", "🔍"],
        ["⚡", "🌟", "🎉"]
    ])
    
    # Generate 5 different post types
    posts = []
    
    # Post 1: Insights format
    post1 = f"""{hook}

As someone working with {audience}, I've been diving deep into how {topic} is {action1} across {industry}.

{insights}
{emoji_set[0]} Market demand is {action2}
{emoji_set[1]} Skills requirements are {action3}
{emoji_set[2]} Innovation cycles are accelerating

{cta}

#{industry.replace(' ', '')} #{topic.replace(' ', '')} #Innovation #Growth #Leadership"""
    
    # Post 2: Story format
    story_starts = [
        f"Last week, I witnessed something remarkable in {industry}",
        f"Three months ago, I couldn't have predicted this {industry} shift",
        f"Yesterday's conversation about {topic} changed my perspective"
    ]
    story_start = random.choice(story_starts)
    
    impact = random.choice([
        "productivity increased by 40%",
        "collaboration improved dramatically", 
        "results exceeded all expectations"
    ])
    
    post2 = f"""{story_start}.

The impact of {topic} was undeniable:
• {impact}
• Decision-making became more data-driven
• Innovation cycles shortened significantly

For {audience} in {industry}, this isn't just a trend—it's the new reality.

How is {topic} changing your daily workflow?

#{industry.replace(' ', '')} #{topic.replace(' ', '')} #Transformation #Success #RealResults"""
    
    # Post 3: Poll format
    poll_questions = [
        f"Quick poll for {audience}: What's your biggest {topic} challenge?",
        f"Honest question: Is {topic} overhyped or underutilized in {industry}?",
        f"Help me settle a debate: What's the #1 {topic} benefit?"
    ]
    poll_q = random.choice(poll_questions)
    
    post3 = f"""{poll_q}

A) Implementation complexity
B) Cost concerns
C) Skill gaps  
D) Resistance to change

Working with {audience}, I see huge variation in {topic} readiness across {industry}.

Some organizations are crushing it, others are struggling to get started.

Drop your vote in comments + share what's working for you! 📊

#{industry.replace(' ', '')} #{topic.replace(' ', '')} #Poll #Community #Insights"""
    
    # Post 4: Hot take format
    hot_takes = [
        f"Unpopular opinion: Most {industry} companies are doing {topic} wrong",
        f"Hot take: {topic} isn't the problem in {industry}—implementation is",
        f"Bold prediction: {topic} will be standard in {industry} within 18 months"
    ]
    hot_take = random.choice(hot_takes)
    
    post4 = f"""{hot_take}.

Here's why I believe this:

→ Technology adoption varies widely across organizations
→ Implementation strategy often lacks proper planning
→ Change management is frequently an afterthought

For {audience}, the window of opportunity is narrowing.

Am I wrong? Prove me wrong in the comments! 🔥

#{industry.replace(' ', '')} #{topic.replace(' ', '')} #Controversial #RealTalk #ChangeManagement"""
    
    # Post 5: Data format
    data_hooks = [
        f"The latest {industry} research on {topic} is eye-opening",
        f"New data reveals surprising {topic} trends in {industry}",
        f"Industry report: {topic} adoption in {industry} accelerating"
    ]
    data_hook = random.choice(data_hooks)
    
    metrics = [
        "73% increase in adoption",
        "2.3x improvement in efficiency", 
        "41% reduction in costs"
    ]
    
    post5 = f"""{data_hook}.

Key findings for {audience}:

📊 {metrics[0]}
📈 {metrics[1]}
🎯 {metrics[2]}

If you're in {industry} and not tracking these metrics, you're flying blind.

What data points matter most in your {topic} journey?

#{industry.replace(' ', '')} #{topic.replace(' ', '')} #Data #Research #Metrics #Results"""
    
    posts = [post1, post2, post3, post4, post5]
    
    return "\n\n" + "="*50 + "\n\n".join([f"POST {i+1}:\n{post}" for i, post in enumerate(posts)])

def parse_posts(content):
    """Parse the generated content into individual posts"""
    if "=" in content and "POST" in content:
        # Handle the template format
        sections = content.split("="*50)
        posts = []
        for section in sections[1:]:  # Skip first empty section
            if section.strip():
                posts.append(section.strip())
        return posts
    else:
        # Handle other formats
        posts = []
        lines = content.split('\n')
        current_post = ""
        
        for line in lines:
            if line.strip().startswith(('POST 1:', 'POST 2:', 'POST 3:', 'POST 4:', 'POST 5:')):
                if current_post:
                    posts.append(current_post.strip())
                current_post = line.replace('POST ', '').replace(':', '').strip() + '\n'
            else:
                current_post += line + '\n'
        
        if current_post:
            posts.append(current_post.strip())
        
        return posts if posts else [content]  # Return content as single post if parsing fails

# Main App Interface
def main():
    # Header
    st.markdown('<div class="main-header">🚀 LinkedIn Post Generator</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Create engaging LinkedIn content in seconds</div>', unsafe_allow_html=True)
    
    # Sidebar for inputs
    with st.sidebar:
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
    
    # Main content area
    if generate_button:
        if not topic:
            st.warning("Please enter a topic to generate posts about.")
            return
            
        if not os.getenv("HUGGINGFACE_API_KEY"):
            st.error("Hugging Face API key not found. Please check your configuration.")
            return
        
        # Show loading spinner
        with st.spinner("Generating your LinkedIn posts..."):
            content = generate_linkedin_posts(topic, industry, tone, audience, post_type)
        
        if content:
            st.success("✅ Posts generated successfully!")
            
            # Parse and display posts
            posts = parse_posts(content)
            
            if posts:
                st.markdown("## 📱 Your Generated Posts")
                
                for i, post in enumerate(posts, 1):
                    with st.expander(f"📝 Post {i}", expanded=True):
                        st.markdown(f'<div class="post-container">{post}</div>', unsafe_allow_html=True)
                        
                        if st.button(f"📋 Copy Post {i}", key=f"copy_{i}"):
                            st.success(f"Post {i} ready to copy!")
                
                # Download option
                st.markdown("---")
                all_posts = "\n\n" + "="*50 + "\n\n".join([f"POST {i+1}:\n{post}" for i, post in enumerate(posts)])
                st.download_button(
                    label="📥 Download All Posts",
                    data=all_posts,
                    file_name=f"linkedin_posts_{topic.replace(' ', '_')}.txt",
                    mime="text/plain"
                )
            else:
                st.error("Could not parse the generated posts. Please try again.")
    
    else:
        # Landing page content
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

if __name__ == "__main__":
    main()
