import mysql.connector
from mysql.connector import errorcode

# database config for the MySQL connection
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'andreygwapo123',
    'database': 'ssis_v2_db' 
}

def get_db_connection():
    """Establishes and returns a MySQL database connection."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your username or password") # Will call if the username or password is wrong
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print(f"Database '{DB_CONFIG['database']}' does not exist.")
            # Will call if the database does not exist
            try:
                temp_config = {k: v for k, v in DB_CONFIG.items() if k != 'database'}
                conn_no_db = mysql.connector.connect(**temp_config)
                cursor = conn_no_db.cursor()
                cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_CONFIG['database']}")
                print(f"Database '{DB_CONFIG['database']}' created or already exists.")
                cursor.execute(f"USE {DB_CONFIG['database']}") 
                cursor.close()
                conn_no_db.close()
                # Trying to connect again with the database specified upon interacting
                conn = mysql.connector.connect(**DB_CONFIG)
                return conn
            except mysql.connector.Error as creation_err:
                print(f"Failed to create/select database or connect after attempt: {creation_err}")
                return None
        else:
            print(f"MySQL Connection Error: {err}")
        return None

class Database:
    def __init__(self, table_name: str, pk_col_name: str, columns_sql_names: list, create_table_sql: str):
        self.table_name = table_name
        self.pk_col_name = pk_col_name # SQL primary key column name (e.g., "studentID")
        self.columns_sql_names = columns_sql_names # List of all SQL column names for this table
        self.create_table_sql = create_table_sql
        self.initialize()

    def initialize(self):
        # This method calls the SQL table if it doesn't exist using the provided DDL.
        conn = get_db_connection()
        if conn is None:
            print(f"Cannot initialize table {self.table_name}, no database connection.")
            return
        cursor = conn.cursor()
        try:
            cursor.execute(self.create_table_sql)
            conn.commit()
        except mysql.connector.Error as err:
            print(f"Error initializing database table {self.table_name}: {err}")
        finally:
            cursor.close()
            conn.close()

    def execute_query(self, query, params=None, fetch_one=False, fetch_all=False, is_dml=False):
        # This method calls the SQL Query if it doesn't exist using the provided values.
        conn = get_db_connection()
        if conn is None:
            return None if fetch_one or fetch_all else False
        
        cursor = conn.cursor(dictionary=(fetch_one or fetch_all))
        result = None
        try:
            cursor.execute(query, params)
            if is_dml: 
                conn.commit()
                result = cursor.rowcount 
            elif fetch_one:
                result = cursor.fetchone()
            elif fetch_all:
                result = cursor.fetchall()
            return result
        except mysql.connector.Error as err:
            print(f"SQL Error in table {self.table_name} for the query '{query[:100]}...': {err}")
            if is_dml: conn.rollback()
            return None if fetch_one or fetch_all else False
        finally:
            cursor.close()
            conn.close()

    def get_all(self, keyword=None, filter_criteria=None): 
        query = f"SELECT * FROM {self.table_name}"
        params = []
        conditions = []

        if keyword and self.columns_sql_names:
            keyword_conditions = []
            for col_sql_name in self.columns_sql_names:
                keyword_conditions.append(f"`{col_sql_name}` LIKE %s")
                params.append(f"%{keyword}%")
            if keyword_conditions:
                conditions.append("(" + " OR ".join(keyword_conditions) + ")")
        
        if filter_criteria and isinstance(filter_criteria, dict): 
            for col, val in filter_criteria.items():
                if col in self.columns_sql_names: 
                    conditions.append(f"`{col}` = %s")
                    params.append(val)

        if conditions:
            query += " WHERE " + " AND ".join(conditions)
            
        return self.execute_query(query, tuple(params), fetch_all=True) or []


    def check(self, id_to_check):
        query = f"SELECT EXISTS(SELECT 1 FROM {self.table_name} WHERE `{self.pk_col_name}` = %s) AS record_exists"
        result = self.execute_query(query, (str(id_to_check).upper(),), fetch_one=True)
        # Access the result by the alias 'record_exists'
        return result['record_exists'] == 1 if result and 'record_exists' in result else False


    def insert_one(self, data: dict):
        cols_to_insert = [f"`{col}`" for col in data.keys() if col in self.columns_sql_names]
        placeholders = ', '.join(['%s'] * len(cols_to_insert))
        sql_values = tuple(str(data[col_name.strip('`')]).upper() if data[col_name.strip('`')] is not None else None for col_name in cols_to_insert)

        if not cols_to_insert: return False
        query = f"INSERT INTO {self.table_name} ({', '.join(cols_to_insert)}) VALUES ({placeholders})"
        return self.execute_query(query, sql_values, is_dml=True) > 0


    def edit(self, data: dict):
        target_id = str(data.get(self.pk_col_name)).upper()
        if not target_id: return False

        set_clauses = []
        sql_values = []
        for key, value in data.items():
            if key != self.pk_col_name and key in self.columns_sql_names:
                set_clauses.append(f"`{key}` = %s")
                sql_values.append(str(value).upper() if value is not None else None)
        
        if not set_clauses: return False
        sql_values.append(target_id)
        query = f"UPDATE {self.table_name} SET {', '.join(set_clauses)} WHERE `{self.pk_col_name}` = %s"
        return self.execute_query(query, tuple(sql_values), is_dml=True) > 0

    def remove(self, id_to_remove):
        query = f"DELETE FROM {self.table_name} WHERE `{self.pk_col_name}` = %s"
        return self.execute_query(query, (str(id_to_remove).upper(),), is_dml=True) > 0
    
    def get_ids(self):
        query = f"SELECT `{self.pk_col_name}` FROM {self.table_name} ORDER BY `{self.pk_col_name}` ASC"
        records = self.execute_query(query, fetch_all=True)
        rows = ["No Selection"]
        if records:
            for record_dict in records: 
                rows.append(str(record_dict[self.pk_col_name]))
        return list(dict.fromkeys(rows))

    def get_program_ids(self): 
        return self.get_ids()
        
    def get_college_ids(self): 
        return self.get_ids()

CREATE_COLLEGES_SQL = """
CREATE TABLE IF NOT EXISTS colleges (
    collegeCODE VARCHAR(255) PRIMARY KEY,
    collegeNAME VARCHAR(255) NOT NULL
)"""

CREATE_PROGRAMS_SQL = """
CREATE TABLE IF NOT EXISTS programs (
    programID VARCHAR(255) PRIMARY KEY,
    programNAME VARCHAR(255) NOT NULL,
    collegeCODE VARCHAR(255),
    FOREIGN KEY (collegeCODE) REFERENCES colleges(collegeCODE) ON DELETE CASCADE
)"""

CREATE_STUDENTS_SQL = """
CREATE TABLE IF NOT EXISTS students (
    studentID VARCHAR(255) PRIMARY KEY,
    FIRSTNAME VARCHAR(255) NOT NULL,
    LASTNAME VARCHAR(255) NOT NULL,
    SEX VARCHAR(255),
    programCODE VARCHAR(255),
    `YEAR LEVEL` VARCHAR(255),
    FOREIGN KEY (programCODE) REFERENCES programs(programID) ON DELETE CASCADE
)"""

COLLEGES_SQL_COLS = ["collegeCODE", "collegeNAME"]
PROGRAMS_SQL_COLS = ["programID", "programNAME", "collegeCODE"]
STUDENTS_SQL_COLS = ["studentID", "FIRSTNAME", "LASTNAME", "SEX", "programCODE", "YEAR LEVEL"]

# example ni sha for Version 2
colleges = Database(
    table_name='colleges', 
    pk_col_name='collegeCODE',
    columns_sql_names=COLLEGES_SQL_COLS,
    create_table_sql=CREATE_COLLEGES_SQL
)
programs = Database(
    table_name='programs', 
    pk_col_name='programID',
    columns_sql_names=PROGRAMS_SQL_COLS,
    create_table_sql=CREATE_PROGRAMS_SQL
)
students = Database(
    table_name='students', 
    pk_col_name='studentID',
    columns_sql_names=STUDENTS_SQL_COLS,
    create_table_sql=CREATE_STUDENTS_SQL
)
