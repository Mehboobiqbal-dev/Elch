import os
import sys

# Ensure Vertex path for this test regardless of .env loaded
os.environ['USE_VERTEX_GENAI'] = os.environ.get('USE_VERTEX_GENAI', 'true')
os.environ['GOOGLE_CLOUD_PROJECT'] = os.environ.get('GOOGLE_CLOUD_PROJECT', 'spendly-cc9f4')
os.environ['GOOGLE_CLOUD_LOCATION'] = os.environ.get('GOOGLE_CLOUD_LOCATION', 'global')

from core.config import settings
from gemini import generate_text


def main():
    print(f"USE_VERTEX_GENAI={settings.USE_VERTEX_GENAI}")
    print(f"PROJECT={settings.GOOGLE_CLOUD_PROJECT} LOCATION={settings.GOOGLE_CLOUD_LOCATION}")
    try:
        out = generate_text("Say 'ready' if this Vertex AI path works.")
        print("\n--- OUTPUT ---\n")
        print(out)
        print("\n--- END OUTPUT ---\n")
    except Exception as e:
        import traceback
        print("\nERROR:", e)
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
