import json
import os

# --- Constants ---
# Pantry staples are given less weight in the matching algorithm.
PANTRY_STAPLES = {
    "salt", "pepper", "water", "oil", "olive oil", "sugar", "flour", 
    "butter", "garlic", "onion", "soy sauce", "vinegar"
}

def load_recipes():
    """Loads the database securely with error handling."""
    try:
        # Tries to find the file in the current directory
        if not os.path.exists('recipes.json'):
            return []
            
        with open('recipes.json', 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading recipes: {e}")
        return []

def calculate_match_score(user_ingredients, recipe_ingredients):
    """
    Advanced Matching Logic:
    - Calculates a weighted score.
    - Core ingredients (not in pantry list) count for 2 points.
    - Pantry staples count for 1 point.
    """
    user_set = set(i.lower().strip() for i in user_ingredients)
    recipe_set = set(i.lower().strip() for i in recipe_ingredients)
    
    if not recipe_set:
        return 0, []

    total_possible_score = 0
    current_score = 0
    
    missing_items = []

    for ingredient in recipe_set:
        # Determine weight
        weight = 1 if ingredient in PANTRY_STAPLES else 2
        total_possible_score += weight
        
        # Check if user has it (partial match support)
        match_found = False
        for user_item in user_set:
            if user_item in ingredient or ingredient in user_item:
                match_found = True
                break
        
        if match_found:
            current_score += weight
        else:
            missing_items.append(ingredient)

    # Avoid division by zero
    if total_possible_score == 0:
        return 0, []
        
    final_score = current_score / total_possible_score
    return final_score, missing_items

def find_matching_recipes(user_ingredients, recipes):
    """
    Filters and sorts recipes based on the weighted match score.
    Returns recipes with at least a 30% match.
    """
    results = []

    for recipe in recipes:
        score, missing = calculate_match_score(user_ingredients, recipe['ingredients'])
        
        # Threshold: Show recipe if > 30% match
        if score >= 0.30:
            recipe_copy = recipe.copy()
            recipe_copy['match_score'] = score
            recipe_copy['missing_ingredients'] = missing
            results.append(recipe_copy)
    
    # Sort by highest score first
    return sorted(results, key=lambda x: x['match_score'], reverse=True)

def filter_recipes(recipes, dietary_filter=None, difficulty_filter=None):
    """Applies side-bar filters."""
    filtered = recipes
    if dietary_filter and dietary_filter != "None":
        filtered = [r for r in filtered if dietary_filter in r.get('dietary', [])]
    if difficulty_filter and difficulty_filter != "Any":
        filtered = [r for r in filtered if r.get('difficulty') == difficulty_filter]
    return filtered

def get_substitutions(ingredient):
    """Provides substitution suggestions."""
    subs = {
        "milk": "almond milk, soy milk, or water",
        "butter": "olive oil, coconut oil, or margarine",
        "egg": "flax seed meal (1 tbsp + 3 tbsp water), applesauce, or yogurt",
        "soy sauce": "tamari (gluten-free) or coconut aminos",
        "sugar": "honey, maple syrup, or stevia",
        "flour": "gluten-free blend, almond flour, or oat flour",
        "ground beef": "lentils, turkey, or plant-based crumble",
        "cream": "coconut milk or greek yogurt"
    }
    # Simple partial match for substitution key
    for key, value in subs.items():
        if key in ingredient.lower():
            return value
    return None
