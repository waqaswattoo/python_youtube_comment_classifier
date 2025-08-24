# STEP 1: Install required libraries
!pip install youtube-comment-downloader matplotlib --quiet

# STEP 2: Import libraries
import re
from youtube_comment_downloader import YoutubeCommentDownloader
import matplotlib.pyplot as plt

# STEP 3: Input YouTube video URL
video_url = input("🔗 Enter YouTube video URL: ")

# STEP 4: Extract Video ID from URL
def extract_video_id(url):
    if "watch?v=" in url:
        return url.split("watch?v=")[-1].split("&")[0]
    elif "youtu.be/" in url:
        return url.split("youtu.be/")[-1].split("?")[0]
    else:
        raise ValueError("❌ Invalid YouTube URL format")

video_id = extract_video_id(video_url)

# STEP 5: Define function to check if a comment is Islamic
def is_islamic_comment(comment):
    comment = comment.lower()
    islamic_keywords = [
        # English
        "allah", "muhammad", "prophet", "islam", "quran", "hadith", "sunnah", "masjid", "mosque",
        "dua", "duaa", "ramadan", "hijab", "halal", "haram", "jannah", "hellfire", "judgment day",
        "zakat", "sadaqah", "sharia", "prayer", "namaz", "fasting", "eid", "imam", "taqwa", "deen","Alhumdlillah",
        "ibadah", "hajj", "umrah", "surah", "verse", "kalima", "salah", "sawm", "tilawat", "adhan","Alhumdlillah","Musalman",

        # Urdu / Roman Urdu
        "اللّٰہ", "الله", "رسول", "محمد", "قرآن", "حدیث", "اسلام", "مسلمان", "نیکی", "گناہ", "عبادت",
        "نماز", "روزہ", "حج", "عمرہ", "صدقہ", "ذکر", "توبہ", "آخرت", "قبر", "قیامت", "سچ", "جنت", "دوزخ",
        "استغفار", "مغفرت", "صبر", "رحمت", "رحمن", "برکت", "اعمال", "درود", "طہارت", "تہجد", "سورۃ", "آیت"," آپ ﷺ","اللہ تعالیٰ",

        # Arabic
        "الله", "محمد", "القرآن", "السنة", "الدعاء", "الصلاة", "الزكاة", "الحج", "الصيام",
        "سبحان الله", "الحمد لله", "الله أكبر", "لا إله إلا الله", "استغفر الله", "رضي الله عنه",
        "بسم الله", "إن شاء الله", "ما شاء الله", "اللهم صل على محمد", "غفر الله", "جنة", "نار","اللہ تعالیٰ","آمین",
    ]
    return any(re.search(rf"\b{re.escape(word)}\b", comment) for word in islamic_keywords)

# STEP 6: Download and classify comments
print("📥 Downloading and classifying YouTube comments...")
downloader = YoutubeCommentDownloader()

islamic_comments = []
non_islamic_comments = []
total_count = 0

try:
    for comment in downloader.get_comments_from_url(f"https://www.youtube.com/watch?v={video_id}", sort_by=0):
        text = comment['text']
        if is_islamic_comment(text):
            islamic_comments.append(text)
        else:
            non_islamic_comments.append(text)
        total_count += 1
except Exception as e:
    print(f"⚠️ Download stopped after {total_count} comments due to error: {e}")

# STEP 7: Show summary
print(f"\n✅ Total comments processed: {total_count}")
print(f"🟩 Islamic comments: {len(islamic_comments)}")
print(f"🟥 Non-Islamic comments: {len(non_islamic_comments)}")

# STEP 8: Plot bar chart
plt.figure(figsize=(8, 5))
categories = ['Islamic', 'Non-Islamic']
counts = [len(islamic_comments), len(non_islamic_comments)]
colors = ['green', 'red']

plt.bar(categories, counts, color=colors)
plt.title('YouTube Comment Classification')
plt.xlabel('Comment Category')
plt.ylabel('Number of Comments')
plt.grid(axis='y', linestyle='--', alpha=0.6)
plt.tight_layout()
plt.show()

# STEP 9: Display Islamic Comments
print("\n🟢 Islamic Comments:\n")
for i, c in enumerate(islamic_comments, 1):
    print(f"{i}. {c}")

# STEP 10: Display Non-Islamic Comments
print("\n🔴 Non-Islamic Comments:\n")
for i, c in enumerate(non_islamic_comments, 1):
    print(f"{i}. {c}")
