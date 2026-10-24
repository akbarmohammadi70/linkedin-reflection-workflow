
import json
import os
import re

from dotenv import load_dotenv
from openai import OpenAI


# ==========================================
# API Configuration
# ==========================================

load_dotenv()

BASE_URL = "https://openrouter.ai/api/v1"
API_KEY = os.getenv("OPENROUTER_API_KEY")
DEFAULT_MODEL = os.getenv(
    "OPENROUTER_MODEL",
    "openai/gpt-4o-mini",
)

if not API_KEY:
    raise ValueError(
        "OPENROUTER_API_KEY was not found in the .env file."
    )

client = OpenAI(
    base_url=BASE_URL,
    api_key=API_KEY,
)


# ==========================================
# Part 1: Basic Reflection Workflow
# ==========================================

def generate_draft(
    topic,
    tone="حرفه‌ای",
    model="openai/gpt-4o-mini",
):
    """Generate an initial Persian LinkedIn post."""

    prompt = f"""
    یک پست فارسی برای شبکه اجتماعی لینکدین بنویس.

    موضوع: {topic}
    لحن: {tone}

    الزامات:
    1. حداکثر 300 کاراکتر، با احتساب فاصله‌ها و هشتگ‌ها.
    2. بین 3 تا 5 هشتگ مرتبط داشته باشد.
    3. متن حرفه‌ای، روان و جذاب باشد.
    4. محتوای پست با موضوع داده‌شده مرتبط باشد.
    5. فقط متن پست را برگردان و توضیح اضافی ننویس.
    """

    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": (
                    "تو یک نویسنده حرفه‌ای محتوای فارسی لینکدین هستی."
                ),
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        temperature=1.0,
    )

    return response.choices[0].message.content.strip()


def reflect_on_draft(
    topic,
    draft,
    tone="حرفه‌ای",
    model="openai/gpt-4o-mini",
):
    """Critique a draft without external quality signals."""

    prompt = f"""
    پیش‌نویس زیر را برای انتشار در لینکدین نقد کن.

    موضوع: {topic}
    لحن موردنظر: {tone}

    پیش‌نویس:
    {draft}

    معیارهای نقد:
    1. ارتباط متن با موضوع
    2. کیفیت نگارش و جذابیت
    3. تناسب لحن با لینکدین
    4. رعایت حداکثر 300 کاراکتر
    5. داشتن 3 تا 5 هشتگ

    نقاط ضعف را مشخص کن و پیشنهادهای عملی برای اصلاح ارائه بده.
    اگر محدودیت طول یا تعداد هشتگ‌ها رعایت نشده است،
    به آن اشاره کن.

    فقط بازخورد را بنویس؛ نسخه نهایی را تولید نکن.
    """

    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": (
                    "تو یک ویراستار دقیق محتوای فارسی لینکدین هستی."
                ),
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        temperature=1.0,
    )

    return response.choices[0].message.content.strip()


def revise_draft(
    topic,
    draft,
    feedback,
    tone="حرفه‌ای",
    model="openai/gpt-4o-mini",
):
    """Revise the draft using reflection feedback."""

    prompt = f"""
    پست لینکدین زیر را بر اساس بازخورد ارائه‌شده اصلاح کن.

    موضوع: {topic}
    لحن: {tone}

    پیش‌نویس اولیه:
    {draft}

    بازخورد:
    {feedback}

    الزامات نسخه نهایی:
    1. حداکثر 300 کاراکتر با احتساب فاصله‌ها و هشتگ‌ها.
    2. بین 3 تا 5 هشتگ مرتبط.
    3. نگارش روان، حرفه‌ای و متناسب با لینکدین.
    4. حفظ پیام اصلی و اصلاح نقاط ضعف.

    فقط نسخه نهایی پست را برگردان.
    """

    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": (
                    "تو یک ویراستار حرفه‌ای محتوای فارسی هستی."
                ),
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        temperature=1.0,
    )

    return response.choices[0].message.content.strip()


def run_linkedin_workflow(
    topic,
    tone="حرفه‌ای",
    model="openai/gpt-4o-mini",
):
    """Run generation, reflection, and revision in sequence."""

    draft = generate_draft(
        topic=topic,
        tone=tone,
        model=model,
    )

    feedback = reflect_on_draft(
        topic=topic,
        draft=draft,
        tone=tone,
        model=model,
    )

    final_post = revise_draft(
        topic=topic,
        draft=draft,
        feedback=feedback,
        tone=tone,
        model=model,
    )

    return {
        "topic": topic,
        "draft": draft,
        "feedback": feedback,
        "final_post": final_post,
    }


# ==========================================
# Part 2: External Feedback
# ==========================================

def check_post_quality(
    post_text,
    max_length=300,
    min_hashtags=3,
    max_hashtags=5,
):
    """Evaluate post length and hashtag count without an LLM."""

    length = len(post_text)

    # Count hashtag tokens beginning with #.
    hashtags = re.findall(r"(?<!\w)#\w+", post_text)
    hashtag_count = len(hashtags)

    return {
        "length": length,
        "within_length_limit": length <= max_length,
        "hashtag_count": hashtag_count,
        "within_hashtag_range": (
            min_hashtags <= hashtag_count <= max_hashtags
        ),
    }


