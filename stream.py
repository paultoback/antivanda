# stream.py 
import spacy
import requests
from bs4 import BeautifulSoup
from transformers import pipeline

class WikiBitsProcessor:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        self.fact_checker = pipeline("text-classification", 
                                   model="facebook/bart-large-mnli")

    def fetch_article(self, url):
        """Fetch Wikipedia article content"""
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            content = soup.find(id="mw-content-text")
            return content.get_text() if content else None
        except Exception as e:
            print(f"Error fetching article: {e}")
            return None

    def analyze_content(self, text):
        """Analyze article content for issues"""
        doc = self.nlp(text)
        
        issues = []
        
        # Check for citation needs
        sentences = [sent.text for sent in doc.sents]
        for sent in sentences:
            if self._needs_citation(sent):
                issues.append(f"Citation needed: {sent[:100]}...")

        # Check neutrality
        neutrality_score = self._check_neutrality(text)
        if neutrality_score < 0.7:
            issues.append("Article may have neutrality issues")

        return issues

    def _needs_citation(self, sentence):
        """Check if a sentence likely needs citation"""
        doc = self.nlp(sentence)
        claim_indicators = ["shows", "proves", "demonstrates", "indicates"]
        return any(token.text.lower() in claim_indicators for token in doc)

    def _check_neutrality(self, text):
        """Evaluate text neutrality"""
        result = self.fact_checker(text, candidate_labels=["neutral", "biased"])
        return result[0]["score"] if result[0]["label"] == "neutral" else 0.0

    def suggest_improvements(self, issues):
        """Generate improvement suggestions based on issues"""
        suggestions = []
        for issue in issues:
            if "Citation needed" in issue:
                suggestions.append("Add reliable sources to support claims")
            if "neutrality" in issue.lower():
                suggestions.append("Rephrase content to maintain neutral point of view")
        return suggestions

if __name__ == "__main__":
    processor = WikiBitsProcessor()
    # Example usage
    url = "https://en.wikipedia.org/wiki/Artificial_intelligence"
    content = processor.fetch_article(url)
    if content:
        issues = processor.analyze_content(content)
        suggestions = processor.suggest_improvements(issues)
        print("Issues:", issues)
        print("Suggestions:", suggestions)