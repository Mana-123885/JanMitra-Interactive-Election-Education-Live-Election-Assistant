COLORS = {
    "dark": {
        "bg":           "#0F0A1A",
        "surface":      "#1A0F2E",
        "surface2":     "#2D1B69",
        "surface3":     "#3B1F6B",
        "primary":      "#A855F7",
        "primary_hover":"#C084FC",
        "secondary":    "#EC4899",
        "accent":       "#F59E0B",
        "gold":         "#FCD34D",
        "text1":        "#FAF5FF",
        "text2":        "#C4B5FD",
        "text3":        "#7C6FAD",
        "border":       "#3B1F6B",
        "success":      "#34D399",
        "warning":      "#FBBF24",
        "error":        "#F87171",
        "card_hover":   "#251545",
    },
    "light": {
        "bg":           "#FAF5FF",
        "surface":      "#FFFFFF",
        "surface2":     "#F3E8FF",
        "surface3":     "#EDE9FE",
        "primary":      "#6B21A8",
        "primary_hover":"#7C3AED",
        "secondary":    "#BE185D",
        "accent":       "#92400E",
        "gold":         "#D97706",
        "text1":        "#1C1917",
        "text2":        "#57534E",
        "text3":        "#A8A29E",
        "border":       "#E9D5FF",
        "success":      "#059669",
        "warning":      "#D97706",
        "error":        "#DC2626",
        "card_hover":   "#F5F3FF",
    }
}
COLORS["Dark"] = COLORS["dark"]
COLORS["Light"] = COLORS["light"]

LEVELS = [
    {"level":1, "title":"Nagarik Seedha",    "hi":"नागरिक सीधा",    "mr":"नागरिक साधा",    "xp":0,    "emoji":"🌱", "color":"#92400E", "desc":"A curious new citizen. Just starting the journey."},
    {"level":2, "title":"Jagruk Nagarik",    "hi":"जागरूक नागरिक",  "mr":"जागरूक नागरिक",  "xp":100,  "emoji":"👁️", "color":"#BE185D", "desc":"Aware and awakened. You know elections exist!"},
    {"level":3, "title":"Chunav Seekhak",    "hi":"चुनाव सीखक",    "mr":"निवडणूक शिकणारा","xp":250,  "emoji":"📚", "color":"#7C3AED", "desc":"An eager learner. Understanding the basics."},
    {"level":4, "title":"Matdata Mitra",     "hi":"मतदाता मित्र",  "mr":"मतदार मित्र",    "xp":500,  "emoji":"🤝", "color":"#6B21A8", "desc":"A voter's friend. You help others understand too."},
    {"level":5, "title":"Lok Sevak",         "hi":"लोक सेवक",      "mr":"लोक सेवक",       "xp":800,  "emoji":"🏛️", "color":"#4C1D95", "desc":"Public servant at heart. Deep civic knowledge."},
    {"level":6, "title":"Chunav Gyani",      "hi":"चुनाव ज्ञानी",  "mr":"निवडणूक ज्ञानी", "xp":1200, "emoji":"🎓", "color":"#BE185D", "desc":"An election scholar. You know the system inside out."},
    {"level":7, "title":"Loktantra Rakshak", "hi":"लोकतंत्र रक्षक","mr":"लोकशाही रक्षक",  "xp":1800, "emoji":"🛡️", "color":"#D97706", "desc":"Defender of democracy. A true civic champion."},
    {"level":8, "title":"Desh ka Neta",      "hi":"देश का नेता",   "mr":"देशाचा नेता",    "xp":2500, "emoji":"👑", "color":"#6B21A8", "desc":"Maximum civic mastery. Democracy Champion!"},
]

BADGES = [
    {"id":"first_step",     "emoji":"👣", "name":"First Step",         "desc":"Completed your first learning stage",              "xp":20,  "cat":"learning"},
    {"id":"bookworm",       "emoji":"📖", "name":"Bookworm",           "desc":"Explored all 12 election process stages",          "xp":100, "cat":"learning"},
    {"id":"type_master",    "emoji":"🏛️", "name":"Type Master",        "desc":"Studied all 5 types of elections",                 "xp":80,  "cat":"learning"},
    {"id":"myth_buster",    "emoji":"💥", "name":"Myth Buster",        "desc":"Debunked all 18 myths",                            "xp":75,  "cat":"learning"},
    {"id":"word_wizard",    "emoji":"📜", "name":"Word Wizard",        "desc":"Read 25+ glossary terms",                          "xp":50,  "cat":"learning"},
    {"id":"quiz_starter",   "emoji":"🎯", "name":"Quiz Starter",       "desc":"Completed your first quiz category",               "xp":25,  "cat":"quiz"},
    {"id":"perfect_score",  "emoji":"💯", "name":"Perfect Score",      "desc":"Scored 10/10 in any quiz category",                "xp":150, "cat":"quiz"},
    {"id":"quiz_champion",  "emoji":"🏆", "name":"Quiz Champion",      "desc":"Completed all 5 quiz categories",                  "xp":200, "cat":"quiz"},
    {"id":"speed_voter",    "emoji":"⚡", "name":"Speed Voter",        "desc":"Answered 5 questions under 8 seconds each",        "xp":60,  "cat":"quiz"},
    {"id":"comeback_kid",   "emoji":"🔄", "name":"Comeback Kid",       "desc":"Improved your score on a retry attempt",           "xp":40,  "cat":"quiz"},
    {"id":"streak_3",       "emoji":"🔥", "name":"On Fire",            "desc":"3-day learning streak",                            "xp":50,  "cat":"streak"},
    {"id":"streak_7",       "emoji":"🌟", "name":"Week Warrior",       "desc":"7-day learning streak",                            "xp":150, "cat":"streak"},
    {"id":"streak_30",      "emoji":"👑", "name":"Democracy Champion", "desc":"30-day learning streak",                           "xp":500, "cat":"streak"},
    {"id":"chatbot_friend", "emoji":"🤖", "name":"Chatbot Friend",     "desc":"Asked the chatbot 10+ questions",                  "xp":30,  "cat":"special"},
    {"id":"civic_hero",     "emoji":"🦸", "name":"Civic Hero",         "desc":"Reached Level 8 — maximum mastery",                "xp":500, "cat":"special"},
    {"id":"early_bird",     "emoji":"🐦", "name":"Early Bird",         "desc":"Used JanMitra on Day 1",                           "xp":10,  "cat":"special"},
    {"id":"polyglot",       "emoji":"🌐", "name":"Polyglot",           "desc":"Used all 3 language modes",                        "xp":60,  "cat":"special"},
    {"id":"voter_ready",    "emoji":"🗳️", "name":"Voter Ready",        "desc":"Completed the Polling Day Simulator",              "xp":100, "cat":"special"},
    {"id":"fact_checker",   "emoji":"🔍", "name":"Fact Checker",       "desc":"Bookmarked 10+ items",                             "xp":40,  "cat":"special"},
    {"id":"constitution",   "emoji":"📰", "name":"Constitution Buff",  "desc":"Read all glossary terms and all election types",   "xp":120, "cat":"special"},
]

APP_NAME = "JanMitra"
APP_NAME_HI = "जनमित्र"
APP_NAME_MR = "जनमित्र"

TAGLINE = "Mera Chunav, Meri Awaaz"
TAGLINE_HI = "मेरा चुनाव, मेरी आवाज़"
TAGLINE_MR = "माझे निवडणूक, माझा आवाज"
