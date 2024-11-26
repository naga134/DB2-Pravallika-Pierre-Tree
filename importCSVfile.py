import tempfile
import os
import time
from neo4j import GraphDatabase

#Functions:


def clear_database(driver):
    print("Clearing database, please wait...")
    with driver.session() as session:
        while True:
            result = session.run("""
                MATCH (n)
                WITH n LIMIT 10000
                DETACH DELETE n
                RETURN COUNT(n) as deletedCount
            """)
            deleted_count = result.single()["deletedCount"]
            if deleted_count == 0:
                break 
    print("Database cleared. Starting to load nodes and relationships...")


# Makes and uploads a batch of rows
def upload_batch_using_load_csv(driver, batch_rows):
    #filtering out rows with null values:
    batch_rows_filtered = [row for row in batch_rows if row[0] is not None and row[1] is not None]

    if not batch_rows_filtered:
        return

    #creating a similar temporary file to hold the batch of rows:
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as temp_file:
        # Write headers
        temp_file.write('cat,subcat\n')
        # Write rows
        for row in batch_rows_filtered:
            #Making sure the values are read correctly:
            cat = row[0].strip().strip('"').replace('\\', '').replace('"', '""')
            subcat = row[1].strip().strip('"').replace('\\', '').replace('"', '""')
            temp_file.write(f'"{cat}","{subcat}"\n')
        temp_file_path = temp_file.name

    cypher_query = f"""
    LOAD CSV WITH HEADERS FROM 'file:///{temp_file_path}' AS row
    MERGE (cat:Category {{name: row.cat}})
    MERGE (subcat:Category {{name: row.subcat}})
    MERGE (cat)-[:HAS_SUBCATEGORY]->(subcat)
    """
    with driver.session() as session:
        session.run(cypher_query)


    os.unlink(temp_file_path)


#makes a loop for the whole file:
def load_csv_and_upload(driver, csv_file):
    with open(csv_file, 'r') as f:
        total_rows = sum(1 for line in f) - 1 #counting the number of rows
        f.seek(0)
        
        next(f)     #header skipped
        
        #reading and processing rows in batches 
        batch_size = 10000
        uploaded_rows = 0
        clear_database(driver)  
        start_loading = time.time()
        for batch in range(0, total_rows, batch_size):
            batch_rows = []
            for _ in range(batch_size):
                try:
                    row = next(f).strip().split(',') #make sure there are no errors while reading the rows
                    batch_rows.append(row)
                    uploaded_rows += 1
                except StopIteration:
                    break 
            if batch_rows:
                upload_batch_using_load_csv(driver, batch_rows)
                percentage_loaded = min(uploaded_rows, total_rows) / total_rows * 100
                print(f"Loaded {min(uploaded_rows, total_rows)} out of {total_rows} rows. ({percentage_loaded:.2f}% completed)", end='\r')
        print()
        end_loading = time.time()
        print("Loaded successfully. Loading time: ", int(end_loading-start_loading), " seconds")



#Execution:

#selecting the file from the directory of the script:
csv_file = os.path.join(os.path.dirname(__file__), 'taxonomy_iw.csv') 

#connecting to the database:
driver = GraphDatabase.driver("bolt://localhost:7687" , auth=("", ""))

#creating index and loading the data
with driver.session() as session:
        session.run("CREATE INDEX nameIndex IF NOT EXISTS FOR (c:Category) ON (c.name);")
load_csv_and_upload(driver, csv_file)