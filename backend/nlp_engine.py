"""
NLP Engine for English Learning Chatbot
Uses NLTK for free, offline natural language processing.
"""

import re
import random
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Ensure required NLTK data is available
for pkg in ["punkt", "stopwords", "wordnet", "averaged_perceptron_tagger", "punkt_tab"]:
    try:
        nltk.data.find(f"tokenizers/{pkg}" if "punkt" in pkg else f"corpora/{pkg}")
    except LookupError:
        nltk.download(pkg, quiet=True)

lemmatizer = WordNetLemmatizer()
try:
    STOP_WORDS = set(stopwords.words("english"))
except Exception:
    STOP_WORDS = set()

# ---------------------------------------------------------------------------
# Lesson content database
# ---------------------------------------------------------------------------

LESSONS = {
    "greetings": {
        "title": "Greetings & Introductions",
        "level": "Beginner",
        "content": """
**Greetings** are the first words we say when we meet someone.

**Formal Greetings:**
- Good morning (before 12 pm)
- Good afternoon (12 pm – 6 pm)
- Good evening (after 6 pm)
- How do you do? (very formal)

**Informal Greetings:**
- Hi! / Hello!
- Hey! (casual)
- What's up? (very casual)

**Introductions:**
- My name is ___.
- I am ___.
- Nice to meet you!
- Pleased to meet you.

**Practice:** Say "Hello, my name is [your name]. Nice to meet you!"
        """,
        "quiz": [
            {
                "question": "Which greeting is used before 12 noon?",
                "options": ["Good evening", "Good afternoon", "Good morning", "Good night"],
                "answer": "Good morning",
                "explanation": "'Good morning' is used as a greeting before noon (12 pm)."
            },
            {
                "question": "Which phrase means 'I am happy to meet you'?",
                "options": ["Good morning", "Nice to meet you", "What's up?", "How do you do?"],
                "answer": "Nice to meet you",
                "explanation": "'Nice to meet you' expresses happiness when meeting someone new."
            },
            {
                "question": "Fill in: 'My ___ is Priya.'",
                "options": ["name", "age", "school", "friend"],
                "answer": "name",
                "explanation": "We say 'My name is ___' when introducing ourselves."
            }
        ]
    },
    "alphabet": {
        "title": "The English Alphabet",
        "level": "Beginner",
        "content": """
The English alphabet has **26 letters**.

**Vowels (5):** A, E, I, O, U
**Consonants (21):** All remaining letters

**Uppercase:** A B C D E F G H I J K L M N O P Q R S T U V W X Y Z
**Lowercase:** a b c d e f g h i j k l m n o p q r s t u v w x y z

**Letter Names (A-Z):**
Ay, Bee, See, Dee, Ee, Eff, Jee, Aitch, Eye, Jay, Kay, El, Em, En, Oh, Pee, Cue, Arr, Ess, Tee, You, Vee, Double-you, Ex, Why, Zee

**Fun fact:** The word "alphabet" comes from the first two Greek letters: Alpha + Beta!
        """,
        "quiz": [
            {
                "question": "How many letters are in the English alphabet?",
                "options": ["24", "25", "26", "28"],
                "answer": "26",
                "explanation": "The English alphabet has exactly 26 letters."
            },
            {
                "question": "Which of these is a vowel?",
                "options": ["B", "C", "E", "F"],
                "answer": "E",
                "explanation": "The vowels in English are A, E, I, O, U."
            },
            {
                "question": "How many vowels are there in English?",
                "options": ["3", "4", "5", "6"],
                "answer": "5",
                "explanation": "There are 5 vowels: A, E, I, O, U."
            }
        ]
    },
    "numbers": {
        "title": "Numbers in English",
        "level": "Beginner",
        "content": """
**Cardinal Numbers (Counting):**
- 1 = one, 2 = two, 3 = three, 4 = four, 5 = five
- 6 = six, 7 = seven, 8 = eight, 9 = nine, 10 = ten
- 11 = eleven, 12 = twelve, 13 = thirteen
- 20 = twenty, 30 = thirty, 100 = one hundred

**Ordinal Numbers (Position/Order):**
- 1st = first, 2nd = second, 3rd = third
- 4th = fourth, 5th = fifth, 10th = tenth

**Useful Phrases:**
- "I have three books."
- "She is in the fifth standard."
- "There are twenty students in our class."
        """,
        "quiz": [
            {
                "question": "How do you say '12' in English?",
                "options": ["Twelve", "Twenty", "Eleven", "Thirteen"],
                "answer": "Twelve",
                "explanation": "12 is written as 'twelve' in English."
            },
            {
                "question": "What is the ordinal form of '3'?",
                "options": ["Three", "Threeth", "Third", "Thrid"],
                "answer": "Third",
                "explanation": "The ordinal form of 3 is 'third' (3rd)."
            },
            {
                "question": "How do you write '100' in words?",
                "options": ["Ten", "One thousand", "One hundred", "Ten hundred"],
                "answer": "One hundred",
                "explanation": "100 = one hundred."
            }
        ]
    },
    "colors": {
        "title": "Colors in English",
        "level": "Beginner",
        "content": """
**Primary Colors:**
- Red (लाल), Blue (नीला), Yellow (पीला)

**Common Colors:**
- Green (हरा), Orange (नारंगी), Purple (बैंगनी)
- White (सफेद), Black (काला), Brown (भूरा)
- Pink (गुलाबी), Grey/Gray (स्लेटी)

**Using Colors in Sentences:**
- The sky is **blue**.
- Grass is **green**.
- The sun is **yellow**.
- My school bag is **black**.

**Shades:**
- Light blue, Dark green, Bright red
        """,
        "quiz": [
            {
                "question": "What color is the sky on a clear day?",
                "options": ["Green", "Blue", "Red", "Orange"],
                "answer": "Blue",
                "explanation": "The sky appears blue on a clear day."
            },
            {
                "question": "Which is a primary color?",
                "options": ["Green", "Orange", "Purple", "Red"],
                "answer": "Red",
                "explanation": "Red, Blue, and Yellow are the three primary colors."
            }
        ]
    },
    "days": {
        "title": "Days of the Week",
        "level": "Beginner",
        "content": """
**The 7 Days of the Week:**

| Number | Day | Hindi |
|--------|-----|-------|
| 1 | Monday | सोमवार |
| 2 | Tuesday | मंगलवार |
| 3 | Wednesday | बुधवार |
| 4 | Thursday | गुरुवार |
| 5 | Friday | शुक्रवार |
| 6 | Saturday | शनिवार |
| 7 | Sunday | रविवार |

**Weekend:** Saturday and Sunday
**Weekdays:** Monday to Friday

**Useful Sentences:**
- "Today is Monday."
- "School is closed on Sunday."
- "My favourite day is Friday!"
        """,
        "quiz": [
            {
                "question": "Which day comes after Monday?",
                "options": ["Wednesday", "Sunday", "Tuesday", "Thursday"],
                "answer": "Tuesday",
                "explanation": "Tuesday comes right after Monday in the week."
            },
            {
                "question": "Which days are the weekend?",
                "options": ["Monday & Tuesday", "Friday & Saturday", "Saturday & Sunday", "Sunday & Monday"],
                "answer": "Saturday & Sunday",
                "explanation": "Saturday and Sunday together form the weekend."
            }
        ]
    },
    "animals": {
        "title": "Animals in English",
        "level": "Beginner",
        "content": """
**Domestic Animals (पालतू जानवर):**
- Dog (कुत्ता), Cat (बिल्ली), Cow (गाय)
- Horse (घोड़ा), Buffalo (भैंस), Goat (बकरी)

**Wild Animals (जंगली जानवर):**
- Lion (शेर), Tiger (बाघ), Elephant (हाथी)
- Deer (हिरण), Monkey (बंदर), Snake (सांप)

**Birds (पक्षी):**
- Parrot (तोता), Peacock (मोर), Crow (कौआ)
- Sparrow (गौरैया), Eagle (बाज)

**Animal Sounds:**
- Dog → barks, Cat → meows
- Cow → moos, Lion → roars
        """,
        "quiz": [
            {
                "question": "What is the English word for 'हाथी'?",
                "options": ["Tiger", "Elephant", "Lion", "Horse"],
                "answer": "Elephant",
                "explanation": "हाथी = Elephant in English."
            },
            {
                "question": "Which animal is called the national bird of India?",
                "options": ["Parrot", "Eagle", "Peacock", "Crow"],
                "answer": "Peacock",
                "explanation": "The Peacock (मोर) is the national bird of India."
            }
        ]
    },
    "sentences": {
        "title": "Making Simple Sentences",
        "level": "Beginner",
        "content": """
A **sentence** has two parts:
1. **Subject** (who/what the sentence is about)
2. **Predicate** (what the subject does or is)

**Sentence Structure:** Subject + Verb + Object

**Examples:**
- I **eat** rice. (Subject=I, Verb=eat, Object=rice)
- She **reads** a book.
- The dog **runs** fast.
- We **go** to school.

**Types of Sentences:**
- **Statement:** The sky is blue.
- **Question:** Is the sky blue?
- **Command:** Please sit down.
- **Exclamation:** What a beautiful day!

**Key Rule:** Every sentence starts with a **Capital Letter** and ends with a **full stop (.)**, **question mark (?)**, or **exclamation mark (!)**.
        """,
        "quiz": [
            {
                "question": "Every sentence must start with a ___.",
                "options": ["small letter", "number", "capital letter", "symbol"],
                "answer": "capital letter",
                "explanation": "Every sentence must begin with a capital (uppercase) letter."
            },
            {
                "question": "Which punctuation ends a question?",
                "options": ["Full stop (.)", "Comma (,)", "Question mark (?)", "Exclamation mark (!)"],
                "answer": "Question mark (?)",
                "explanation": "Questions always end with a question mark (?)."
            }
        ]
    },
    "present_tense": {
        "title": "Present Tense",
        "level": "Intermediate",
        "content": """
**Present Simple** — for habits and facts.

**Structure:**
- I/You/We/They + verb (base form)
- He/She/It + verb + **s/es**

**Examples:**
- I **play** cricket every day.
- She **goes** to school.
- They **eat** lunch at 1 pm.
- He **watches** TV.

**Negative:** Subject + do/does + not + verb
- I **do not** play. / She **does not** play.

**Question:** Do/Does + Subject + verb?
- **Do** you play cricket?
- **Does** she go to school?

**Rules for adding -s/-es:**
- Most verbs → add **-s**: play → plays
- Verbs ending in -s, -sh, -ch, -x, -o → add **-es**: go → goes, watch → watches
        """,
        "quiz": [
            {
                "question": "Choose the correct form: She ___ to school every day.",
                "options": ["go", "going", "goes", "gone"],
                "answer": "goes",
                "explanation": "With 'she', we add -es to 'go' → goes."
            },
            {
                "question": "Make it negative: 'He plays cricket.'",
                "options": ["He not plays cricket.", "He does not play cricket.", "He do not play cricket.", "He is not play cricket."],
                "answer": "He does not play cricket.",
                "explanation": "For he/she/it in negative, use 'does not' + base verb."
            }
        ]
    },
    "vocabulary": {
        "title": "Everyday Vocabulary",
        "level": "Beginner",
        "content": """
**School Words:**
- Book (किताब), Pen (कलम), Pencil (पेंसिल)
- Bag (थैला), Board (श्यामपट्ट), Teacher (अध्यापक)
- Student (विद्यार्थी), Classroom (कक्षा)

**Food Words:**
- Rice (चावल), Bread (रोटी), Water (पानी)
- Milk (दूध), Fruit (फल), Vegetable (सब्जी)

**Body Parts:**
- Head (सिर), Eye (आँख), Ear (कान)
- Nose (नाक), Mouth (मुँह), Hand (हाथ), Foot (पैर)

**Family Members:**
- Mother (माँ), Father (पिताजी), Sister (बहन)
- Brother (भाई), Grandmother (दादी/नानी)
        """,
        "quiz": [
            {
                "question": "What is the English word for 'पानी'?",
                "options": ["Milk", "Water", "Juice", "Tea"],
                "answer": "Water",
                "explanation": "पानी = Water in English."
            },
            {
                "question": "Which word means 'किताब'?",
                "options": ["Pen", "Pencil", "Book", "Bag"],
                "answer": "Book",
                "explanation": "किताब = Book in English."
            }
        ]
    }
}

