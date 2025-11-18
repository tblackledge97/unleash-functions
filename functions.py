import re
import pandas as pd


class JobClassifier:
    def __init__(self, keyword_to_function, seniority_keywords,
                 department_keywords):
        self.keyword_to_function = keyword_to_function
        self.seniority_keywords = seniority_keywords
        self.department_keywords = department_keywords

    def clean_title(self, title: str) -> str:
        """Cleans up the job title string"""
        title = title.lower()
        title = re.sub(r'[^a-z\s]', '', title)
        title = re.sub(r'\s+', ' ', title)
        return title

    def seniority(self, title: str):
        """Loops through seniority keywords
        uses next to return the first match found"""
        for sen, keywords in self.seniority_keywords.items():
            if any(keyword in title for keyword in keywords):
                return sen
        return None

    def function(self, title: str):
        """Loops through keyword, function pairs"""
        return next(
            (v for keyword, v in self.keyword_to_function.items()
             if keyword in title), None)

    def department(self, title: str):
        """Loop through each department
        Use "any" to check if any keyword matches the title
        DONT use next here as this is more clean."""
        for dept, keywords in self.department_keywords.items():
            if any(keyword in title for keyword in keywords):
                return dept
        return None

    def classify(self, df: pd.DataFrame) -> pd.DataFrame:
        """Apply the above"""
        # Clean job titles
        df['Cleaned Title'] = df['Job Title'].astype(str).apply(
            self.clean_title)

        # extract features
        df['Seniority'] = df['Cleaned Title'].apply(self.seniority)
        df['Function'] = df['Cleaned Title'].apply(self.function)
        df['Department'] = df['Cleaned Title'].apply(self.department)

        return df.drop(columns=['Cleaned Title'])
