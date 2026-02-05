import os
import sys
import threading
from kivy.app import App
from kivy.uix.label import Label
from kivy.clock import Clock
import webbrowser

# 1. SETUP DJANGO
# Point this to your project name (check your manage.py to be sure)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings") 
import django
from django.core.management import call_command

def run_server():
    # This starts the server on the phone's local memory
    django.setup()
    # Ensure we bind to port 8000
    call_command("runserver", "127.0.0.1:8000", "--noreload")

class ServerApp(App):
    def build(self):
        # 2. START SERVER IN BACKGROUND
        t = threading.Thread(target=run_server)
        t.daemon = True
        t.start()
        
        # 3. OPEN BROWSER AFTER 3 SECONDS
        # We give the server a moment to warm up
        Clock.schedule_once(self.open_browser, 3)
        
        return Label(text="Starting LuckyX Server...\nPlease wait.")

    def open_browser(self, *args):
        # This opens the user's default browser (Chrome/Samsung Internet) to your offline app
        webbrowser.open("http://127.0.0.1:8000")

if __name__ == "__main__":
    ServerApp().run()
