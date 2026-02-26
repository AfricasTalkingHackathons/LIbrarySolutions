"""
Summary Generation Service

Generates intelligent book summaries using Gemini AI:
- Quick summaries for SMS/USSD (50-100 words)
- Medium summaries for WhatsApp (150-300 words)
- Detailed chapter summaries
- Key takeaways and themes
"""

import os
from typing import Dict, Optional, List
from dataclasses import dataclass
from dotenv import load_dotenv

try:
    from google import genai
except ImportError:
    raise ImportError("Install google-genai: pip install google-genai")

load_dotenv()


@dataclass
class Summary:
    """Summary result"""
    quick: str          # 50-100 words for SMS
    medium: str         # 150-300 words for WhatsApp
    detailed: str       # 500+ words comprehensive
    key_points: List[str]  # Bullet points
    themes: List[str]   # Main themes
    target_audience: str   # Who should read this


class SummaryService:
    """Generate book summaries using Gemini AI"""
    
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY is not set in .env")
        
        self.client = genai.Client(api_key=api_key)
        self.model = "gemini-2.5-flash"
        
        print(f"✓ Summary Service initialized")
    
    def generate_summary(
        self,
        text: str,
        title: str = None,
        author: str = None,
        context: str = None
    ) -> Summary:
        """
        Generate multi-level summaries of a book or text
        
        Args:
            text: Book content or excerpt
            title: Book title
            author: Author name
            context: Additional context (genre, subject, etc.)
        
        Returns:
            Summary object with multiple detail levels
        """
        # Build prompt
        book_info = ""
        if title:
            book_info += f"Title: {title}\n"
        if author:
            book_info += f"Author: {author}\n"
        if context:
            book_info += f"Context: {context}\n"
        
        prompt = f"""You are a librarian creating summaries for rural community members.

{book_info}

Text to summarize:
{text[:5000]}  

Generate summaries at different lengths:

1. QUICK SUMMARY (50-100 words):
Write a very brief SMS-friendly summary focusing on the core message.

2. MEDIUM SUMMARY (150-300 words):
Write a WhatsApp-friendly summary with more detail about the content and value.

3. DETAILED SUMMARY (500+ words):
Write a comprehensive summary covering main topics, arguments, and insights.

4. KEY POINTS:
List 5-7 key takeaways as bullet points.

5. THEMES:
List 3-5 main themes or subjects covered.

6. TARGET AUDIENCE:
Who would benefit most from reading this? (e.g., "Secondary school students studying biology")

Format your response as JSON:
{{
  "quick": "...",
  "medium": "...",
  "detailed": "...",
  "key_points": ["point 1", "point 2", ...],
  "themes": ["theme1", "theme2", ...],
  "target_audience": "..."
}}
"""
        
        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt
            )
            
            # Parse response
            import json
            result_text = response.text.strip()
            
            # Extract JSON from code blocks if present
            if "```json" in result_text:
                result_text = result_text.split("```json")[1].split("```")[0].strip()
            elif "```" in result_text:
                result_text = result_text.split("```")[1].split("```")[0].strip()
            
            summary_data = json.loads(result_text)
            
            return Summary(
                quick=summary_data.get("quick", ""),
                medium=summary_data.get("medium", ""),
                detailed=summary_data.get("detailed", ""),
                key_points=summary_data.get("key_points", []),
                themes=summary_data.get("themes", []),
                target_audience=summary_data.get("target_audience", "General readers")
            )
            
        except Exception as e:
            print(f"Error generating summary: {e}")
            # Fallback to simple summarization
            return self._fallback_summary(text, title, author)
    
    def _fallback_summary(
        self,
        text: str,
        title: str = None,
        author: str = None
    ) -> Summary:
        """Simple fallback if AI fails"""
        # Take first paragraph as quick summary
        paragraphs = text.split("\n\n")
        quick = paragraphs[0][:200] if paragraphs else text[:200]
        
        # Take first few paragraphs as medium
        medium = "\n\n".join(paragraphs[:3])[:500] if len(paragraphs) > 1 else text[:500]
        
        # Full text as detailed (truncated)
        detailed = text[:2000]
        
        book_info = ""
        if title:
            book_info += f"{title}"
        if author:
            book_info += f" by {author}"
        
        return Summary(
            quick=f"{book_info}. {quick}",
            medium=f"{book_info}. {medium}",
            detailed=detailed,
            key_points=["Summary not available"],
            themes=["General"],
            target_audience="General readers"
        )
    
    def summarize_chapter(
        self,
        chapter_text: str,
        chapter_number: int = None,
        chapter_title: str = None
    ) -> str:
        """
        Generate a chapter summary
        
        Args:
            chapter_text: Chapter content
            chapter_number: Chapter number
            chapter_title: Chapter title
        
        Returns:
            Chapter summary (100-200 words)
        """
        chapter_info = ""
        if chapter_number:
            chapter_info += f"Chapter {chapter_number}"
        if chapter_title:
            chapter_info += f": {chapter_title}"
        
        prompt = f"""Summarize this chapter in 100-200 words for a student:

{chapter_info}

{chapter_text[:3000]}

Focus on:
- Main concepts covered
- Important examples or case studies
- How it connects to the overall book

Summary:"""
        
        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt
            )
            return response.text.strip()
            
        except Exception as e:
            print(f"Error summarizing chapter: {e}")
            # Fallback: return first paragraph
            paragraphs = chapter_text.split("\n\n")
            return paragraphs[0][:300] if paragraphs else chapter_text[:300]
    
    def extract_key_concepts(
        self,
        text: str,
        subject: str = None
    ) -> List[str]:
        """
        Extract key concepts/terms from text
        
        Args:
            text: Text to analyze
            subject: Subject area (physics, biology, etc.)
        
        Returns:
            List of key concepts
        """
        subject_info = f" (Subject: {subject})" if subject else ""
        
        prompt = f"""Extract 5-10 key concepts, terms, or ideas from this text{subject_info}.

Text:
{text[:2000]}

List the concepts as a JSON array:
["concept1", "concept2", ...]
"""
        
        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt
            )
            
            import json
            result_text = response.text.strip()
            
            # Extract JSON
            if "```json" in result_text:
                result_text = result_text.split("```json")[1].split("```")[0].strip()
            elif "```" in result_text:
                result_text = result_text.split("```")[1].split("```")[0].strip()
            elif "[" in result_text and "]" in result_text:
                # Find the JSON array
                start = result_text.index("[")
                end = result_text.rindex("]") + 1
                result_text = result_text[start:end]
            
            concepts = json.loads(result_text)
            return concepts
            
        except Exception as e:
            print(f"Error extracting concepts: {e}")
            return []
    
    def compare_books(
        self,
        book1_text: str,
        book2_text: str,
        book1_title: str = "Book 1",
        book2_title: str = "Book 2"
    ) -> str:
        """
        Compare two books and highlight differences/similarities
        
        Args:
            book1_text: First book content
            book2_text: Second book content
            book1_title: First book title
            book2_title: Second book title
        
        Returns:
            Comparison summary
        """
        prompt = f"""Compare these two books and explain:
1. Main similarities
2. Key differences
3. Which might be better for different readers

{book1_title}:
{book1_text[:1500]}

{book2_title}:
{book2_text[:1500]}

Comparison (200-300 words):"""
        
        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt
            )
            return response.text.strip()
            
        except Exception as e:
            print(f"Error comparing books: {e}")
            return f"Unable to compare {book1_title} and {book2_title}"


def get_summary_service():
    """Get summary service instance"""
    return SummaryService()


if __name__ == "__main__":
    # Test summary generation
    print("📝 Summary Generation Service")
    service = SummaryService()
    
    sample_text = """
    Thermodynamics is the branch of physics that deals with heat, work, temperature, 
    and the statistical behavior of systems with a large number of particles. 
    
    The first law of thermodynamics states that energy cannot be created or destroyed,
    only converted from one form to another. This is also known as the law of 
    conservation of energy.
    
    The second law introduces the concept of entropy, stating that the total entropy
    of an isolated system can never decrease over time. This law explains why certain
    processes are irreversible.
    """
    
    summary = service.generate_summary(
        text=sample_text,
        title="Introduction to Thermodynamics",
        author="Dr. Smith",
        context="Physics textbook for university students"
    )
    
    print(f"\n✓ Quick Summary:\n{summary.quick}\n")
    print(f"✓ Key Points: {', '.join(summary.key_points)}")
    print(f"✓ Themes: {', '.join(summary.themes)}")
