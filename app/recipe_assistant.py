import os
import google.generativeai as genai
from dotenv import load_dotenv
from app.prompts import create_recipe_prompt
import re

class RecipeAssistant:
    def __init__(self):
        load_dotenv()
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        self.model = genai.GenerativeModel(os.getenv("AI_MODEL"))

    def _parse_section(self, text: str, section_name: str) -> str:
        pattern = f'【{section_name}】\s*(.*?)(?=【|$)'
        match = re.search(pattern, text, re.DOTALL)
        return match.group(1).strip() if match else ""

    def _parse_list(self, text: str, section_name: str) -> list[str]:
        section = self._parse_section(text, section_name)
        return [line.strip() for line in section.split('\n') if line.strip()]

    def get_recipe(self, ingredients: str) -> dict:
        try:
            prompt = create_recipe_prompt(ingredients)
            response = self.model.generate_content(prompt)
            text = response.text

            return {
                "dish_name": self._parse_section(text, "料理名"),
                "cooking_time": self._parse_section(text, "調理時間"),
                "ingredients": self._parse_list(text, "材料（2人分）"),
                "steps": self._parse_list(text, "手順")
            }
        except Exception as e:
            return {"error": str(e)} 