import streamlit as st
import pandas as pd
from PIL import Image
import time
from logic import load_recipes, find_matching_recipes, filter_recipes, get_substitutions

# --- AI Service Simulation ---
def identify_ingredients_from_image(image):
    """
    Simulates calling an AI Vision API (e.g., GPT-4o, Gemini Pro Vision).
    In a real deployment, you would replace this with actual API code.
    """
    # Simulate network latency for realism
    time.sleep(1.5)
    
    # Mock return data based on a successful "scan"
    return ["eggs", "avocado", "bread", "tomato", "cheese"]

# --- UI Configuration ---
st.set_page_config(
    page_title="Smart Recipe Generator",
    page_icon="🍳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for a cleaner look
st.markdown("""
<style>
    .stButton>button {
        width: 100%;
        border-radius: 5px;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 10px;
        border-radius: 5px;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

# --- Header ---
st.title("🍳 Smart Recipe Generator")
st.markdown("""
**Upload a photo of your fridge** or enter ingredients manually to discover what you can cook today!
""")

# --- Sidebar: Filters ---
st.sidebar.header("⚙️ Preferences")
diet_pref = st.sidebar.selectbox("Dietary Restriction", ["None", "Vegetarian", "Vegan", "Gluten-Free"])
diff_pref = st.sidebar.selectbox("Difficulty Level", ["Any", "Easy", "Medium", "Hard"])

# --- Main Interface ---
col1, col2 = st.columns([1, 1], gap="large")

# State management for ingredients
if 'ingredients_list' not in st.session_state:
    st.session_state.ingredients_list = []

with col1:
    st.subheader("1. Add Ingredients")
    
    # Image Input
    uploaded_file = st.file_uploader("📸 Upload Food Photo", type=['jpg', 'png', 'jpeg'])
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption='Uploaded Image', width=300)
        
        if st.button("🔍 Analyze Image"):
            with st.spinner('AI is identifying ingredients...'):
                detected = identify_ingredients_from_image(image)
                st.session_state.ingredients_list.extend(detected)
                st.session_state.ingredients_list = list(set(st.session_state.ingredients_list)) # Dedupe
                st.success(f"Found: {', '.join(detected)}")

    # Manual Input
    st.write("---")
    text_input = st.text_input("📝 Manual Entry", placeholder="e.g. chicken, rice, garlic")
    if st.button("Add Text Ingredients"):
        if text_input:
            new_items = [x.strip() for x in text_input.split(',')]
            st.session_state.ingredients_list.extend(new_items)
            st.session_state.ingredients_list = list(set(st.session_state.ingredients_list))

    # Display Current List
    if st.session_state.ingredients_list:
        st.write("### 🛒 Your Basket:")
        st.info(", ".join(st.session_state.ingredients_list))
        if st.button("Clear Basket"):
            st.session_state.ingredients_list = []
            st.rerun()

# --- Recipe Results ---
with col2:
    st.subheader("2. Suggested Recipes")
    
    if st.session_state.ingredients_list:
        # Load DB
        all_recipes = load_recipes()
        
        # 1. Filter
        filtered_db = filter_recipes(all_recipes, 
                                     dietary_filter=None if diet_pref == "None" else diet_pref,
                                     difficulty_filter=None if diff_pref == "Any" else diff_pref)
        
        # 2. Match
        matches = find_matching_recipes(st.session_state.ingredients_list, filtered_db)
        
        if not matches:
            st.warning("No recipes found matching your criteria. Try adding more staple ingredients like 'salt', 'oil', or 'onion'.")
        else:
            st.write(f"Found {len(matches)} recipes matching your ingredients!")
            
            for recipe in matches:
                # Color code match score
                score_color = "green" if recipe['match_score'] > 0.7 else "orange" if recipe['match_score'] > 0.5 else "red"
                
                with st.expander(f"🍽️ {recipe['name']} | Match: :{score_color}[{int(recipe['match_score']*100)}%]"):
                    
                    # Layout inside expander
                    rc1, rc2 = st.columns(2)
                    
                    with rc1:
                        st.markdown(f"**Cuisine:** {recipe['cuisine']}")
                        st.markdown(f"**Time:** ⏱️ {recipe['time_minutes']} min")
                        st.markdown(f"**Difficulty:** {recipe['difficulty']}")
                        st.markdown(f"**Calories:** 🔥 {recipe['nutrition']['calories']}")
                        st.markdown(f"**Protein:** 💪 {recipe['nutrition']['protein']}")
                    
                    with rc2:
                        st.markdown("**Missing Ingredients:**")
                        if recipe['missing_ingredients']:
                            for missing in recipe['missing_ingredients']:
                                sub = get_substitutions(missing)
                                if sub:
                                    st.markdown(f"- ❌ {missing} *(Try: {sub})*")
                                else:
                                    st.markdown(f"- ❌ {missing}")
                        else:
                            st.success("You have everything!")

                    st.markdown("---")
                    st.markdown("**Instructions:**")
                    for idx, step in enumerate(recipe['steps'], 1):
                        st.markdown(f"{idx}. {step}")
                    
                    # User Feedback Mockup
                    st.markdown("---")
                    fb_col1, fb_col2 = st.columns([1,3])
                    with fb_col1:
                        if st.button("⭐ Save", key=f"save_{recipe['id']}"):
                            st.toast(f"Saved {recipe['name']} to favorites!")
    else:
        st.info("👈 Add ingredients to see recipes here.")