# ---------------------------------------------------------------------------
# Intent patterns (keyword → intent mapping)
# ---------------------------------------------------------------------------

INTENT_PATTERNS = [
    # Greeting intents
    (r"\b(hi|hello|hey|helo|hii|namaste)\b", "greeting"),
    (r"\b(good morning|good afternoon|good evening|good night)\b", "greeting"),

    # Specific lesson topics — MUST come before generic list_lessons
    (r"\b(greet|greeting|greetings|introduction|introduce)\b", "lesson_greetings"),
    (r"\b(alphabet|abcd|abc|letter)\b", "lesson_alphabet"),
    (r"\b(number|count|counting|digit)\b", "lesson_numbers"),
    (r"\b(color|colour|colours|colors|red|blue|green|yellow)\b", "lesson_colors"),
    (r"\b(day|week|weekday|monday|tuesday|wednesday|thursday|friday|saturday|sunday)\b", "lesson_days"),
    (r"\b(animal|animals|dog|cat|cow|lion|tiger|elephant|bird|parrot)\b", "lesson_animals"),
    (r"\b(sentence|grammar|punctuation)\b", "lesson_sentences"),
    (r"\b(present tense|tense|verb)\b", "lesson_present_tense"),
    (r"\b(word|vocab|vocabulary|meaning)\b", "lesson_vocabulary"),

    # Generic lesson listing — after all specific topics
    (r"\b(lesson|lessons|topic|topics|all|learn|teach|study|chapter)\b", "list_lessons"),

    # Quiz intents
    (r"\b(quiz|test|question|exam|practice|exercise)\b", "start_quiz"),

    # Help / meta
    (r"\b(help|what can you do|commands|options|menu)\b", "help"),

    # Motivational / encouragement
    (r"\b(thanks|thank you|dhanyawad|shukriya|great|good)\b", "encouragement"),

    # Score / progress
    (r"\b(score|progress|result|how am i doing)\b", "progress"),

    # Farewell
    (r"\b(bye|goodbye|alvida|see you)\b", "farewell"),
]

