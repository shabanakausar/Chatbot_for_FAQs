import json
import spacy
import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import random

class LuxuryBoutiqueChatbot:
    def __init__(self, faq_file_path):
        self.faqs = self.load_faqs(faq_file_path)
        self.nlp = spacy.load("en_core_web_sm")
        self.collections = self.get_unique_collections()
        
        # Initialize NLP components
        self.search_texts = self.build_search_context()
        self.vectorizer = TfidfVectorizer(
            tokenizer=self.preprocess_text,
            min_df=2,
            token_pattern=None
        )
        self.question_vectors = self.vectorizer.fit_transform(self.search_texts)

    def load_faqs(self, file_path):
        """Load and validate FAQ data with proper error handling"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                return data.get("faqs", [])
        except Exception as e:
            st.error(f"Error loading FAQ file: {str(e)}")
            return []

    def get_unique_collections(self):
        """Extract unique collections from FAQs"""
        return list({faq.get('collection', '') for faq in self.faqs})

    def build_search_context(self):
        """Create enhanced search context with key information"""
        contexts = []
        for faq in self.faqs:
            context = (
                f"{faq['question']} "
                f"{faq.get('answer', '')} "
                f"{' '.join(faq.get('tags', []))} "
                f"{faq.get('collection', '')} "
                f"{faq.get('price_range', '')} "
                f"{self.process_services(faq.get('services', []))}"
            )
            contexts.append(context)
        return contexts

    def process_services(self, services):
        """Convert service tuples to searchable text"""
        return ' '.join([f"SERVICE_{s[0].replace(' ', '_')}" for s in services])

    def preprocess_text(self, text):
        """Enhanced text preprocessing with price awareness"""
        doc = self.nlp(text)
        tokens = []
        for token in doc:
            if token.is_stop or token.is_punct:
                continue
            if token.like_num or token.is_currency:
                tokens.append(token.text.lower())
            elif token.is_alpha and len(token) > 2:
                tokens.append(token.lemma_.lower())
        return tokens or ['boutique', 'shirt']

    def generate_response(self, user_query):
        """Generate responses with priority to pricing and collections"""
        # First handle price queries
        if any(word in user_query.lower() for word in ['price', 'cost', 'how much']):
            return self.handle_pricing_query(user_query)
            
        # Then handle collection queries
        for collection in self.collections:
            if collection.lower() in user_query.lower():
                return self.handle_collection_query(collection)
        
        # General response handling
        query_vec = self.vectorizer.transform([user_query])
        similarities = cosine_similarity(query_vec, self.question_vectors)
        best_idx = similarities.argmax()
        
        if similarities[0, best_idx] > 0.4:
            return self.format_response(self.faqs[best_idx])
        return self.get_fallback_response()

    def handle_pricing_query(self, query):
        """Specialized pricing response handler"""
        price_info = []
        for faq in self.faqs:
            if 'price_range' in faq:
                if faq['price_range'].lower() in query.lower():
                    price_info.append(
                        f"**{faq.get('collection', 'Collection')}**\n"
                        f"Price Range: {faq['price_range']}\n"
                        f"Inclusions: {faq['answer']}\n"
                    )
        return "\n".join(price_info) if price_info else self.get_fallback_pricing()

    def handle_collection_query(self, collection):
        """Handle collection-specific queries"""
        collection_faqs = [f for f in self.faqs if f.get('collection') == collection]
        if not collection_faqs:
            return f"Sorry, we couldn't find details about {collection}"
            
        response = [
            f"✨ **{collection}** ✨",
            "Featured in this collection:"
        ]
        for faq in collection_faqs[:3]:
            response.append(f"- {faq['question']}")
        return "\n".join(response)

    def format_response(self, faq):
        """Format FAQ response with rich formatting"""
        response = []
        if 'price_range' in faq:
            response.append(f"💰 **Price Range:** {faq['price_range']}")
        response.append(faq['answer'])
        if 'services' in faq:
            response.append("\n**Services Available:**")
            response.extend([f"- {s[0]} ({s[2]})" for s in faq['services'][:2]])
        return "\n".join(response)

    def get_fallback_response(self):
        """Default response when no matches found"""
        suggestions = [
            "Ask about our Casual, Premium, or Luxury collections",
            "Need price ranges? Try: 'What's the cost of premium shirts?'",
            "Ask about services like alterations or monogramming"
        ]
        return f"Here are some suggestions:\n" + "\n- ".join(suggestions)

    def get_fallback_pricing(self):
        """Default pricing response"""
        return (
            "Our collections are priced at:\n"
            "- 🎨 Casual: $45-$65\n"
            "- 🌟 Premium: $85-$120\n"
            "- 🎁 Luxury: $150+"
        )

# Streamlit UI Configuration
st.set_page_config(page_title="Boutique Assistant", page_icon="👔")

# Custom Styling
st.markdown("""
<style>
    [data-testid=stSidebar] { background-color: #f8f9fa; }
    .stChatInput input { border: 2px solid #4a4a4a; }
    .stMarkdown { color: #2d3436; }
</style>
""", unsafe_allow_html=True)

# Chat Interface
st.title("👑 She Designs FAQ CHATBOT")
st.markdown("""
**Ask about:**
- Collection [Casual, Luxury Artisan, Premium Designer] Prices
- Shirt Care
- Custom Services
- Shipping Options
""")

# Initialize Chatbot
try:
    bot = LuxuryBoutiqueChatbot("faqs.json")
except Exception as e:
    st.error(f"Failed to initialize chatbot: {str(e)}")
    st.stop()

# Chat History Management
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Chat History
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User Input Handling
if prompt := st.chat_input("How can I assist with our luxury shirts today?"):
    # Add user message
    
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Generate response
    try:
        response = bot.generate_response(prompt)
    except Exception as e:
        response = f"Error generating response: {str(e)}"
    
    # Add bot response
    st.session_state.messages.append({"role": "assistant", "content": response})
    
    # Rerun to update display
    st.rerun()

# Sidebar Information
with st.sidebar:
    st.header("Boutique Services")
    st.markdown("""
    - **Custom Tailoring** ✂️
    - **Monogramming** 🧵
    - **VIP Consultations** 👑
    - **Eco-Friendly Cleaning** 🌿
    """)
    
    st.divider()
    st.subheader("Try Asking:")
    st.markdown("""
    - "Price of casual shirts"
    - "What's in the luxury collection?"
    - "How to care for silk shirts"
    - "Do you offer gift wrapping?"
    """)
    
    if st.button("Clear Conversation"):
        st.session_state.messages = []
        st.rerun()