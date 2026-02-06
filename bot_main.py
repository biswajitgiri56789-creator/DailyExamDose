"""
🤖 MAIN TELEGRAM BOT - RUNS 24/7 FOREVER
Posts educational questions every 30 minutes
"""

import asyncio
import time
import json
import os
import sys
import random
from datetime import datetime
from telegram import Bot
from telegram.error import TelegramError, RetryAfter
import logging

# লগিং সেটআপ
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# কনফিগারেশন লোড
try:
    from config import *
except ImportError as e:
    logger.error(f"❌ Config file error: {e}")
    sys.exit(1)

class DailyExamDoseBot:
    def __init__(self):
        self.bot = None
        self.running = True
        self.post_counter = 0
        self.error_counter = 0
        self.start_time = datetime.now()
        
        # ডাটা লোড
        self.data = self.load_all_data()
        
        # পরিসংখ্যান
        self.stats = self.calculate_statistics()
        
        logger.info("🤖 Daily Exam Dose Bot initialized!")
    
    def load_all_data(self):
        """সকল ডাটা ফাইল লোড"""
        data = {}
        
        for class_key, class_info in CLASSES.items():
            file_path = class_info['file']
            
            if os.path.exists(file_path):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data[class_key] = json.load(f)
                    logger.info(f"✅ Loaded: {class_info['name']}")
                except Exception as e:
                    logger.error(f"❌ Error loading {file_path}: {e}")
                    data[class_key] = {}
            else:
                logger.warning(f"⚠️ File not found: {file_path}")
                data[class_key] = {}
        
        return data
    
    def calculate_statistics(self):
        """পরিসংখ্যান ক্যালকুলেট"""
        stats = {
            "total_questions": 0,
            "unposted_questions": 0,
            "posted_questions": 0,
            "by_class": {}
        }
        
        for class_key, class_data in self.data.items():
            class_stats = {"subjects": 0, "questions": 0, "unposted": 0}
            
            for subject, chapters in class_data.items():
                class_stats["subjects"] += 1
                for chapter, chapter_data in chapters.items():
                    questions = chapter_data.get("questions", [])
                    class_stats["questions"] += len(questions)
                    stats["total_questions"] += len(questions)
                    
                    if not chapter_data.get("posted", False):
                        class_stats["unposted"] += len(questions)
                        stats["unposted_questions"] += len(questions)
                    else:
                        stats["posted_questions"] += len(questions)
            
            stats["by_class"][class_key] = class_stats
        
        return stats
    
    def find_unposted_questions(self):
        """পোস্ট করা হয়নি এমন প্রশ্ন খোঁজা"""
        selected = {}
        
        for class_key, class_info in CLASSES.items():
            class_data = self.data.get(class_key, {})
            
            if not class_data:
                continue
            
            # আনপোস্টেড সাবজেক্ট ও চ্যাপ্টার খোঁজা
            unposted_items = []
            
            for subject, chapters in class_data.items():
                for chapter, chapter_data in chapters.items():
                    if not chapter_data.get("posted", False):
                        questions = chapter_data.get("questions", [])
                        if questions:
                            unposted_items.append({
                                "subject": subject,
                                "chapter": chapter,
                                "data": chapter_data
                            })
            
            if unposted_items:
                # র‍্যান্ডম একটি আইটেম নির্বাচন
                item = random.choice(unposted_items)
                
                # র‍্যান্ডম একটি প্রশ্ন নির্বাচন
                question = random.choice(item["data"]["questions"])
                
                # র‍্যান্ডম সাজেশন
                suggestion = random.choice(item["data"]["suggestions"])
                
                selected[class_key] = {
                    "class_name": class_info["name"],
                    "subject": item["subject"],
                    "chapter": item["chapter"],
                    "question": question,
                    "suggestion": suggestion,
                    "chapter_data": item["data"]
                }
        
        return selected if selected else None
    
    def create_telegram_post(self, questions_data):
        """টেলিগ্রাম পোস্ট তৈরি"""
        if not questions_data:
            return None
        
        post_lines = []
        
        # হেডার
        post_lines.append("📚 **ডেইলি এক্সাম ডোজ** 📚")
        post_lines.append("━━━━━━━━━━━━━━━━━━━━")
        post_lines.append("")
        
        # প্রতিটি ক্লাসের প্রশ্ন
        for class_key, q_data in questions_data.items():
            post_lines.append(q_data["class_name"])
            post_lines.append(f"📘 **সাবজেক্ট:** {q_data['subject']}")
            post_lines.append(f"📖 **চ্যাপ্টার:** {q_data['chapter']}")
            post_lines.append("")
            post_lines.append(f"❓ **প্রশ্ন:** {q_data['question']}")
            post_lines.append("")
            post_lines.append(f"💡 **সাজেশন:** {q_data['suggestion']}")
            post_lines.append("")
            post_lines.append("━━━━━━━━━━━━━━━━━━━━")
            post_lines.append("")
        
        # ফুটার
        current_time = datetime.now().strftime("%I:%M %p")
        current_date = datetime.now().strftime("%d/%m/%Y")
        
        post_lines.append(f"⏰ **সময়:** {current_time}")
        post_lines.append(f"📅 **তারিখ:** {current_date}")
        post_lines.append(f"📊 **পোস্ট নং:** #{self.post_counter + 1}")
        
        # হ্যাশট্যাগ
        hashtags = [
            "#DailyExamDose",
            "#StudyMaterial", 
            "#ExamPreparation",
            "#Education",
            "#StudentHelp"
        ]
        post_lines.append(" ".join(hashtags))
        
        return "\n".join(post_lines)
    
    def mark_as_posted(self, questions_data):
        """প্রশ্ন পোস্ট করা হয়েছে মার্ক করা"""
        for class_key, q_data in questions_data.items():
            if class_key in self.data:
                subject = q_data["subject"]
                chapter = q_data["chapter"]
                
                if subject in self.data[class_key] and chapter in self.data[class_key][subject]:
                    self.data[class_key][subject][chapter]["posted"] = True
                    self.data[class_key][subject][chapter]["post_count"] = \
                        self.data[class_key][subject][chapter].get("post_count", 0) + 1
        
        # পরিসংখ্যান আপডেট
        self.stats = self.calculate_statistics()
    
    def save_all_data(self):
        """ডাটা সেভ"""
        for class_key, class_info in CLASSES.items():
            if class_key in self.data:
                file_path = class_info['file']
                try:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        json.dump(self.data[class_key], f, ensure_ascii=False, indent=2)
                except Exception as e:
                    logger.error(f"❌ Error saving {file_path}: {e}")
    
    async def send_to_channel(self, post_text):
        """টেলিগ্রাম চ্যানেলে পাঠানো"""
        if not self.bot:
            try:
                self.bot = Bot(token=BOT_TOKEN)
            except Exception as e:
                logger.error(f"❌ Bot initialization failed: {e}")
                return False
        
        max_retries = 3
        
        for attempt in range(max_retries):
            try:
                await self.bot.send_message(
                    chat_id=CHANNEL_USERNAME,
                    text=post_text,
                    parse_mode='Markdown',
                    disable_web_page_preview=True
                )
                return True
                
            except RetryAfter as e:
                wait_time = e.retry_after
                logger.warning(f"⏳ Rate limit, waiting {wait_time} seconds...")
                await asyncio.sleep(wait_time)
                
            except TelegramError as e:
                logger.warning(f"⚠️ Telegram error (attempt {attempt+1}/{max_retries}): {e}")
                await asyncio.sleep(10)
                
            except Exception as e:
                logger.error(f"❌ Unexpected error: {e}")
                self.error_counter += 1
                await asyncio.sleep(30)
        
        return False
    
    async def make_post(self):
        """একটি পোস্ট তৈরি ও পাঠানো"""
        logger.info(f"🔄 Preparing post #{self.post_counter + 1}...")
        
        # আনপোস্টেড প্রশ্ন খোঁজা
        questions_data = self.find_unposted_questions()
        
        if not questions_data:
            logger.warning("⚠️ No unposted questions found!")
            
            # নতুন প্রশ্ন জেনারেট করার চেষ্টা
            if self.stats["unposted_questions"] < AUTO_GENERATE_WHEN_LOW:
                logger.info("🔄 Generating more questions...")
                self.generate_more_questions()
                questions_data = self.find_unposted_questions()
            
            if not questions_data:
                logger.error("❌ Still no questions found!")
                return False
        
        # পোস্ট টেক্সট তৈরি
        post_text = self.create_telegram_post(questions_data)
        
        if not post_text:
            logger.error("❌ Failed to create post text")
            return False
        
        # টেলিগ্রামে পাঠানো
        logger.info("📤 Sending to Telegram...")
        success = await self.send_to_channel(post_text)
        
        if success:
            # মার্ক করা
            self.mark_as_posted(questions_data)
            
            self.post_counter += 1
            self.error_counter = 0
            
            # প্রতি ১০ পোস্টে ডাটা সেভ
            if self.post_counter % 10 == 0:
                self.save_all_data()
                self.log_statistics()
            
            logger.info(f"✅ Post #{self.post_counter} sent successfully!")
            return True
        else:
            logger.error("❌ Failed to send post")
            self.error_counter += 1
            return False
    
    def generate_more_questions(self):
        """আরো প্রশ্ন জেনারেট"""
        try:
            # data_generator ইম্পোর্ট
            import data_generator as gen
            generator = gen.QuestionGenerator()
            
            # প্রতিটি ক্লাসে নতুন প্রশ্ন যোগ
            for class_key, class_info in CLASSES.items():
                if class_key in self.data:
                    for subject in class_info['subjects'][:5]:  # প্রথম ৫টি সাবজেক্ট
                        if subject not in self.data[class_key]:
                            self.data[class_key][subject] = {}
                        
                        # নতুন চ্যাপ্টার সংখ্যা
                        existing_chapters = len(self.data[class_key][subject])
                        new_chapter_num = existing_chapters + 1
                        
                        # নতুন চ্যাপ্টার তৈরি
                        chapter_name = f"চ্যাপ্টার {new_chapter_num}: নতুন গুরুত্বপূর্ণ অংশ"
                        
                        # ১০টি নতুন প্রশ্ন
                        new_questions = []
                        for i in range(1, 11):
                            if "college" in class_key:
                                template = random.choice(generator.templates_english)
                                question = template.format(topic=f"{subject} New Topic {i}")
                            else:
                                template = random.choice(generator.templates_bangla)
                                question = template.format(topic=f"{subject} - নতুন টপিক {i}")
                            new_questions.append(question)
                        
                        # সাজেশন
                        suggestions = random.sample(generator.suggestions, 3)
                        
                        self.data[class_key][subject][chapter_name] = {
                            "questions": new_questions,
                            "suggestions": suggestions,
                            "posted": False,
                            "post_count": 0,
                            "created_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        }
            
            logger.info("✅ Generated additional questions")
            self.save_all_data()
            self.stats = self.calculate_statistics()
            
        except Exception as e:
            logger.error(f"❌ Error generating questions: {e}")
    
    def log_statistics(self):
        """পরিসংখ্যান লগ"""
        uptime = datetime.now() - self.start_time
        days = uptime.days
        hours = uptime.seconds // 3600
        
        stats = {
            "total_posts": self.post_counter,
            "uptime": f"{days}d {hours}h",
            "total_questions": self.stats["total_questions"],
            "unposted_questions": self.stats["unposted_questions"],
            "error_count": self.error_counter,
            "last_update": datetime.now().isoformat()
        }
        
        logger.info(f"📊 Statistics: {stats}")
        
        # ফাইলে সেভ
        with open("bot_stats.json", "w", encoding="utf-8") as f:
            json.dump(stats, f, indent=2, ensure_ascii=False)
    
    def show_banner(self):
        """স্টার্টআপ ব্যানার"""
        print("\n" + "="*60)
        print("🚀 DAILY EXAM DOSE BOT - 24/7 FOREVER")
        print("="*60)
        print(f"📢 Channel: {CHANNEL_USERNAME}")
        print(f"⏰ Post Interval: {POST_EVERY_MINUTES} minutes")
        print(f"📅 Started: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"📊 Questions: {self.stats['total_questions']:,} total")
        print(f"📈 Unposted: {self.stats['unposted_questions']:,} remaining")
        print("="*60)
        print("🔄 Bot is running... (Ctrl+C to stop)")
        print()
    
    async def run_forever(self):
        """২৪/৭ চলমান লুপ"""
        self.show_banner()
        
        last_post_time = time.time()
        
        while self.running:
            try:
                current_time = time.time()
                elapsed = current_time - last_post_time
                
                # যদি পোস্ট করার সময় হয়ে যায়
                if elapsed >= (POST_EVERY_MINUTES * 60):
                    success = await self.make_post()
                    
                    if success:
                        last_post_time = current_time
                    else:
                        logger.warning("⚠️ Post failed, waiting 5 minutes...")
                        await asyncio.sleep(300)  # 5 minutes
                
                # স্ট্যাটাস বার
                remaining = int((POST_EVERY_MINUTES * 60) - elapsed)
                mins = remaining // 60
                secs = remaining % 60
                
                print(f"⏳ Next post: {mins:02d}:{secs:02d} | Posts: {self.post_counter} | Errors: {self.error_counter}", end="\r")
                
                # 1 সেকেন্ড অপেক্ষা
                await asyncio.sleep(1)
                
            except KeyboardInterrupt:
                print("\n\n🛑 Stopping bot...")
                self.running = False
                
            except Exception as e:
                logger.error(f"⚠️ Main loop error: {e}")
                self.error_counter += 1
                
                if self.error_counter > MAX_ERRORS:
                    logger.error("🚨 Too many errors, stopping...")
                    break
                
                await asyncio.sleep(SLEEP_ON_ERROR)
        
        # ক্লিনআপ
        self.cleanup()
    
    def cleanup(self):
        """ক্লিনআপ"""
        logger.info("🧹 Cleaning up...")
        
        # শেষ ডাটা সেভ
        self.save_all_data()
        
        # ফাইনাল লগ
        uptime = datetime.now() - self.start_time
        days = uptime.days
        hours = uptime.seconds // 3600
        
        logger.info(f"👋 Bot stopped after {days} days {hours} hours")
        logger.info(f"📊 Total posts made: {self.post_counter}")

# মেইন ফাংশন
async def main():
    """প্রোগ্রাম এন্ট্রি পয়েন্ট"""
    
    # বট টোকেন চেক
    if "YOUR_BOT_TOKEN_HERE" in BOT_TOKEN:
        print("❌❌❌ ERROR: Bot token not set!")
        print("Please edit config.py and set your BOT_TOKEN")
        print("Get token from: @BotFather on Telegram")
        return
    
    # ডাটা ফোল্ডার চেক
    if not os.path.exists("data"):
        print("📁 Creating data folder...")
        os.makedirs("data")
    
    # ডাটা ফাইল চেক
    data_files_exist = all(os.path.exists(info['file']) for _, info in CLASSES.items())
    
    if not data_files_exist:
        print("📝 Data files not found!")
        print("Run: python data_generator.py to generate questions")
        
        # অটো জেনারেট করার চেষ্টা
        try:
            import data_generator
            print("🔄 Auto-generating data...")
            generator = data_generator.QuestionGenerator()
            generator.generate_all()
            print("✅ Data generated successfully!")
        except Exception as e:
            print(f"❌ Error generating data: {e}")
            return
    
    # বট শুরু
    bot = DailyExamDoseBot()
    
    try:
        await bot.run_forever()
    except KeyboardInterrupt:
        print("\n👋 Bot stopped by user")
    except Exception as e:
        print(f"\n❌ Critical error: {e}")

if __name__ == "__main__":
    asyncio.run(main())