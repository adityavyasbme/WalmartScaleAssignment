import requests


def health_check(backend_url):
    r = requests.get(backend_url+'healthCheck')
    res = r.content
    if b'true' in res:
        return True
    else:
        return False


def add_health_check_button(st, backend_url):
    if st.button("Backend Health Check"):
        try:
            res = health_check(backend_url)
            if res:
                data = "Health Check Success"
            else:
                data = "Health Check Failed"
        except Exception as e:
            data = "Health Check Failed. Please Check Logs"
            print(e)
        st.write(data)
