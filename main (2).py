#!/usr/bin/env python3
"""
Telegram AFK Bot with Flask Keepalive Server
"""

import logging
import signal
import sys
from threading import Thread
from time import sleep

from bot import AFKBot
from web_server import WebServer
from config import WEB_HOST, WEB_PORT

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class AFKBotService:
    def __init__(self):
        self.bot = AFKBot()
        self.web_server = WebServer(host=WEB_HOST, port=WEB_PORT)
        self.running = True
        
    def signal_handler(self, signum, frame):
        """Handle shutdown signals"""
        logger.info(f"Received signal {signum}, shutting down...")
        self.running = False
        sys.exit(0)
    
    def start_web_server(self):
        """Start Flask web server in a separate thread"""
        try:
            logger.info("Starting web server thread...")
            self.web_server.run()
        except Exception as e:
            logger.error(f"Web server error: {e}")
    
    def start_bot(self):
        """Start Telegram bot with automatic restart"""
        while self.running:
            try:
                logger.info("Starting Telegram bot...")
                self.bot.run()
                if self.running:
                    logger.warning("Bot stopped unexpectedly, restarting in 10 seconds...")
                    sleep(10)
                    # Create new bot instance to avoid session issues
                    self.bot = AFKBot()
            except Exception as e:
                logger.error(f"Bot error: {e}")
                if self.running:
                    logger.info("Restarting bot in 10 seconds...")
                    sleep(10)
                    # Create new bot instance
                    self.bot = AFKBot()
                else:
                    break
    
    def run(self):
        """Start both bot and web server"""
        # Setup signal handlers
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        
        try:
            # Start web server in background thread
            web_thread = Thread(target=self.start_web_server, daemon=True)
            web_thread.start()
            
            # Give web server time to start
            sleep(2)
            logger.info("Web server started successfully")
            
            # Start bot in main thread (Pyrogram needs main thread for async)
            self.start_bot()
            
        except KeyboardInterrupt:
            logger.info("Received keyboard interrupt, shutting down...")
        except Exception as e:
            logger.error(f"Application error: {e}")
            raise
        finally:
            logger.info("Application stopped")

def main():
    """Main entry point"""
    try:
        logger.info("=== Starting AFK Bot Service ===")
        service = AFKBotService()
        service.run()
    except Exception as e:
        logger.error(f"Failed to start service: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
