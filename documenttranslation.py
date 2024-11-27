from transformers import MBartForConditionalGeneration, MBartTokenizer
from pdf2image import convert_from_path
import pytesseract
from docx import Document
import torch
from PyPDF2 import PdfReader

class DocumentTranslator:
    def __init__(self):
        # Initialize the model and tokenizer
        self.model_name = "facebook/mbart-large-50-many-to-many-mmt"
        self.model = MBartForConditionalGeneration.from_pretrained(self.model_name)
        self.tokenizer = MBartTokenizer.from_pretrained(self.model_name)
        
        # Set source and target languages
        self.src_lang = "en_XX"
        self.tgt_lang = "hi_IN"
        
    def extract_text(self, file_path):
        """Extract text from different document formats"""
        file_extension = file_path.split('.')[-1].lower()
        
        if file_extension == 'txt':
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
                
        elif file_extension == 'pdf':
            # Using PyPDF2 instead of pdf2image
            reader = PdfReader(file_path)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            return text
            
        elif file_extension in ['docx', 'doc']:
            doc = Document(file_path)
            return " ".join([paragraph.text for paragraph in doc.paragraphs])
            
        else:
            raise ValueError("Unsupported file format")

    def translate_text(self, text, max_length=1024):
        """Translate text from English to Hindi"""
        # Encode the text
        encoded = self.tokenizer(text, return_tensors="pt", max_length=max_length, truncation=True)
        
        # Set the language tokens
        self.tokenizer.src_lang = self.src_lang
        encoded = self.tokenizer(text, return_tensors="pt")
        
        # Generate translation
        generated_tokens = self.model.generate(
            **encoded,
            forced_bos_token_id=self.tokenizer.lang_code_to_id[self.tgt_lang],
            max_length=max_length,
            num_beams=5,
            length_penalty=1.0
        )
        
        # Decode the generated tokens
        translation = self.tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)[0]
        return translation

    def translate_document(self, file_path):
        """Main method to translate document"""
        try:
            # Extract text from document
            text = self.extract_text(file_path)
            
            # Split text into chunks if it's too long
            chunks = [text[i:i+1000] for i in range(0, len(text), 1000)]
            
            # Translate each chunk
            translated_chunks = []
            for chunk in chunks:
                translated_chunk = self.translate_text(chunk)
                translated_chunks.append(translated_chunk)
            
            # Combine translated chunks
            final_translation = " ".join(translated_chunks)
            return final_translation
            
        except Exception as e:
            return f"Translation failed: {str(e)}"

# Example usage
def main():
    translator = DocumentTranslator()
    
    # Example translation
    file_path = "SP-PPT-SCRIPT.pdf"  # Replace with actual file path
    translated_text = translator.translate_document(file_path)
    
    # Save translated text
    with open("translated_document.txt", "w", encoding="utf-8") as f:
        f.write(translated_text)

if __name__ == "__main__":
    main()