import streamlit as st

st.set_page_config(page_title="FedEx Store", page_icon="🚚", layout="wide")

# HEADER
st.title("🚚 FedEx Store")
st.subheader("Ship. Track. Deliver. Fast & Reliable Across Nigeria")

col1, col2, col3 = st.columns(3)
col1.button("📦 Track Package")
col2.button("💰 Get Quote") 
col3.button("🚛 Book Pickup")

st.divider()

# TRACK SECTION
st.header("Track Your Package")
tracking_id = st.text_input("Enter Tracking Number", placeholder="FX123456789NG")

if st.button("Track Now"):
    if tracking_id:
        st.success(f"Tracking: {tracking_id}")
        st.write("**Status:** In Transit")
        st.write("**Last Update:** Onitsha Hub - Sept 7, 2026 2:30 PM")
        st.progress(60)
        st.write("Estimated Delivery: Sept 9, 2026")
    else:
        st.warning("Please enter a tracking number")

st.divider()

# SERVICES
st.header("Our Services")
s1, s2, s3 = st.columns(3)
with s1:
    st.subheader("⚡ Express Delivery")
    st.write("Next day delivery within Nigeria")
with s2:
    st.subheader("🌍 International")
    st.write("Ship to USA, UK, Canada & more")
with s3:
    st.subheader("💳 Pay with BTC & Naira")
    st.write("Crypto and bank payments accepted")

st.divider()

# FOOTER
st.caption("© 2026 FedEx Store. Based in Onitsha, Anambra State, Nigeria.")