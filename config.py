"""
🎯 FINAL CONFIGURATION FILE
SET YOUR BOT TOKEN AND CHANNEL HERE
"""

# ==================== TELEGRAM SETTINGS ====================
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"  # Step 6-এ বসাবেন
CHANNEL_USERNAME = "@Daily_ExamDose"  # আপনার চ্যানেলের ইউজারনেম

# ==================== POSTING SETTINGS ====================
POST_EVERY_MINUTES = 30  # প্রতি 30 মিনিট পর পর পোস্ট করবে
NO_RESET_SYSTEM = True   # কখনো প্রশ্ন রিসেট হবে না
RUN_FOREVER = True       # বছর বছর চলবে

# ==================== CLASS SETTINGS ====================
CLASSES = {
    "11": {
        "name": "ক্লাস ১১",
        "file": "data/class_11.json",
        "subjects": [
            "পদার্থবিজ্ঞান", "রসায়ন", "জীববিজ্ঞান", "গণিত", "উচ্চতর গণিত",
            "ইংরেজি", "বাংলা", "ইতিহাস", "ভূগোল", "পৌরনীতি",
            "অর্থনীতি", "যুক্তিবিদ্যা", "সমাজবিজ্ঞান", "মনোবিজ্ঞান", "কৃষিশিক্ষা",
            "শারীরিক শিক্ষা", "চারু ও কারুকলা", "তথ্য ও যোগাযোগ প্রযুক্তি"
        ]
    },
    "12": {
        "name": "ক্লাস ১২",
        "file": "data/class_12.json",
        "subjects": [
            "পদার্থবিজ্ঞান", "রসায়ন", "জীববিজ্ঞান", "গণিত", "উচ্চতর গণিত",
            "ইংরেজি", "বাংলা", "ইতিহাস", "ভূগোল", "পৌরনীতি",
            "অর্থনীতি", "যুক্তিবিদ্যা", "সমাজবিজ্ঞান", "মনোবিজ্ঞান", "কৃষিশিক্ষা",
            "হিসাববিজ্ঞান", "ব্যবসায় ব্যবস্থাপনা", "ফিন্যান্স, ব্যাংকিং ও বীমা"
        ]
    },
    "college_1": {
        "name": "কলেজ ১ম বর্ষ",
        "file": "data/college_1.json",
        "subjects": [
            "Accounting", "Management", "Marketing", "Finance", "Economics",
            "Statistics", "Mathematics", "English", "Bangla", "Physics",
            "Chemistry", "Biology", "Computer Science", "Psychology", "Sociology"
        ]
    },
    "college_2": {
        "name": "কলেজ ২য় বর্ষ",
        "file": "data/college_2.json",
        "subjects": [
            "Advanced Accounting", "Business Management", "Digital Marketing",
            "Investment Analysis", "Microeconomics", "Data Science", "Calculus",
            "Business English", "Advanced Bangla", "Programming", "Database",
            "Web Development", "Software Engineering", "Networking"
        ]
    },
    "college_3": {
        "name": "কলেজ ৩য় বর্ষ",
        "file": "data/college_3.json",
        "subjects": [
            "Corporate Finance", "Strategic Management", "International Marketing",
            "Banking & Insurance", "Macroeconomics", "Artificial Intelligence",
            "Machine Learning", "Advanced Mathematics", "Research Methodology",
            "Thesis Writing", "Project Management", "Entrepreneurship"
        ]
    }
}

# ==================== BOT SAFETY ====================
MAX_ERRORS = 100
SLEEP_ON_ERROR = 30
AUTO_GENERATE_WHEN_LOW = 1000  # যখন ১০০০ প্রশ্ন বাকি থাকে, নতুন জেনারেট করবে

print("✅ Config file loaded successfully!")