LESSON_KEY_MAP = {
    "lesson_greetings": "greetings",
    "lesson_alphabet": "alphabet",
    "lesson_numbers": "numbers",
    "lesson_colors": "colors",
    "lesson_days": "days",
    "lesson_animals": "animals",
    "lesson_sentences": "sentences",
    "lesson_present_tense": "present_tense",
    "lesson_vocabulary": "vocabulary",
}

# ---------------------------------------------------------------------------
# NLP Processing
# ---------------------------------------------------------------------------

def preprocess(text: str) -> str:
    """Lowercase and strip the input text."""
    return text.lower().strip()


def detect_intent(text: str) -> str:
    """Return the best-matching intent for the given user message."""
    cleaned = preprocess(text)
    for pattern, intent in INTENT_PATTERNS:
        if re.search(pattern, cleaned, re.IGNORECASE):
            return intent
    return "unknown"


def get_lesson_response(lesson_key: str) -> dict:
    """Return a lesson payload by key."""
    lesson = LESSONS.get(lesson_key)
    if not lesson:
        return {"type": "error", "text": "Sorry, I couldn't find that lesson."}
    return {
        "type": "lesson",
        "title": lesson["title"],
        "level": lesson["level"],
        "content": lesson["content"],
        "lesson_key": lesson_key,
    }


