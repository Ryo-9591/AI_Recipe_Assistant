def create_recipe_prompt(ingredients: str) -> str:
    return f"""
    以下の材料を使用したレシピを提案してください：
    {ingredients}

    以下の形式で出力してください：
    【料理名】
    【調理時間】
    【材料（2人分）】
    【手順】
    """ 