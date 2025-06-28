import os
import pathway as pw
from phi.model.groq import Groq

class key:
    def __init__(self, groq_api_key, license_key):
        self.gemini_api_key = groq_api_key
        pw.set_license_key(license_key)
        os.environ['GROQ_API_KEY'] = groq_api_key
        os.environ["TESSDATA_PREFIX"] = "/usr/share/tesseract/tessdata/"

key_instance = key("your_groq_api_key", "your-license-key")