def get_quiz(lesson_key: str) -> dict:
    """Return quiz questions for a lesson, or a random lesson if none specified."""
    if lesson_key and lesson_key in LESSONS:
        questions = LESSONS[lesson_key]["quiz"]
        title = LESSONS[lesson_key]["title"]
    else:
        # Pick a random lesson
        key = random.choice(list(LESSONS.keys()))
        questions = LESSONS[key]["quiz"]
        title = LESSONS[key]["title"]
        lesson_key = key

    return {
        "type": "quiz",
        "lesson_key": lesson_key,
        "title": title,
        "questions": questions,
    }


def list_all_lessons() -> dict:
    lesson_list = [
        {"key": k, "title": v["title"], "level": v["level"]}
        for k, v in LESSONS.items()
    ]
    return {
        "type": "lesson_list",
        "lessons": lesson_list,
        "text": "Here are all available lessons. Click any topic to start learning!",
    }


GREETING_RESPONSES = [
    "Namaste! 🙏 Welcome to your English Learning Chatbot! I am here to help you learn English step by step. Type **help** to see what I can do!",
    "Hello! 👋 I am your English teacher bot! Ready to learn? Type **lessons** to see all topics.",
    "Hi there! 😊 Great to see you! Let's learn English together. What topic would you like to study today?",
]

