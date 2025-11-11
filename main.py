# Main class that does all the classification
import pandas as pd
from keywords import (  # type: ignore
    keyword_to_function,
    seniority_keywords,
    department_keywords
)
from functions import JobClassifier


def main():
    input_file = "/Users/tristanblackledge/unleash-functions/allContacts.csv"
    df = pd.read_csv(input_file)

    # Drop rows with missing job titles
    df = df.dropna(subset=['Job Title'])

    # create the classifier
    # Initialize the class with dictionaries
    classifier = JobClassifier(
        keyword_to_function=keyword_to_function,
        department_keywords=department_keywords,
        seniority_keywords=seniority_keywords
    )

    # Classifiy the DF
    # applies the cleaning and functions from functions.py
    # returns a new DF with extra columns
    classifier_df = classifier.classify(df)

    # Save the results to a new output file
    output_file = "enriched_contacts.xlsx"
    classifier_df.to_excel(output_file, index=False)

    print("Data exported to ", output_file)


if __name__ == "__main__":
    main()
