from fastapi import FastAPI, Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.recipe_assistant import RecipeAssistant
from pydantic import BaseModel
from typing import List
import os

app = FastAPI()

# 静的ファイルを提供するための設定
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# レシピアシスタントのインスタンスを作成
recipe_assistant = RecipeAssistant()

class RecipeResponse(BaseModel):
    dish_name: str
    cooking_time: str
    ingredients: List[str]
    steps: List[str]

class AlternativeResponse(BaseModel):
    alternatives: List[str]
    notes: str

@app.get("/")
async def read_root():
    # ルートパスでindex.htmlを返す
    return FileResponse('app/static/index.html')

@app.post("/recipe", response_model=RecipeResponse)
async def generate_recipe(ingredients: str = Query(..., description="材料をカンマ区切りで入力")):
    recipe = recipe_assistant.get_recipe(ingredients)
    return recipe

@app.post("/alternative", response_model=AlternativeResponse)
async def suggest_alternative(ingredient: str = Query(..., description="代替案を探したい材料を入力")):
    alternatives = recipe_assistant.get_alternative(ingredient)
    return alternatives

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 