import os


def set_env_vars():
    env = os.environ.get('ENVIRONMENT', 'Not Set')
    if env == "Not Set":
        print("Setting env variables")
        os.environ["ENVIRONMENT"] = 'local'  # 'dev' 'test' 'prod'
    env = os.environ.get('ENVIRONMENT', 'Not Set')
    if env == "Not Set":
        raise Exception("Environment not set")
    elif env == 'local':
        os.environ["base_path"] = "http://localhost:8501"
        os.environ["backend"] = "http://localhost:8000/api/"
    else:
        os.environ["base_path"] = "WHATEVER THE HOSTING URL IS"
        # If running through docker compose
        os.environ["backend"] = "http://fastapi:8000/api/"
