from st_pages import Page, add_page_title, show_pages
import os


env = os.environ.get('ENVIRONMENT', 'Not Set')
if env == "Not Set":
    print("Setting env variables")
    os.environ["ENVIRONMENT"] = 'local'  # 'dev' 'test' 'prod'

relative_path = "src/application/"
relative_pages_path = "src/application/pages/"

show_pages(
    [
        Page(relative_pages_path + "Page1.py", "Demo Page 1", "🏠"),
    ]
)
