import google.generativeai as genai
from django.conf import settings
from PIL import Image
import time

genai.configure(api_key=settings.GEMINI_API_KEY)

class PlantAnalyzer:

    @staticmethod
    def analyze_plant(image):
        image_data = Image.open(image)
        image_data.thumbnail((512, 512))
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
        max_tries = 3
        for attempt in range(max_tries):
            try:
                response = model.generate_content([image_data,prompt],
                    generation_config=genai.GenerationConfig(
                    max_output_tokens=1024
                ))
                return response.text
            except Exception as e:
                if attempt < max_tries - 1:
                    time.sleep(5)
                else:
                    raise