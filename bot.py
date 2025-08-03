from pyrogram import filters
from pyrogram.client import Client
from pyrogram.types import ChatMember
import logging
import time
from datetime import datetime, timedelta
from config import API_ID, API_HASH, BOT_TOKEN, SESSION_NAME, EMOJIS

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AFKBot:
    def __init__(self):
        self.app = Client(
            SESSION_NAME,
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN
        )
        self.afk_users = {}
        self.setup_handlers()
    
    def setup_handlers(self):
        """Setup all message handlers"""
        
        @self.app.on_message(filters.command("afk") & filters.group)
        async def afk_handler(client, message):
            try:
                # Get AFK reason from command arguments
                reason = " ".join(message.command[1:]) or "AFK"
                user_id = message.from_user.id
                
                # Store AFK status with timestamp
                self.afk_users[user_id] = {
                    'reason': reason,
                    'timestamp': time.time()
                }
                
                # Send confirmation message
                await message.reply(
                    f"💤 {message.from_user.mention} is now AFK: {reason}"
                )
                logger.info(f"User {message.from_user.first_name} ({user_id}) set AFK: {reason}")
                
            except Exception as e:
                logger.error(f"Error in AFK handler: {e}")
                await message.reply("❌ Failed to set AFK status. Please try again.")
        
        @self.app.on_message(filters.group & ~filters.command(["afk", "tagall", "all", "help", "start"]))
        async def remove_afk(client, message):
            try:
                if message.from_user and message.from_user.id in self.afk_users:
                    user_id = message.from_user.id
                    afk_data = self.afk_users[user_id]
                    
                    # Calculate AFK duration
                    afk_duration = time.time() - afk_data['timestamp']
                    duration_text = self.format_duration(afk_duration)
                    
                    # Remove AFK status
                    del self.afk_users[user_id]
                    
                    # Send welcome back message with duration
                    await message.reply(
                        f"👋 {message.from_user.mention} is back!\n⏰ You were AFK for: {duration_text}"
                    )
                    logger.info(f"User {message.from_user.first_name} ({user_id}) is back from AFK after {duration_text}")
                    
            except Exception as e:
                logger.error(f"Error in remove AFK handler: {e}")
        
        @self.app.on_message(filters.command(["tagall", "all"]) & filters.group)
        async def tag_all(client, message):
            try:
                # Check if bot has admin privileges
                try:
                    me = await client.get_chat_member(message.chat.id, "me")
                    if not me.privileges or not me.privileges.can_manage_chat:
                        await message.reply("❌ I must be admin to tag everyone.")
                        return
                except Exception as perm_error:
                    logger.error(f"Permission check failed: {perm_error}")
                    await message.reply("❌ Failed to check permissions. Make sure I'm an admin.")
                    return
                
                
                count = 0
                tagged = ""
                total_tagged = 0
                
                # Get chat members and tag non-AFK users
                async for member in client.get_chat_members(message.chat.id):
                    try:
                        # Skip bots and AFK users
                        if member.user.is_bot or member.user.id in self.afk_users:
                            continue
                        
                        # Skip deleted accounts
                        if member.user.is_deleted:
                            continue
                        
                        # Add user to tag list
                        emoji = EMOJIS[count % len(EMOJIS)]
                        user_name = member.user.first_name or "User"
                        tagged += f"{emoji} [{user_name}](tg://user?id={member.user.id})\n"
                        count += 1
                        total_tagged += 1
                        
                        # Send message every 5 users to avoid hitting limits
                        if count % 5 == 0:
                            await message.reply(tagged, disable_web_page_preview=True)
                            tagged = ""
                            
                    except Exception as member_error:
                        logger.error(f"Error processing member: {member_error}")
                        continue
                
                # Send remaining tagged users
                if tagged:
                    await message.reply(tagged, disable_web_page_preview=True)
                
                # Send summary if no users were tagged
                if total_tagged == 0:
                    await message.reply("👥 No active users to tag (excluding bots and AFK users).")
                else:
                    logger.info(f"Tagged {total_tagged} users in chat {message.chat.id}")
                    
            except Exception as e:
                logger.error(f"Error in tagall handler: {e}")
                await message.reply("❌ Failed to tag users. Please try again.")
        
        @self.app.on_message(filters.command("help"))
        async def help_command(client, message):
            help_text = """
🤖 **AFK Bot Commands:**

/afk [reason] - Set yourself as AFK with optional reason
/tagall or /all - Tag all active users
/help - Show this help message

**Features:**
• Automatically removes AFK status when you send a message
• Only non-AFK users are tagged in tagall
• Bot must be admin to access member list
"""
            await message.reply(help_text)
        
        @self.app.on_message(filters.command("start"))
        async def start_command(client, message):
            start_text = """
👋 **Welcome to AFK Bot!**

I can help you manage AFK (Away From Keyboard) status in your groups.

**Commands:**
/afk [reason] - Set yourself as AFK
/tagall - Tag all active users
/help - Show detailed help

Add me to a group and make me admin to start using!
"""
            await message.reply(start_text)
        
        @self.app.on_message(filters.group & ~filters.command(["afk", "tagall", "all", "help", "start"]))
        async def afk_mention_handler(client, message):
            try:
                # Check for replies to AFK users
                if message.reply_to_message and message.reply_to_message.from_user:
                    replied_user_id = message.reply_to_message.from_user.id
                    if replied_user_id in self.afk_users:
                        afk_data = self.afk_users[replied_user_id]
                        afk_duration = time.time() - afk_data['timestamp']
                        duration_text = self.format_duration(afk_duration)
                        
                        await message.reply(
                            f"💤 {message.reply_to_message.from_user.mention} is AFK!\n"
                            f"📝 Reason: {afk_data['reason']}\n"
                            f"⏰ AFK since: {duration_text} ago"
                        )
                        return
                
                # Check for mentions in message
                if message.entities:
                    for entity in message.entities:
                        if entity.type.name == "TEXT_MENTION" and entity.user:
                            user_id = entity.user.id
                            if user_id in self.afk_users:
                                afk_data = self.afk_users[user_id]
                                afk_duration = time.time() - afk_data['timestamp']
                                duration_text = self.format_duration(afk_duration)
                                
                                await message.reply(
                                    f"💤 {entity.user.mention} is AFK!\n"
                                    f"📝 Reason: {afk_data['reason']}\n"
                                    f"⏰ AFK since: {duration_text} ago"
                                )
                                return
                        elif entity.type.name == "MENTION":
                            # Handle @username mentions
                            mention_text = message.text[entity.offset:entity.offset + entity.length]
                            username = mention_text[1:]  # Remove @ symbol
                            
                            # Find user by username in AFK list
                            for afk_user_id, afk_data in self.afk_users.items():
                                try:
                                    user_info = await client.get_users(afk_user_id)
                                    if user_info.username and user_info.username.lower() == username.lower():
                                        afk_duration = time.time() - afk_data['timestamp']
                                        duration_text = self.format_duration(afk_duration)
                                        
                                        await message.reply(
                                            f"💤 @{username} is AFK!\n"
                                            f"📝 Reason: {afk_data['reason']}\n"
                                            f"⏰ AFK since: {duration_text} ago"
                                        )
                                        return
                                except:
                                    continue
                            
            except Exception as e:
                logger.error(f"Error in AFK mention handler: {e}")
    
    def format_duration(self, seconds):
        """Format duration in seconds to human readable format"""
        if seconds < 60:
            return f"{int(seconds)} seconds"
        elif seconds < 3600:
            minutes = int(seconds // 60)
            return f"{minutes} minute{'s' if minutes != 1 else ''}"
        elif seconds < 86400:
            hours = int(seconds // 3600)
            minutes = int((seconds % 3600) // 60)
            if minutes > 0:
                return f"{hours} hour{'s' if hours != 1 else ''} and {minutes} minute{'s' if minutes != 1 else ''}"
            else:
                return f"{hours} hour{'s' if hours != 1 else ''}"
        else:
            days = int(seconds // 86400)
            hours = int((seconds % 86400) // 3600)
            if hours > 0:
                return f"{days} day{'s' if days != 1 else ''} and {hours} hour{'s' if hours != 1 else ''}"
            else:
                return f"{days} day{'s' if days != 1 else ''}"
    
    def run(self):
        """Start the bot with automatic reconnection"""
        max_retries = 5
        retry_delay = 10
        
        for attempt in range(max_retries):
            try:
                logger.info(f"Starting AFK Bot... (Attempt {attempt + 1}/{max_retries})")
                self.app.run()
                break  # If we get here, bot stopped normally
            except Exception as e:
                logger.error(f"Bot crashed: {e}")
                if attempt < max_retries - 1:
                    logger.info(f"Retrying in {retry_delay} seconds...")
                    time.sleep(retry_delay)
                    retry_delay *= 2  # Exponential backoff
                else:
                    logger.error("Max retries reached. Bot failed to start.")
                    raise
