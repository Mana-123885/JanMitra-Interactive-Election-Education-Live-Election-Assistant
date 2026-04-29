import json
import random
from core.database import increment_chatbot_questions, save_chat_message

class ChatbotService:
    def __init__(self, faq_path="data/chatbot_faq.json"):
        with open(faq_path, "r", encoding="utf-8") as f:
            self.faq = json.load(f)
            
    def get_response(self, user_query):
        increment_chatbot_questions()
        save_chat_message("user", user_query)
        
        query = user_query.lower()
        best_match = None
        max_keywords = 0
        
        for entry in self.faq:
            match_count = sum(1 for kw in entry['keywords'] if kw in query)
            if match_count > max_keywords:
                max_keywords = match_count
                best_match = entry
        
        if best_match and max_keywords > 0:
            response = best_match['answer']
        else:
            response = "I'm sorry, I couldn't find specific information on that. Could you try rephrasing? You can ask about 'voter registration', 'EVM', 'Model Code of Conduct', or 'MP vs MLA'."
            
        save_chat_message("bot", response)
        return response

chatbot_service = ChatbotService()
