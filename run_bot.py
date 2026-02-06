#!/usr/bin/env python3
"""
🚀 EASY RUNNER SCRIPT
Run this to start the bot easily
"""

import os
import sys
import subprocess

def check_python():
    """Python চেক"""
    print("🔍 Checking Python...")
    
    try:
        result = subprocess.run([sys.executable, "--version"], 
                              capture_output=True, text=True)
        print(f"✅ Python: {result.stdout.strip()}")
        return True
    except:
        print("❌ Python not found!")
        return False

def install_requirements():
    """লাইব্রেরি ইনস্টল"""
    print("📦 Installing requirements...")
    
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Requirements installed!")
        return True
    except:
        print("❌ Failed to install requirements")
        return False

def check_config():
    """কনফিগারেশন চেক"""
    print("⚙️ Checking config...")
    
    if not os.path.exists("config.py"):
        print("❌ config.py not found!")
        return False
    
    with open("config.py", "r", encoding="utf-8") as f:
        content = f.read()
    
    if "YOUR_BOT_TOKEN_HERE" in content:
        print("⚠️ Warning: Bot token not set in config.py")
        print("Please edit config.py and add your bot token")
        return False
    
    return True

def generate_data():
    """ডাটা জেনারেট"""
    print("📝 Checking data...")
    
    # config থেকে ফাইল নাম পড়া
    import config
    
    files_exist = True
    for _, info in config.CLASSES.items():
        if not os.path.exists(info['file']):
            files_exist = False
            break
    
    if not files_exist:
        print("🔄 Data files not found, generating...")
        
        try:
            import data_generator
            generator = data_generator.QuestionGenerator()
            generator.generate_all()
            print("✅ Data generated successfully!")
            return True
        except Exception as e:
            print(f"❌ Error generating data: {e}")
            return False
    
    print("✅ Data files exist")
    return True

def start_bot():
    """বট শুরু"""
    print("\n" + "="*50)
    print("🚀 STARTING DAILY EXAM DOSE BOT")
    print("="*50)
    
    try:
        import bot_main
        import asyncio
        
        asyncio.run(bot_main.main())
        return True
        
    except KeyboardInterrupt:
        print("\n👋 Bot stopped")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """মেইন ফাংশন"""
    print("="*60)
    print("🤖 DAILY EXAM DOSE - FINAL SETUP")
    print("="*60)
    
    # Step 1: Python check
    if not check_python():
        return
    
    # Step 2: Install requirements
    if not install_requirements():
        return
    
    # Step 3: Config check
    if not check_config():
        return
    
    # Step 4: Generate data
    if not generate_data():
        return
    
    # Step 5: Start bot
    start_bot()

if __name__ == "__main__":
    main()