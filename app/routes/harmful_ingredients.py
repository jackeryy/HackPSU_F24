harmful_ingredients_risks = {
    "Aspartame": [
        "Headaches and migraines",
        "Dizziness",
        "Possible carcinogenic effects (cancer risk)",
        "Neurological symptoms (neurotoxicity)",
        "Weight gain"
    ],
    "Sucralose": [
        "Altered gut microbiota",
        "Weight gain",
        "Increased risk of type 2 diabetes",
        "Digestive issues",
        "Possible link to cancer"
    ],
    "High Fructose Corn Syrup": [
        "Increased risk of obesity",
        "Type 2 diabetes",
        "Heart disease",
        "Fatty liver disease",
        "Metabolic syndrome"
    ],
    "Sodium Benzoate": [
        "Hyperactivity in children (linked to ADHD)",
        "May form benzene (a known carcinogen) when combined with vitamin C",
        "Allergic reactions in sensitive individuals"
    ],
    "Butylated Hydroxyanisole (BHA)": [
        "Classified as a possible human carcinogen",
        "Linked to stomach cancer in animal studies",
        "Hormonal disruptions"
    ],
    # ... Add more ingredients here
}

# Function to check for harmful ingredients
def check_harmful_ingredients(ingredient_list):
    detected_harmful_ingredients = []
    for ingredient in harmful_ingredients_risks:
        if ingredient.lower() in ingredient_list.lower():
            detected_harmful_ingredients.append(ingredient)
    return detected_harmful_ingredients

# Function to get health risks for detected harmful ingredients
def get_ingredient_risks(detected_ingredients):
    risks = {}
    for ingredient in detected_ingredients:
        if ingredient in harmful_ingredients_risks:
            risks[ingredient] = harmful_ingredients_risks[ingredient]
    return risks