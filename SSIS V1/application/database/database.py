import pandas as pd
import os

# Will use this for the absolute path to the directory where database.py is located. Instead of /folder/filename.py
DB_Directory = os.path.dirname(os.path.abspath(__file__))

class Database:
    def __init__(self, filename: str, columns: list):
        self.columns = columns
        self.filename = os.path.join(DB_Directory, f"{filename}.csv")
        self.initialize()

    def initialize(self):
        # This method creates the CSV file with headers if it doesn't exist.
        if not os.path.exists(self.filename):
            try:
                df = pd.DataFrame(columns=self.columns)
                df.to_csv(self.filename, index=False)
            except Exception as e:
                print(f"Error initializing database file {self.filename}: {e}")


    def get_all(self):
        """
        Retrieves all records from the CSV file.
        Returns a list of dictionaries, or an empty list if an error occurs or file is empty.
        """
        try:
            if not os.path.exists(self.filename):
                print(f"Warning: Data file {self.filename} not found. Attempting to initialize.")
                self.initialize()
            if os.path.exists(self.filename) and os.path.getsize(self.filename) == 0:
                print(f"Warning: Data file {self.filename} is empty. Re-initializing with headers.")
                self.initialize()
            df = pd.read_csv(self.filename)
            return df.to_dict('records')
        except pd.errors.EmptyDataError:
            print(f"Warning: Data file {self.filename} is empty or contains no data. Returning empty list.")
            return []
        except FileNotFoundError:
            print(f"Error: Data file {self.filename} was not found. Returning empty list.")
            return []
        except Exception as e:
            print(f"An error occurred while reading {self.filename}: {e}. Returning empty list.")
            return []

    def check(self, id_to_check):
        try:
            df = pd.read_csv(self.filename)
            if 'ID' not in df.columns: 
                return False
            return (df['ID'].astype(str) == str(id_to_check).upper()).any()
        except (FileNotFoundError, pd.errors.EmptyDataError):
            return False 
        except Exception as e:
            print(f"Error checking ID in {self.filename}: {e}")
            return False


    def insert_one(self, data: dict):
        try:
            processed_data = {key: str(value).upper() for key, value in data.items()}
            df = pd.read_csv(self.filename)
            if not all(col in df.columns for col in self.columns):
                df = pd.DataFrame(columns=self.columns) 
            new_df = pd.DataFrame([processed_data], columns=self.columns) 
            df = pd.concat([df, new_df], ignore_index=True)
            df.to_csv(self.filename, index=False)
            return True
        except Exception as e:
            print(f"Error inserting data into {self.filename}: {e}")
            return False

    def edit(self, data: dict):
        try:
            df = pd.read_csv(self.filename)
            if 'ID' not in df.columns: 
                print(f"Error editing {self.filename}: 'ID' column missing.")
                return False
            processed_data = {key: str(value).upper() for key, value in data.items()}
            match_idx = -1
            target_id = str(processed_data.get('ID')).upper()
            for index, row_id in enumerate(df['ID'].astype(str)):
                if row_id.upper() == target_id:
                    match_idx = index
                    break
            if match_idx != -1:
                for key, value in processed_data.items():
                    if key in df.columns:
                        df.loc[match_idx, key] = value
                df.to_csv(self.filename, index=False)
                return True
            else:
                print(f"Error editing {self.filename}: ID '{target_id}' not found.")
                return False 
        except Exception as e:
            print(f"Error editing data in {self.filename}: {e}")
            return False

    def remove(self, id_to_remove):
        try:
            df = pd.read_csv(self.filename)
            if 'ID' not in df.columns:
                return False # Cannot remove if ID column doesn't exist
            # Ensure comparison is robust (string vs string)
            initial_len = len(df)
            df = df[df['ID'].astype(str) != str(id_to_remove).upper()]
            if len(df) < initial_len: 
                df.to_csv(self.filename, index=False)
                return True
            return False 
        except Exception as e:
            print(f"Error removing data from {self.filename}: {e}")
            return False          
    def get_ids(self): 
        all_records = self.get_all() 
        rows = ["No Selection"] 
        for row in all_records:
            if isinstance(row, dict) and "ID" in row:
                rows.append(str(row["ID"]))
        return list(dict.fromkeys(rows)) 
    def get_program_ids(self):
        return self.get_ids()       
    def get_college_ids(self):
        return self.get_ids()

# example ni sha
programs = Database('programs', ["ID", "NAME", "COLLEGE"])
students = Database('students', ["ID", "FIRSTNAME", "LASTNAME", "SEX", "PROGRAM", "YEAR LEVEL"])
colleges = Database('colleges', ["ID", "NAME"])