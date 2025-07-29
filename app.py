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

def generate_linkedin_posts(topic, industry, tone, audience, post_type):
    """Generate LinkedIn posts using Hugging Face API with fallback"""
    
    prompt = f"""Create 5 engaging LinkedIn posts about "{topic}" for the {industry} industry.

Target audience: {audience}
Tone: {tone}
Post type: {post_type}

Requirements for each post:
- 150-300 words
- Include 3-5 relevant hashtags
- Include a call-to-action
- Use emojis appropriately
- Format clearly as POST 1:, POST 2:, etc.

POST 1:"""
    
    try:
        API_URL = "https://api-inference.huggingface.co/models/microsoft/DialoGPT-medium"
        headers = {"Authorization": f"Bearer {os.getenv('HUGGINGFACE_API_KEY')}"}
        
        payload = {
            "inputs": prompt,
            "parameters": {
                "max_new_tokens": 1500,
                "temperature": 0.7,
                "top_p": 0.9,
                "do_sample": True
            },
            "options": {
                "wait_for_model": True
            }
        }
        
        response = requests.post(API_URL, headers=headers, json=payload)
        
        if response.status_code == 200:
            result = response.json()
            if isinstance(result, list) and len(result) > 0:
                generated_text = result[0].get('generated_text', '')
                if generated_text.startswith(prompt):
                    generated_text = generated_text[len(prompt):]
                
                if len(generated_text) > 200:
                    return generated_text
                else:
                    return generate_template_posts(topic, industry, tone, audience, post_type)
            else:
                return generate_template_posts(topic, industry, tone, audience, post_type)
        else:
            return generate_template_posts(topic, industry, tone, audience, post_type)
            
    except Exception as e:
        return generate_template_posts(topic, industry, tone, audience, post_type)

def get_industry_specifics(industry, topic):
    """Get industry-specific jargon, pain points, and terminology"""
    
    industry_data = {
        "Technology": {
            "jargon": ["MVP", "sprint", "scalability", "API integration", "tech stack", "DevOps", "CI/CD"],
            "pain_points": ["technical debt", "scaling challenges", "security vulnerabilities", "legacy systems"],
            "metrics": ["uptime", "response time", "user adoption", "churn rate", "deployment frequency"],
            "roles": ["developers", "product managers", "engineering teams", "DevOps engineers"],
            "buzzwords": ["digital transformation", "cloud-native", "microservices", "containerization"]
        },
        "Healthcare": {
            "jargon": ["EHR systems", "HIPAA compliance", "patient outcomes", "care coordination", "clinical workflows"],
            "pain_points": ["regulatory compliance", "patient safety", "documentation burden", "interoperability"],
            "metrics": ["patient satisfaction scores", "readmission rates", "clinical quality measures", "care efficiency"],
            "roles": ["clinicians", "healthcare administrators", "care teams", "medical professionals"],
            "buzzwords": ["value-based care", "population health", "telehealth adoption", "clinical excellence"]
        },
        "Finance": {
            "jargon": ["portfolio optimization", "risk management", "compliance frameworks", "liquidity management"],
            "pain_points": ["regulatory changes", "market volatility", "operational risk", "compliance costs"],
            "metrics": ["alpha generation", "Sharpe ratio", "AUM growth", "client retention"],
            "roles": ["financial advisors", "portfolio managers", "risk analysts", "compliance officers"],
            "buzzwords": ["fintech disruption", "robo-advisory", "ESG investing", "regulatory technology"]
        },
        "Marketing": {
            "jargon": ["attribution modeling", "funnel optimization", "customer journey mapping", "conversion tracking"],
            "pain_points": ["ad spend efficiency", "attribution gaps", "customer acquisition costs", "brand measurement"],
            "metrics": ["ROAS", "LTV:CAC ratio", "engagement rates", "conversion optimization"],
            "roles": ["performance marketers", "growth teams", "brand managers", "marketing analysts"],
            "buzzwords": ["omnichannel strategy", "personalization at scale", "marketing automation", "customer experience"]
        },
        "Sales": {
            "jargon": ["pipeline velocity", "quota attainment", "deal progression", "sales enablement"],
            "pain_points": ["lead quality", "sales cycle length", "quota pressure", "territory coverage"],
            "metrics": ["win rates", "average deal size", "sales velocity", "pipeline coverage ratios"],
            "roles": ["sales development reps", "account executives", "sales managers", "revenue operations"],
            "buzzwords": ["revenue intelligence", "predictive analytics", "social selling", "sales acceleration"]
        }
    }
    
    return industry_data.get(industry, {
        "jargon": ["best practices", "operational efficiency", "strategic initiatives"],
        "pain_points": ["market challenges", "operational inefficiencies", "competitive pressure"],
        "metrics": ["performance indicators", "success metrics", "ROI measurements"],
        "roles": ["professionals", "managers", "team leaders"],
        "buzzwords": ["digital innovation", "operational excellence", "strategic transformation"]
    })

