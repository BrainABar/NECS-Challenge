"""
    Used by flask to run internal server
    It is not recommended to use it during production but useful during
    development.
"""
from app import create_app

if __name__ == '__main__':
    app = create_app()
    app.run()