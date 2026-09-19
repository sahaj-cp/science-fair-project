import stramlit as st
st.set_page_config(page_title="login portal",layout='centered')
st.title("welcome")
st.subheader("please login the app")
#username password input
username=st.text_input("enter username")
password=st.text_input("enter password")
type=("password")
#login button
if st.button('login'):
  if username == "admin"and "password=="12345";
  st.success("login successfully")
  st.write(f"Hello[username},your dashboard is ready")
else:
  st.error("you enter wrong password and username please enter again")
