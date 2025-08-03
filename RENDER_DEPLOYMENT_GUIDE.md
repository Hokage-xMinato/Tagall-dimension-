# 🚀 Deploy Your Telegram Bot to Render.com (FREE 24/7)

## Step 1: Get GitHub Account
1. Go to **github.com**
2. Click **"Sign up"**
3. Create free account with your email

## Step 2: Upload Your Code to GitHub
1. Click **"Create repository"** on GitHub
2. Name it: `telegram-afk-bot`
3. Make it **Public** (required for free Render)
4. Click **"Create repository"**

## Step 3: Upload Files
Upload these files to your GitHub repository:
- `main.py`
- `bot.py` 
- `web_server.py`
- `config.py`
- `render_requirements.txt`
- `start.sh`
- `render.yaml`

## Step 4: Deploy on Render
1. Go to **render.com**
2. Click **"Get Started for Free"**
3. Sign up with your **GitHub account**
4. Click **"New +"** → **"Web Service"**
5. Select your `telegram-afk-bot` repository
6. Choose these settings:
   - **Name**: telegram-afk-bot
   - **Environment**: Python 3
   - **Build Command**: `pip install -r render_requirements.txt`
   - **Start Command**: `python main.py`
   - **Plan**: FREE

## Step 5: Add Environment Variables
In Render dashboard, add these:
- **API_ID**: 22776206
- **API_HASH**: ada968d0b6551a6c766b864ecfeffcd5  
- **BOT_TOKEN**: 8046947223:AAE-vBQ6rw0pHm9JvCjSHjv1fZ5qYtR7b0A
- **WEB_PORT**: 10000

## Step 6: Deploy & Get URL
1. Click **"Create Web Service"**
2. Wait 3-5 minutes for deployment
3. Get your URL: `https://your-app-name.onrender.com`

## Step 7: Update Uptime Monitoring
Point your uptime bot to the new Render URL!

## ✅ Result: 24/7 Bot Running FREE!
- No more 10-minute sleep
- Your uptime monitoring works perfectly
- 750 free hours/month (enough for 24/7)

## 🔗 Your Bot URL Structure:
- **Main**: `https://your-app.onrender.com/`
- **Status**: `https://your-app.onrender.com/status`
- **Health**: `https://your-app.onrender.com/health`