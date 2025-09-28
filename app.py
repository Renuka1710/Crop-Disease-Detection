from flask import Flask, render_template, request

app = Flask(__name__)

DISEASE_DB = {
    "tomato": {
        "yellow leaves": {
            "disease": "Nitrogen deficiency / Early blight",
            "pesticides": ["Apply balanced NPK fertilizer", "If fungal: Copper oxychloride (follow label)"] ,
            "advice": "Check soil moisture and fertilize. Remove heavily infected leaves."
        },
        "white spots": {
        
            "disease": "Powdery mildew",
            "pesticides": ["Sulfur-based fungicide", "Neem oil as organic option"],
            "advice": "Improve air circulation; avoid overhead watering."
        }
    },
    "cotton": {
        "holes in leaves": {
            "disease": "Caterpillar / Bollworm",
            "pesticides": ["Spinosad (insecticide)", "Bacillus thuringiensis (Bt) for organic control"],
            "advice": "Monitor and use pheromone traps; apply insecticide according to label."
        }
    },
    "rice": {
        "brown spots": {
            "disease": "Brown spot disease (fungal)",
            "pesticides": ["Tricyclazole (fungicide)", "Copper fungicide"],
            "advice": "Use recommended fungicides and maintain proper water levels."
        }
    }
}

@app.route('/', methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        crop = request.form.get("crop", "").strip().lower()
        symptom = request.form.get("symptom", "").strip().lower()

        if not crop or not symptom:
            result = {"error": "Please enter both crop and symptom."}
        else:
            crop_db = DISEASE_DB.get(crop)
            if crop_db and symptom in crop_db:
                result = crop_db[symptom]
                result["crop"] = crop.title()
                result["symptom"] = symptom
            else:
                result = {"disease":"Not Found",
                          "pesticides":["Consult local agricultural extension officer"],
                          "advice":"No match found in database. Consider consulting an expert or uploading a photo for diagnosis."}
                result["crop"] = crop.title()
                result["symptom"] = symptom

        return render_template('result.html', result=result)

    known_crops = sorted(DISEASE_DB.keys())
    return render_template('index.html', known_crops=known_crops)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
