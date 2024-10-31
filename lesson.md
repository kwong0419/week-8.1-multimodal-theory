# Lesson 8.1: Image Comparison Tool Using Gemini Multimodal Vision

## <ins>Objectives</ins>

This tool provides an intuitive way to analyze and understand the similarities and differences between two images using AI vision capabilities.

## <ins>Setup</ins>  

**Reminder:** Remember to `setup` and `activate` your virtual environment, choose your python interpreter and install the ipykernel. If you do not remember how please refer to the [Python Workspace Setup Instructions](https://github.com/jdrichards-pursuit/python-virtual-environment-setup).

### 1. Retrieving Your API Key

Before we begin, you will need to retrieve your Gemini API key.

If you do not have one, use the following set of instructions to sign up for an account and retrieve your API key.

[Gemini API Key](https://github.com/jdrichards-pursuit/gemini-api-key-acquire?tab=readme-ov-file)

### 2. Setting Up Your Environment Variables

Now that you have your API key, you can set up your environment variables.

Create a new file called `.env` and add the following line of code:

```bash
API_KEY=<your-api-key>
```
### 3. Installing Required Libraries

Another efficient way to install the required libraries is to create a `requirements.txt` file and place your libraries in it.

Create a `requirements.txt` file and add the following libraries (do not include the numbers):

1. python-dotenv
2. requests
3. google-generativeai
4. Pillow

Once you have added the libraries to your `requirements.txt` file, you can install them by running the following command:

```bash
pip install -r requirements.txt
```

The `-r` flag is used to read the requirements from the `requirements.txt` file and install the libraries.


### 4. Importing Required Libraries

Now that you have your API key, you've installed the required libraries and have activated your virtual environment, you can import the required libraries in your `main.py` file.

```python
import os
import requests
import google.generativeai as genai
from urllib.parse import urlparse
from dotenv import load_dotenv
from PIL import Image
```
#### Library Walkthrough

- **`os`**
  - Built-in Python library for OS operations

- **`requests`**
  - Python library for making HTTP requests

- **`google.generativeai`**
  - Official Google Generative AI library
  - Provides access to Gemini's multimodal capabilities

- **`urllib.parse`**
  - Built-in Python library for URL parsing
  - Breaks down URLs into components for security checks

- **`dotenv`**
  - Loads environment variables from `.env` files

- **`PIL`**
  - Python Imaging Library (Pillow)
  - Handles image opening and processing

## <ins>Declaring `setup_api()` Function</ins>

This time we will create a `setup` function to load our API key from the `.env` file as well as initialize and configure our Gemini model which we will later invoke and store in the `model` variable.

```python
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
```

### `setup_api()` Function Walkthrough

#### Environment Setup
- Loads environment variables from `.env` file
- Retrieves API key from environment variables
- Configures Gemini API with the retrieved key

#### Model Configuration
Sets up model parameters:
- `temperature`: 0.4 (lower value for more focused/deterministic outputs)
- `top_p`: 0.99 (controls diversity of outputs)
- `top_k`: 0 (disabled, letting top_p handle output selection)
- `max_output_tokens`: 4096 (maximum length of generated responses)

### Return Value

Returns a configured instance of `GenerativeModel` using:
- Model: 'gemini-1.5-flash'
- Custom configuration settings as defined above


## <ins>Declaring Core Functions</ins>

Next we will declare our core functions for this application. It is best practice to declare functions with a single responsibility and keep your code modular. We will do this by creating a function for each of the following tasks:

- **validate_file()** & **is_valid_url()**: Ensures input images meet format requirements and URL validity
- **download_and_validate_image()**: Securely downloads images from provided URLs
- **analyze_image_similarities()**: Utilizes Gemini's vision capabilities to perform detailed image analysis, examining:
    - Main elements and content
    - Color palettes and tonal qualities
Emotional mood and feeling
    - Common themes and visual elements
    - Complementary aspects between images

## 1. Function Declaration: `is_valid_url()`

```python
def is_valid_url(url_string):
    result = urlparse(url_string)
    return all([result.scheme, result.netloc])
```

### `is_valid_url()` Function Walkthrough

#### URL Parsing
- Uses `urlparse` from the `urllib.parse` module to break down the URL into its components
- Returns a ParseResult object containing various URL components

#### Key Components Checked
1. `result.scheme`:
   - The protocol/scheme part of the URL (e.g., 'http', 'https')
   - Must be present for a valid URL
   - Located before the '://' in a URL

2. `result.netloc`:
   - The network location/hostname part of the URL
   - Must be present for a valid URL
   - Examples: 'www.google.com', 'ai.google.dev'

#### Validation Logic

- Uses `all()` to check if both components are present
- Returns `True` only if both scheme and netloc exist
- Returns `False` if either component is missing

#### Example Usage (do not copy to your `main.py` file)

```python
# Valid URL
is_valid_url('https://ai.google.dev')  # Returns True

# Invalid URLs
is_valid_url('not-a-url')  # Returns False
is_valid_url('http://')    # Returns False (no netloc)
is_valid_url('google.com') # Returns False (no scheme)
```

## 2. Function Declaration: `validate_file()`

```python
def validate_file(filename):
    allowed_extensions = ['.jpg', '.jpeg', '.png', '.gif']
    file_extension = os.path.splitext(filename)[1].lower()
    return file_extension in allowed_extensions
```

### `validate_file()` Function Walkthrough

#### Purpose
The validate_file function performs a security check to ensure that only supported image file formats are processed by the application

#### Key Components

1. `allowed_extensions`:
   - List of approved file extensions ['.jpg', '.jpeg', '.png', '.gif']
   - Case-insensitive validation (uses .lower())
   - Restricted to common image formats

2. `os.path.splitext()`:
   - Splits filename into base and extension
   - Returns tuple of (name, extension)
   - Example: 'image.JPG' -> ('image', '.jpg')

#### Validation Logic
- Extracts file extension using os.path.splitext
- Converts extension to lowercase for case-insensitive comparison
- Returns True only if extension is in allowed list
- Returns False for all other extensions

#### Example Usage

```python
# Valid files
validate_file('photo.jpg')     # Returns True
validate_file('image.PNG')     # Returns True 
validate_file('avatar.gif')    # Returns True

# Invalid files
validate_file('document.pdf')  # Returns False
validate_file('script.py')     # Returns False
validate_file('noextension')   # Returns False
```

## 3. Function Declaration: `download_file_from_url()`

```python
def download_file_from_url(url, filename):
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    return filename
```

### `download_file_from_url()` Function Walkthrough

#### Purpose

The download_file_from_url function securely downloads a file from a URL and saves it locally with streaming support to handle large files efficiently.

#### Key Components

1. `requests.get(url, stream=True)`:
   - Creates a streaming HTTP request
   - `stream=True` prevents loading entire file into memory
   - Returns a response object for handling the download

2. `r.raise_for_status()`:
   - Checks if request was successful (status code 200)
   - Raises an exception for bad HTTP responses
   - Common security practice for handling downloads

3. `iter_content(chunk_size=8192)`:
   - Streams file data in 8KB chunks
   - Memory efficient for large files
   - Standard chunk size for good performance

#### Download Logic

- Opens URL connection with context manager
- Creates/opens local file in binary write mode ('wb')
- Streams content in chunks to local file
- Returns local filename on successful download

#### Example Usage (do not copy to your `main.py` file)

```python
# Download an image file
local_file = download_file_from_url('https://example.com/image.jpg', 'local_image.jpg')

# Handle potential errors
try:
    file = download_file_from_url('https://example.com/file.pdf', 'local.pdf')
except requests.exceptions.RequestException as e:
    print(f"Download failed: {e}")
```

## 4. Function Declaration: `download_and_validate_image()`

```python
def download_and_validate_image(url, filename):
    if not is_valid_url(url):
        raise ValueError("Invalid URL provided")
    
    if not validate_file(filename):
        raise ValueError("Invalid file extension")
        
    return download_file_from_url(url, filename)
```

#### Purpose
The download_and_validate_image function combines URL validation, file extension validation, and secure file downloading into a single robust function to safely handle image downloads.

#### Key Components
1. `URL Validation`:
   - Uses is_valid_url() to check URL structure
   - Validates presence of scheme (http/https) and network location
   - Raises ValueError if URL is malformed

2. `File Extension Validation`:
   - Uses `validate_file()` function to check file extension
   - Ensures file type matches allowed image formats
   - Raises ValueError if extension is not allowed

3. `Secure Download`:
   - Calls download_file_from_url() function only after validations pass
   - Implements streaming download for efficiency
   - Returns local filename on successful download

#### Security Features

- Prevents malicious file uploads
- Validates file types before processing
- Protects against path traversal attacks

#### Example Usage (do not copy to your `main.py` file)

```python

try:
    # Valid image download
    local_file = download_and_validate_image(
        'https://example.com/image.jpg',
        'local_image.jpg'
    )

    # Invalid cases
    download_and_validate_image(
        'not-a-url',  # Raises ValueError for invalid URL
        'image.jpg'
    )
    download_and_validate_image(
        'https://example.com/image.jpg',
        'document.pdf'  # Raises ValueError for invalid extension
    )
except ValueError as e:
    print(f"Validation failed: {e}")
```

## 5. Function Declaration: `analyze_image_similarities()`

```python
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
```

#### Purpose

The analyze_image_similarities function leverages Gemini's multimodal capabilities to perform a detailed comparative analysis between two images, using a carefully structured prompt to ensure consistent and comprehensive results.

#### Key Components

1. `Image Loading`:
   - Uses PIL ('Pillow'  , Python Imaging Library) to open both images
   - Handles images in their native format
   - Prepares images for Gemini model processing

2. `Structured Prompt`:
   - Uses a detailed, multi-part prompt structure
   - Breaks analysis into 5 specific categories
   - Requests clear sectioning in the response

3. `Model Generation`:
   - Combines images and prompt into single generation request
   - Returns text-based analysis
   - Maintains consistent output format

#### Prompt Strategy Analysis

- Uses numbered lists for clear organization
- Employs specific directives for each analysis point
- Requests structured response format
- Builds from concrete (elements) to abstract (mood)
- Ends with synthesis (complementary aspects)

#### Example Usage (do not copy to your `main.py` file)

```python
# Analyze two local images
response = analyze_image_similarities(
    model,
    'path/to/image1.jpg',
    'path/to/image2.jpg'
)

# Print structured analysis
print(response)
```
### 6. `main()` Function Declaration and Execution: 

The next block of code will be the main function that will run the application, including the setup, the core functions and the user interface. The goal is for the user to be able to input two image URLs and get a detailed analysis of their similarities and differences.

When you run the code, you will be prompted to enter the URLs of the two images you want to compare. The application will then download the images, analyze their similarities and differences, and print the results in your terminal.

```python
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
```
#### Purpose
The main function orchestrates the entire image comparison workflow, handling user input, image downloads, analysis, and cleanup in a robust error-handled environment.

#### Key Components
1. `API Initialization`:
   - Sets up Gemini API configuration
   - Creates model instance with predefined parameters
   - Handles potential API setup failures

2. `Image URL Input Loops`:
   - Two separate while loops for each image URL
   - Provides 'quit' option for user exit
   - Validates URLs and file types
   - Downloads images with proper error handling
   - Gives user feedback on successful downloads

3. `Image Analysis`:
   - Calls analyze_image_similarities with downloaded images
   - Uses Gemini's vision capabilities
   - Prints detailed analysis results
   - Handles potential analysis failures

4. `Cleanup Operations`:
   - Removes temporary downloaded images
   - Ensures no residual files remain
   - Maintains system cleanliness

#### Error Handling Strategy
- Uses nested try-except blocks for granular error control
- Provides specific error messages for different failure points
- Ensures graceful exit in case of failures
- Prevents resource leaks through cleanup

## <ins>Running the Code</ins>

1. You will need two image URLs to run the code. You can use the following URLs for testing.

Highly recommended, go to [Unsplash](https://unsplash.com/) and find two images that you like and use the URLs of those images.

Unslplash Instructions:
- choose a photo
- `Ctrl + Click` on the image
- click "Copy Image Address"
- paste the URL into your terminal when prompted

OR

Use the following URLs for testing:

- https://plus.unsplash.com/premium_photo-1664286775680-29687e7b6b92?q=80&w=2938&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D
- https://plus.unsplash.com/premium_photo-1681880956707-b79bf0f57d90?q=80&w=2942&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D

2. In your terminal, run the following command:

```bash
python3 main.py
```
At each prompt, paste in your photo URL.

You should see the text results in your terminal.
