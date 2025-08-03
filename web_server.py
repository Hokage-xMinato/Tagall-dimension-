from flask import Flask
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WebServer:
    def __init__(self, host="0.0.0.0", port=5000):
        self.app = Flask(__name__)
        self.host = host
        self.port = port
        self.setup_routes()
    
    def setup_routes(self):
        @self.app.route('/')
        def home():
            return "Bot alive"
        
        @self.app.route('/status')
        def status():
            return {"status": "running", "message": "AFK Bot is active"}
        
        @self.app.route('/health')
        def health():
            return {"health": "ok", "service": "telegram-afk-bot"}
    
    def run(self):
        try:
            logger.info(f"Starting web server on {self.host}:{self.port}")
            self.app.run(host=self.host, port=self.port, debug=False)
        except Exception as e:
            logger.error(f"Failed to start web server: {e}")
