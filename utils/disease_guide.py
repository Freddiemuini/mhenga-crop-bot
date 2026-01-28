import logging

logger = logging.getLogger(__name__)

# Crop name mapping - helps identify crops from various naming conventions
CROP_NAME_MAP = {
    "maize": {"name": "Maize (Corn)", "scientific": "Zea mays"},
    "corn": {"name": "Maize (Corn)", "scientific": "Zea mays"},
    "zea": {"name": "Maize (Corn)", "scientific": "Zea mays"},
    "tomato": {"name": "Tomato", "scientific": "Solanum lycopersicum"},
    "solanum": {"name": "Tomato", "scientific": "Solanum lycopersicum"},
    "wheat": {"name": "Wheat", "scientific": "Triticum aestivum"},
    "triticum": {"name": "Wheat", "scientific": "Triticum aestivum"},
    "rice": {"name": "Rice", "scientific": "Oryza sativa"},
    "oryza": {"name": "Rice", "scientific": "Oryza sativa"},
    "cassava": {"name": "Cassava", "scientific": "Manihot esculenta"},
    "manihot": {"name": "Cassava", "scientific": "Manihot esculenta"},
    "banana": {"name": "Banana", "scientific": "Musa spp."},
    "plantain": {"name": "Banana/Plantain", "scientific": "Musa spp."},
    "musa": {"name": "Banana", "scientific": "Musa spp."},
    "bean": {"name": "Bean", "scientific": "Phaseolus vulgaris"},
    "phaseolus": {"name": "Bean", "scientific": "Phaseolus vulgaris"},
    "legume": {"name": "Legumes", "scientific": "Fabaceae"},
    "potato": {"name": "Potato", "scientific": "Solanum tuberosum"},
    "onion": {"name": "Onion", "scientific": "Allium cepa"},
    "cabbage": {"name": "Cabbage", "scientific": "Brassica oleracea"},
    "kale": {"name": "Kale", "scientific": "Brassica oleracea var. acephala"},
    "pepper": {"name": "Pepper", "scientific": "Capsicum spp."},
    "capsicum": {"name": "Pepper", "scientific": "Capsicum spp."},
    "carrot": {"name": "Carrot", "scientific": "Daucus carota"},
    "spinach": {"name": "Spinach", "scientific": "Spinacia oleracea"},
    "lettuce": {"name": "Lettuce", "scientific": "Lactuca sativa"},
    "pumpkin": {"name": "Pumpkin", "scientific": "Cucurbita moschata"},
    "squash": {"name": "Squash", "scientific": "Cucurbita spp."},
    "cucumber": {"name": "Cucumber", "scientific": "Cucumis sativus"},
    "watermelon": {"name": "Watermelon", "scientific": "Citrullus lanatus"},
    "melon": {"name": "Melon", "scientific": "Cucumis melo"},
    "sorghum": {"name": "Sorghum", "scientific": "Sorghum bicolor"},
    "millet": {"name": "Millet", "scientific": "Pennisetum glaucum"},
    "sugarcane": {"name": "Sugarcane", "scientific": "Saccharum officinarum"},
    "coconut": {"name": "Coconut", "scientific": "Cocos nucifera"},
}

