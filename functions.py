import pandas as pd

url = "/Users/tristanblackledge/unleash-functions/allContacts.csv"

keyword_to_function = {
    # Engineering
    "engineer": "Engineering",
    "developer": "Engineering",
    "programmer": "Engineering",
    "technician": "Engineering",

    # Data & Analytics
    "data": "Data & Analytics",
    "scientist": "Data & Analytics",
    "analyst": "Data & Analytics",
    "bi": "Data & Analytics",

    # Product
    "product": "Product",

    # Design
    "designer": "Design",
    "ux": "Design",
    "ui": "Design",
    "graphic": "Design",

    # Operations
    "operations": "Operations",
    "logistics": "Operations",
    "supply": "Operations",
    "procurement": "Operations",

    # Sales
    "sales": "Sales",
    "account": "Sales",
    "business development": "Sales",

    # Marketing
    "marketing": "Marketing",
    "brand": "Marketing",
    "advertising": "Marketing",

    # Finance
    "finance": "Finance",
    "accountant": "Finance",
    "auditor": "Finance",

    # HR
    "hr": "Human Resources",
    "human resources": "Human Resources",
    "recruiter": "Human Resources",

    # Customer Support
    "support": "Customer Success / Support",
    "service": "Customer Success / Support",

    # IT / Infrastructure
    "it": "IT / Infrastructure",
    "network": "IT / Infrastructure",
    "sysadmin": "IT / Infrastructure",

    # Legal
    "legal": "Legal & Compliance",
    "lawyer": "Legal & Compliance",
    "compliance": "Legal & Compliance",

    # Leadership / Executive
    "chief": "Leadership / Executive",
    "ceo": "Leadership / Executive",
    "director": "Leadership / Executive",
    "vp": "Leadership / Executive",

    # R&D
    "research": "Research & Development",

    # Consulting
    "consultant": "Consulting / Advisory",
    "advisor": "Consulting / Advisory",

    # Education / Training
    "trainer": "Education / Training",
    "educator": "Education / Training",

    # Facilities / Maintenance
    "maintenance": "Facilities / Maintenance",
    "facility": "Facilities / Maintenance",

    # Strategy / Planning
    "strategy": "Strategy / Planning",
    "planner": "Strategy / Planning",

    # Field / Operations
    "operator": "Operations (Field / Manual)"
}

department_keywords = {
    # Engineering / Technology
    "engineering": ["engineer", "developer", "programmer", "technician",
                    "sysadmin", "it", "infrastructure", "network",
                    "architect"],

    # Data / Analytics / AI / ML
    "data": ["data", "analyst", "scientist", "machine learning", "ml", "ai",
             "bi", "analytics", "research"],

    # Product / Design
    "product": ["product", "ux", "ui", "designer", "graphic", "visual"],

    # Operations / Logistics / Supply
    "operations": ["operations", "logistics", "supply", "procurement",
                   "warehouse", "fulfillment", "maintenance", "facility",
                   "operator"],

    # Sales
    "sales": ["sales", "account", "business development", "partnership"],

    # Marketing / Brand / Advertising
    "marketing": ["marketing", "brand", "advertising", "pr", "content"],

    # Finance / Accounting
    "finance": ["finance", "accountant", "auditor", "controller", "financial"],

    # Human Resources / People
    "hr": ["hr", "human resources", "recruiter", "talent", "learning",
           "training", "development"],

    # Customer Success / Support
    "customer success": ["support", "customer", "service", "helpdesk"],

    # Legal / Compliance / Risk
    "legal": ["legal", "lawyer", "attorney", "compliance", "risk"],

    # Leadership / Executive / Strategy
    "leadership": ["ceo", "cxo", "cto", "chief", "vp", "director", "executive",
                   "president", "strategy", "planning"],

    # Consulting / Advisory
    "consulting": ["consultant", "advisor", "specialist"],

    # Research & Development / Science
    "r&d": ["research", "scientist", "lab", "investigator"],

    # Education / Training
    "education": ["trainer", "educator", "learning", "instruction"],

    # Facilities / Maintenance
    "facilities": ["maintenance", "facility", "operations", "operator"],

    # Miscellaneous / Other
    "other": ["partner", "founder", "cofounder", "owner", "board", "chairman",
              "chairwoman"]
}


seniority_keywords = [
    "intern",
    "trainee",
    "junior",
    "assistant",
    "apprentice",
    "associate",
    "graduate",
    "entry-level",
    "entry level",
    "staff",
    "specialist",
    "analyst",
    "coordinator",
    "technician",
    "consultant",
    "professional",
    "engineer",
    "senior",
    "lead",
    "principal",
    "sr",
    "experienced",
    "expert",
    "advisor",
    "mentor",
    "manager",
    "supervisor",
    "team lead",
    "foreman",
    "head of",
    "head",
    "controller",
    "director",
    "managing",
    "executive",
    "vp",
    "vice president",
    "deputy director",
    "associate director",
    "chief",
    "ceo",
    "coo",
    "cfo",
    "cto",
    "cmo",
    "cio",
    "chro",
    "president",
    "founder",
    "cofounder",
    "owner",
    "partner",
    "chairman",
    "chairwoman",
    "chairperson",
    "board member",
    "non executive director",
    "leader",
    "leadership",
    "directorate",
    "fellow",
    "principal investigator"
]


def load_and_clean():

    # turn into dataframe
    df = pd.read_csv(url)
    # drop NaN values
    df = df.dropna()
    # clean the job titles
    df['Job Title'] = df['Job Title'].str.lower()
    # turn to lowercase
    df['Cleaned Title'] = df['Job Title'].str.lower()
    # strop whitespace
    df['Cleaned Title'] = df['Job Title'].str.strip()
    # remove punctuation
    df['Cleaned Title'] = df['Job Title'].str.replace(r'[^a-zA-Z\s]', '',
                                                      regex=True)
    # normalise the spacing
    df['Cleaned Title'] = df['Job Title'].str.replace(r'\s+', ' ', regex=True)

    return df


def basic_counts(df):

    # basic count of the most common job titles
    title_counts = df["Job Title"].value_counts().head(20)

    print(title_counts)


def seniority(df):
    # go through the job title and extract seniority words
    df['seniority'] = df['Job Title'].apply(
        lambda title: next((word for word in seniority_keywords if word in
                            title.lower()), None)
    )


def function(df):
    df['Function'] = df['Job Title'].apply(
        lambda title: next(
            (keyword_to_function[word] for word in keyword_to_function if word
             in title.lower()),
            None
        )
    )


def department(df):
    df['department'] = df['Job Title'].apply(
        lambda title: next(
            (dept for dept, keywords in department_keywords.items()
             if any(kw in title.lower() for kw in keywords)),
            None
        )
    )


def main():
    df = load_and_clean()
    seniority(df)
    function(df)
    department(df)
    df.drop(columns=['Cleaned Title'], inplace=True)
    # assuming your DataFrame is called df
    output_file = "enriched_contacts.xlsx"
    df.to_excel(output_file, index=False)
    print(f"Data exported to {output_file}")


if __name__ == "__main__":
    main()
