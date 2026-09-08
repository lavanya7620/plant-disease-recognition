"""
Human-readable descriptions and general treatment/management guidance for each
class in the New Plant Diseases Dataset. This is general horticultural
guidance, not a substitute for advice from a local agricultural extension
office — actual treatment can depend on region, severity, and crop variety.
"""

DISEASE_INFO = {
    "Apple___Apple_scab": {
        "crop": "Apple", "condition": "Apple Scab (fungal)",
        "description": "Olive-green to black scabby spots on leaves and fruit, caused by Venturia inaequalis.",
        "treatment": "Remove and destroy fallen leaves in autumn to reduce spores. Apply a protectant fungicide (e.g. captan or myclobutanil) starting at bud break. Choose scab-resistant varieties when replanting.",
    },
    "Apple___Black_rot": {
        "crop": "Apple", "condition": "Black Rot (fungal)",
        "description": "Purple-bordered leaf spots and rotting fruit with concentric rings, caused by Botryosphaeria obtusa.",
        "treatment": "Prune out dead/cankered wood and mummified fruit. Apply fungicides (captan/thiophanate-methyl) during the growing season. Improve air circulation via pruning.",
    },
    "Apple___Cedar_apple_rust": {
        "crop": "Apple", "condition": "Cedar Apple Rust (fungal)",
        "description": "Bright orange-yellow spots on leaves; requires a nearby cedar/juniper host to complete its life cycle.",
        "treatment": "Remove nearby juniper/cedar hosts if feasible. Apply fungicide (myclobutanil) from pink bud stage through several weeks after petal fall. Plant resistant apple cultivars.",
    },
    "Apple___healthy": {
        "crop": "Apple", "condition": "Healthy",
        "description": "No visible disease symptoms detected.",
        "treatment": "Maintain regular monitoring, balanced fertilization, and good orchard sanitation.",
    },
    "Blueberry___healthy": {
        "crop": "Blueberry", "condition": "Healthy",
        "description": "No visible disease symptoms detected.",
        "treatment": "Maintain acidic soil pH, adequate mulching, and routine pruning for airflow.",
    },
    "Cherry_(including_sour)___Powdery_mildew": {
        "crop": "Cherry", "condition": "Powdery Mildew (fungal)",
        "description": "White powdery fungal growth on leaves and shoots, caused by Podosphaera clandestina.",
        "treatment": "Apply sulfur-based or potassium bicarbonate fungicides. Prune to improve air circulation and avoid excess nitrogen fertilization.",
    },
    "Cherry_(including_sour)___healthy": {
        "crop": "Cherry", "condition": "Healthy",
        "description": "No visible disease symptoms detected.",
        "treatment": "Continue routine pruning and monitoring for early signs of mildew.",
    },
    "Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot": {
        "crop": "Corn (Maize)", "condition": "Gray Leaf Spot (fungal)",
        "description": "Rectangular grayish-tan lesions along leaf veins, caused by Cercospora zeae-maydis.",
        "treatment": "Rotate crops away from corn for 1-2 years, use resistant hybrids, and apply foliar fungicides (strobilurin or triazole) if disease pressure is high.",
    },
    "Corn_(maize)___Common_rust_": {
        "crop": "Corn (Maize)", "condition": "Common Rust (fungal)",
        "description": "Small, reddish-brown, powdery pustules on both leaf surfaces, caused by Puccinia sorghi.",
        "treatment": "Plant rust-resistant hybrids. Fungicide application is rarely needed unless infection is severe and early in the season.",
    },
    "Corn_(maize)___Northern_Leaf_Blight": {
        "crop": "Corn (Maize)", "condition": "Northern Leaf Blight (fungal)",
        "description": "Long, cigar-shaped gray-green to tan lesions on leaves, caused by Exserohilum turcicum.",
        "treatment": "Use resistant hybrids, rotate crops, till under residue, and apply fungicide if detected early with favorable disease conditions (humid, moderate temps).",
    },
    "Corn_(maize)___healthy": {
        "crop": "Corn (Maize)", "condition": "Healthy",
        "description": "No visible disease symptoms detected.",
        "treatment": "Continue crop rotation and monitoring practices.",
    },
    "Grape___Black_rot": {
        "crop": "Grape", "condition": "Black Rot (fungal)",
        "description": "Circular brown leaf lesions and shriveled, mummified berries, caused by Guignardia bidwellii.",
        "treatment": "Remove mummified berries and infected canes during dormant pruning. Apply fungicides (mancozeb/myclobutanil) starting at bud break through veraison.",
    },
    "Grape___Esca_(Black_Measles)": {
        "crop": "Grape", "condition": "Esca / Black Measles (fungal)",
        "description": "Tiger-stripe leaf discoloration and dark spotting on berries, caused by a complex of wood-rotting fungi.",
        "treatment": "No curative fungicide exists; remove and destroy severely infected vines/wood, avoid large pruning wounds, and protect wounds with a fungicidal paste.",
    },
    "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)": {
        "crop": "Grape", "condition": "Leaf Blight / Isariopsis Leaf Spot (fungal)",
        "description": "Dark brown angular leaf spots that can cause premature defoliation.",
        "treatment": "Improve canopy airflow via leaf removal/pruning, apply copper-based or mancozeb fungicides, and remove fallen infected leaves.",
    },
    "Grape___healthy": {
        "crop": "Grape", "condition": "Healthy",
        "description": "No visible disease symptoms detected.",
        "treatment": "Maintain canopy management and routine disease scouting.",
    },
    "Orange___Haunglongbing_(Citrus_greening)": {
        "crop": "Orange", "condition": "Huanglongbing / Citrus Greening (bacterial)",
        "description": "Blotchy mottled leaves and lopsided, bitter fruit, spread by the Asian citrus psyllid.",
        "treatment": "No cure exists; remove and destroy infected trees to prevent spread, and control the psyllid vector with approved insecticides. Use certified disease-free nursery stock.",
    },
    "Peach___Bacterial_spot": {
        "crop": "Peach", "condition": "Bacterial Spot (bacterial)",
        "description": "Small dark angular spots on leaves and pitted lesions on fruit, caused by Xanthomonas campestris.",
        "treatment": "Plant resistant varieties, apply copper-based bactericides during dormancy, and avoid overhead irrigation that spreads bacteria.",
    },
    "Peach___healthy": {
        "crop": "Peach", "condition": "Healthy",
        "description": "No visible disease symptoms detected.",
        "treatment": "Continue routine orchard sanitation and monitoring.",
    },
    "Pepper,_bell___Bacterial_spot": {
        "crop": "Bell Pepper", "condition": "Bacterial Spot (bacterial)",
        "description": "Small water-soaked spots that turn brown/scabby on leaves and fruit, caused by Xanthomonas species.",
        "treatment": "Use certified disease-free seed, apply copper-based bactericides, rotate crops, and avoid working in fields when foliage is wet.",
    },
    "Pepper,_bell___healthy": {
        "crop": "Bell Pepper", "condition": "Healthy",
        "description": "No visible disease symptoms detected.",
        "treatment": "Maintain crop rotation and monitor for early spotting symptoms.",
    },
    "Potato___Early_blight": {
        "crop": "Potato", "condition": "Early Blight (fungal)",
        "description": "Dark concentric-ringed 'target' spots on older leaves, caused by Alternaria solani.",
        "treatment": "Rotate crops, remove infected debris, ensure balanced fertilization, and apply fungicides (chlorothalonil/mancozeb) at first sign of disease.",
    },
    "Potato___Late_blight": {
        "crop": "Potato", "condition": "Late Blight (oomycete)",
        "description": "Water-soaked lesions that rapidly turn brown/black with white fungal growth on leaf undersides, caused by Phytophthora infestans.",
        "treatment": "Destroy infected plants promptly, avoid overhead irrigation, apply protectant fungicides (chlorothalonil/copper) preventatively in humid weather, and plant certified seed potatoes.",
    },
    "Potato___healthy": {
        "crop": "Potato", "condition": "Healthy",
        "description": "No visible disease symptoms detected.",
        "treatment": "Continue crop rotation and monitor foliage regularly, especially in humid weather.",
    },
    "Raspberry___healthy": {
        "crop": "Raspberry", "condition": "Healthy",
        "description": "No visible disease symptoms detected.",
        "treatment": "Maintain pruning for airflow and monitor canes for cane blight or rust.",
    },
    "Soybean___healthy": {
        "crop": "Soybean", "condition": "Healthy",
        "description": "No visible disease symptoms detected.",
        "treatment": "Continue crop rotation and scout regularly for rust or leaf spot diseases.",
    },
    "Squash___Powdery_mildew": {
        "crop": "Squash", "condition": "Powdery Mildew (fungal)",
        "description": "White powdery patches on leaves and stems, common in warm, dry conditions with high humidity at night.",
        "treatment": "Apply sulfur, potassium bicarbonate, or neem oil at first sign. Improve spacing/airflow and choose resistant varieties.",
    },
    "Strawberry___Leaf_scorch": {
        "crop": "Strawberry", "condition": "Leaf Scorch (fungal)",
        "description": "Small purple spots that merge into scorched, dry-looking leaf blotches, caused by Diplocarpon earlianum.",
        "treatment": "Remove infected leaves after harvest, avoid overhead watering, ensure good spacing for airflow, and apply fungicides (captan) if severe.",
    },
    "Strawberry___healthy": {
        "crop": "Strawberry", "condition": "Healthy",
        "description": "No visible disease symptoms detected.",
        "treatment": "Continue mulching, spacing, and routine leaf inspection.",
    },
    "Tomato___Bacterial_spot": {
        "crop": "Tomato", "condition": "Bacterial Spot (bacterial)",
        "description": "Small dark greasy spots on leaves and raised scabby spots on fruit, caused by Xanthomonas species.",
        "treatment": "Use disease-free seed/transplants, apply copper-based bactericides, rotate crops, and avoid overhead irrigation.",
    },
    "Tomato___Early_blight": {
        "crop": "Tomato", "condition": "Early Blight (fungal)",
        "description": "Dark concentric 'target-spot' lesions on lower/older leaves, caused by Alternaria solani.",
        "treatment": "Remove lower infected leaves, mulch to prevent soil splash, rotate crops, and apply fungicides (chlorothalonil/mancozeb) preventatively.",
    },
    "Tomato___Late_blight": {
        "crop": "Tomato", "condition": "Late Blight (oomycete)",
        "description": "Water-soaked, rapidly-spreading lesions with white mold on leaf undersides, caused by Phytophthora infestans.",
        "treatment": "Remove and destroy infected plants immediately, avoid overhead watering, and apply protectant fungicides preventatively during cool, wet weather.",
    },
    "Tomato___Leaf_Mold": {
        "crop": "Tomato", "condition": "Leaf Mold (fungal)",
        "description": "Pale yellow spots on upper leaf surface with olive-green velvety mold underneath, favored by high humidity.",
        "treatment": "Improve greenhouse/field ventilation, reduce humidity, space plants for airflow, and apply fungicides (chlorothalonil) if needed.",
    },
    "Tomato___Septoria_leaf_spot": {
        "crop": "Tomato", "condition": "Septoria Leaf Spot (fungal)",
        "description": "Small circular spots with dark borders and gray centers, mainly on lower leaves.",
        "treatment": "Remove infected lower leaves, mulch to reduce soil splash, rotate crops, and apply fungicides (chlorothalonil/copper) at first sign.",
    },
    "Tomato___Spider_mites Two-spotted_spider_mite": {
        "crop": "Tomato", "condition": "Two-Spotted Spider Mite (pest)",
        "description": "Fine yellow stippling on leaves with possible webbing, caused by Tetranychus urticae infestation.",
        "treatment": "Spray with insecticidal soap or horticultural oil, increase humidity, and introduce predatory mites for biological control in severe infestations.",
    },
    "Tomato___Target_Spot": {
        "crop": "Tomato", "condition": "Target Spot (fungal)",
        "description": "Brown lesions with concentric rings on leaves, stems, and fruit, caused by Corynespora cassiicola.",
        "treatment": "Remove infected debris, improve airflow through pruning/spacing, and apply fungicides (chlorothalonil/azoxystrobin) if disease pressure is high.",
    },
    "Tomato___Tomato_Yellow_Leaf_Curl_Virus": {
        "crop": "Tomato", "condition": "Tomato Yellow Leaf Curl Virus (viral)",
        "description": "Upward curling, yellowing, and stunted leaves; spread by whiteflies.",
        "treatment": "No cure exists; remove and destroy infected plants, control whitefly populations with insecticides/reflective mulch, and use resistant varieties.",
    },
    "Tomato___Tomato_mosaic_virus": {
        "crop": "Tomato", "condition": "Tomato Mosaic Virus (viral)",
        "description": "Mottled light/dark green mosaic pattern on leaves with possible curling and stunting.",
        "treatment": "No cure exists; remove and destroy infected plants, disinfect tools between plants, wash hands after handling tobacco products, and use resistant varieties.",
    },
    "Tomato___healthy": {
        "crop": "Tomato", "condition": "Healthy",
        "description": "No visible disease symptoms detected.",
        "treatment": "Continue routine scouting, staking/pruning for airflow, and balanced fertilization.",
    },
}
