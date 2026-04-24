import google.generativeai as genai
import os
import json
import time
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def extract_pdf_data(file_path):
    if not os.path.exists(file_path):
        print(f"Error: File not found at {file_path}")
        return None
        
    # Thay đổi model name để tránh lỗi 404 trên các phiên bản API cũ
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    prompt = """
Analyze this document and extract the Title, Author, Main Topics, and any Tables. 
Output exactly as a JSON object matching this exact format:
{
    "document_id": "pdf-doc-001",
    "content": "Title: [Title]\\n\\nMain Topics: [Main Topics]\\n\\nTables: [Tables]",
    "source_type": "PDF",
    "author": "[Insert author name here or Unknown]",
    "timestamp": null,
    "source_metadata": {"original_file": "lecture_notes.pdf"}
}
"""
    
    print(f"Uploading {file_path} to Gemini...")
    try:
        pdf_file = genai.upload_file(path=file_path)
        print("Generating content from PDF using Gemini...")
        max_retries = 2
        base_delay = 2
        
        for attempt in range(max_retries):
            try:
                response = model.generate_content([pdf_file, prompt])
                content_text = response.text
                
                # Simple cleanup if the response is wrapped in markdown json block
                if content_text.startswith("```json"):
                    content_text = content_text[7:]
                if content_text.endswith("```"):
                    content_text = content_text[:-3]
                if content_text.startswith("```"):
                    content_text = content_text[3:]
                    
                extracted_data = json.loads(content_text.strip())
                return extracted_data
                
            except Exception as e:
                error_str = str(e).lower()
                if "429" in error_str or "quota" in error_str or "exhausted" in error_str:
                    if attempt < max_retries - 1:
                        delay = base_delay * (2 ** attempt)
                        print(f"Rate limited (429). Retrying in {delay} seconds...")
                        time.sleep(delay)
                    else:
                        print(f"Failed to extract PDF data after {max_retries} attempts due to rate limits: {e}")
                        break
                else:
                    print(f"Generation error: {e}")
                    break
    except Exception as e:
        print(f"Failed to process with Gemini: {e}")

    # ==========================================
    # FALLBACK: OPENAI
    # ==========================================
    print("Gemini failed. Falling back to OpenAI...")
    openai_key = os.getenv("OPENAI_API_KEY")
    if not openai_key:
        print("Error: OPENAI_API_KEY not found in .env. Cannot use fallback.")
        return None
        
    try:
        import PyPDF2
        from openai import OpenAI
        
        print("Extracting text locally for OpenAI...")
        text_content = ""
        with open(file_path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                extracted = page.extract_text()
                if extracted:
                    text_content += extracted + "\n"
                    
        client = OpenAI(api_key=openai_key)
        
        # Limit token size for safety
        openai_prompt = prompt + "\n\nHere is the document content:\n" + text_content[:20000]
        
        print("Generating content using OpenAI (gpt-4o-mini)...")
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a data extraction assistant. Output only valid JSON matching the user's schema."},
                {"role": "user", "content": openai_prompt}
            ],
            response_format={"type": "json_object"}
        )
        
        content_text = response.choices[0].message.content
        extracted_data = json.loads(content_text.strip())
        return extracted_data
        
    except ImportError:
        print("Missing libraries! To use the OpenAI fallback, please run: pip install openai PyPDF2")
        return None
    except Exception as e:
        print(f"OpenAI fallback failed: {e}")
        return None
