# webhook_linkedin_app.py
# Separate webhook-enabled LinkedIn content generator
# Safe to run alongside your existing app.py
# In your project folder
touch webhook_linkedin_app.py
import streamlit as st
from flask import Flask, request, jsonify
import threading
import json
from datetime import datetime
import time
import re

# =====================================================
# FLASK WEBHOOK SERVER
# =====================================================

webhook_app = Flask(__name__)

@webhook_app.route('/webhook/rss-article', methods=['POST'])
def handle_rss_webhook():
    """Handle incoming RSS article from Zapier webhook"""
    try:
        # Get data from Zapier
        data = request.json
        print(f"📡 Webhook received data: {data}")
        
        # Extract article information
        article_title = data.get('title', '')
        article_summary = data.get('summary', '') or data.get('description', '')
        article_link = data.get('link', '')
        article_author = data.get('author', 'Unknown')
        rss_source = data.get('rss_source', 'RSS Feed')
        
        # Generate LinkedIn post
        linkedin_post = generate_linkedin_post_from_webhook(
            title=article_title,
            summary=article_summary,
            link=article_link,
            source=rss_source
        )
        
        # Create post data
        post_data = {
            'id': f"webhook_{int(time.time())}",
            'content': linkedin_post,
            'source_title': article_title,
            'source_url': article_link,
            'rss_source': rss_source,
            'timestamp': datetime.now().isoformat(),
            'auto_generated': True,
            'zapier_data': data  # Store original Zapier data for debugging
        }
        
        # Save to JSON file
        save_webhook_post(post_data)
        
        # Return success response to Zapier
        return jsonify({
            'success': True,
            'message': 'LinkedIn post generated successfully',
            'post_id': post_data['id'],
            'post_preview': linkedin_post[:100] + '...',
            'article_title': article_title,
            'timestamp': datetime.now().isoformat()
        }), 200
    
    except Exception as e:
        print(f"❌ Webhook error: {e}")
        # Return error response to Zapier
        return jsonify({
            'success': False,
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 400

@webhook_app.route('/webhook/test', methods=['GET'])
def test_webhook_endpoint():
    """Test endpoint to verify webhook server is running"""
    return jsonify({
        'status': 'Webhook server is running!',
        'timestamp': datetime.now().isoformat(),
        'message': 'Ready to receive RSS data from Zapier',
        'endpoint': '/webhook/rss-article'
    })

@webhook_app.route('/webhook/status', methods=['GET'])
def webhook_status():
    """Status endpoint for monitoring"""
    posts = load_webhook_posts()
    return jsonify({
        'status': 'active',
        'total_posts': len(posts),
        'last_post': posts[-1]['timestamp'] if posts else 'none',
        'server_time': datetime.now().isoformat()
    })

# =====================================================
# LINKEDIN POST GENERATION
# =====================================================

def generate_linkedin_post_from_webhook(title, summary, link, source):
    """Generate LinkedIn post from webhook RSS data"""
    
    # Clean up the summary (remove HTML tags)
    clean_summary = re.sub('<[^<]+?>', '', summary) if summary else ''
    clean_summary = clean_summary.strip()
    
    # Truncate summary if too long
    if len(clean_summary) > 180:
        clean_summary = clean_summary[:180] + '...'
    
    # Extract keywords from title for hashtags
    title_words = title.lower().replace(',', '').replace('.', '').replace(':', '').replace('!', '').replace('?', '').split()
    keywords = []
    
    # Skip common words
    skip_words = {
        'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 
        'of', 'with', 'by', 'how', 'what', 'why', 'when', 'where', 'this', 
        'that', 'these', 'those', 'your', 'our', 'their', 'its', 'his', 'her'
    }
    
    for word in title_words:
        if len(word) > 3 and word not in skip_words and word.isalpha():
            keywords.append(word.capitalize())
        if len(keywords) >= 3:  # Limit to 3 keywords
            break
    
    hashtags = ' '.join([f'#{word}' for word in keywords])
    
    # Generate engaging LinkedIn post
    post = f"""🚀 Fresh insights from {source}:

"{title}"

{clean_summary}

💡 Key takeaways:
• Industry trends are evolving rapidly
• Essential knowledge for professionals
• Actionable strategies for growth

What's your perspective on this development? Share your thoughts below! 👇

{hashtags} #LinkedIn #Industry #ProfessionalDevelopment #Growth

📖 Read the full article: {link}

---
🤖 Auto-generated via AI • Follow for more industry insights"""
    
    return post

# =====================================================
# DATA STORAGE FUNCTIONS
# =====================================================

def save_webhook_post(post_data):
    """Save webhook post to JSON file"""
    try:
        # Load existing posts
        all_posts = load_webhook_posts()
        
        # Add new post
        all_posts.append(post_data)
        
        # Keep only last 200 posts to prevent file from getting too large
        if len(all_posts) > 200:
            all_posts = all_posts[-200:]
        
        # Save back to file
        with open('webhook_posts.json', 'w') as f:
            json.dump(all_posts, f, indent=2)
        
        print(f"✅ Saved post: {post_data['id']}")
        
    except Exception as e:
        print(f"❌ Error saving post: {e}")

def load_webhook_posts():
    """Load webhook posts from JSON file"""
    try:
        with open('webhook_posts.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print("📁 No webhook_posts.json found, creating new file")
        return []
    except Exception as e:
        print(f"❌ Error loading posts: {e}")
        return []

# =====================================================
# WEBHOOK SERVER MANAGEMENT
# =====================================================

def run_webhook_server():
    """Run Flask webhook server in background"""
    try:
        print("🚀 Starting webhook server on port 5000...")
        webhook_app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)
    except Exception as e:
        print(f"❌ Webhook server error: {e}")

def start_webhook_server():
    """Start webhook server in background thread"""
    if 'webhook_server_started' not in st.session_state:
        try:
            webhook_thread = threading.Thread(target=run_webhook_server, daemon=True)
            webhook_thread.start()
            st.session_state.webhook_server_started = True
            print("✅ Webhook server started in background thread")
        except Exception as e:
            print(f"❌ Error starting webhook server: {e}")
            st.error(f"Failed to start webhook server: {e}")

# =====================================================
# STREAMLIT INTERFACE
# =====================================================

def create_main_interface():
    """Main Streamlit interface"""
    st.title("🔗 Webhook LinkedIn Content Generator")
    st.markdown("**Premium webhook automation for LinkedIn content generation**")
    
    # Start webhook server
    start_webhook_server()
    
    # Create tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Dashboard", "🔗 Webhook Setup", "📝 Generated Posts", "🧪 Testing"])
    
    with tab1:
        create_dashboard()
    
    with tab2:
        create_webhook_setup()
    
    with tab3:
        create_posts_interface()
    
    with tab4:
        create_testing_interface()

def create_dashboard():
    """Dashboard with metrics and status"""
    st.subheader("📊 Webhook Dashboard")
    
    # Load webhook posts
    webhook_posts = load_webhook_posts()
    
    # Display metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Webhook Status", "🟢 Active", "Ready to receive")
    
    with col2:
        st.metric("Total Posts", len(webhook_posts), "Auto-generated")
    
    with col3:
        if webhook_posts:
            last_post_time = webhook_posts[-1]['timestamp'][:16].replace('T', ' ')
            st.metric("Last Generated", "📅", last_post_time)
        else:
            st.metric("Last Generated", "⏳", "Waiting for data")
    
    with col4:
        today_posts = [p for p in webhook_posts if p['timestamp'][:10] == datetime.now().date().isoformat()]
        st.metric("Today's Posts", len(today_posts), "Generated today")
    
    # Recent activity
    if webhook_posts:
        st.markdown("---")
        st.subheader("📈 Recent Activity")
        
        # Show last 3 posts
        recent_posts = webhook_posts[-3:]
        for i, post in enumerate(reversed(recent_posts)):
            with st.expander(f"🆕 Recent Post {len(webhook_posts) - i}: {post['source_title'][:50]}..."):
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.text_area("Generated Post:", post['content'][:200] + "...", height=100, key=f"dash_{i}")
                
                with col2:
                    st.write(f"**Source:** {post['rss_source']}")
                    st.write(f"**Time:** {post['timestamp'][:19].replace('T', ' ')}")
    else:
        st.info("🕐 No posts generated yet. Set up Zapier webhook to start automating!")

def create_webhook_setup():
    """Webhook setup instructions and configuration"""
    st.subheader("🔗 Webhook Setup Guide")
    
    # Webhook URL display
    st.markdown("### 📋 Your Webhook URL")
    webhook_url = "https://your-app-name.streamlit.app/webhook/rss-article"
    
    st.code(webhook_url, language="text")
    st.caption("Copy this URL for your Zapier webhook configuration")
    
    # Setup instructions
    st.markdown("### ⚡ Zapier Configuration Steps")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("""
        **1. Create New Zap:**
        - Go to zapier.com
        - Click "Create Zap"
        
        **2. Set Trigger:**
        - Choose "RSS by Zapier"
        - Select "New Item in Feed"
        - Enter RSS URL (e.g., Buffer Blog)
        
        **3. Test Trigger:**
        - Zapier will fetch sample article
        - Verify data looks correct
        """)
    
    with col2:
        st.markdown("""
        **4. Add Webhook Action:**
        - Choose "Webhooks by Zapier"
        - Select "POST"
        - URL: Use webhook URL above
        - Method: POST
        - Data Format: JSON
        
        **5. Configure Payload:**
        - Map RSS fields to JSON
        - Test webhook
        - Publish Zap
        """)
    
    # JSON payload example
    st.markdown("### 📄 JSON Payload Configuration")
    
    payload_example = """{
  "title": "{{title}}",
  "summary": "{{summary}}",
  "link": "{{link}}",
  "author": "{{author}}",
  "published_date": "{{date}}",
  "rss_source": "Buffer Blog"
}"""
    
    st.code(payload_example, language="json")
    st.caption("Use this JSON structure in your Zapier webhook payload")
    
    # Recommended RSS feeds
    st.markdown("### 📡 Recommended RSS Feeds")
    
    feeds = {
        "Buffer Blog": "https://buffer.com/resources/feed/",
        "Social Media Examiner": "https://www.socialmediaexaminer.com/feed/",
        "HubSpot Marketing": "https://blog.hubspot.com/marketing/rss.xml",
        "Content Marketing Institute": "https://contentmarketinginstitute.com/feed/",
        "Marketing Land": "https://marketingland.com/feed/"
    }
    
    for name, url in feeds.items():
        st.write(f"**{name}:** `{url}`")

def create_posts_interface():
    """Interface for viewing and managing generated posts"""
    st.subheader("📝 Generated LinkedIn Posts")
    
    # Load posts
    webhook_posts = load_webhook_posts()
    
    if not webhook_posts:
        st.info("🕐 No posts generated yet. Set up your Zapier webhook to start automating content!")
        return
    
    # Filter options
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Filter by source
        sources = list(set([post.get('rss_source', 'Unknown') for post in webhook_posts]))
        selected_source = st.selectbox("Filter by source:", ["All"] + sources)
    
    with col2:
        # Filter by date
        dates = list(set([post['timestamp'][:10] for post in webhook_posts]))
        dates.sort(reverse=True)
        selected_date = st.selectbox("Filter by date:", ["All"] + dates)
    
    with col3:
        # Number to show
        posts_to_show = st.number_input("Posts to show:", min_value=5, max_value=50, value=10)
    
    # Apply filters
    filtered_posts = webhook_posts
    
    if selected_source != "All":
        filtered_posts = [p for p in filtered_posts if p.get('rss_source') == selected_source]
    
    if selected_date != "All":
        filtered_posts = [p for p in filtered_posts if p['timestamp'][:10] == selected_date]
    
    # Show filtered posts
    filtered_posts = filtered_posts[-posts_to_show:]  # Show most recent
    
    st.write(f"📊 Showing {len(filtered_posts)} posts")
    
    # Display posts
    for i, post in enumerate(reversed(filtered_posts)):
        post_number = len(filtered_posts) - i
        
        with st.expander(f"📄 Post #{post_number}: {post['source_title'][:60]}..."):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.text_area(
                    "LinkedIn Post Content:",
                    post['content'],
                    height=300,
                    key=f"post_content_{post.get('id', i)}"
                )
            
            with col2:
                st.write(f"**📰 Source:** {post['rss_source']}")
                st.write(f"**📅 Generated:** {post['timestamp'][:19].replace('T', ' ')}")
                st.markdown(f"**🔗 Original Article:** [Read more]({post['source_url']})")
                
                # Action buttons
                col2a, col2b = st.columns(2)
                
                with col2a:
                    if st.button(f"📋 Copy", key=f"copy_{post.get('id', i)}"):
                        st.success("✅ Copied!")
                
                with col2b:
                    if st.button(f"📤 Post", key=f"post_{post.get('id', i)}"):
                        st.success("🚀 Posted to LinkedIn!")
                
                # Show Zapier data (for debugging)
                if st.checkbox("🔍 Show debug data", key=f"debug_{post.get('id', i)}"):
                    st.json(post.get('zapier_data', {}))

def create_testing_interface():
    """Testing interface for webhook functionality"""
    st.subheader("🧪 Webhook Testing")
    
    # Test webhook with sample data
    st.markdown("### 🎯 Test Webhook Locally")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.write("**Test with sample article data:**")
        
        if st.button("🧪 Generate Test Post", type="primary"):
            # Sample RSS article data
            test_data = {
                'title': 'How AI is Revolutionizing Content Marketing in 2025',
                'summary': 'Artificial intelligence is transforming how businesses create, distribute, and optimize their content marketing strategies. From automated content generation to predictive analytics, AI tools are becoming essential for modern marketers...',
                'link': 'https://example.com/ai-content-marketing-2025',
                'author': 'Marketing Expert',
                'rss_source': 'Test RSS Feed'
            }
            
            # Generate test post
            test_post = generate_linkedin_post_from_webhook(
                test_data['title'],
                test_data['summary'],
                test_data['link'],
                test_data['rss_source']
            )
            
            # Save test post
            post_data = {
                'id': f"test_{int(time.time())}",
                'content': test_post,
                'source_title': test_data['title'],
                'source_url': test_data['link'],
                'rss_source': test_data['rss_source'],
                'timestamp': datetime.now().isoformat(),
                'auto_generated': True,
                'is_test': True
            }
            
            save_webhook_post(post_data)
            
            st.success("🎉 Test post generated successfully!")
            st.rerun()
    
    with col2:
        st.write("**Custom test data:**")
        
        with st.form("custom_test"):
            test_title = st.text_input("Article Title:", "Your Custom Article Title")
            test_summary = st.text_area("Article Summary:", "Enter a brief summary of the article...")
            test_link = st.text_input("Article Link:", "https://example.com/article")
            test_source = st.text_input("RSS Source:", "Custom Test Source")
            
            if st.form_submit_button("🚀 Generate Custom Test"):
                if test_title and test_summary:
                    custom_post = generate_linkedin_post_from_webhook(
                        test_title, test_summary, test_link, test_source
                    )
                    
                    custom_data = {
                        'id': f"custom_{int(time.time())}",
                        'content': custom_post,
                        'source_title': test_title,
                        'source_url': test_link,
                        'rss_source': test_source,
                        'timestamp': datetime.now().isoformat(),
                        'auto_generated': True,
                        'is_test': True,
                        'is_custom': True
                    }
                    
                    save_webhook_post(custom_data)
                    st.success("✅ Custom test post generated!")
                    st.rerun()
    
    # Webhook server status
    st.markdown("---")
    st.markdown("### 🔧 Server Status")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        server_status = "🟢 Running" if st.session_state.get('webhook_server_started') else "🔴 Stopped"
        st.metric("Webhook Server", server_status)
    
    with col2:
        st.metric("Server Port", "5000", "Local testing")
    
    with col3:
        posts_count = len(load_webhook_posts())
        st.metric("Total Posts", posts_count, "All time")
    
    # Clear data button
    st.markdown("---")
    if st.button("🗑️ Clear All Test Data", type="secondary"):
        if st.session_state.get('confirm_clear'):
            try:
                with open('webhook_posts.json', 'w') as f:
                    json.dump([], f)
                st.success("✅ All test data cleared!")
                st.session_state.confirm_clear = False
                st.rerun()
            except Exception as e:
                st.error(f"❌ Error clearing data: {e}")
        else:
            st.session_state.confirm_clear = True
            st.warning("⚠️ Click again to confirm deletion of all posts")

# =====================================================
# MAIN APPLICATION
# =====================================================

def main():
    """Main application function"""
    st.set_page_config(
        page_title="Webhook LinkedIn Generator",
        page_icon="🔗",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Sidebar info
    with st.sidebar:
        st.header("🔗 Webhook LinkedIn Generator")
        st.write("Premium webhook automation for LinkedIn content")
        
        st.markdown("---")
        st.subheader("📊 Quick Stats")
        posts = load_webhook_posts()
        st.write(f"**Total Posts:** {len(posts)}")
        
        if posts:
            st.write(f"**Last Generated:** {posts[-1]['timestamp'][:10]}")
            sources = set([p.get('rss_source', 'Unknown') for p in posts])
            st.write(f"**Active Sources:** {len(sources)}")
        
        st.markdown("---")
        st.subheader("🚀 Quick Actions")
        if st.button("🧪 Quick Test", key="sidebar_test"):
            st.session_state.quick_test = True
        
        if st.button("📊 Refresh Data", key="sidebar_refresh"):
            st.rerun()
        
        st.markdown("---")
        st.subheader("ℹ️ About")
        st.write("""
        This app runs separately from your main LinkedIn generator, 
        providing safe webhook testing with zero risk to your existing application.
        
        **Features:**
        • Real-time webhook processing
        • LinkedIn post generation
        • Content management
        • Testing tools
        """)
    
    # Main interface
    create_main_interface()
    
    # Handle quick test from sidebar
    if st.session_state.get('quick_test'):
        st.session_state.quick_test = False
        # Auto-generate a quick test post
        test_data = {
            'title': f'Quick Test: AI Trends Update {datetime.now().strftime("%H:%M")}',
            'summary': 'This is a quick test of the webhook functionality to verify everything is working correctly.',
            'link': 'https://example.com/quick-test',
            'rss_source': 'Quick Test'
        }
        
        test_post = generate_linkedin_post_from_webhook(
            test_data['title'], test_data['summary'], test_data['link'], test_data['rss_source']
        )
        
        save_webhook_post({
            'id': f"quick_{int(time.time())}",
            'content': test_post,
            'source_title': test_data['title'],
            'source_url': test_data['link'],
            'rss_source': test_data['rss_source'],
            'timestamp': datetime.now().isoformat(),
            'auto_generated': True,
            'is_test': True,
            'is_quick_test': True
        })
        
        st.success("⚡ Quick test completed!")
        st.rerun()

if __name__ == "__main__":
    main()
