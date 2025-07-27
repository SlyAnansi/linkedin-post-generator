import streamlit as st
import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure OpenAI

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
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #0066cc;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def generate_linkedin_posts(topic, industry, tone, audience, post_type):
    """Generate LinkedIn posts using Hugging Face API"""
    
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
                # Clean up the response
                if generated_text.startswith(prompt):
                    generated_text = generated_text[len(prompt):]
                
                # If response is too short, try a simpler approach
                if len(generated_text) < 200:
                    return generate_simple_posts(topic, industry, tone, audience, post_type)
                
                return generated_text
            else:
                return generate_simple_posts(topic, industry, tone, audience, post_type)
        else:
            st.error(f"API Error: {response.status_code}")
            return generate_simple_posts(topic, industry, tone, audience, post_type)
            
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return generate_simple_posts(topic, industry, tone, audience, post_type)

def generate_simple_posts(topic, industry, tone, audience, post_type):
    """Fallback function with template-based posts"""
    
    posts = [
        f"""🚀 The future of {topic} in {industry} is here!

As someone targeting {audience}, I've been exploring how {topic} is transforming our industry. The results are fascinating.

Here's what I've learned:
✅ Innovation is accelerating faster than ever
✅ Early adopters are seeing significant advantages  
✅ The time to act is now

What's your experience with {topic}? Share your thoughts below! 👇

#{industry.replace(' ', '')} #{topic.replace(' ', '')} #Innovation #FutureOfWork #Leadership""",

        f"""💡 {post_type}: Why {topic} matters for {industry} professionals

Speaking to my fellow {audience}, this trend can't be ignored anymore.

3 key insights:
🔹 Market demand is shifting rapidly
🔹 Skills requirements are evolving
🔹 Competitive advantage comes from early adoption

The question isn't IF this will impact your career, but WHEN.

How are you preparing for these changes?

#{industry.replace(' ', '')} #{topic.replace(' ', '')} #CareerDevelopment #ProfessionalGrowth""",

        f"""🎯 Personal experience: How {topic} changed my perspective on {industry}

As someone who works with {audience} daily, I've seen firsthand how {topic} is reshaping our field.

The transformation has been remarkable:
• Increased efficiency across teams
• Better outcomes for stakeholders  
• New opportunities emerging daily

If you're in {industry}, this is your moment to lead the change.

What steps are you taking to stay ahead?

#{industry.replace(' ', '')} #{topic.replace(' ', '')} #Leadership #Change #Growth""",

        f"""🔥 Hot take: {topic} is the game-changer {industry} has been waiting for

Controversial opinion? Maybe. But here's why I believe this...

After working with {audience} for years, I've noticed a pattern:
→ Those who embrace change thrive
→ Those who resist get left behind
→ The middle ground is disappearing

{topic} isn't just a trend - it's the new standard.

Agree or disagree? Let's discuss! 💬

#{industry.replace(' ', '')} #{topic.replace(' ', '')} #Controversial #Innovation #FutureThinking""",

        f"""📊 Data doesn't lie: {topic} is transforming {industry} faster than expected

Latest research shows something interesting for {audience}...

The numbers are compelling:
📈 Adoption rates are accelerating
📈 ROI is exceeding expectations
📈 Competitive gaps are widening

If you're in {industry}, the data suggests it's time to act.

What metrics are you tracking in this space?

#{industry.replace(' ', '')} #{topic.replace(' ', '')} #Data #Analytics #Strategy #Growth"""
    ]
    
    return "\n\n" + "="*50 + "\n\n".join([f"POST {i+1}:\n{post}" for i, post in enumerate(posts)])

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
            
        if not os.getenv("OPENAI_API_KEY"):
            st.error("OpenAI API key not found. Please check your configuration.")
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
