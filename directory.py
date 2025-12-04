import pandas as pd
import sqlite3
import os
import re


def import_excel_to_sqlite(
    excel_file_path, db_file_path, table_name="student_directory"
):
    """
    Reads an Excel file with specific columns and writes it to a SQLite database.
    """
    if not os.path.exists(excel_file_path):
        print(f"Error: The file '{excel_file_path}' was not found.")
        return

    print(f"Reading file: {excel_file_path}...")

    try:
        # Read Excel, ensuring IDs are strings to keep leading zeros
        df = pd.read_excel(excel_file_path, dtype=str)

        column_mapping = {
            "Directory Opt In": "directory_opt_in",
            "Household ID": "household_id",
            "Student ID": "student_id",
            "Student First Name": "student_first_name",
            "Student Last Name": "student_last_name",
            "Grade": "grade",
            "Guardian First": "guardian_first_name",
            "Guardian Last": "guardian_last_name",
            "Relationship": "relationship",
            "Contact Sequence": "contact_sequence",
            "Mailing 1": "mailing_address_1",
            "Mailing 2": "mailing_address_2",
            "Directory Phone #": "directory_phone",
        }

        df.rename(columns=column_mapping, inplace=True)
        df = df.fillna("")

        # Remove SIBLING relationships
        # We check .str.upper() to catch 'Sibling', 'SIBLING', or 'sibling'
        df = df[df["relationship"].str.upper() != "SIBLING"]

        # Apply Title Case to all columns to normalize inconsistent input
        # This ensures 'road' becomes 'Road' before we standardize it
        df = df.apply(lambda x: x.str.title())

        # Correct situations where we _don't_ want title case
        df["grade"] = df["grade"].str.upper()

        # --- Address Standardization Logic ---
        address_corrections = {
            "Street": "St",
            "Avenue": "Ave",
            "Boulevard": "Blvd",
            "Place": "Pl",
            "Drive": "Dr",
            "Lane": "Ln",
            "Road": "Rd",
            "Court": "Ct",
            "Circle": "Cir",
            "Trail": "Trl",
            "Parkway": "Pkwy",
            "Highway": "Hwy",
            "North": "N",
            "South": "S",
            "East": "E",
            "West": "W",
            "Northeast": "NE",
            "Northwest": "NW",
            "Southeast": "SE",
            "Southwest": "SW",
            "Apartment": "Apt",
            "Suite": "Ste",
            "Building": "Bldg",
            "Floor": "Fl",
            "Square": "Sq",
            "Turnpike": "Tpke",
            "Po Box": "PO Box",
        }

        def standardize_address(text):
            if not isinstance(text, str):
                return text

            for full_word, abbr in address_corrections.items():
                # Use regex \b boundaries to replace whole words only
                # e.g., Replace 'East' but not 'Eastern'
                pattern = r"\b" + re.escape(full_word) + r"\b"
                text = re.sub(pattern, abbr, text)

            text = re.sub(r"\s+", " ", text)  # remove multiple spaces
            text = text.replace(".", "")  # remove periods

            return text.strip()

        def standardize_citystatezip(text):
            if not isinstance(text, str):
                return text

            city, statezip = text.split(",", maxsplit=1)
            state, zip = statezip.strip().split(" ", maxsplit=1)
            zip = zip.strip().split("-", maxsplit=1)[0]  # remove +4 from zip

            if zip == "44023":  # Some people like to say Bainbridge/Auburn
                city = "Chagrin Falls"
                state = "OH"

            return "%s, %s %s" % (
                city.strip(),
                state.strip().upper(),
                zip.strip(),
            )

        # Apply standardization to address columns
        df["mailing_address_1"] = df["mailing_address_1"].apply(
            standardize_address
        )
        df["mailing_address_2"] = df["mailing_address_2"].apply(
            standardize_citystatezip
        )
        # -------------------------------------

        print(f"Connecting to database: {db_file_path}...")
        conn = sqlite3.connect(db_file_path)

        df.to_sql(table_name, conn, if_exists="replace", index=False)

        print(f"Success! Raw data imported into table '{table_name}'.")
        conn.close()

    except Exception as e:
        print(f"An error occurred during import: {e}")


def process_and_export_households(db_file_path, output_excel_path):
    """
    Reads from SQLite, groups by Household ID to combine family members,
    and exports a formatted directory to Excel.
    """
    print(f"Processing data from {db_file_path}...")

    try:
        conn = sqlite3.connect(db_file_path)

        # 1. Read the raw data back from SQL
        query = "SELECT * FROM student_directory"
        df = pd.read_sql_query(query, conn)
        conn.close()

        # Create a full name column for guardians
        df["full_guardian_name"] = (
            df["guardian_first_name"].str.strip()
            + " "
            + df["guardian_last_name"].str.strip()
        )

        # Create a display name for kids: First Name (Grade)
        df["kid_display"] = (
            df["student_first_name"].str.strip()
            + " ("
            + df["grade"].astype(str).str.strip()
            + ")"
        )

        # 2. Define helper functions for aggregation
        # We use set() to remove duplicates (e.g. if a student is listed twice for Mom and Dad)
        # We use sorted() to keep the order consistent
        def join_unique_names(series):
            unique_names = sorted(set(name for name in series if name))
            return ", ".join(unique_names)

        # 3. Group by Household ID and apply aggregation rules
        # specific aggregation logic for each column
        grouped_df = (
            df.groupby("household_id")
            .agg(
                {
                    "student_last_name": "first",  # Use student last name for the household
                    "kid_display": join_unique_names,  # Combine all kids names with grades
                    "full_guardian_name": join_unique_names,  # Combine all adult names (FULL NAMES NOW)
                    "mailing_address_1": "first",  # Address should be same for household
                    "mailing_address_2": "first",
                    "directory_phone": "first",
                }
            )
            .reset_index()
        )

        # 4. Rename columns to match the desired output
        final_columns = {
            "household_id": "Household ID",
            "student_last_name": "Last Name",
            "kid_display": "Kids Names",
            "full_guardian_name": "Adult Names",
            "mailing_address_1": "Address",
            "mailing_address_2": "Address Line 2",
            "directory_phone": "Phone",
        }
        grouped_df.rename(columns=final_columns, inplace=True)

        # 5. Reorder columns
        desired_order = [
            "Last Name",
            "Kids Names",
            "Adult Names",
            "Address",
            "Address Line 2",
            "Phone",
            "Household ID",
        ]
        grouped_df = grouped_df[desired_order]

        # 6. Write to Excel
        print(f"Writing processed data to {output_excel_path}...")
        grouped_df.to_excel(output_excel_path, index=False)
        print("Success! Directory file created.")

    except Exception as e:
        print(f"An error occurred during processing: {e}")


# --- Execution Block ---
if __name__ == "__main__":
    # REPLACE THESE VALUES WITH YOUR ACTUAL FILE NAMES
    source_excel = "input/directory 2526.xlsx"
    temp_db = "output/directory.db"
    final_output = "output/directory 2526 output.xlsx"

    # Run the function
    import_excel_to_sqlite(source_excel, temp_db)

    # Step 2: Process SQLite data and export combined Excel
    process_and_export_households(temp_db, final_output)
