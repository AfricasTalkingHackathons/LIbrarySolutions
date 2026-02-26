"""
Translation Service

Provides multilingual translation for:
- Book content and summaries
- SMS/USSD messages
- Metadata and descriptions

Supports major African and international languages.
"""

import os
from typing import Dict, List, Optional
from dataclasses import dataclass
from dotenv import load_dotenv

try:
    from google import genai
except ImportError:
    raise ImportError("Install google-genai: pip install google-genai")

load_dotenv()


# Language codes and names
SUPPORTED_LANGUAGES = {
    "en": "English",
    "sw": "Swahili",
    "fr": "French",
    "ar": "Arabic",
    "ha": "Hausa",
    "yo": "Yoruba",
    "ig": "Igbo",
    "am": "Amharic",
    "zu": "Zulu",
    "xh": "Xhosa",
    "so": "Somali",
    "es": "Spanish",
    "pt": "Portuguese",
}


@dataclass
class Translation:
    """Translation result"""
    original_text: str
    translated_text: str
    source_lang: str
    target_lang: str
    confidence: float = 1.0


class TranslationService:
    """Translate text using Gemini AI"""
    
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY is not set in .env")
        
        self.client = genai.Client(api_key=api_key)
        self.model = "gemini-2.5-flash"
        
        print(f"✓ Translation Service initialized")
    
    def translate(
        self,
        text: str,
        target_lang: str,
        source_lang: str = "en",
        preserve_formatting: bool = False
    ) -> Translation:
        """
        Translate text to target language
        
        Args:
            text: Text to translate
            target_lang: Target language code (e.g., 'sw' for Swahili)
            source_lang: Source language code (default: 'en')
            preserve_formatting: Keep original formatting (paragraphs, bullets, etc.)
        
        Returns:
            Translation object
        """
        if target_lang not in SUPPORTED_LANGUAGES:
            raise ValueError(f"Unsupported language: {target_lang}")
        
        if source_lang == target_lang:
            return Translation(
                original_text=text,
                translated_text=text,
                source_lang=source_lang,
                target_lang=target_lang,
                confidence=1.0
            )
        
        source_name = SUPPORTED_LANGUAGES.get(source_lang, source_lang)
        target_name = SUPPORTED_LANGUAGES[target_lang]
        
        format_instruction = ""
        if preserve_formatting:
            format_instruction = """
Important: Preserve the original formatting including:
- Paragraph breaks
- Bullet points and numbering
- Line breaks
- Special formatting
"""
        
        prompt = f"""Translate the following text from {source_name} to {target_name}.

{format_instruction}

Provide a natural, culturally appropriate translation that maintains the original meaning.

Original text:
{text}

Translation in {target_name}:"""
        
        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt
            )
            
            translated_text = response.text.strip()
            
            return Translation(
                original_text=text,
                translated_text=translated_text,
                source_lang=source_lang,
                target_lang=target_lang,
                confidence=0.95  # High confidence for AI translation
            )
            
        except Exception as e:
            print(f"Translation error: {e}")
            # Return original text as fallback
            return Translation(
                original_text=text,
                translated_text=text,
                source_lang=source_lang,
                target_lang=target_lang,
                confidence=0.0
            )
    
    def translate_summary(
        self,
        summary: str,
        target_lang: str,
        summary_type: str = "quick"
    ) -> str:
        """
        Translate a book summary to target language
        
        Args:
            summary: Summary text
            target_lang: Target language code
            summary_type: Type of summary (quick, medium, detailed)
        
        Returns:
            Translated summary
        """
        # Add context about summary type
        if summary_type == "quick":
            context = "This is a brief SMS-friendly book summary (50-100 words)."
        elif summary_type == "medium":
            context = "This is a WhatsApp-friendly book summary (150-300 words)."
        else:
            context = "This is a detailed book summary."
        
        translation = self.translate(
            text=f"{context}\n\n{summary}",
            target_lang=target_lang,
            preserve_formatting=True
        )
        
        # Remove the context from translation
        translated = translation.translated_text
        if "\n\n" in translated:
            parts = translated.split("\n\n", 1)
            if len(parts) > 1:
                translated = parts[1]
        
        return translated
    
    def translate_batch(
        self,
        texts: List[str],
        target_lang: str,
        source_lang: str = "en"
    ) -> List[Translation]:
        """
        Translate multiple texts in batch
        
        Args:
            texts: List of texts to translate
            target_lang: Target language code
            source_lang: Source language code
        
        Returns:
            List of Translation objects
        """
        translations = []
        
        for text in texts:
            translation = self.translate(
                text=text,
                target_lang=target_lang,
                source_lang=source_lang
            )
            translations.append(translation)
        
        return translations
    
    def detect_language(self, text: str) -> str:
        """
        Detect the language of text
        
        Args:
            text: Text to analyze
        
        Returns:
            Language code (e.g., 'en', 'sw')
        """
        prompt = f"""Detect the language of this text and respond with ONLY the ISO 639-1 language code.

Supported codes: {', '.join(SUPPORTED_LANGUAGES.keys())}

Text:
{text[:500]}

Language code:"""
        
        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt
            )
            
            lang_code = response.text.strip().lower()
            
            # Validate it's a supported language
            if lang_code in SUPPORTED_LANGUAGES:
                return lang_code
            else:
                return "en"  # Default to English
                
        except Exception as e:
            print(f"Language detection error: {e}")
            return "en"  # Default to English
    
    def translate_metadata(
        self,
        metadata: Dict,
        target_lang: str
    ) -> Dict:
        """
        Translate book metadata
        
        Args:
            metadata: Metadata dictionary
            target_lang: Target language code
        
        Returns:
            Translated metadata dictionary
        """
        translated = metadata.copy()
        
        # Fields to translate
        translatable_fields = [
            "title",
            "author",
            "description",
            "summary",
            "subject",
            "tags"
        ]
        
        for field in translatable_fields:
            if field in metadata and metadata[field]:
                value = metadata[field]
                
                if isinstance(value, str):
                    translation = self.translate(
                        text=value,
                        target_lang=target_lang
                    )
                    translated[field] = translation.translated_text
                    
                elif isinstance(value, list):
                    # Translate list items (e.g., tags)
                    translations = self.translate_batch(
                        texts=value,
                        target_lang=target_lang
                    )
                    translated[field] = [t.translated_text for t in translations]
        
        return translated
    
    def get_multilingual_summary(
        self,
        summary: str,
        languages: List[str]
    ) -> Dict[str, str]:
        """
        Get summary in multiple languages
        
        Args:
            summary: Summary text in English
            languages: List of target language codes
        
        Returns:
            Dictionary mapping language codes to translations
        """
        multilingual = {"en": summary}  # Original in English
        
        for lang in languages:
            if lang != "en":
                translated = self.translate_summary(
                    summary=summary,
                    target_lang=lang
                )
                multilingual[lang] = translated
        
        return multilingual
    
    def localize_message(
        self,
        message_template: str,
        target_lang: str,
        variables: Dict[str, str] = None
    ) -> str:
        """
        Localize a message template with variables
        
        Args:
            message_template: Template with {variable} placeholders
            target_lang: Target language code
            variables: Dictionary of variable values
        
        Returns:
            Localized message
        """
        # First, translate the template
        translation = self.translate(
            text=message_template,
            target_lang=target_lang
        )
        
        translated_template = translation.translated_text
        
        # Fill in variables if provided
        if variables:
            try:
                localized = translated_template.format(**variables)
            except KeyError:
                # If placeholder names changed in translation, use original
                localized = message_template.format(**variables)
        else:
            localized = translated_template
        
        return localized


def get_translation_service():
    """Get translation service instance"""
    return TranslationService()


if __name__ == "__main__":
    # Test translation
    print("🌍 Translation Service")
    service = TranslationService()
    
    # Test English to Swahili
    text = "Welcome to the library. Search for books using natural language."
    
    translation = service.translate(
        text=text,
        target_lang="sw",
        source_lang="en"
    )
    
    print(f"\nOriginal ({translation.source_lang}): {translation.original_text}")
    print(f"Translated ({translation.target_lang}): {translation.translated_text}")
    print(f"Confidence: {translation.confidence}")
    
    # Test language detection
    swahili_text = "Karibu maktabani. Tafuta vitabu kwa lugha ya kawaida."
    detected = service.detect_language(swahili_text)
    print(f"\nDetected language: {detected} ({SUPPORTED_LANGUAGES.get(detected)})")
    
    # Test multilingual summary
    summary = "This book teaches physics concepts through real-world examples."
    multilingual = service.get_multilingual_summary(
        summary=summary,
        languages=["sw", "fr"]
    )
    
    print("\n✓ Multilingual summary generated:")
    for lang, text in multilingual.items():
        print(f"  {SUPPORTED_LANGUAGES.get(lang, lang)}: {text}")
