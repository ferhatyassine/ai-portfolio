"""Small skills lexicon (tech + soft skills) with aliases, used to read job offers and check claims."""
import re

SKILLS = {
    "python": ["python"], "c#": ["c#", "csharp", "c sharp"], ".net": [".net", "dotnet", "asp.net"],
    "sql": ["sql", "t-sql", "pl/sql"], "oracle": ["oracle"], "sql server": ["sql server", "mssql"],
    "git": ["git", "github", "gitlab"], "javascript": ["javascript", "js", "node.js", "nodejs"],
    "java": ["java"], "html/css": ["html", "css"], "react": ["react"], "docker": ["docker"],
    "cloud": ["cloud", "aws", "azure", "gcp"], "linux": ["linux", "bash"], "r": ["r language", "rstudio"],
    "machine learning": ["machine learning", "ml", "pytorch", "tensorflow"],
    "generative ai": ["generative ai", "gen ai", "genai", "llm", "llms", "language model"],
    "testing": ["testing", "unit test", "pytest", "qa"], "agile": ["agile", "scrum", "sprint"],
    "api": ["api", "rest", "restful"], "data analysis": ["data analysis", "analytics", "data analyst"],
    "teamwork": ["teamwork", "team player", "collaborat", "équipe"],
    "communication": ["communication", "present", "bilingual", "bilingue"],
    "problem solving": ["problem solving", "problem-solving", "troubleshoot", "debug"],
}


def find_skills(text):
    """Return the canonical skills mentioned in text (word-boundary aware)."""
    low = text.lower()
    found = []
    for canon, aliases in SKILLS.items():
        for a in aliases:
            if re.search(rf"(?<![\w]){re.escape(a)}(?![\w])", low):
                found.append(canon)
                break
    return found
