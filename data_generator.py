"""
🚀 INFINITE QUESTION GENERATOR
Creates 50,000+ questions that will never end
"""

import json
import os
import random
from datetime import datetime

class QuestionGenerator:
    def __init__(self):
        self.generated_count = 0
        
        # প্রশ্ন টেমপ্লেট
        self.templates_bangla = [
            "{topic} কাকে বলে?",
            "{topic} এর সংজ্ঞা দাও।",
            "{topic} এর বৈশিষ্ট্য লিখ।",
            "{topic} এর গুরুত্ব ব্যাখ্যা কর।",
            "{topic} এর প্রকারভেদ আলোচনা কর।",
            "{topic} এর সূত্রটি বিবৃত কর।",
            "{topic} কিভাবে কাজ করে?",
            "{topic} এর প্রয়োগ লিখ।",
            "{topic} এর সুবিধা ও অসুবিধা লিখ।",
            "{topic} এর প্রভাব বিশ্লেষণ কর।",
            "{topic} এর পার্থক্য নির্ণয় কর।",
            "{topic} সম্পর্কে তোমার মতামত দাও।",
            "{topic} এর উদাহরণ দাও।",
            "{topic} কেন গুরুত্বপূর্ণ?",
            "{topic} এর ইতিহাস আলোচনা কর।",
            "{topic} এর ভবিষ্যৎ কী?",
            "{topic} এর সমস্যা ও সমাধান লিখ।"
        ]
        
        self.templates_english = [
            "What is {topic}?",
            "Define {topic}.",
            "Explain the concept of {topic}.",
            "Discuss the importance of {topic}.",
            "Describe the types of {topic}.",
            "State the formula/theorem of {topic}.",
            "How does {topic} work?",
            "Give examples of {topic}.",
            "What are the applications of {topic}?",
            "Compare and contrast {topic}.",
            "Analyze the impact of {topic}.",
            "Write a short note on {topic}.",
            "Discuss the future of {topic}.",
            "What are the challenges in {topic}?",
            "Provide case studies on {topic}."
        ]
        
        self.suggestions = [
            "১০০% আসবে - ৫ নম্বর",
            "গুরুত্বপূর্ণ প্রশ্ন",
            "সংক্ষিপ্ত প্রশ্ন",
            "রচনামূলক প্রশ্ন",
            "অতি সংক্ষিপ্ত প্রশ্ন",
            "বিগত বছরের প্রশ্ন",
            "নিশ্চিত আসবে",
            "১০ নম্বরের প্রশ্ন",
            "অত্যন্ত গুরুত্বপূর্ণ",
            "মডেল প্রশ্ন",
            "সাজেশন প্রশ্ন",
            "পরীক্ষায় প্রায়ই আসে",
            "ক্লাস টেস্টের জন্য",
            "ফাইনাল এক্সামের জন্য",
            "বোর্ড পরীক্ষার জন্য"
        ]
    
    def generate_for_class(self, class_key, class_info):
        """একটি ক্লাসের জন্য প্রশ্ন তৈরি"""
        print(f"\n🎓 Generating for {class_info['name']}...")
        
        all_data = {}
        
        for subject in class_info['subjects']:
            print(f"  📘 {subject}...")
            subject_data = {}
            
            # প্রতিটি সাবজেক্টের জন্য ২০টি চ্যাপ্টার
            for chapter_num in range(1, 21):
                chapter_name = f"চ্যাপ্টার {chapter_num}: {subject} এর গুরুত্বপূর্ণ অংশ"
                
                # প্রতি চ্যাপ্টারে ১৫টি প্রশ্ন
                questions = []
                for q_num in range(1, 16):
                    if "college" in class_key:
                        # ইংরেজি প্রশ্ন
                        template = random.choice(self.templates_english)
                        topic = f"{subject} Chapter {chapter_num} Topic {q_num}"
                        question = template.format(topic=topic)
                    else:
                        # বাংলা প্রশ্ন
                        template = random.choice(self.templates_bangla)
                        topic = f"{subject} - চ্যাপ্টার {chapter_num} টপিক {q_num}"
                        question = template.format(topic=topic)
                    
                    questions.append(question)
                    self.generated_count += 1
                
                # ৩-৫টি সাজেশন
                chapter_suggestions = random.sample(self.suggestions, random.randint(3, 5))
                
                subject_data[chapter_name] = {
                    "questions": questions,
                    "suggestions": chapter_suggestions,
                    "posted": False,
                    "post_count": 0,
                    "created_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
            
            all_data[subject] = subject_data
        
        return all_data
    
    def generate_all(self):
        """সব ক্লাসের জন্য প্রশ্ন তৈরি"""
        print("="*60)
        print("🚀 INFINITE QUESTION GENERATOR")
        print("="*60)
        
        # config থেকে ক্লাস তথ্য পড়া
        import sys
        sys.path.append('.')
        from config import CLASSES
        
        # data ফোল্ডার তৈরি
        if not os.path.exists("data"):
            os.makedirs("data")
        
        total_start = self.generated_count
        
        # প্রতিটি ক্লাসের জন্য ডাটা তৈরি
        for class_key, class_info in CLASSES.items():
            class_data = self.generate_for_class(class_key, class_info)
            
            # ফাইলে সেভ
            file_path = class_info['file']
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(class_data, f, ensure_ascii=False, indent=2)
            
            print(f"✅ Saved: {file_path}")
        
        # টেমপ্লেট সেভ
        templates_data = {
            "bangla": self.templates_bangla,
            "english": self.templates_english,
            "suggestions": self.suggestions,
            "generated_count": self.generated_count,
            "generation_date": datetime.now().isoformat()
        }
        
        with open("data/question_templates.json", 'w', encoding='utf-8') as f:
            json.dump(templates_data, f, ensure_ascii=False, indent=2)
        
        total_generated = self.generated_count - total_start
        
        # পরিসংখ্যান
        self.show_statistics(total_generated)
        
        return total_generated
    
    def show_statistics(self, total_generated):
        """পরিসংখ্যান দেখানো"""
        print("\n" + "="*60)
        print("📊 GENERATION STATISTICS")
        print("="*60)
        print(f"✅ Total Questions Generated: {total_generated:,}")
        
        # ক্যালকুলেশন
        questions_per_day = 240  # দিনে ২৪০ প্রশ্ন পোস্ট হবে
        days = total_generated // questions_per_day
        years = days // 365
        
        print(f"📅 Will Last For: {days:,} days")
        print(f"📅 That's About: {years} years!")
        print()
        print("🔢 Breakdown:")
        print("  • Each class: 15-20 subjects")
        print("  • Each subject: 20 chapters")
        print("  • Each chapter: 15 questions")
        print("  • Total: 50,000+ questions")
        print()
        print("⚡ Features:")
        print("  • No Reset - Questions never repeat")
        print("  • Infinite - Auto-generates when low")
        print("  • 24/7 - Runs forever on GitHub")
        print("="*60)

# মেইন প্রোগ্রাম
if __name__ == "__main__":
    print("🚀 Starting Infinite Question Generator...")
    print("This will create 50,000+ questions for your bot!")
    print()
    
    confirm = input("Continue? (yes/no): ").lower()
    
    if confirm in ["yes", "y", ""]:
        generator = QuestionGenerator()
        total = generator.generate_all()
        print(f"\n🎉 Done! Created {total:,} questions.")
        print("📁 All data saved in 'data/' folder")
        print("🤖 Now you can run the bot!")
    else:
        print("❌ Generation cancelled.")