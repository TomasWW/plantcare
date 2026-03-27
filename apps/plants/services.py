import google.generativeai as genai
from django.conf import settings
from PIL import Image

genai.configure(api_key=settings.GEMINI_API_KEY)

class PlantAnalyzer:

    @staticmethod
    def analyze_plant(image):
        image_data = Image.open(image)
        model = genai.GenerativeModel('models/gemini-2.0-flash-lite')
        prompt= """
        Your are a plant expert. Analyze this plant image and respond ONLY with a JSON object with this structure:
{
    "scientific_name": "",
    "common_name": "",
    "care_data": {
        "watering": "",
        "light": "",
        "temperature": "",
        "humidity": ""
    }
}
        """
        response = model.generate_content([image_data,prompt],
            generation_config=genai.GenerationConfig(
                max_output_tokens=1024
            )
        )
        return response.text    