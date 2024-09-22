import webview
import threading
import os

# Function to start the Django development server
def start_django():
    os.system('python manage.py runserver 127.0.0.1:5100')

if __name__ == '__main__':
    # Start Django in a new thread
    threading.Thread(target=start_django).start()

    # Create a desktop window using pywebview
    webview.create_window('Stone Crusher App', 'http://127.0.0.1:5100')
    webview.start()
