import streamlit as st
import sqlite3
import hashlib
import datetime

# DATABASE SETUP
conn = sqlite3.connect('fedex.db', check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS users
             (id INTEGER PRIMARY KEY, email TEXT, password TEXT, name TEXT)''')
c.execute('''CREATE TABLE IF NOT EXISTS orders
             (id INTEGER PRIMARY KEY, user_email TEXT, tracking TEXT,
              pickup TEXT, delivery TEXT, weight REAL, status TEXT, date TEXT)''')
conn.commit()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def generate_tracking():
    return "FX" + str(datetime.datetime.now().timestamp()).replace(".", "")[:10] + "NG"

# SESSION STATE
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.email = ""

st.set_page_config(page_title="FedEx Store", page_icon="🚚", layout="wide")

# LOGIN / SIGNUP PAGE
if not st.session_state.logged_in:
    st.title("🚚 FedEx Store")
    tab1, tab2 = st.tabs(["Login", "Create Account"])

    with tab1:
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            c.execute("SELECT * FROM users WHERE email=? AND password=?",
                      (email, hash_password(password)))
            if c.fetchone():
                st.session_state.logged_in = True
                st.session_state.email = email
                st.rerun()
            else:
                st.error("Wrong email or password")

    with tab2:
        name = st.text_input("Full Name")
        new_email = st.text_input("Email ")
        new_password = st.text_input("Password ", type="password")
        if st.button("Sign Up"):
            try:
                c.execute("INSERT INTO users VALUES (NULL,?,?)",
                          (new_email, hash_password(new_password), name))
                conn.commit()
                st.success("Account created! Please login")
            except:
                st.error("Email already exists")

# DASHBOARD - AFTER LOGIN
else:
    st.sidebar.title(f"Welcome 👋")
    st.sidebar.write(st.session_state.email)
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

    st.title("🚚 FedEx Store Dashboard")

    menu = st.sidebar.radio("Menu", ["Book Shipment", "Track Package", "My Orders", "Get Quote"])

    # 1. BOOK SHIPMENT
    if menu == "Book Shipment":
        st.header("📦 Book a Pickup")
        col1, col2 = st.columns(2)
        with col1:
            pickup = st.text_input("Pickup Address", placeholder="123 Main St, Onitsha")
            delivery = st.text_input("Delivery Address")
        with col2:
            weight = st.number_input("Weight (kg)", 0.5, 50.0, 1.0)
            phone = st.text_input("Phone Number")

        if st.button("Create Waybill - ₦3,500"):
            tracking = generate_tracking()
            date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
            c.execute("INSERT INTO orders VALUES (NULL,?,?,?,?,?,?,?)",
                      (st.session_state.email, tracking, pickup, delivery, weight, "Processing", date))
            conn.commit()
            st.success(f"Order Created! Your Tracking ID: {tracking}")
            st.info("Pay ₦3,500 to complete booking. Pay with BTC or Card coming soon")

    # 2. TRACK PACKAGE
    elif menu == "Track Package":
        st.header("🔍 Track Your Package")
        tracking_id = st.text_input("Enter Tracking Number")
        if st.button("Track"):
            c.execute("SELECT * FROM orders WHERE tracking=?", (tracking_id,))
            order = c.fetchone()
            if order:
                st.success(f"Status: {order[6]}")
                st.write(f"From: {order[3]}")
                st.write(f"To: {order[4]}")
                st.write(f"Booked: {order[7]}")
                st.progress(50 if order[6]=="Processing" else 100)
            else:
                st.error("Tracking number not found")

    # 3. MY ORDERS
    elif menu == "My Orders":
        st.header("📋 My Orders")
        c.execute("SELECT * FROM orders WHERE user_email=?", (st.session_state.email,))
        orders = c.fetchall()
        if orders:
            for o in orders:
                with st.expander(f"{o[2]} - {o[6]}"):
                    st.write(f"From: {o[3]}")
                    st.write(f"To: {o[4]}")
                    st.write(f"Weight: {o[5]}kg")
                    st.write(f"Date: {o[7]}")
        else:
            st.info("No orders yet")

    # 4. GET QUOTE
    elif menu == "Get Quote":
        st.header("💰 Get Shipping Quote")
        from_city = st.selectbox("From", ["Onitsha", "Lagos", "Abuja", "PH"])
        to_city = st.selectbox("To", ["Lagos", "Abuja", "PH", "Onitsha"])
        weight = st.number_input("Weight kg", 1, 20, 2)
        price = weight * 1750 # ₦1750 per kg example
        if st.button("Calculate"):
            st.metric("Estimated Price", f"${price:,}")