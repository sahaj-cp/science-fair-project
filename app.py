import streamlit as st

# पेज कॉन्फ़िगरेशन
st.set_page_config(
    page_title="Science Fair Portal",
    page_icon="🚀",
    layout="centered"
)

# कस्टम CSS - प्रीमियम और क्लीन लुक के लिए
st.markdown("""
    <style>
    .main {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
    }
    .stTextInput > div > div > input {
        border-radius: 10px;
        border: 1px solid #3b82f6;
        padding: 10px 14px;
    }
    .stButton > button {
        width: 100%;
        border-radius: 10px;
        height: 48px;
        background: linear-gradient(90deg, #2563eb, #3b82f6);
        color: white;
        font-weight: 600;
        font-size: 16px;
        border: none;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        background: linear-gradient(90deg, #1d4ed8, #2563eb);
        box-shadow: 0 4px 14px rgba(37, 99, 235, 0.4);
    }
    </style>
""", unsafe_allow_html=True)

# लॉगिन स्टेट मैनेज करने के लिए session_state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# अगर लॉगिन नहीं है तो लॉगिन कार्ड दिखेगा
if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align: center; color: #60a5fa;'>🚀 Science Fair Portal</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #94a3b8;'>Please sign in to access your dashboard</p>", unsafe_allow_html=True)
    
    # क्लीन कार्ड कंटेनर
    with st.container(border=True):
        st.subheader("Login")
        username = st.text_input("Username", placeholder="Enter your username")
        password = st.text_input("Password", type="password", placeholder="Enter your password")
        
        st.write("") # थोड़ा स्पेस
        if st.button("Sign In"):
            if username == "admin" and password == "12345":
                st.session_state.logged_in = True
                st.session_state.username = username
                st.rerun()
            else:
                st.error("Invalid username or password. Please try again.")

# लॉगिन होने के बाद दिखने वाला डैशबोर्ड
else:
    st.balloons() # सेलिब्रेशन एनिमेशन
    st.title(f"Welcome, {st.session_state.username}!")
    st.success("You are successfully logged in.")
    
    # डैशबोर्ड कार्ड्स
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="Project Status", value="Active", delta="Ready")
    with col2:
        st.metric(label="Fair Date", value="Oct 2026", delta="Upcoming")
        
    with st.container(border=True):
        st.write("### 📊 Project Overview")
        st.info("Here you can display your science fair models, data charts, and project documentation.")
        
    if st.button("Log Out"):
        st.session_state.logged_in = False
        st.rerun()