def generate_template_posts(topic, industry, tone, audience, post_type):
    """Generate varied posts using templates with randomization"""
    
    # Get industry-specific terminology
    industry_data = get_industry_specifics(industry, topic)
    industry_jargon = random.choice(industry_data["jargon"])
    industry_pain = random.choice(industry_data["pain_points"])
    industry_metric = random.choice(industry_data["metrics"])
    industry_role = random.choice(industry_data["roles"])
    industry_buzzword = random.choice(industry_data["buzzwords"])
    
    # Different hooks based on tone
    tone_hooks = {
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
    
    # Get hooks for the selected tone
    hooks = tone_hooks.get(tone, tone_hooks["Professional"])
    selected_hook = random.choice(hooks)
    
    # Random elements
    insights_list = ["3 key insights:", "Here's what I've learned:", "The data shows:", "My observations:", "Industry trends reveal:"]
    action_words_1 = ["accelerating", "advancing", "evolving", "developing"]
    action_words_2 = ["transforming", "reshaping", "revolutionizing", "modernizing"]
    action_words_3 = ["emerging", "expanding", "growing", "scaling"]
    
    cta_options = [
        f"What's your experience with {topic}? Share below! 👇",
        f"How is {topic} impacting your {industry} work?",
        f"What {topic} trends are you seeing in {industry}?",
        f"Thoughts on {topic} in our industry? Let's discuss! 💬",
        f"How are you leveraging {topic} in {industry}?",
        f"What's your {topic} success story? Drop it in comments!"
    ]
    
    emoji_sets = [
        ["🚀", "⭐", "💫", "✨"],
        ["🎯", "📊", "📈", "🔥"],
        ["💡", "🧠", "🔍", "💭"],
        ["⚡", "🌟", "🎉", "🏆"]
    ]
    
    # Select random elements
    insights = random.choice(insights_list)
    action1 = random.choice(action_words_1)
    action2 = random.choice(action_words_2)
    action3 = random.choice(action_words_3)
    cta = random.choice(cta_options)
    emojis = random.choice(emoji_sets)
    
    # Generate 5 different posts
    posts = []
    
    # Post 1: Insights format with industry jargon
    post1 = f"""{selected_hook}

As someone working with {industry_role}, I've been diving deep into how {topic} is {action1} across {industry}.

{insights}
{emojis[0]} {industry_buzzword} is {action2} market dynamics
{emojis[1]} {industry_jargon} requirements are {action3}
{emojis[2]} {industry_metric} optimization is accelerating
{emojis[3]} Competitive advantages around {industry_pain} are emerging

{cta}

#{industry.replace(' ', '')} #{topic.replace(' ', '')} #Innovation #Growth #Leadership"""
    
    # Post 2: Story format with industry specifics
    story_options = [
        f"Last week, I witnessed a breakthrough in {industry_jargon} implementation",
        f"Three months ago, our {industry_role} couldn't have predicted this {industry} shift",
        f"Yesterday's conversation about {industry_pain} and {topic} changed my perspective",
        f"I just had the most interesting discussion with {industry_role} about {industry_buzzword}"
    ]
    story_start = random.choice(story_options)
    
    impact_options = [
        f"{industry_metric} improved by 40%",
        f"{industry_jargon} collaboration improved dramatically",
        f"{industry_pain} resolution exceeded all expectations",
        f"ROI on {industry_buzzword} was better than anticipated"
    ]
    impact = random.choice(impact_options)
    
    post2 = f"""{story_start}.

The impact of {topic} on our {industry_buzzword} was undeniable:
• {impact}
• {industry_jargon} decision-making became more data-driven
• {industry_metric} cycles shortened significantly
• {industry_role} collaboration reached new levels

For {audience} in {industry}, this isn't just a trend—it's the new reality of {industry_pain} management.

How is {topic} changing your {industry_jargon} workflow?

#{industry.replace(' ', '')} #{topic.replace(' ', '')} #Transformation #Success #RealResults"""
    
    # Post 3: Poll format
    poll_questions = [
        f"Quick poll for {audience}: What's your biggest {topic} challenge in {industry}?",
        f"Honest question: Is {topic} overhyped or underutilized in {industry}?",
        f"Help me settle a debate: What's the #1 {topic} benefit for {industry}?",
        f"Survey time: How ready is {industry} for widespread {topic} adoption?"
    ]
    poll_q = random.choice(poll_questions)
    
    post3 = f"""{poll_q}

A) Implementation complexity
B) Cost and budget concerns
C) Skills and training gaps
D) Resistance to change

Working with {audience}, I see huge variation in {topic} readiness across {industry}.

Some organizations are absolutely crushing it, while others are still struggling to get started.

Drop your vote in comments + share what's working (or not working) for you! 📊

#{industry.replace(' ', '')} #{topic.replace(' ', '')} #Poll #Community #Insights"""
    
    # Post 4: Contrarian/Hot take format
    contrarian_options = [
        f"Unpopular opinion: Most {industry} companies are doing {topic} wrong",
        f"Hot take: {topic} isn't the problem in {industry}—implementation is",
        f"Controversial statement: {topic} alone won't save struggling {industry} businesses",
        f"Bold prediction: {topic} will be standard in {industry} within 18 months"
    ]
    contrarian = random.choice(contrarian_options)
    
    post4 = f"""{contrarian}.

Here's why I believe this:

→ Technology adoption varies widely across organizations
→ Implementation strategy often lacks proper planning
→ Change management is frequently an afterthought
→ Leadership buy-in tends to be superficial

For {audience}, the window of opportunity is narrowing fast.

Am I completely wrong here? Prove me wrong in the comments! 🔥

#{industry.replace(' ', '')} #{topic.replace(' ', '')} #Controversial #RealTalk #ChangeManagement"""
    
    # Post 5: Data/Research format
    data_hooks = [
        f"The latest {industry} research on {topic} is absolutely eye-opening",
        f"New data reveals some surprising {topic} trends in {industry}",
        f"Just analyzed 6 months of {topic} data from across {industry}",
        f"Industry report: {topic} adoption in {industry} is accelerating"
    ]
    data_hook = random.choice(data_hooks)
    
    metrics_sets = [
        ["73% increase in adoption rates", "2.3x improvement in efficiency", "41% reduction in operational costs"],
        ["89% of leaders now see clear value", "156% ROI within first 12 months", "64% faster project completion"],
        ["92% user satisfaction rating", "78% of teams want expanded training", "85% would recommend to others"]
    ]
    metrics = random.choice(metrics_sets)
    
    post5 = f"""{data_hook}.

Key findings for {audience}:

📊 {metrics[0]}
📈 {metrics[1]}
🎯 {metrics[2]}

If you're in {industry} and not tracking these metrics, you're essentially flying blind.

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
        
        return posts if posts else [content]

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
        
        # Upgrade section
        st.markdown("---")
        st.markdown("### 🚀 Love this tool?")
        st.markdown("**Upgrade to Pro:**")
        st.markdown("• 20+ industry templates")
        st.markdown("• Advanced customization")
        st.markdown("• Priority support")
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
        
        # Features showcase
        st.markdown("---")
        st.markdown("## 💡 What You Get")
        
        feature_col1, feature_col2 = st.columns(2)
        
        with feature_col1:
            st.markdown("**✅ Professional Quality Posts**")
            st.markdown("Each post is crafted for maximum engagement")
            st.markdown("**✅ Industry-Specific Content**") 
            st.markdown("Tailored for your exact industry and audience")
            st.markdown("**✅ Multiple Formats**")
            st.markdown("Stories, polls, insights, data-driven posts")
        
        with feature_col2:
            st.markdown("**✅ Smart Hashtag Integration**")
            st.markdown("Relevant hashtags automatically included")
            st.markdown("**✅ Engagement Optimized**")
            st.markdown("Clear CTAs and conversation starters")
            st.markdown("**✅ Ready to Post**")
            st.markdown("Copy-paste directly to LinkedIn")

    # Footer
    st.markdown("---")
    st.markdown("**Ready to dominate LinkedIn? Generate your posts above! 🚀**")
    st.markdown("*Built with ❤️ for LinkedIn professionals*")

if __name__ == "__main__":
    main()