ENCOURAGEMENT_RESPONSES = [
    "You're doing great! Keep it up! 🌟",
    "Wonderful! Learning English is a great skill. Keep practising! 💪",
    "Thank you! I am happy to help you learn. Come back anytime! 😊",
    "That's the spirit! Every day you practise, you get better! 🎉",
]


def process_message(user_message: str, context: dict = None) -> dict:
    """
    Main entry point. Takes user message + optional context,
    returns a response payload dict.
    """
    context = context or {}
    intent = detect_intent(user_message)

    # --- Handle lesson intents ---
    if intent in LESSON_KEY_MAP:
        lesson_key = LESSON_KEY_MAP[intent]
        return get_lesson_response(lesson_key)

    if intent == "greeting":
        return {
            "type": "text",
            "text": random.choice(GREETING_RESPONSES),
        }

    if intent == "list_lessons":
        return list_all_lessons()

    if intent == "start_quiz":
        # Check if context tells us which lesson
        lesson_key = context.get("current_lesson")
        return get_quiz(lesson_key)

    if intent == "help":
        return {
            "type": "help",
            "text": (
                "🤖 **I can help you with:**\n\n"
                "📚 **Lessons** — Type a topic name like:\n"
                "- *alphabet*, *numbers*, *colors*, *greetings*\n"
                "- *days*, *animals*, *sentences*, *vocabulary*, *present tense*\n\n"
                "📝 **Quiz** — Type **quiz** to test your knowledge\n\n"
                "📋 **All Lessons** — Type **lessons** to see all topics\n\n"
                "💬 **Just talk to me** — I understand English and Hindi words!\n\n"
                "🌟 **Tip:** Start with **greetings** if you are a beginner!"
            ),
        }

    if intent == "encouragement":
        return {
            "type": "text",
            "text": random.choice(ENCOURAGEMENT_RESPONSES),
        }

    if intent == "farewell":
        return {
            "type": "text",
            "text": "Goodbye! 👋 Keep practising English every day. You are doing great! Alvida! 🙏",
        }

    if intent == "progress":
        return {
            "type": "text",
            "text": (
                "📊 **Your progress is tracked locally in your browser!**\n\n"
                "Complete lessons and quizzes to earn points. "
                "Your score is shown in the top-right corner. "
                "Every correct quiz answer gives you **10 points**! 🌟"
            ),
        }

    # --- Fallback: fuzzy topic matching ---
    cleaned = preprocess(user_message)
    for key, lesson in LESSONS.items():
        if key in cleaned or lesson["title"].lower() in cleaned:
            return get_lesson_response(key)

    # --- Ultimate fallback ---
    return {
        "type": "text",
        "text": (
            "I did not understand that. 🤔\n\n"
            "Try typing:\n"
            "- **lessons** — to see all topics\n"
            "- **quiz** — to take a test\n"
            "- **help** — to see all commands\n"
            "- A topic name like **greetings** or **alphabet**"
        ),
    }
