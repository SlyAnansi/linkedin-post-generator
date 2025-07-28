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
    """Enhanced function with multiple variations and randomization"""
    
    # Different opening hooks based on tone
    hooks = {
        "Professional": [
            f"📊 Industry insight: {topic} is reshaping {industry}",
            f"🎯 Strategic perspective on {topic} in {industry}",
            f"📈 Market analysis: The {topic} transformation in {industry}",
            f"🔍 Deep dive: How {topic} impacts {industry} professionals"
        ],
        "Conversational": [
            f"💬 Let's talk about {topic} in {industry}",
            f"🤔 Here's what I've been thinking about {topic}",
            f"☕ Coffee chat topic: {topic} and its impact on {industry}",
            f"💭 Real talk about {topic} in our industry"
        ],
        "Inspirational": [
            f"🚀 The future of {topic} in {industry} starts with YOU",
            f"✨ Transform your {industry} career with {topic}",
            f"🌟 Why {topic} is your {industry} superpower",
            f"💫 Unlock your potential: {topic} in {industry}"
        ],
        "Educational": [
            f"📚 {topic} 101 for {industry} professionals",
            f"🎓 What every {industry} pro should know about {topic}",
            f"📖 The complete guide to {topic} in {industry}",
            f"🧠 Master {topic}: A {industry} perspective"
        ],
        "Humorous": [
            f"😅 {topic} in {industry}: It's complicated",
            f"🎭 Plot twist: {topic} actually makes sense in {industry}",
            f"😂 Me trying to explain {topic} to {industry} folks",
            f"🤪 {topic} in {industry}: Expectations vs Reality"
        ],
        "Thought-provoking": [
            f"🤯 Unpopular opinion: {topic} will change {industry} forever",
            f"🧩 The {topic} puzzle in {industry} nobody talks about",
            f"⚡ Controversial take: {topic} isn't what you think in {industry}",
            f"🔥 Hot take: {topic} is the {industry} game-changer"
        ],
        "Personal/Storytelling": [
            f"📖 My {topic} journey in {industry}",
            f"💡 How {topic} changed my {industry} perspective",
            f"🛤️ The day {topic} transformed my {industry} career",
            f"🎯 Personal story: {topic} lessons from {industry}"
        ]
    }
    
    # Different content structures
    insight_types = [
        "3 key insights:",
        "Here's what I've learned:",
        "The data shows:",
        "My observations:",
        "Industry trends reveal:",
        "Recent research indicates:",
        "What surprised me most:"
    ]
    
    action_words = [
        ["accelerating", "advancing", "evolving"],
        ["transforming", "reshaping", "revolutionizing"], 
        ["emerging", "developing", "expanding"],
        ["optimizing", "enhancing", "improving"]
    ]
    
    # Different CTAs
    ctas = [
        f"What's your experience with {topic}? Share below! 👇",
        f"How is {topic} impacting your {industry} work?",
        f"What {topic} trends are you seeing in {industry}?",
        f"Thoughts on {topic} in our industry? Let's discuss! 💬",
        f"How are you leveraging {topic} in {industry}?",
        f"What's your {topic} success story? Drop it in comments!",
        f"Agree or disagree? Share your {topic} perspective! 🤔"
    ]
    
    # Different emoji sets
    emoji_sets = [
        ["🚀", "⭐", "💫", "✨"],
        ["🎯", "📊", "📈", "🔥"],
        ["💡", "🧠", "🔍", "💭"],
        ["⚡", "🌟", "🎉", "🏆"],
        ["🔧", "🛠️", "⚙️", "🔨"]
    ]
    
    # Generate varied posts
    posts = []
    used_structures = []
    selected_hook = random.choice(hooks.get(tone, hooks["Professional"]))
    selected_emojis = random.choice(emoji_sets)
    
    # Post 1: Hook + Insights format
    insights = random.choice(insight_types)
    actions = [random.choice(group) for group in action_words]
    cta = random.choice(ctas)
    
    post1 = f"""{selected_hook}

As someone working with {audience}, I've been diving deep into how {topic} is {actions[0]} across {industry}.

{insights}
{selected_emojis[0]} Market demand is {actions[1]}
{selected_emojis[1]} Skills requirements are {actions[2]}  
{selected_emojis[2]} Competitive advantages are {actions[3]}

{cta}

#{industry.replace(' ', '')} #{topic.replace(' ', '')} #Innovation #Growth #Leadership"""
    
    # Post 2: Story format
    story_starters = [
        f"Last week, I witnessed something remarkable in {industry}",
        f"Three months ago, I couldn't have predicted this {industry} shift",
        f"Yesterday's {industry} meeting changed my perspective on {topic}",
        f"I just had the most interesting conversation about {topic} with {audience}"
    ]
    
    story_impacts = [
        "productivity increased by 40%",
        "collaboration improved dramatically",
        "results exceeded all expectations",
        "ROI was better than anticipated",
        "team efficiency skyrocketed"
    ]
    
    post2 = f"""{random.choice(story_starters)}.

The impact of {topic} was undeniable:
- {random.choice(story_impacts)}
- Decision-making became more data-driven
- Innovation cycles shortened significantly

For {audience} in {industry}, this isn't just a trend—it's the new reality.

How is {topic} changing your daily workflow?

#{industry.replace(' ', '')} #{topic.replace(' ', '')} #Transformation #Success #RealResults"""
    
    # Post 3: Question/Poll format
    poll_questions = [
        f"Quick poll for {audience}: What's your biggest {topic} challenge in {industry}?",
        f"Honest question: Is {topic} overhyped or underutilized in {industry}?",
        f"Help me settle a debate: What's the #1 {topic} benefit for {industry}?",
        f"Survey time: How ready is {industry} for widespread {topic} adoption?"
    ]
    
    poll_options = [
        ["A) Implementation complexity", "B) Cost concerns", "C) Skill gaps", "D) Resistance to change"],
        ["A) Definitely overhyped", "B) Perfect balance", "C) Severely underutilized", "D) Too early to tell"],
        ["A) Cost savings", "B) Efficiency gains", "C) Better outcomes", "D) Competitive advantage"],
        ["A) Completely ready", "B) Making progress", "C) Just getting started", "D) Not ready at all"]
    ]
    
    post3 = f"""{random.choice(poll_questions)}

{chr(10).join(random.choice(poll_options))}

Working with {audience}, I see huge variation in {topic} readiness across {industry}.

Some organizations are crushing it, others are struggling to get started.

Drop your vote in comments + share what's working (or not working) for you! 📊

#{industry.replace(' ', '')} #{topic.replace(' ', '')} #Poll #Community #Insights"""
    
    # Post 4: Contrarian/Hot take format
    contrarian_takes = [
        f"Unpopular opinion: Most {industry} companies are doing {topic} wrong",
        f"Hot take: {topic} isn't the problem in {industry}—implementation is",
        f"Controversial statement: {topic} alone won't save struggling {industry} businesses",
        f"Bold prediction: {topic} will be standard in {industry} within 18 months"
    ]
    
    supporting_points = [
        ["They're focusing on tools instead of strategy", "Training is an afterthought", "ROI measurement is inconsistent"],
        ["Technology is solid, but change management fails", "Leadership buy-in is superficial", "Teams aren't properly prepared"],
        ["Cultural transformation must come first", "Process optimization needs attention", "People development is the real key"],
        ["Early adopters prove it works", "Economic pressure demands efficiency", "Competition will force adoption"]
    ]
    
    post4 = f"""{random.choice(contrarian_takes)}.

Here's why I believe this:

{chr(10).join([f"→ {point}" for point in random.choice(supporting_points)])}

For {audience}, the window of opportunity is narrowing.

Am I wrong? Prove me wrong in the comments! 🔥

#{industry.replace(' ', '')} #{topic.replace(' ', '')} #Controversial #RealTalk #ChangeYourMind"""
    
    # Post 5: Data/Research format
    data_hooks = [
        f"The latest {industry} research on {topic} is eye-opening",
        f"New data reveals surprising {topic} trends in {industry}",
        f"Just analyzed 6 months of {topic} data from {industry}",
        f"Industry report: {topic} adoption in {industry} accelerating"
    ]
    
    metrics = [
        ["73% increase in adoption", "2.3x improvement in efficiency", "41% reduction in costs"],
        ["89% of leaders see value", "156% ROI within 12 months", "64% faster project completion"],
        ["92% user satisfaction rate", "78% of teams want more training", "85% would recommend to others"],
        ["67% plan increased investment", "54% expanding implementation", "81% see competitive advantage"]
    ]
    
    post5 = f"""{random.choice(data_hooks)}.

Key findings for {audience}:

📊 {random.choice(metrics)[0]}
📈 {random.choice(metrics)[1]}  
🎯 {random.choice(metrics)[2]}

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
