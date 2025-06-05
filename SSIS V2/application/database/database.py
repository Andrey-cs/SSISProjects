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
            print("Something is wrong with your username or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print(f"Database '{DB_CONFIG['database']}' does not exist.")
            try:
                temp_config = {k: v for k, v in DB_CONFIG.items() if k != 'database'}
                conn_no_db = mysql.connector.connect(**temp_config)
                cursor = conn_no_db.cursor()
                cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_CONFIG['database']}")
                print(f"Database '{DB_CONFIG['database']}' created or already exists.")
                cursor.execute(f"USE {DB_CONFIG['database']}")
                cursor.close()
                conn_no_db.close()
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
        self.pk_col_name = pk_col_name
        self.columns_sql_names = columns_sql_names
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

            for statement in self.create_table_sql.split(';'):
                if statement.strip(): 
                    cursor.execute(statement)
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

    def get_all(self, keyword=None, filter_criteria=None, sort_by=None, sort_order='ASC'):
        params = []
        conditions = []
        

        if self.table_name == 'programs' and keyword:

            query = f"SELECT {self.table_name}.* FROM {self.table_name} LEFT JOIN colleges ON {self.table_name}.collegeCODE = colleges.collegeCODE"
            keyword_conditions = []
            for col_sql_name in self.columns_sql_names: #
                keyword_conditions.append(f"{self.table_name}.`{col_sql_name}` LIKE %s")
                params.append(f"%{keyword}%")

            keyword_conditions.append(f"colleges.`collegeNAME` LIKE %s")
            params.append(f"%{keyword}%")
            
            if keyword_conditions:
                conditions.append("(" + " OR ".join(keyword_conditions) + ")")

        else: 
            query = f"SELECT * FROM {self.table_name}"
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
                    conditions.append(f"{self.table_name}.`{col}` = %s" if self.table_name == 'programs' and keyword else f"`{col}` = %s")
                    params.append(val)

        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        
        orderByClause = ""
        if self.table_name == 'students':
            if sort_by and sort_by in self.columns_sql_names:
                if sort_by == 'YEAR LEVEL':
                    orderByClause = """
                        ORDER BY
                          CASE `YEAR LEVEL`
                            WHEN 'FIRST YEAR' THEN 1
                            WHEN 'SECOND YEAR' THEN 2
                            WHEN 'THIRD YEAR' THEN 3
                            WHEN 'FOURTH YEAR' THEN 4
                            WHEN 'IRREGULAR' THEN 5
                            ELSE 6 
                          END"""
                    orderByClause += f" {sort_order}, studentID ASC"
                else: 
                    orderByClause = f" ORDER BY `{sort_by}` {sort_order}, studentID ASC"
            else: 
                orderByClause = """
                    ORDER BY
                      CASE `YEAR LEVEL`
                        WHEN 'FIRST YEAR' THEN 1
                        WHEN 'SECOND YEAR' THEN 2
                        WHEN 'THIRD YEAR' THEN 3
                        WHEN 'FOURTH YEAR' THEN 4
                        WHEN 'IRREGULAR' THEN 5
                        ELSE 6 
                      END ASC, studentID ASC"""
        elif sort_by and sort_by in self.columns_sql_names:
             orderByClause = f" ORDER BY `{sort_by}` {sort_order}"
        
        query += orderByClause
            
        return self.execute_query(query, tuple(params), fetch_all=True) or []


    def check(self, id_to_check):
        query = f"SELECT EXISTS(SELECT 1 FROM {self.table_name} WHERE `{self.pk_col_name}` = %s) AS record_exists"
        result = self.execute_query(query, (str(id_to_check).upper(),), fetch_one=True)
        return result['record_exists'] == 1 if result and 'record_exists' in result else False


    def insert_one(self, data: dict):
        cols_to_insert = [f"`{col}`" for col in data.keys() if col in self.columns_sql_names]
        placeholders = ', '.join(['%s'] * len(cols_to_insert))
        sql_values_list = []
        for col_name_with_backticks in cols_to_insert:
            col_name = col_name_with_backticks.strip('`')
            value = data.get(col_name)
            if isinstance(value, str):
                sql_values_list.append(value.upper())
            else:
                sql_values_list.append(value)
        sql_values = tuple(sql_values_list)

        if not cols_to_insert: return False
        query = f"INSERT INTO {self.table_name} ({', '.join(cols_to_insert)}) VALUES ({placeholders})"
        return self.execute_query(query, sql_values, is_dml=True) > 0


    def edit(self, data: dict):
        target_id = str(data.get(self.pk_col_name)).upper()
        if not target_id: return False

        set_clauses = []
        sql_values = []
        for key, value_raw in data.items():
            if key != self.pk_col_name and key in self.columns_sql_names:
                set_clauses.append(f"`{key}` = %s")
                current_value = value_raw
                if isinstance(current_value, str):
                    sql_values.append(current_value.upper())
                else:
                    sql_values.append(current_value)
        
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

COLLEGES_SQL_COLS = ["collegeCODE", "collegeNAME"] # columns for college tab
PROGRAMS_SQL_COLS = ["programID", "programNAME", "collegeCODE"] # columns for the programs tab
STUDENTS_SQL_COLS = ["studentID", "FIRSTNAME", "LASTNAME", "SEX", "programCODE", "YEAR LEVEL"] # coluumns for the students tab

# example ni sha
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