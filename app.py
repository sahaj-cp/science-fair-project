import streamlit as st
import sqlite3
import hashlib

# ----------------- डेटाबेस सेटअप (SQLite) -----------------
def get_connection():
    conn = sqlite3.connect("users.db", check_same_thread=False)
    return conn

def create_table():
    conn = get_connection()
    c = conn.cursor()
    # यूज़र टेबल बनाना
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT
        )
    """)
    conn.commit()
    conn.close()

# पासवर्ड को सुरक्षित (Hash) बनाने के लिए फ़ंक्शन
def make_hashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password, hashed_text):
    if make_hashes(password) == hashed_text:
        return hashed_text
    return False

# नया यूज़र ऐड करने के लिए
def add_user(username, password):
    conn = get_connection()
    c = conn.cursor()
    c.execute("INSERT INTO users(username, password) VALUES (?, ?)", (username, password))
    conn.commit()
    conn.close()

# लॉगिन चेक करने के लिए
def login_user(username, password):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    data = c.fetchall()
    conn.close()
    return data

# टेबल इनिशियलाइज़ करें
create_table()

# ----------------- पेज कॉन्फ़िगरेशन व CSS -----------------
st.set_page_config(
    page_title="Science Fair Portal",
    page_icon="🚀",
    layout="centered"
)

st.markdown("""
    <style>
    .stTextInput > div > div > input {
        border-radius: 10px;
        border: 1px solid #3b82f6;
        padding: 10px 14px;
    }
    .stButton > button {
        width: 100%;
        border-radius: 10px;
        height: 46px;
        background: linear-gradient(90deg, #2563eb, #3b82f6);
        color: white;
        font-weight: 600;
        font-size: 16px;
        border: none;
    }
    </style>
""", unsafe_allow_html=True)

# ----------------- सेशन स्टेट -----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

# ----------------- मुख्य ऐप लॉजिक -----------------
if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align: center; color: #3b82f6;'>🚀 Science Fair Portal</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: gray;'>Sign in or create a new account</p>", unsafe_allow_html=True)

    # लॉगिन और साइन अप के लिए दो अलग-अलग टैब
    tab_login, tab_signup = st.tabs(["🔑 Login", "📝 Sign Up"])

    # टैब 1: लॉगिन
    with tab_login:
        with st.container(border=True):
            st.subheader("Sign In to Your Account")
            login_user_input = st.text_input("Username", key="login_user", placeholder="Enter username")
            login_pass_input = st.text_input("Password", type="password", key="login_pass", placeholder="Enter password")
            
            st.write("")
            if st.button("Login", key="btn_login"):
                hashed_pass = make_hashes(login_pass_input)
                result = login_user(login_user_input, hashed_pass)
                
                if result:
                    st.session_state.logged_in = True
                    st.session_state.username = login_user_input
                    st.rerun()
                else:
                    st.error("गलत Username या Password! कृपया दोबारा जाँचें।")

    # टैब 2: साइन अप (नया खाता बनाना)
    with tab_signup:
        with st.container(border=True):
            st.subheader("Create a New Account")
            new_user = st.text_input("Choose a Username", key="signup_user", placeholder="Choose username")
            new_pass = st.text_input("Create Password", type="password", key="signup_pass", placeholder="Create password")
            confirm_pass = st.text_input("Confirm Password", type="password", key="signup_confirm", placeholder="Confirm password")
            
            st.write("")
            if st.button("Register Account", key="btn_signup"):
                if not new_user or not new_pass:
                    st.warning("कृपया सभी फ़ील्ड भरें!")
                elif new_pass != confirm_pass:
                    st.error("पासवर्ड मैच नहीं हो रहे हैं!")
                else:
                    try:
                        # पासवर्ड को हैश करके डेटाबेस में सुरक्षित सेव करना
                        add_user(new_user, make_hashes(new_pass))
                        st.success("अकाउंट सफलतापूर्वक बन गया! अब 'Login' टैब में जाकर साइन इन करें।")
                    except sqlite3.IntegrityError:
                        st.error("यह Username पहले से मौजूद है। कृपया कोई दूसरा नाम चुनें।")

# ----------------- लॉगिन के बाद का डैशबोर्ड -----------------
else:
    st.balloons()
    st.title(f"Welcome back, {st.session_state.username}!")
    st.success("You are successfully logged in.")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="Account Status", value="Verified", delta="Active")
    with col2:
        st.metric(label="Portal Role", value="Participant", delta="Ready")
        
    with st.container(border=True):
        st.write("### 📊 Your Project Dashboard")
        st.write(f"Hello *{st.session_state.username}*, your science fair workspace is active.")
        
    st.write("")
    if st.button("Log Out"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.rerun()
