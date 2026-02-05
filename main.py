import os
import threading
import webbrowser
from kivy.app import App
from kivy.uix.label import Label
from kivy.clock import Clock

# --- THE CONFIGURATION ---
# This tells the phone: "The settings are inside the folder named 'backend'"
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")

import django
from django.core.management import call_command

class ServerApp(App):
    def build(self):
        # 1. Start the website in a background thread
        t = threading.Thread(target=self.run_server)
        t.daemon = True
        t.start()
        
        # 2. Show a loading screen
        return Label(text="Loading LuckyX...\nPlease wait 5 seconds.")

    def run_server(self):
        try:
            # Wake up Django
            django.setup()
            
            # Open the browser automatically after 5 seconds
            Clock.schedule_once(self.open_browser, 5)
            
            # Start the server on the phone (Localhost port 8000)
            call_command("runserver", "127.0.0.1:8000", "--noreload")
        except Exception as e:
            print(f"Error: {e}")

    def open_browser(self, *args):
        # This opens Chrome on the phone to your offline site
        webbrowser.open("http://127.0.0.1:8000")

if __name__ == "__main__":
    ServerApp().run()
