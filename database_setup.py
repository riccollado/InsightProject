import sqlite3

conn = sqlite3.connect('/home/priyanka/projects/final/RUNS/DB/Results.db')
print("Opened database successfully");

conn.execute('''CREATE TABLE EXPERIMENT
         (ID INTEGER  PRIMARY KEY     AUTOINCREMENT,
          METHOD TEXT            NOT NULL,
          NO_NODES INT           NOT NULL,
          NO_LAYERS INT          NOT NULL,
          NO_SCENARIOS INT       NOT NULL,
          FIRST_BOOTSTRAP_SIZE INT ,
          SECOND_BOOTSRAP_SIZE INT ,
          TOTAL_TIME INT
          );''')
print("EXPERIMENT Table created successfully");
 

conn.execute('''CREATE TABLE RESULTS
          (EXPERIMENT_ID INT                        NOT NULL,
          TREE_LEVEL INT                            NOT NULL,
          SUBPROBLEM_CONSTRAINTS TEXT               NOT NULL,
          SUBPROBLEM_EXPECTEDVALUE REAL             NOT NULL,
          BOOTSTAPPED_Z_EXPECTEDVALUE REAL          NOT NULL,
          BOOTSTAPPED_Z_STANDARDEVIATION REAL       NOT NULL,
          SCENARIOS_AT_LEVEL INT                    NOT NULL,
          TOTAL_SCENARIOS INT                       NOT NULL,
          RECORDSET TEXT                            NOT NULL,
          SINGLETON TEXT                            NOT NULL  
          );''')

print("RESULTS Table created successfully");

conn.close()
