import os
import requests
import google.generativeai as genai
from urllib.parse import urlparse
from dotenv import load_dotenv
from PIL import Image

def setup_api():
    load_dotenv()
    api_key = os.getenv('API_KEY')
    genai.configure(api_key=api_key)

    model_config = {
        "temperature": 0.4,
        "top_p": 0.99,
        "top_k": 0,
        "max_output_tokens": 4096,
    }
    return genai.GenerativeModel('gemini-1.5-flash', generation_config=model_config)

def is_valid_url(url_string):
    result = urlparse(url_string)
    return all([result.scheme, result.netloc])

def validate_file(filename):
    allowed_extensions = ['.jpg', '.jpeg', '.png', '.gif']
    file_extension = os.path.splitext(filename)[1].lower()
    return file_extension in allowed_extensions

def download_file_from_url(url, filename):
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    return filename

def download_and_validate_image(url, filename):
    if not is_valid_url(url):
        raise ValueError("Invalid URL provided")
    
    if not validate_file(filename):
        raise ValueError("Invalid file extension")
        
    return download_file_from_url(url, filename)


def analyze_image_similarities(model, image1_path, image2_path):
    image1 = Image.open(image1_path)
    image2 = Image.open(image2_path)
    
    prompt = """Compare these two images and provide a detailed analysis of their similarities and differences:
    1. Describe the main elements in each image
    2. Compare their color palettes and overall tone
    3. Analyze the mood or emotional feeling of each image
    4. Identify any common themes or visual elements
    5. Suggest how these images might complement each other
    
    Please structure your response in clear sections."""
    
    response = model.generate_content([image1, image2, prompt])
    return response.text


# Main function
def main():
    try:
        # Initialize API
        print("Setting up API...")
        model = setup_api()
        
        # Get URLs from user
        while True:
            url1 = input("Enter the first image URL (or 'quit' to exit): ").strip()
            if url1.lower() == 'quit':
                exit()
            
            try:
                image1_path = download_and_validate_image(url1, "image1.jpg")
                print(f"First image saved as: {image1_path}")
                break
            except Exception as e:
                print(f"Error: {str(e)}")
                
        while True:
            url2 = input("Enter the second image URL (or 'quit' to exit): ").strip()
            if url2.lower() == 'quit':
                exit()
            
            try:
                image2_path = download_and_validate_image(url2, "image2.jpg")
                print(f"Second image saved as: {image2_path}")
                break
            except Exception as e:
                print(f"Error: {str(e)}")
        
        # Analyze similarities
        print("\nAnalyzing image similarities...")
        similarities = analyze_image_similarities(model, image1_path, image2_path)
        print("\nImage Analysis:")
        print(similarities)
        
        # Cleanup
        os.remove(image1_path)
        os.remove(image2_path)
        
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == '__main__':
    main()