DISEASE_GUIDE = {
    "corn_leaf_blight": {
        "crop_name": "Maize (Corn)",
        "crop_scientific_name": "Zea mays",
        "description": "A fungal disease that causes elongated lesions on maize leaves, reducing photosynthesis.",
        "aliases": ["corn_blight", "maize_blight", "leaf_blight", "corn", "maize", "blight"],
        "prevention": [
            "Rotate crops with non-host plants",
            "Use resistant maize varieties",
            "Remove infected crop residues"
        ],
        "control": [
            "Apply fungicides such as mancozeb or azoxystrobin",
            "Improve field drainage to reduce humidity"
        ]
    },
    "maize_rust": {
        "crop_name": "Maize (Corn)",
        "crop_scientific_name": "Zea mays",
        "description": "A fungal disease producing reddish-brown pustules on maize leaves.",
        "aliases": ["corn_rust", "wheat_rust_like"],
        "prevention": [
            "Plant resistant maize varieties",
            "Avoid overcrowding crops"
        ],
        "control": [
            "Spray fungicides like triazoles (tebuconazole, propiconazole)",
            "Monitor and remove heavily infected plants"
        ]
    },
    "tomato_early_blight": {
        "crop_name": "Tomato",
        "crop_scientific_name": "Solanum lycopersicum",
        "description": "A common tomato disease causing concentric dark spots on leaves and fruit rot.",
        "aliases": ["tomato_blight", "early_blight"],
        "prevention": [
            "Use disease-free seeds",
            "Practice crop rotation",
            "Mulch to prevent soil splash"
        ],
        "control": [
            "Spray copper-based fungicides",
            "Remove and destroy infected plants"
        ]
    },
    "tomato_late_blight": {
        "crop_name": "Tomato",
        "crop_scientific_name": "Solanum lycopersicum",
        "description": "A devastating tomato and potato disease with water-soaked lesions that spread rapidly.",
        "aliases": ["late_blight", "potato_blight", "tomato_rot"],
        "prevention": [
            "Plant resistant varieties",
            "Ensure good field ventilation"
        ],
        "control": [
            "Apply fungicides like chlorothalonil or metalaxyl",
            "Remove infected plants immediately"
        ]
    },
    "wheat_rust": {
        "crop_name": "Wheat",
        "crop_scientific_name": "Triticum aestivum",
        "description": "A fungal disease causing reddish-brown or yellow pustules on wheat leaves and stems.",
        "aliases": ["wheat_leaf_rust", "stem_rust", "stripe_rust"],
        "prevention": [
            "Plant resistant wheat varieties",
            "Practice crop rotation",
            "Clean agricultural tools"
        ],
        "control": [
            "Apply triadimefon or tebuconazole fungicides",
            "Remove heavily infected plants"
        ]
    },
    "rice_leaf_blast": {
        "crop_name": "Rice",
        "crop_scientific_name": "Oryza sativa",
        "description": "A destructive fungal disease causing diamond-shaped lesions on rice leaves.",
        "aliases": ["rice_blast", "leaf_blast"],
        "prevention": [
            "Use resistant rice varieties",
            "Maintain proper water management",
            "Avoid excessive nitrogen fertilizer"
        ],
        "control": [
            "Apply triazole fungicides",
            "Remove infected plants immediately"
        ]
    },
    "cassava_mosaic": {
        "crop_name": "Cassava",
        "crop_scientific_name": "Manihot esculenta",
        "description": "A viral disease causing yellowing and mosaic patterns on cassava leaves.",
        "aliases": ["cassava_leaf_mosaic", "mosaic", "cassava_disease"],
        "prevention": [
            "Use virus-free cuttings",
            "Control whitefly vectors",
            "Practice crop rotation"
        ],
        "control": [
            "Remove and destroy infected plants",
            "Use resistant cassava varieties"
        ]
    },
    "banana_sigatoka": {
        "crop_name": "Banana",
        "crop_scientific_name": "Musa spp.",
        "description": "A fungal leaf spot disease causing dark streaks and lesions on banana leaves.",
        "aliases": ["sigatoka", "banana_leaf_spot", "black_sigatoka"],
        "prevention": [
            "Use disease-free planting material",
            "Practice good field sanitation",
            "Avoid overhead irrigation"
        ],
        "control": [
            "Apply mancozeb or chlorothalonil fungicides",
            "Remove affected leaves"
        ]
    },
    "powdery_mildew": {
        "crop_name": "Legumes/Vegetables",
        "crop_scientific_name": "Various",
        "description": "A fungal disease causing white powdery coating on leaves and stems.",
        "aliases": ["mildew", "white_mold", "powdery_mildew_fungal"],
        "prevention": [
            "Ensure good air circulation",
            "Avoid overcrowding",
            "Use resistant varieties"
        ],
        "control": [
            "Spray sulfur-based fungicides",
            "Apply neem oil"
        ]
    },
    "downy_mildew": {
        "crop_name": "Vegetables/Crops",
        "crop_scientific_name": "Various",
        "description": "A fungal disease causing yellow lesions with gray mold on leaf undersides.",
        "aliases": ["downy_fungal", "mold", "gray_mold"],
        "prevention": [
            "Improve field drainage",
            "Increase air circulation",
            "Use disease-resistant varieties"
        ],
        "control": [
            "Apply metalaxyl or mancozeb fungicides",
            "Remove infected leaves"
        ]
    },
    "bean_rust": {
        "crop_name": "Bean",
        "crop_scientific_name": "Phaseolus vulgaris",
        "description": "A fungal disease producing rust-colored pustules on bean leaves and pods.",
        "aliases": ["rust", "bean_disease"],
        "prevention": [
            "Plant resistant bean varieties",
            "Ensure good air circulation",
            "Remove plant debris"
        ],
        "control": [
            "Apply sulfur or copper fungicides",
            "Remove heavily infected plants"
        ]
    },
    "common_bean_blight": {
        "crop_name": "Bean",
        "crop_scientific_name": "Phaseolus vulgaris",
        "description": "A bacterial disease causing angular brown lesions on bean leaves.",
        "aliases": ["bean_blight", "bacterial_blight"],
        "prevention": [
            "Use disease-free seeds",
            "Rotate crops",
            "Avoid working in wet fields"
        ],
        "control": [
            "Remove infected plants",
            "Use resistant varieties"
        ]
    },
    "potato_late_blight": {
        "crop_name": "Potato",
        "crop_scientific_name": "Solanum tuberosum",
        "description": "A serious fungal disease causing water-soaked lesions on potato leaves and tubers.",
        "aliases": ["potato_blight"],
        "prevention": [
            "Use certified seed potatoes",
            "Ensure good soil drainage",
            "Avoid overhead irrigation"
        ],
        "control": [
            "Apply fungicides like metalaxyl or mancozeb",
            "Remove infected plants",
            "Use resistant varieties"
        ]
    },
    "bacterial_wilt": {
        "crop_name": "Vegetables/Crops",
        "crop_scientific_name": "Various",
        "description": "A serious bacterial disease causing wilting and death of plants.",
        "aliases": ["wilt", "bacterial_disease"],
        "prevention": [
            "Control insect vectors",
            "Use resistant varieties",
            "Practice crop rotation"
        ],
        "control": [
            "Remove infected plants immediately",
            "Control vectors using pesticides"
        ]
    },
    "leaf_curl": {
        "crop_name": "Vegetables/Crops",
        "crop_scientific_name": "Various",
        "description": "A viral disease causing curling and distortion of leaves.",
        "aliases": ["curl", "viral_disease"],
        "prevention": [
            "Control whitefly and aphid vectors",
            "Use resistant varieties",
            "Plant early to avoid peak vector populations"
        ],
        "control": [
            "Remove infected plants",
            "Apply appropriate pesticides for vector control"
        ]
    },
    "anthracnose": {
        "crop_name": "Various Crops",
        "crop_scientific_name": "Various",
        "description": "A fungal disease causing dark, sunken lesions on leaves, stems, and fruit.",
        "aliases": ["anthrax", "fungal_spot"],
        "prevention": [
            "Use disease-free seeds",
            "Improve field drainage",
            "Remove plant debris"
        ],
        "control": [
            "Apply copper or benzimidazole fungicides",
            "Remove infected plants"
        ]
    },
    "septoria_leaf_spot": {
        "crop_name": "Wheat/Cereals",
        "crop_scientific_name": "Triticum aestivum",
        "description": "A fungal disease causing circular lesions with dark borders on wheat leaves.",
        "aliases": ["leaf_spot", "septoria"],
        "prevention": [
            "Use resistant wheat varieties",
            "Remove crop residues",
            "Practice crop rotation"
        ],
        "control": [
            "Apply triazole fungicides",
            "Remove infected leaves"
        ]
    },
    "fusarium_wilt": {
        "crop_name": "Various Crops",
        "crop_scientific_name": "Various",
        "description": "A soil-borne fungal disease causing wilting and discoloration of vascular tissue.",
        "aliases": ["fusarium", "wilting"],
        "prevention": [
            "Use disease-free seeds and soil",
            "Rotate crops with non-susceptible plants",
            "Maintain proper drainage"
        ],
        "control": [
            "Remove infected plants",
            "Solarize soil in serious cases"
        ]
    },
    "black_spot": {
        "crop_name": "Various Crops",
        "crop_scientific_name": "Various",
        "description": "A fungal disease causing dark spots on leaves and stems.",
        "aliases": ["spot", "fungal_spot"],
        "prevention": [
            "Ensure good air circulation",
            "Avoid overhead irrigation",
            "Remove infected leaves"
        ],
        "control": [
            "Apply copper or sulfur fungicides",
            "Improve field sanitation"
        ]
    },
    "white_fly_damage": {
        "crop_name": "Various Crops",
        "crop_scientific_name": "Bemisia tabaci",
        "description": "Damage caused by whitefly insects feeding on plant sap.",
        "aliases": ["whitefly", "insect_damage"],
        "prevention": [
            "Use yellow sticky traps",
            "Plant resistant varieties",
            "Maintain field sanitation"
        ],
        "control": [
            "Apply insecticidal soaps",
            "Use neem oil",
            "Release natural predators"
        ]
    },
    "aphid_infestation": {
        "crop_name": "Various Crops",
        "crop_scientific_name": "Aphidoidea",
        "description": "Damage caused by aphid insects that suck plant sap and transmit viruses.",
        "aliases": ["aphid", "pest"],
        "prevention": [
            "Use reflective mulches",
            "Encourage natural predators",
            "Monitor plants regularly"
        ],
        "control": [
            "Spray insecticidal soaps",
            "Use neem oil",
            "Release ladybugs or lacewings"
        ]
    },
    "mite_damage": {
        "crop_name": "Various Crops",
        "crop_scientific_name": "Acari",
        "description": "Damage caused by spider mites that cause yellowing and stippling of leaves.",
        "aliases": ["mite", "spider_mite"],
        "prevention": [
            "Maintain adequate humidity",
            "Ensure good air circulation",
            "Remove affected leaves"
        ],
        "control": [
            "Apply sulfur-based acaricides",
            "Use neem oil",
            "Release predatory mites"
        ]
    },
    "healthy_crop": {
        "crop_name": "Healthy Plant",
        "crop_scientific_name": "N/A",
        "description": "The plant appears to be healthy with no visible signs of disease.",
        "aliases": ["healthy", "normal", "good", "ok"],
        "prevention": [
            "Continue good farming practices",
            "Monitor regularly for early signs of disease",
            "Maintain proper irrigation and fertilization"
        ],
        "control": [
            "No disease control measures needed",
            "Continue preventive practices"
        ]
    }
}


