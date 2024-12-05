import re
from docx import Document
import os

class DocumentProcessor:
    def __init__(self, file_path):
        self.file_path = file_path
        self.supported_extensions = {'.docx', '.txt', '.vtt', '.doc'}
        
    def process(self):
        """Main processing method"""
        # Get file extension
        _, ext = os.path.splitext(self.file_path)
        if ext not in self.supported_extensions:
            raise ValueError("Unsupported file type")
        
        # Extract text based on file type
        if ext == '.docx':
            text = self._extract_docx()
        else:
            text = self._extract_txt()
        
        # Process the text
        cleaned_text = self._remove_timestamps(text)
        formatted_text = self._format_text(cleaned_text)
        
        return formatted_text
    
    def _extract_docx(self):
        """Extract text from Word document"""
        doc = Document(self.file_path)
        return '\n'.join(paragraph.text for paragraph in doc.paragraphs)
    
    def _extract_txt(self):
        """Extract text from txt file"""
        with open(self.file_path, 'r', encoding='utf-8') as file:
            return file.read()
    
    def _remove_timestamps(self, text):
        """Remove transcript-style timestamps and markers"""
        # Remove line numbers
        text = re.sub(r'^\d+\s*$', '', text, flags=re.MULTILINE)
        
        # Remove timestamp lines (including arrows)
        text = re.sub(r'\d{2}:\d{2}:\d{2}\.\d{3}\s*-->\s*\d{2}:\d{2}:\d{2}\.\d{3}', '', text)
        
        # Remove any remaining timestamps in various formats
        patterns = [
            r'\d{2}:\d{2}:\d{2}\.\d{3}',  # 00:00:00.000
            r'\[\d{2}:\d{2}:\d{2}\]',      # [00:00:00]
            r'\(\d{2}:\d{2}\s*(?:AM|PM)\)', # (12:34 PM)
            r'\d{2}:\d{2}:\d{2}',           # 00:00:00
            r'\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}', # 2024-01-01 15:30:45
        ]
        
        for pattern in patterns:
            text = re.sub(pattern, '', text)
        
        return text
    
    def _format_text(self, text):
        """Format the text for better readability"""
        # Remove empty lines
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        
        # Join lines that appear to be part of the same sentence
        formatted_lines = []
        current_sentence = []
        
        for line in lines:
            # If line ends with punctuation or appears complete, start a new sentence
            if (line.endswith(('.', '!', '?')) or 
                len(line) > 50 or  # Longer lines might be complete thoughts
                line.endswith((':'))):  # Speaker indicators
                if current_sentence:
                    current_sentence.append(line)
                    formatted_lines.append(' '.join(current_sentence))
                    current_sentence = []
                else:
                    formatted_lines.append(line)
            else:
                current_sentence.append(line)
        
        # Add any remaining sentence
        if current_sentence:
            formatted_lines.append(' '.join(current_sentence))
        
        # Join paragraphs with double newlines for readability
        formatted_text = '\n\n'.join(formatted_lines)
        
        # Clean up any multiple spaces
        formatted_text = re.sub(r'\s+', ' ', formatted_text)
        
        # Clean up "uh" and "um" fillers (optional)
        formatted_text = re.sub(r'\s*,?\s*uh\s*,?\s*', ' ', formatted_text, flags=re.IGNORECASE)
        formatted_text = re.sub(r'\s*,?\s*um\s*,?\s*', ' ', formatted_text, flags=re.IGNORECASE)

        # Add line break after each sentence
        formatted_text = re.sub(r'\.(?=\s|$)', '.\n', formatted_text)
        
        return formatted_text.strip()