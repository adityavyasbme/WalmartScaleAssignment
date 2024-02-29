def hide_footer(st):
    style = """
    <style>
    footer {
        visibility:hidden;
    }
    </style>
    """
    st.markdown(style, unsafe_allow_html=True)