def get_disease_info(disease_name):
    """Get disease information from the guide with enhanced matching"""
    if not disease_name:
        return get_default_disease_info()
    
    disease_key = disease_name.lower().strip().replace(" ", "_").replace("-", "_")
    
    logger.info(f"Looking up disease: '{disease_name}' (normalized: '{disease_key}')")
    
    # Try exact match first
    if disease_key in DISEASE_GUIDE:
        result = DISEASE_GUIDE[disease_key]
        logger.info(f"Found exact match: {disease_key} -> Crop: {result['crop_name']}")
        return result
    
    # Try alias match
    for guide_key, disease_info in DISEASE_GUIDE.items():
        aliases = disease_info.get("aliases", [])
        if disease_key in aliases:
            logger.info(f"Found alias match: {disease_key} -> {guide_key} -> Crop: {disease_info['crop_name']}")
            return disease_info
    
    # Try to extract crop name and match from disease name
    for crop_keyword, crop_info in CROP_NAME_MAP.items():
        if crop_keyword in disease_key:
            logger.info(f"Found crop keyword '{crop_keyword}' in disease name: {disease_key}")
            # Find disease matching this crop
            for guide_key, disease_info in DISEASE_GUIDE.items():
                if crop_keyword in guide_key or crop_keyword in disease_info.get("crop_name", "").lower():
                    logger.info(f"Matched with disease for crop {crop_keyword}: {guide_key}")
                    return disease_info
            # If no disease found for this crop, return a generic response with crop info
            return {
                "crop_name": crop_info["name"],
                "crop_scientific_name": crop_info["scientific"],
                "description": f"A disease affecting {crop_info['name']}. Please consult a local agricultural officer for specific identification.",
                "prevention": ["General good farming practices", "Crop rotation", "Use resistant varieties"],
                "control": ["Consult local agricultural extension officer for specific treatment"]
            }
    
    # Try partial match with better scoring
    best_match = None
    best_score = 0
    
    for guide_key, disease_info in DISEASE_GUIDE.items():
        # Check if normalized key contains or is contained in disease_key
        if disease_key in guide_key or guide_key in disease_key:
            score = len(set(disease_key) & set(guide_key)) / max(len(disease_key), len(guide_key))
            if score > best_score:
                best_score = score
                best_match = disease_info
    
    if best_match and best_score > 0.5:
        logger.info(f"Found partial match with score {best_score} -> Crop: {best_match['crop_name']}")
        return best_match
    
    # Try word-based matching
    disease_words = set(disease_key.split("_"))
    for guide_key, disease_info in DISEASE_GUIDE.items():
        guide_words = set(guide_key.split("_"))
        # If at least 50% of words match
        if disease_words & guide_words:
            match_ratio = len(disease_words & guide_words) / max(len(disease_words), len(guide_words))
            if match_ratio > 0.4:
                logger.info(f"Found word-based match: {guide_key} (ratio: {match_ratio}) -> Crop: {disease_info['crop_name']}")
                return disease_info
    
    logger.warning(f"No match found for disease: '{disease_name}'. Returning default info.")
    return get_default_disease_info()


def get_default_disease_info():
    """Return default disease information"""
    return {
        "crop_name": "Unknown Crop",
        "crop_scientific_name": "Unknown",
        "description": "No detailed information available. Please consult a local agricultural extension officer or provide a clearer image for better identification.",
        "prevention": [
            "General good farming practices:",
            "- Crop rotation with non-host plants",
            "- Use resistant/certified varieties",
            "- Proper field sanitation"
        ],
        "control": [
            "Recommended actions:",
            "- Consult local agricultural extension officer for identification and treatment",
            "- Monitor affected crops closely",
            "- Remove heavily infected plants if necessary"
        ]
    }
