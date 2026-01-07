import random
import re

class EmailGenerator:
    
    def _clean_word(self, word: str) -> str:
        
        word = word.lower().strip()
        return re.sub(r"[^a-z0-9]", "", word)

    def generate_random_email(self, word: str) -> str:
        
        word = self._clean_word(word)
        number = random.randint(10, 9999)
        return f"{word}{number}@gmail.com"
    
import string

class EmailGenerator:
    def generate_random_email(self, word):
        suffix = random.randint(100, 999)
        domains = ["gmail.com"]
        domain = random.choice(domains)

        clean_word = "".join(c for c in word.lower() if c.isalnum())
        return f"{clean_word}{suffix}@{domain}"
