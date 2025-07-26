import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

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
    """Generate LinkedIn posts using OpenAI API"""
    
    prompt = f"""
    Create 5 engaging LinkedIn posts about "{topic}" for the {industry} industry.
    
    Requirements:
    - Target audience: {audience}
    - Tone: {tone}
    - Post type: {post_type}
    - Each post should be 150-300 words
    - Include relevant hashtags (3-5 per post)
    - Make them scroll-stopping and engaging
    - Include a clear call-to-action
    - Use line breaks for readability
    - Add emojis where appropriate
    
    Format each post clearly with "POST 1:", "POST 2:", etc.
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a LinkedIn content expert who creates viral, engaging posts that drive high engagement rates."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=2000,
            temperature=0.7
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        st.error(f"Error generating posts: {str(e)}")
        return None

def parse_posts(content):
    """Parse the generated content into individual posts"""
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
    
    return posts

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
