import re
from typing import Dict

# Lightweight, deterministic replies without any external AI/ML

MENU_TEXT = (
    """Available topics:\n\n"
    "- Crop tips\n"
    "- Pest and disease control\n"
    "- Soil health\n"
    "- Weather preparation\n"
    "- Government schemes\n"
    "- ML roadmap (learning guide)\n\n"
    "You can also use commands: /menu, /ml-roadmap"""
)

ML_ROADMAP = (
    """🧭 Step-by-Step Roadmap to Build a Machine Learning Model\n\n"
    "---\n\n"
    "🪜 Step 1: Understand What ML Means\n\n"
    "Machine Learning = teaching computers to learn from data and make predictions without hardcoding rules.\n\n"
    "> You give past crop data (rainfall, soil, yield).\n"
    "The ML model learns the pattern.\n"
    "Then, for new data, it predicts the expected yield. 🌾\n\n"
    "---\n\n"
    "🧰 Step 2: Set Up Your Tools\n\n"
    "Install these locally (or use Google Colab online):\n\n"
    "pip install numpy pandas matplotlib scikit-learn\n\n"
    "Optional but helpful:\n"
    "- Jupyter Notebook → testing\n"
    "- VS Code/Cursor → development\n"
    "- Google Colab → cloud notebook\n\n"
    "---\n\n"
    "📚 Step 3: Learn the Basics\n\n"
    "Data (CSV), Features & Labels (X→Y), Train/Test split, Accuracy.\n\n"
    "👉 Example (yield prediction): Features: area, soil fertility, rainfall; Label: predicted yield\n\n"
    "---\n\n"
    "🧪 Step 4: Build Your First Model\n\n"
    "import pandas as pd\nfrom sklearn.linear_model import LinearRegression\n\n"
    "data = { 'area': [1,2,3,4,5], 'fertility': [1.2,1.5,1.7,2.0,2.2], 'yield': [1.3,2.5,3.0,4.1,4.8] }\n"
    "df = pd.DataFrame(data)\nX = df[['area','fertility']]; y = df['yield']\n"
    "model = LinearRegression(); model.fit(X, y)\n"
    "print(model.predict([[2.5, 1.8]])[0])\n\n"
    "---\n\n"
    "📊 Step 5: Try Different Models\n"
    "DecisionTreeClassifier, KNeighborsClassifier, RandomForestRegressor (scikit-learn).\n\n"
    "🔍 Step 6: Real Data: Kaggle, UCI, Govt portals.\n\n"
    "🚀 Step 7: Projects: Yield prediction, Rainfall prediction, House prices.\n\n"
    "🧠 Step 8: Deep Learning (optional): TensorFlow/PyTorch."""
)

RICE_TIPS = (
    """For rice cultivation in Telugu states:\n"
    "• Best sowing time: June-July (Kharif)\n"
    "• Use certified seeds\n"
    "• Maintain 2-3 inches water level\n"
    "• Apply NPK fertilizers as recommended\n"
    "• Control weeds regularly\n"
    "• Protect from stem borer pests"""
)

PEST_TIPS = (
    """Pest and disease management:\n"
    "• Use integrated pest management (IPM)\n"
    "• Monitor crops regularly\n"
    "• Use neem-based products\n"
    "• Follow recommended pesticide schedules\n"
    "• Maintain crop diversity"""
)

SOIL_TIPS = (
    """Soil health improvement:\n"
    "• Test soil every 2-3 years\n"
    "• Add organic matter (compost/FYM)\n"
    "• Apply balanced NPK\n"
    "• Practice crop rotation\n"
    "• Maintain pH 6.0–7.5"""
)

WEATHER_TIPS = (
    """Weather-related farming:\n"
    "• Check local forecasts regularly\n"
    "• Choose drought-resistant varieties\n"
    "• Conserve water; use drip if possible\n"
    "• Mulch to retain moisture\n"
    "• Plan irrigation schedules"""
)

SCHEMES = (
    """Government schemes (India):\n"
    "• PM-KISAN: ₹6,000/year DBT\n"
    "• PM Fasal Bima Yojana: Crop insurance\n"
    "• Soil Health Card\n"
    "• PM Krishi Sinchai: Irrigation support\n"
    "State: Rythu Bandhu/Bharosa, input subsidies."""
)


def _match_keywords(text: str, keywords) -> bool:
    t = text.lower()
    return any(k in t for k in keywords)


def reply(message: str, session_id: str = "") -> Dict[str, str]:
    text = message.strip()
    lower = text.lower()

    # Slash commands
    if lower.startswith('/menu') or lower == 'menu' or lower == 'help':
        return {"content": MENU_TEXT}
    if lower.startswith('/ml-roadmap') or _match_keywords(lower, ['ml roadmap', 'machine learning roadmap']):
        return {"content": ML_ROADMAP}

    # Topic matching (deterministic)
    if _match_keywords(lower, ['rice', 'paddy', 'వరి']):
        return {"content": RICE_TIPS}
    if _match_keywords(lower, ['pest', 'disease', 'bug', 'insect']):
        return {"content": PEST_TIPS}
    if _match_keywords(lower, ['soil', 'fertilizer', 'nutrient', 'manure', 'compost', 'ph']):
        return {"content": SOIL_TIPS}
    if _match_keywords(lower, ['weather', 'rain', 'drought', 'climate']):
        return {"content": WEATHER_TIPS}
    if _match_keywords(lower, ['scheme', 'subsidy', 'government', 'yojana']):
        return {"content": SCHEMES}

    # Learning guide by generic ML keywords
    if _match_keywords(lower, ['machine learning', 'build model', 'chatbot', 'ai model', 'ml ']):
        return {"content": ML_ROADMAP}

    # Default menu prompt
    return {"content": MENU_TEXT}
