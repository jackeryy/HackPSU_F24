import requests
NUTRITIONIX_APP_ID = '38216dbf'
NUTRITIONIX_API_KEY = 'efc68bcd7238c449074ccee19e84e2c6'

api_url = 'https://trackapi.nutritionix.com/v2/search/instant'

harmful_ingredients_risks ={
    "Aspartame": [
        "Headaches and migraines",
        "Dizziness",
        "Seizures",
        "Possible carcinogenic effects (linked to cancer)",
        "Neurological symptoms (neurotoxicity)"
    ],
    "Sucralose": [
        "Altered gut microbiota",
        "Weight gain",
        "Increased risk of type 2 diabetes",
        "Digestive issues (bloating, gas)",
        "Possible link to cancer in long-term studies"
    ],
    "High Fructose Corn Syrup (HFCS)": [
        "Increased risk of obesity",
        "Type 2 diabetes",
        "Heart disease",
        "Fatty liver disease",
        "Insulin resistance"
    ],
    "Sodium Benzoate": [
        "Hyperactivity in children (linked to ADHD)",
        "Formation of benzene (a known carcinogen) when combined with vitamin C",
        "Allergic reactions (skin rashes, itching)",
        "Asthma"
    ],
    "Canola Oil": [
        "High in omega-6 fatty acids, leading to inflammation",
        "Increased risk of heart disease due to oxidation",
        "Linked to insulin resistance",
        "Possible carcinogenic effects when heated to high temperatures"
    ],
    "Soybean Oil": [
        "High in omega-6 fatty acids, leading to chronic inflammation",
        "Linked to obesity and metabolic disorders",
        "Potential endocrine disruption",
        "Increased risk of heart disease"
    ],
    "Safflower Oil": [
        "High omega-6 content, promoting inflammation",
        "Associated with increased risk of heart disease",
        "May contribute to obesity and metabolic syndrome",
        "Potentially increases LDL cholesterol levels"
    ],
    "Cottonseed Oil": [
        "High in omega-6 fatty acids, causing inflammation",
        "Often extracted using chemical solvents",
        "May contain pesticide residues",
        "Associated with higher risk of cardiovascular diseases"
    ],
    "Sunflower Oil": [
        "High omega-6 fatty acids, leading to chronic inflammation",
        "Increased risk of heart disease and metabolic syndrome",
        "Oxidizes easily, producing harmful free radicals",
        "Potential endocrine disruptor"
    ],
    "Butylated Hydroxyanisole (BHA)": [
        "Classified as a possible human carcinogen by the International Agency for Research on Cancer (IARC)",
        "Linked to cancer in animal studies",
        "Hormonal disruptions (endocrine disruption)"
    ],
    "Butylated Hydroxytoluene (BHT)": [
        "Possible carcinogenic effects (linked to cancer)",
        "Liver and kidney damage",
        "Developmental toxicity",
        "Endocrine disruption"
    ],
    "Monosodium Glutamate (MSG)": [
        "Headaches (commonly called 'Chinese Restaurant Syndrome')",
        "Nausea and vomiting",
        "Obesity and metabolic disorders",
        "Neurotoxicity (possible effects on the nervous system)",
        "Allergic reactions (flushing, chest pain)"
    ],
    "Red 40 (Artificial Coloring)": [
        "Hyperactivity in children",
        "Allergic reactions (especially in individuals with aspirin sensitivity)",
        "Possible carcinogenic effects (linked to cancer in animal studies)"
    ],
    "Yellow 5 (Tartrazine)": [
        "Hyperactivity in children",
        "Allergic reactions (especially in individuals with aspirin sensitivity)",
        "Potential link to cancer",
        "Asthma"
    ],
    "Potassium Bromate": [
        "Carcinogenic (linked to cancer in animal studies)",
        "Banned in many countries, but still used in some bread products in the USA",
        "Kidney damage",
        "Neurological disorders"
    ],
    "Carrageenan": [
        "Inflammation of the gastrointestinal tract",
        "Increased risk of colon cancer",
        "Digestive discomfort (bloating, diarrhea, stomach cramps)",
        "Possible allergic reactions"
    ],
    "Partially Hydrogenated Oils (Trans Fats)": [
        "Increased risk of heart disease",
        "Increased cholesterol levels",
        "Higher risk of stroke",
        "Inflammation",
        "Type 2 diabetes"
    ],
    "Propyl Gallate": [
        "Endocrine disruption",
        "Skin irritations and rashes",
        "Possible carcinogenic effects",
        "Liver damage"
    ],
    "Titanium Dioxide": [
        "Possible carcinogenic effects (classified as possibly carcinogenic by IARC)",
        "Respiratory issues when inhaled",
        "Gastrointestinal irritation",
        "Increased risk of inflammatory bowel disease"
    ]
}


userIngredients = {}
#call ingredients will return the harmful ingredients in the food
def call_ingredients(food_item):
    headers = {
    'x-app-id': NUTRITIONIX_APP_ID,
    'x-app-key': NUTRITIONIX_API_KEY,
    'Content-Type': 'application/json'
    }
    body = {
        "query": food_item
    }
    response = requests.post(api_url, json=body, headers=headers)
    data = response.json()

    if 'branded' in data and data['branded']:
            # Get the nix_item_id for the first branded food item
            branded_food = data['branded'][0]
            food_name = branded_food['food_name']
            item_id = branded_food['nix_item_id']
            # Fetch detailed item data using nix_item_id
            item_details_url = f"https://trackapi.nutritionix.com/v2/search/item?nix_item_id={item_id}"
            item_response = requests.get(item_details_url, headers=headers)
            item_data = item_response.json()
            # Extract ingredients

            if 'foods' in item_data and item_data['foods']:
                ingredients = item_data['foods'][0].get('nf_ingredient_statement', 'N/A')
                if ingredients != 'N/A':
                    print(f"Ingredients for {food_name}: {ingredients}")
                    for ingredient in ingredients.split(','):
                        ingredient = ingredient.strip()
                        if ingredient in harmful_ingredients_risks:
                            userIngredients[ingredient] = harmful_ingredients_risks[ingredient]
                else:
                    print(f"No ingredient information found for {food_name}")
    return userIngredients