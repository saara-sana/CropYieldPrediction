import joblib
import pandas as pd
import gradio as gr

# ==========================================================
# Load Trained Model and Label Encoders
# ==========================================================

model = joblib.load("models/random_forest.pkl")
label_encoders = joblib.load("models/label_encoders.pkl")

# ==========================================================
# Prediction Function
# ==========================================================

def predict_yield(
    crop,
    crop_year,
    season,
    state,
    area,
    annual_rainfall,
    fertilizer,
    pesticide,
):
    # ----------------------------
    # Input Validation
    # ----------------------------
    if crop_year is None or area is None or annual_rainfall is None \
        or fertilizer is None or pesticide is None:
        return "❌ Please fill all numeric fields."

    if (
        crop_year < 0
        or area < 0
        or annual_rainfall < 0
        or fertilizer < 0
        or pesticide < 0
    ):
        return "❌ Values cannot be negative."

    # ----------------------------
    # Encode categorical features
    # ----------------------------
    crop = label_encoders["Crop"].transform([crop])[0]
    season = label_encoders["Season"].transform([season])[0]
    state = label_encoders["State"].transform([state])[0]

    # ----------------------------
    # Create input dataframe
    # ----------------------------
    input_data = pd.DataFrame([{
        "Crop": crop,
        "Crop_Year": crop_year,
        "Season": season,
        "State": state,
        "Area": area,
        "Annual_Rainfall": annual_rainfall,
        "Fertilizer": fertilizer,
        "Pesticide": pesticide
    }])

    prediction = model.predict(input_data)[0]

    return f"🌾 Estimated Yield: {prediction:.2f} Tons/Hectare"


# ==========================================================
# Dropdown Lists
# ==========================================================

crop_list = list(label_encoders["Crop"].classes_)
season_list = list(label_encoders["Season"].classes_)
state_list = list(label_encoders["State"].classes_)

# ==========================================================
# User Interface
# ==========================================================

with gr.Blocks(title="SASI_AIML Crop Yield Prediction") as demo:

    # ==========================
    # Header
    # ==========================

    with gr.Row():

        with gr.Column(scale=1):

            gr.Image(
                value="app/assets/sasi_logo.png",
                show_label=False,
                interactive=False,
                width=110,
                height=110
            )

        with gr.Column(scale=6):

            gr.Markdown("""
# 🌾 SASI_AIML Crop Yield Prediction

### AI-powered Crop Yield Prediction using Machine Learning
""")

    gr.Markdown("---")

    # ==========================
    # Main Layout
    # ==========================

    with gr.Row():

        # --------------------------
        # Left Column
        # --------------------------

        with gr.Column():

            gr.Markdown("## 🌱 Crop Information")

            with gr.Group():

                crop = gr.Dropdown(
                    choices=crop_list,
                    label="🌾 Crop"
                )

                crop_year = gr.Number(
                    label="📅 Crop Year",
                    placeholder="Example: 2020",
                    value=None
                )

                season = gr.Dropdown(
                    choices=season_list,
                    label="🌦️ Season"
                )

                state = gr.Dropdown(
                    choices=state_list,
                    label="📍 State"
                )

                area = gr.Number(
                    label="🌱 Area (hectares)",
                    placeholder="Example: 500",
                    value=None
                )

                annual_rainfall = gr.Number(
                    label="🌧️ Annual Rainfall (mm)",
                    placeholder="Example: 1200",
                    value=None
                )

                fertilizer = gr.Number(
                    label="🧪 Fertilizer",
                    placeholder="Example: 350",
                    value=None
                )

                pesticide = gr.Number(
                    label="🐛 Pesticide",
                    placeholder="Example: 20",
                    value=None
                )

        # --------------------------
        # Right Column
        # --------------------------

        with gr.Column():

            gr.Markdown("## 📈 Prediction Result")

            prediction_output = gr.Textbox(
                label="🌾 Estimated Yield",
                lines=1,
                interactive=False
            )

            predict_btn = gr.Button(
                "🚀 Predict Yield",
                variant="primary"
            )

            clear_btn = gr.ClearButton(
                components=[
                    crop,
                    crop_year,
                    season,
                    state,
                    area,
                    annual_rainfall,
                    fertilizer,
                    pesticide,
                    prediction_output
                ],
                value="🗑 Clear"
            )

    # ==========================
    # Button Event
    # ==========================

    predict_btn.click(
        fn=predict_yield,
        inputs=[
            crop,
            crop_year,
            season,
            state,
            area,
            annual_rainfall,
            fertilizer,
            pesticide
        ],
        outputs=prediction_output
    )

    # ==========================
    # Footer
    # ==========================

    gr.Markdown("""
---

<center>

### Developed by **SASI_AIML**

Machine Learning Project • Crop Yield Prediction

</center>
""")

# ==========================================================

demo.launch()