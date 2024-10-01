import streamlit as st

# Pages
### Auth Pages
page_auth_welcome = st.Page(page="app/auth/welcome.py", title="Welcome", url_path="/welcome" )
page_auth_login = st.Page(page="app/auth/login.py", title="Login", url_path="/login")
page_auth_register = st.Page(page="app/auth/register.py", title="Register", url_path="/register")
page_auth_terms = st.Page(page="app/auth/terms.py", title="Terms and Conditions", url_path="/terms")
pages_auth = [page_auth_welcome, page_auth_login, page_auth_register, page_auth_terms]