def reflect_on_draft_with_feedback(
    topic,
    draft,
    quality_signals,
    tone="حرفه‌ای",
    model="openai/gpt-4o-mini",
):
    """Critique a draft using externally measured quality signals."""

    length = quality_signals["length"]
    within_length = quality_signals["within_length_limit"]
    hashtag_count = quality_signals["hashtag_count"]
    within_hashtags = quality_signals["within_hashtag_range"]

    length_status = (
        "رعایت شده است"
        if within_length
        else "رعایت نشده است"
    )

    hashtag_status = (
        "رعایت شده است"
        if within_hashtags
        else "رعایت نشده است"
    )

    quality_report = f"""
    نتایج ارزیابی خودکار پست:

    - طول پست: {length} کاراکتر.
    - حداکثر طول مجاز: 300 کاراکتر.
    - وضعیت محدودیت طول: {length_status}.
    - تعداد هشتگ‌ها: {hashtag_count}.
    - محدوده مجاز هشتگ‌ها: 3 تا 5.
    - وضعیت محدودیت هشتگ‌ها: {hashtag_status}.

    داده‌های خام:
    {json.dumps(quality_signals, ensure_ascii=False)}
    """

    prompt = f"""
    پیش‌نویس زیر را برای انتشار در لینکدین نقد کن.

    موضوع: {topic}
    لحن موردنظر: {tone}

    پیش‌نویس:
    {draft}

    {quality_report}

    نتایج ارزیابی خودکار را مبنا قرار بده.
    محدودیت‌های نقض‌شده را با اعداد دقیق مشخص کن.
    علاوه بر محدودیت‌ها، کیفیت نگارش، جذابیت و ارتباط متن
    با موضوع را نیز بررسی کن.

    پیشنهادهای عملی برای اصلاح ارائه بده.
    فقط بازخورد را بنویس و نسخه نهایی را تولید نکن.
    """

    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": (
                    "تو یک ویراستار دقیق محتوای فارسی لینکدین هستی."
                ),
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        temperature=1.0,
    )

    return response.choices[0].message.content.strip()


# ==========================================
# Display Results
# ==========================================

def print_workflow_result(result):
    """Display the initial draft, feedback, and final post."""

    print("\n" + "=" * 70)
    print(f"موضوع: {result['topic']}")
    print("=" * 70)

    print("\n[پیش‌نویس اولیه]")
    print(result["draft"])

    print("\n[بازخورد]")
    print(result["feedback"])

    print("\n[نسخه نهایی]")
    print(result["final_post"])

    print("\n[ارزیابی کیفیت نسخه نهایی]")

    signals = check_post_quality(result["final_post"])

    print(
        json.dumps(
            signals,
            ensure_ascii=False,
            indent=4,
        )
    )


# ==========================================
# Main Execution
# ==========================================

def main():
    model = DEFAULT_MODEL

    # Test the workflow with two different topics.
    topics = [
        "معرفی یک دوره آموزشی جدید درباره هوش مصنوعی و ساخت AI Agent",
        "اعلام یک دستاورد کاری در بهبود استقرار نرم‌افزار "
        "با Kubernetes و CI/CD",
    ]

    for topic in topics:
        result = run_linkedin_workflow(
            topic=topic,
            tone="حرفه‌ای",
            model=model,
        )

        print_workflow_result(result)

    # Compare reflection with and without external feedback.
    print("\n" + "=" * 70)
    print("مقایسه بازخورد معمولی با بازخورد بیرونی")
    print("=" * 70)

    bad_post = (
        "امروز تجربه جدیدی در زمینه اتوماسیون زیرساخت و بهبود "
        "فرآیندهای استقرار نرم‌افزار به دست آوردم. "
        "یادگیری مستمر و به‌اشتراک‌گذاری تجربه‌ها به رشد "
        "حرفه‌ای کمک می‌کند."
    )

    topic = "بهبود فرآیندهای استقرار نرم‌افزار"

    # Measure the post using Python rules.
    quality_signals = check_post_quality(bad_post)

    print("\n[پست نمونه]")
    print(bad_post)

    print("\n[سیگنال‌های کیفیت]")
    print(
        json.dumps(
            quality_signals,
            ensure_ascii=False,
            indent=4,
        )
    )

    # Run reflection without external quality signals.
    ordinary_feedback = reflect_on_draft(
        topic=topic,
        draft=bad_post,
        tone="حرفه‌ای",
        model=model,
    )

    print("\n[بازخورد بدون سیگنال بیرونی]")
    print(ordinary_feedback)

    # Run reflection with external quality signals.
    external_feedback = reflect_on_draft_with_feedback(
        topic=topic,
        draft=bad_post,
        quality_signals=quality_signals,
        tone="حرفه‌ای",
        model=model,
    )

    print("\n[بازخورد با سیگنال بیرونی]")
    print(external_feedback)


if __name__ == "__main__":
    main()
