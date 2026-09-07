import streamlit as st
import sqlite3
import hashlib
import datetime

# DATABASE SETUP
conn = sqlite3.connect('fedex.db', check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS users
             (id INTEGER PRIMARY KEY, email TEXT UNIQUE, password TEXT, name TEXT)''')
c.execute('''CREATE TABLE IF NOT EXISTS orders
             (id INTEGER PRIMARY KEY, user_email TEXT, tracking TEXT,
              pickup TEXT, delivery TEXT, weight REAL, status TEXT, date TEXT)''')
conn.commit()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def generate_tracking():
    return "FX" + str(datetime.datetime.now().timestamp()).replace(".", "")[:10] + "NG"

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.email = ""

st.set_page_config(page_title="FedEx Store", page_icon="🚚", layout="wide")

# LOGIN / SIGNUP PAGE
if not st.session_state.logged_in:
    st.title("🚚 FedEx Store")
    tab1, tab2 = st.tabs(["Login", "Create Account"])

    with tab1:
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_pass")
        if st.button("Login"):
            c.execute("SELECT * FROM users WHERE email=? AND password=?",
                      (email, hash_password(password)))
            if c.fetchone():
                st.session_state.logged_in = True
                st.session_state.email = email
                st.rerun()
            else:
                st.error("Wrong email or password. Did you create the account?")

    with tab2:
        name = st.text_input("Full Name", key="signup_name")
        new_email = st.text_input("Email ", key="signup_email")
        new_password = st.text_input("Password ", type="password", key="signup_pass")
        if st.button("Sign Up"):
            try:
                c.execute("INSERT INTO users VALUES (NULL,?,?,?)",  # FIXED: 3 ?
                          (new_email, hash_password(new_password), name))
                conn.commit()
                st.success("Account created! Now go to Login tab")
            except sqlite3.IntegrityError:
                st.error("Email already exists. Try logging in")

# DASHBOARD - AFTER LOGIN
else:
    st.sidebar.title(f"Welcome 👋")
    st.sidebar.write(st.session_state.email)
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

    st.title("🚚 FedEx Store Dashboard")
    st.success("You are logged in!")