import requests
NUTRITIONIX_APP_ID = '38216dbf'
NUTRITIONIX_API_KEY = 'efc68bcd7238c449074ccee19e84e2c6'

api_url = 'https://trackapi.nutritionix.com/v2/search/instant'

harmful_ingredients_risks = {
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
    ],
    "Artificial Sweeteners (Acesulfame Potassium, Saccharin)": [
        "Possible carcinogenic effects",
        "Altered gut microbiota",
        "Increased risk of glucose intolerance",
        "Potential endocrine disruption"
    ],
    "Nitrates/Nitrites (Sodium Nitrate, Sodium Nitrite)": [
        "Linked to colorectal cancer",
        "Methemoglobinemia (a blood disorder)",
        "Formation of nitrosamines (carcinogens) in the stomach",
        "Increased risk of cardiovascular diseases"
    ],
    "Sodium Phosphates": [
        "Kidney damage in high amounts",
        "Increased risk of cardiovascular disease",
        "Disrupted calcium-phosphorus balance, leading to bone loss",
        "Digestive issues (bloating, diarrhea)"
    ],
    "Artificial Flavoring": [
        "Allergic reactions (hives, itching)",
        "Respiratory issues (wheezing, asthma)",
        "Potential neurotoxicity (linked to headaches, dizziness)",
        "Possible endocrine disruption"
    ],
    "Polysorbate 80": [
        "Inflammation of the gastrointestinal tract",
        "Increased risk of metabolic syndrome",
        "Possible link to infertility in animal studies",
        "Disruption of the gut microbiome"
    ],
    "Sodium Aluminum Sulfate": [
        "Linked to neurotoxicity (possible connection to Alzheimer's disease)",
        "Bone weakness and mineral loss",
        "Gastrointestinal irritation",
        "Possible carcinogenic effects"
    ],
    "Azodicarbonamide (ADA)": [
        "Classified as a potential carcinogen in certain conditions (when heated)",
        "Banned in many countries but used in baked goods as a dough conditioner",
        "Linked to respiratory issues (asthma)",
        "Possible allergic reactions"
    ],
    "Polydimethylsiloxane": [
        "Linked to digestive issues in large amounts",
        "Possible bioaccumulation and toxicity concerns",
        "Skin and eye irritations in industrial exposure"
    ],
    "Brominated Vegetable Oil (BVO)": [
        "Linked to memory loss and cognitive impairment",
        "Possible buildup of bromine in the body, leading to toxicity",
        "Neurological effects (headaches, fatigue)",
        "Increased risk of thyroid disorders"
    ],
    "Caramel Coloring (Class III and IV)": [
        "Formation of 4-Methylimidazole (4-MEI), a possible carcinogen",
        "Linked to increased cancer risk in animal studies",
        "Hyperactivity and behavioral issues in children",
        "Possible liver toxicity"
    ],
    "Sodium Lauryl Sulfate (SLS)": [
        "Skin irritations (eczema, rashes)",
        "Eye irritations",
        "Digestive discomfort if ingested",
        "Potential hormone disruption"
    ],
    "Phthalates (Found in some food packaging)": [
        "Endocrine disruption (affects hormone balance)",
        "Increased risk of developmental and reproductive issues",
        "Linked to asthma and allergies in children",
        "Possible carcinogenic effects"
    ],
    "Parabens (Used as preservatives)": [
        "Hormonal imbalances (endocrine disruption)",
        "Increased risk of breast cancer",
        "Potential link to reproductive issues",
        "Skin irritation and allergic reactions"
    ],
    "Olestra (Fat Substitute)": [
        "Inhibits the absorption of fat-soluble vitamins (A, D, E, K)",
        "Causes digestive issues (bloating, diarrhea, cramping)",
        "May lead to nutrient deficiencies",
        "Possible link to gastrointestinal discomfort and urgency"
    ],
    "Bisphenol A (BPA, found in plastics and food containers)": [
        "Endocrine disruption (mimics estrogen)",
        "Linked to reproductive issues and infertility",
        "Increased risk of cancer (breast, prostate)",
        "Potential link to obesity and metabolic disorders"
    ],
    "Propylene Glycol": [
        "Skin irritation and allergic reactions",
        "Linked to respiratory issues when inhaled in large amounts",
        "Potential liver and kidney damage with chronic exposure",
        "Possible neurotoxicity in high doses"
    ],
    "Tertiary Butylhydroquinone (TBHQ)": [
        "Possible carcinogenic effects (linked to stomach cancer in animal studies)",
        "Linked to immune system suppression",
        "May cause vision disturbances and behavioral changes in high doses",
        "Digestive discomfort (nausea, vomiting)"
    ],
    "Artificial Trans Fats (Fully Hydrogenated Oils)": [
        "Increased risk of cardiovascular disease",
        "Elevated LDL (bad) cholesterol and reduced HDL (good) cholesterol",
        "Increased risk of stroke",
        "Linked to insulin resistance and type 2 diabetes"
    ],
    "Phosphoric Acid": [
        "Linked to lower bone density (due to impaired calcium absorption)",
        "Increased risk of kidney stones and kidney damage",
        "Erosion of tooth enamel",
        "Potential link to gastrointestinal irritation"
    ],
    "Dimethylpolysiloxane": [
        "Possible buildup of silicon compounds in the body",
        "Digestive discomfort (bloating, gas)",
        "Potential link to autoimmune issues",
        "Not well studied, raising concerns about long-term health effects"
    ],
    "Brominated Flour": [
        "Linked to thyroid dysfunction due to bromine interference with iodine absorption",
        "Associated with neurological effects (headaches, fatigue)",
        "Banned in many countries due to potential carcinogenic effects",
        "Linked to kidney and nerve damage"
    ],
    "Erythrosine (Red 3)": [
        "Linked to thyroid tumors in animal studies",
        "Potential carcinogenic effects",
        "May cause hyperactivity and behavioral issues in children",
        "Banned in cosmetics due to health concerns but still allowed in food"
    ],
    "Calcium Propionate": [
        "Linked to behavioral issues in children (hyperactivity, irritability)",
        "Possible gastrointestinal discomfort (bloating, nausea)",
        "May cause allergic reactions (skin rashes)",
        "Potential disruption of gut microbiota"
    ],
    "Aluminum Additives (Aluminum Sulfate, Aluminum Silicate)": [
        "Potential neurotoxicity (linked to Alzheimer's disease)",
        "Possible link to bone weakness and mineral loss",
        "Digestive discomfort",
        "Accumulates in the body with long-term exposure"
    ],
    "Sodium Caseinate": [
        "Potential allergic reactions (especially in individuals with dairy allergies)",
        "Digestive discomfort (bloating, diarrhea) in lactose-intolerant individuals",
        "May cause inflammation in sensitive individuals",
        "Possible link to cardiovascular issues"
    ],
    "Silicon Dioxide": [
        "Respiratory issues when inhaled in large quantities (industrial exposure)",
        "Linked to kidney damage in high doses",
        "Possible link to autoimmune disorders",
        "Potential gastrointestinal irritation"
    ],
    "Sorbic Acid (and Sorbates)": [
        "Skin irritations and allergic reactions (hives, rashes)",
        "Potential respiratory irritation in high doses",
        "May cause digestive discomfort (nausea, vomiting)",
        "Linked to immune suppression in some studies"
    ],
    "Ethoxyquin": [
        "Classified as a potential human carcinogen",
        "Used as a pesticide but sometimes found in animal feed and preserved foods",
        "Linked to liver and kidney damage",
        "Possible endocrine disruption"
    ],
    "Calcium Disodium EDTA": [
        "May cause digestive discomfort (nausea, vomiting)",
        "Linked to kidney damage and mineral imbalances in high doses",
        "Possible allergic reactions",
        "Potential link to reproductive toxicity in animal studies"
    ],
    "Sodium Nitrite": [
        "Formation of nitrosamines (carcinogens) when cooked at high temperatures",
        "Linked to an increased risk of gastric cancer",
        "May contribute to oxidative stress in the body",
        "Can exacerbate heart disease and high blood pressure"
    ],
    "Sodium Metabisulfite": [
        "Linked to allergic reactions, especially in individuals with asthma",
        "Possible gastrointestinal irritation (nausea, diarrhea)",
        "Potential for skin irritation (rashes, hives)",
        "May trigger respiratory problems in sensitive individuals"
    ],
    "Potassium Sorbate": [
        "Linked to skin allergies (rashes, itching)",
        "Possible respiratory issues (asthma, coughing)",
        "May cause digestive problems (nausea, diarrhea)",
        "Potential disruption of gut microbiota"
    ],
    "Sodium Erythorbate": [
        "Potential gastrointestinal distress in high amounts",
        "Linked to allergic reactions in sensitive individuals",
        "Possible link to kidney stones when consumed in large quantities",
        "May cause headaches and dizziness"
    ],
    "Sodium Stearoyl Lactylate": [
        "Potential digestive irritation (bloating, cramping)",
        "May cause allergic reactions in sensitive individuals",
        "Linked to possible skin irritations",
        "Possible disruption of the gut microbiome"
    ],
    "Disodium Inosinate and Disodium Guanylate": [
        "Often used with MSG, can lead to 'Chinese Restaurant Syndrome' (headaches, nausea)",
        "May cause allergic reactions in sensitive individuals",
        "Linked to gastrointestinal discomfort",
        "Potential for skin reactions (rashes)"
    ],
    "Sodium Carboxymethylcellulose (CMC)": [
        "May cause digestive problems (bloating, diarrhea)",
        "Linked to increased inflammation in the gut",
        "Possible disruption of the gut microbiota",
        "Potential carcinogenic effects in long-term animal studies"
    ]
}

userIngredients = {}
#call ingredients will return the harmful ingredients in the food

def call_ingredients(food_item):
    userIngredients = {}
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

def all_ingredients(food_item):
    userIngredients = []
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
                        userIngredients.append(ingredient)
                else:
                    print(f"No ingredient information found for {food_name}")
                    
    return userIngredients
