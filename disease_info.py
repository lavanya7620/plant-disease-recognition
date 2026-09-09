"""
Structured disease information for each class in the New Plant Diseases
Dataset: crop, condition, visible symptoms, likely causes, and general
treatment/management guidance. This is general horticultural knowledge, not
a substitute for advice from a local agricultural extension office — actual
treatment can depend on region, severity, and crop variety.
"""

DISEASE_INFO = {
    "Apple___Apple_scab": {
        "crop": "Apple", "condition": "Apple Scab (fungal)",
        "symptoms": "Olive-green to black scabby, velvety spots on leaves and fruit; infected leaves may pucker, curl, and drop early.",
        "causes": "Caused by the fungus Venturia inaequalis, which overwinters in fallen leaf litter and is favored by cool, wet spring weather.",
        "treatment": "Remove and destroy fallen leaves in autumn to reduce spores. Apply a protectant fungicide (e.g. captan or myclobutanil) starting at bud break. Choose scab-resistant varieties when replanting.",
    },
    "Apple___Black_rot": {
        "crop": "Apple", "condition": "Black Rot (fungal)",
        "symptoms": "Purple-bordered circular leaf spots ('frogeye leaf spot') and rotting fruit with concentric brown-to-black rings; can also cause branch cankers.",
        "causes": "Caused by the fungus Botryosphaeria obtusa, which overwinters in dead wood, mummified fruit, and cankers.",
        "treatment": "Prune out dead/cankered wood and mummified fruit. Apply fungicides (captan/thiophanate-methyl) during the growing season. Improve air circulation via pruning.",
    },
    "Apple___Cedar_apple_rust": {
        "crop": "Apple", "condition": "Cedar Apple Rust (fungal)",
        "symptoms": "Bright orange-yellow spots on the upper leaf surface, sometimes with small black dots at the center; can cause premature leaf drop.",
        "causes": "Caused by the fungus Gymnosporangium juniperi-virginianae, which requires a nearby juniper/cedar host to complete its life cycle.",
        "treatment": "Remove nearby juniper/cedar hosts if feasible. Apply fungicide (myclobutanil) from pink bud stage through several weeks after petal fall. Plant resistant apple cultivars.",
    },
    "Apple___healthy": {
        "crop": "Apple", "condition": "Healthy",
        "symptoms": "No visible disease symptoms; leaves are uniformly green with no spots, lesions, or discoloration.",
        "causes": "N/A — plant is healthy.",
        "treatment": "Maintain regular monitoring, balanced fertilization, and good orchard sanitation.",
    },
    "Blueberry___healthy": {
        "crop": "Blueberry", "condition": "Healthy",
        "symptoms": "No visible disease symptoms; foliage is uniformly green and vigorous.",
        "causes": "N/A — plant is healthy.",
        "treatment": "Maintain acidic soil pH, adequate mulching, and routine pruning for airflow.",
    },
    "Cherry_(including_sour)___Powdery_mildew": {
        "crop": "Cherry", "condition": "Powdery Mildew (fungal)",
        "symptoms": "White to gray powdery fungal growth on leaves, shoots, and sometimes fruit; leaves may curl, pucker, or turn pale.",
        "causes": "Caused by the fungus Podosphaera clandestina, favored by moderate temperatures and high humidity.",
        "treatment": "Apply sulfur-based or potassium bicarbonate fungicides. Prune to improve air circulation and avoid excess nitrogen fertilization.",
    },
    "Cherry_(including_sour)___healthy": {
        "crop": "Cherry", "condition": "Healthy",
        "symptoms": "No visible disease symptoms; leaves are uniformly green with no powdery coating or spotting.",
        "causes": "N/A — plant is healthy.",
        "treatment": "Continue routine pruning and monitoring for early signs of mildew.",
    },
    "Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot": {
        "crop": "Corn (Maize)", "condition": "Gray Leaf Spot (fungal)",
        "symptoms": "Rectangular, grayish-tan lesions running parallel to leaf veins; lesions can merge and cause significant leaf death.",
        "causes": "Caused by the fungus Cercospora zeae-maydis, favored by warm, humid weather and continuous corn planting (residue buildup).",
        "treatment": "Rotate crops away from corn for 1-2 years, use resistant hybrids, and apply foliar fungicides (strobilurin or triazole) if disease pressure is high.",
    },
    "Corn_(maize)___Common_rust_": {
        "crop": "Corn (Maize)", "condition": "Common Rust (fungal)",
        "symptoms": "Small, reddish-brown, powdery pustules scattered on both leaf surfaces.",
        "causes": "Caused by the fungus Puccinia sorghi, favored by cool temperatures and high humidity/extended leaf wetness.",
        "treatment": "Plant rust-resistant hybrids. Fungicide application is rarely needed unless infection is severe and early in the season.",
    },
    "Corn_(maize)___Northern_Leaf_Blight": {
        "crop": "Corn (Maize)", "condition": "Northern Leaf Blight (fungal)",
        "symptoms": "Long, cigar-shaped, gray-green to tan lesions on leaves, sometimes with a dark border.",
        "causes": "Caused by the fungus Exserohilum turcicum, favored by moderate temperatures and extended periods of leaf wetness.",
        "treatment": "Use resistant hybrids, rotate crops, till under residue, and apply fungicide if detected early with favorable disease conditions (humid, moderate temps).",
    },
    "Corn_(maize)___healthy": {
        "crop": "Corn (Maize)", "condition": "Healthy",
        "symptoms": "No visible disease symptoms; leaves are uniformly green with no lesions or rust pustules.",
        "causes": "N/A — plant is healthy.",
        "treatment": "Continue crop rotation and monitoring practices.",
    },
    "Grape___Black_rot": {
        "crop": "Grape", "condition": "Black Rot (fungal)",
        "symptoms": "Circular reddish-brown leaf lesions with dark borders; berries shrivel into hard, black 'mummies'.",
        "causes": "Caused by the fungus Guignardia bidwellii, which overwinters in mummified berries and infected canes.",
        "treatment": "Remove mummified berries and infected canes during dormant pruning. Apply fungicides (mancozeb/myclobutanil) starting at bud break through veraison.",
    },
    "Grape___Esca_(Black_Measles)": {
        "crop": "Grape", "condition": "Esca / Black Measles (fungal)",
        "symptoms": "Tiger-stripe pattern of yellow/brown discoloration between leaf veins; dark spotting or streaking on berries; sudden vine collapse in severe cases.",
        "causes": "Caused by a complex of wood-rotting fungi that infect grapevines through pruning wounds.",
        "treatment": "No curative fungicide exists; remove and destroy severely infected vines/wood, avoid large pruning wounds, and protect wounds with a fungicidal paste.",
    },
    "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)": {
        "crop": "Grape", "condition": "Leaf Blight / Isariopsis Leaf Spot (fungal)",
        "symptoms": "Dark brown, angular leaf spots that can merge and cause premature leaf drop.",
        "causes": "Caused by the fungus Pseudocercospora vitis (Isariopsis leaf spot), favored by warm, humid conditions.",
        "treatment": "Improve canopy airflow via leaf removal/pruning, apply copper-based or mancozeb fungicides, and remove fallen infected leaves.",
    },
    "Grape___healthy": {
        "crop": "Grape", "condition": "Healthy",
        "symptoms": "No visible disease symptoms; leaves are uniformly green with no spotting or discoloration.",
        "causes": "N/A — plant is healthy.",
        "treatment": "Maintain canopy management and routine disease scouting.",
    },
    "Orange___Haunglongbing_(Citrus_greening)": {
        "crop": "Orange", "condition": "Huanglongbing / Citrus Greening (bacterial)",
        "symptoms": "Blotchy, asymmetric yellow mottling on leaves; lopsided, bitter, poorly colored fruit; twig dieback.",
        "causes": "Caused by the bacterium Candidatus Liberibacter spp., spread by the Asian citrus psyllid insect.",
        "treatment": "No cure exists; remove and destroy infected trees to prevent spread, and control the psyllid vector with approved insecticides. Use certified disease-free nursery stock.",
    },
    "Peach___Bacterial_spot": {
        "crop": "Peach", "condition": "Bacterial Spot (bacterial)",
        "symptoms": "Small, dark, angular water-soaked spots on leaves that may fall out leaving a 'shot-hole' look; pitted, cracked lesions on fruit.",
        "causes": "Caused by the bacterium Xanthomonas campestris pv. pruni, spread by wind-driven rain and favored by warm, wet weather.",
        "treatment": "Plant resistant varieties, apply copper-based bactericides during dormancy, and avoid overhead irrigation that spreads bacteria.",
    },
    "Peach___healthy": {
        "crop": "Peach", "condition": "Healthy",
        "symptoms": "No visible disease symptoms; leaves are uniformly green with no spotting.",
        "causes": "N/A — plant is healthy.",
        "treatment": "Continue routine orchard sanitation and monitoring.",
    },
    "Pepper,_bell___Bacterial_spot": {
        "crop": "Bell Pepper", "condition": "Bacterial Spot (bacterial)",
        "symptoms": "Small, water-soaked spots on leaves that turn brown and scabby; raised, rough spots on fruit.",
        "causes": "Caused by Xanthomonas species, spread by splashing water and favored by warm, humid, wet conditions.",
        "treatment": "Use certified disease-free seed, apply copper-based bactericides, rotate crops, and avoid working in fields when foliage is wet.",
    },
    "Pepper,_bell___healthy": {
        "crop": "Bell Pepper", "condition": "Healthy",
        "symptoms": "No visible disease symptoms; leaves are uniformly green with no spotting.",
        "causes": "N/A — plant is healthy.",
        "treatment": "Maintain crop rotation and monitor for early spotting symptoms.",
    },
    "Potato___Early_blight": {
        "crop": "Potato", "condition": "Early Blight (fungal)",
        "symptoms": "Dark, concentric-ringed 'target' spots on older/lower leaves, often with yellowing around the lesions.",
        "causes": "Caused by the fungus Alternaria solani, favored by warm temperatures, alternating wet/dry conditions, and plant stress.",
        "treatment": "Rotate crops, remove infected debris, ensure balanced fertilization, and apply fungicides (chlorothalonil/mancozeb) at first sign of disease.",
    },
    "Potato___Late_blight": {
        "crop": "Potato", "condition": "Late Blight (oomycete)",
        "symptoms": "Water-soaked, irregularly-shaped lesions that rapidly turn brown-black, often with white fungal growth on the leaf underside in humid conditions.",
        "causes": "Caused by the oomycete Phytophthora infestans (the pathogen behind the Irish potato famine), favored by cool, wet weather.",
        "treatment": "Destroy infected plants promptly, avoid overhead irrigation, apply protectant fungicides (chlorothalonil/copper) preventatively in humid weather, and plant certified seed potatoes.",
    },
    "Potato___healthy": {
        "crop": "Potato", "condition": "Healthy",
        "symptoms": "No visible disease symptoms; foliage is uniformly green with no lesions.",
        "causes": "N/A — plant is healthy.",
        "treatment": "Continue crop rotation and monitor foliage regularly, especially in humid weather.",
    },
    "Raspberry___healthy": {
        "crop": "Raspberry", "condition": "Healthy",
        "symptoms": "No visible disease symptoms; canes and foliage appear vigorous with no spotting or dieback.",
        "causes": "N/A — plant is healthy.",
        "treatment": "Maintain pruning for airflow and monitor canes for cane blight or rust.",
    },
    "Soybean___healthy": {
        "crop": "Soybean", "condition": "Healthy",
        "symptoms": "No visible disease symptoms; leaves are uniformly green with no spotting or rust pustules.",
        "causes": "N/A — plant is healthy.",
        "treatment": "Continue crop rotation and scout regularly for rust or leaf spot diseases.",
    },
    "Squash___Powdery_mildew": {
        "crop": "Squash", "condition": "Powdery Mildew (fungal)",
        "symptoms": "White, powdery fungal patches on leaves and stems, which can eventually cover the entire leaf surface.",
        "causes": "Caused by fungi such as Podosphaera xanthii and Erysiphe cichoracearum, favored by warm, dry days combined with high humidity or cool nights.",
        "treatment": "Apply sulfur, potassium bicarbonate, or neem oil at first sign. Improve spacing/airflow and choose resistant varieties.",
    },
    "Strawberry___Leaf_scorch": {
        "crop": "Strawberry", "condition": "Leaf Scorch (fungal)",
        "symptoms": "Small, irregular purple spots that merge into larger scorched, dry-looking blotches on leaves.",
        "causes": "Caused by the fungus Diplocarpon earlianum, favored by wet, humid conditions and dense plantings.",
        "treatment": "Remove infected leaves after harvest, avoid overhead watering, ensure good spacing for airflow, and apply fungicides (captan) if severe.",
    },
    "Strawberry___healthy": {
        "crop": "Strawberry", "condition": "Healthy",
        "symptoms": "No visible disease symptoms; leaves are uniformly green with no spotting.",
        "causes": "N/A — plant is healthy.",
        "treatment": "Continue mulching, spacing, and routine leaf inspection.",
    },
    "Tomato___Bacterial_spot": {
        "crop": "Tomato", "condition": "Bacterial Spot (bacterial)",
        "symptoms": "Small, dark, greasy-looking spots on leaves; raised, rough, scabby spots on fruit.",
        "causes": "Caused by Xanthomonas species, spread by splashing water/rain and favored by warm, humid weather.",
        "treatment": "Use disease-free seed/transplants, apply copper-based bactericides, rotate crops, and avoid overhead irrigation.",
    },
    "Tomato___Early_blight": {
        "crop": "Tomato", "condition": "Early Blight (fungal)",
        "symptoms": "Dark, concentric 'target-spot' lesions on lower/older leaves, often with yellowing around them.",
        "causes": "Caused by the fungus Alternaria solani, favored by warm temperatures, humidity, and plant stress.",
        "treatment": "Remove lower infected leaves, mulch to prevent soil splash, rotate crops, and apply fungicides (chlorothalonil/mancozeb) preventatively.",
    },
    "Tomato___Late_blight": {
        "crop": "Tomato", "condition": "Late Blight (oomycete)",
        "symptoms": "Water-soaked lesions that spread rapidly and turn brown-black, with white fungal growth visible on leaf undersides in humid conditions.",
        "causes": "Caused by the oomycete Phytophthora infestans, favored by cool, wet weather.",
        "treatment": "Remove and destroy infected plants immediately, avoid overhead watering, and apply protectant fungicides preventatively during cool, wet weather.",
    },
    "Tomato___Leaf_Mold": {
        "crop": "Tomato", "condition": "Leaf Mold (fungal)",
        "symptoms": "Pale yellow spots on the upper leaf surface with olive-green to grayish-purple velvety mold on the underside.",
        "causes": "Caused by the fungus Passalora fulva, favored by high humidity and poor air circulation (common in greenhouses).",
        "treatment": "Improve greenhouse/field ventilation, reduce humidity, space plants for airflow, and apply fungicides (chlorothalonil) if needed.",
    },
    "Tomato___Septoria_leaf_spot": {
        "crop": "Tomato", "condition": "Septoria Leaf Spot (fungal)",
        "symptoms": "Small, circular spots with dark borders and tan/gray centers, often with tiny black specks inside; mainly on lower/older leaves.",
        "causes": "Caused by the fungus Septoria lycopersici, favored by warm, wet, humid conditions and splashing water.",
        "treatment": "Remove infected lower leaves, mulch to reduce soil splash, rotate crops, and apply fungicides (chlorothalonil/copper) at first sign.",
    },
    "Tomato___Spider_mites Two-spotted_spider_mite": {
        "crop": "Tomato", "condition": "Two-Spotted Spider Mite (pest)",
        "symptoms": "Fine yellow/white stippling or speckling on leaves, sometimes with fine webbing on the underside of leaves in heavy infestations.",
        "causes": "Caused by an infestation of the two-spotted spider mite (Tetranychus urticae), favored by hot, dry conditions.",
        "treatment": "Spray with insecticidal soap or horticultural oil, increase humidity, and introduce predatory mites for biological control in severe infestations.",
    },
    "Tomato___Target_Spot": {
        "crop": "Tomato", "condition": "Target Spot (fungal)",
        "symptoms": "Brown lesions with concentric target-like rings on leaves, stems, and fruit.",
        "causes": "Caused by the fungus Corynespora cassiicola, favored by warm, humid conditions.",
        "treatment": "Remove infected debris, improve airflow through pruning/spacing, and apply fungicides (chlorothalonil/azoxystrobin) if disease pressure is high.",
    },
    "Tomato___Tomato_Yellow_Leaf_Curl_Virus": {
        "crop": "Tomato", "condition": "Tomato Yellow Leaf Curl Virus (viral)",
        "symptoms": "Upward curling and yellowing of leaves; stunted, bushy plant growth; reduced fruit set.",
        "causes": "Caused by Tomato yellow leaf curl virus (TYLCV), transmitted by the silverleaf/sweetpotato whitefly (Bemisia tabaci).",
        "treatment": "No cure exists; remove and destroy infected plants, control whitefly populations with insecticides/reflective mulch, and use resistant varieties.",
    },
    "Tomato___Tomato_mosaic_virus": {
        "crop": "Tomato", "condition": "Tomato Mosaic Virus (viral)",
        "symptoms": "Mottled light-green/dark-green mosaic pattern on leaves, sometimes with curling, distortion, or stunting.",
        "causes": "Caused by Tomato mosaic virus (ToMV), spread mechanically via handling, tools, and contaminated seed (including via tobacco products).",
        "treatment": "No cure exists; remove and destroy infected plants, disinfect tools between plants, wash hands after handling tobacco products, and use resistant varieties.",
    },
    "Tomato___healthy": {
        "crop": "Tomato", "condition": "Healthy",
        "symptoms": "No visible disease symptoms; leaves are uniformly green with no spotting, curling, or mottling.",
        "causes": "N/A — plant is healthy.",
        "treatment": "Continue routine scouting, staking/pruning for airflow, and balanced fertilization.",
    },
}