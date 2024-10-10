"""
Install the Google AI Python SDK

$ pip install google-generativeai
"""

import os
import google.generativeai as genai

genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# Create the model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  generation_config=generation_config,
  # safety_settings = Adjust safety settings
  # See https://ai.google.dev/gemini-api/docs/safety-settings
)

response = model.generate_content([
  "You are a product marketer targeting a Gen Z audience. Create exciting and\nfresh advertising copy for products and their simple description. Keep copy\nunder a few sentences long.",
  "Product: Eco-Friendly Phone Case",
  "Product copy: Protect your phone and the planet! Our Eco-Friendly Phone Case is made from 100% biodegradable materials, giving your device the ultimate defense while reducing waste. Style meets sustainability—switch to a case that cares!",
  "Product: Portable Blender",
  "Product copy: Blend on the go! Our Portable Blender is your new kitchen buddy, perfect for whipping up smoothies, protein shakes, and more wherever you are. With its sleek design and USB rechargeable battery, you can fuel your adventures with fresh goodness anytime, anywhere!",
  "Product: Vintage baseball cap",
  "Product copy: ",
])

print(response.text)