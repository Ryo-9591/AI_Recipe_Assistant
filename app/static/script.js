const el = {
    ingredients: document.getElementById('ingredients'),
    recipe: document.getElementById('recipe'),
    loading: document.getElementById('loading'),
    button: document.getElementById('generateButton')
};

const showLoading = () => {
    el.loading.style.display = 'block';
    el.recipe.style.display = 'none';
    el.button.disabled = true;
};

const hideLoading = () => {
    el.loading.style.display = 'none';
    el.button.disabled = false;
};

const showError = msg => {
    el.recipe.innerHTML = `<p class="error">${msg}</p>`;
    el.recipe.style.display = 'block';
};

const showRecipe = data => {
    el.recipe.innerHTML = `
        <h2>${data.dish_name}</h2>
        <p><strong>調理時間:</strong> ${data.cooking_time}</p>
        <p><strong>材料（2人分）:</strong></p>
        <ul>${data.ingredients.map(ing => `<li>${ing}</li>`).join('')}</ul>
        <p><strong>手順:</strong></p>
        <ol>${data.steps.map(step => `<li>${step}</li>`).join('')}</ol>
    `;
    el.recipe.style.display = 'block';
};

const generateRecipe = async () => {
    const ingredients = el.ingredients.value.trim();
    if (!ingredients) return showError('材料を入力してください。');

    showLoading();
    try {
        const res = await fetch(`/recipe?ingredients=${encodeURIComponent(ingredients)}`, { method: 'POST' });
        const data = await res.json();
        data.error ? showError(data.error) : showRecipe(data);
    } catch (e) {
        showError(`エラーが発生しました: ${e.message}`);
    } finally {
        hideLoading();
    }
};