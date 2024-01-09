import streamlit as st

#card 
def card_info(title, subtitle1, subtitle2, text, link):

    st.markdown(
        f"""
    <div class="card-main" style="width: 100%;" "border-radius: 30px;">
    <div class="card-body">
        <h5 class="card-title" style="text-align: center;">{title}</h5>
        <h6 class="card-subtitle mb-2 text-muted" style="text-align: center;">{subtitle1}</h6>
        <h6 class="card-subtitle mb-2 text-muted" style="text-align: center;">{subtitle2}</h6>
        <p class="card-text" style="text-align: left;">{text}</p>
        <a href="#" class="card-link" style="text-align: center;">{link}</a>
    </div>
    </div>
        """, unsafe_allow_html=True
        )      