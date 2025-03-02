import os
import requests
import streamlit as st

# --- API Key Handling ---
RAPIDAPI_KEY = os.getenv("RapidAPI") if os.getenv("RapidAPI") else st.secrets["rapidapi"]["key"]

# --- API URL ---
BASE_URL = "https://real-time-amazon-data.p.rapidapi.com/best-sellers"

# --- Available Categories ---
CATEGORIES = {
    "Software": "software",
    "Electronics": "electronics",
    "Automotive": "automotive",
    "Beauty": "beauty",
    "Home": "home"
}

# --- Streamlit UI ---
st.set_page_config(page_title="Amazon Best Sellers", layout="wide")

st.title("📦 Amazon Best Sellers Tracker")
st.write("Discover the top-selling products in different categories on Amazon in real-time.")

# --- Improve Category Selection Visibility ---
st.markdown("### 🛒 Select a Product Category")
selected_category_label = st.radio("Choose a category:", list(CATEGORIES.keys()), horizontal=True)

# Get the corresponding API category value
selected_category = CATEGORIES[selected_category_label]

# --- API Call ---
def fetch_best_sellers(category):
    querystring = {
        "category": category,
        "type": "BEST_SELLERS",
        "page": "1",
        "country": "US"
    }
    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": "real-time-amazon-data.p.rapidapi.com"
    }

    try:
        response = requests.get(BASE_URL, headers=headers, params=querystring)
        response.raise_for_status()
        return response.json().get("data", {}).get("best_sellers", [])
    except requests.exceptions.RequestException as e:
        st.error(f"⚠️ Error fetching data: {e}")
        return []

# --- Fetch & Display Data ---
best_sellers = fetch_best_sellers(selected_category)

st.subheader(f"📌 Showing Best Sellers in **{selected_category_label}**")

if best_sellers:
    for product in best_sellers:
        with st.container():
            st.image(product["product_photo"], width=150)
            st.subheader(f"#{product['rank']} {product['product_title']}")
            st.write(f"**Price:** {product['product_price']}")
            st.write(f"⭐ **Rating:** {product['product_star_rating']} ({format(product['product_num_ratings'], ',')} reviews)")
            st.write(f"🔗 [View on Amazon]({product['product_url']})")
            st.markdown("---")
else:
    st.warning("No data available. Try selecting a different category.")

# --- Footer ---
st.markdown(
    """
    <hr>
    <p style="text-align: center;">
    <b>Amazon Best Sellers Tracker</b> &copy; 2025<br>
    Developed by <a href="https://www.linkedin.com/in/josh-poresky956/" target="_blank">Josh Poresky</a>
    </p>
    """,
    unsafe_allow_html=True
)
