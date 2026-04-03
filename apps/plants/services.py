from openai import OpenAI
from django.conf import settings
import logging
import time
import base64
    
logger= logging.getLogger(__name__)
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=settings.OPENROUTER_API_KEY,
)
models = {
    "nvidia/nemotron-nano-12b-v2-vl:free": "Nvidia Nemotron Nano VL",
    "google/gemma-3-27b-it:free": "Google Gemma 3 27B IT",
    "google/gemma-3-4b-it:free": "Google Gemma 3 4B IT",
    "google/gemma-3-12b-it:free": "Google Gemma 3 12B IT",
    "nvidia/llama-nemotron-embed-vl-1b-v2:free": "NVIDIA LLaMA Nemotron Embed VL 1B V2"
    }
class PlantAnalyzer:

    @staticmethod
    def analyze_plant(image):
        image.seek(0)
        image_base64 = base64.b64encode(image.read()).decode('utf-8')
        
        prompt = """
        You are a plant expert. Analyze this plant image and respond ONLY with a JSON object with this structure:
        How frecuent shoud I water it? How much light does it need? What is the ideal temperature and humidity for this plant?
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
        
        max_tries = len(models)
        for attempt,model_id in enumerate(models.keys()):
            logger.info(f"Trying model: {model_id} (attempt {attempt + 1}/{max_tries})")

            try:
                response = client.chat.completions.create(
                    model=model_id,
                    messages=[
                        {
                            "role": "user",
                            "content": [
                                {"type": "text", "text": prompt},
                                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_base64}"}},
                            ]
                        }
                    ]
                )
                return response.choices[0].message.content
            except Exception as e:
                logger.error(f"Model {model_id} failed: {str(e)}")
                if attempt < max_tries - 1:
                    time.sleep(2)
                else:
                    raise Exception(f"All models failed. Last error: {str(e)}")