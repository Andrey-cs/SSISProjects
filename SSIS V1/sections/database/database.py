import pandas as pd
import os

class database:
    def __init__(self, filename: str, columns: list):
        self.columns = columns
        self.filename = f"./sections/database/{filename}.csv"  
        self.initialize()

    def initialize(self):
        os.makedirs(os.path.dirname(self.filename), exist_ok=True)  
        if not os.path.exists(self.filename):
            df = pd.DataFrame(columns=self.columns)
            df.to_csv(self.filename, index=False)

    def get_all(self):
        df = pd.read_csv(self.filename)
        return df.to_dict('records')

    def check(self, id_to_check):
        df = pd.read_csv(self.filename)
        return (df[self.columns[0]].str.upper() == id_to_check.upper()).any()  

    def insert_one(self, data):
        for key in list(data.keys()):
            data[key] = data[key].upper()
        df = pd.read_csv(self.filename)
        new_df = pd.DataFrame([data])
        df = pd.concat([df, new_df], ignore_index=True)
        df.to_csv(self.filename, index=False)
        return True

    def edit(self, data):
        for key in list(data.keys()):
            data[key] = data[key].upper()
        df = pd.read_csv(self.filename)
        key_column = self.columns[0]  
        for index, row in df.iterrows():
            if row[key_column] == data[key_column]:
                for key in data.keys():
                    df.at[index, key] = data[key]
                break
        df.to_csv(self.filename, index=False)
        return True

    def remove(self, id_to_remove):
        df = pd.read_csv(self.filename)
        key_column = self.columns[0]  
        df = df[df[key_column] != id_to_remove]
        df.to_csv(self.filename, index=False)


programs = database('programsInfo', ["Program Code", "Program Name"])
colleges = database('collegesInfo', ["College Code", "College Name"])
students = database('studentsInfo', ["ID", "First Name", "Last Name", "Sex", "Age", "Program Code", "Year Level"])
