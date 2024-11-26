# Database Project 2023/2024 

-------------

## Technology Stack and Project Design

We choose Neo4J as the technology for our project. In the current implementation, we utilised a Python script to import the data and establish associations from the CSV file using cypher-shell commands.

The database has a simple structure:
each record is a node with a label "category", which are connected to other nodes using relationship "has_subcategory".  

-------------

## Implementation Process

We are using a python script "importCSVfile.py" to first clear the database and then upload the original csv file to the database in batches of 10 000 rows. The script creates temporary files with csv extention, writes the batch rows on it, and then uses this cypher query to load it into a database, and create nodes and relationships from them:

```cypher
    LOAD CSV WITH HEADERS FROM 'file:///{temp_file_path}' AS row
    MERGE (cat:Category {{name: row.cat}})
    MERGE (subcat:Category {{name: row.subcat}})
    MERGE (cat)-[:HAS_SUBCATEGORY]->(subcat)
```
All of this is done after implementing indexing on `"name"` property in the database.

This method reduces load on the memory and helps import the data much faster. Without this we were importing the data at a rate of 12 hours and now it can be done in a couple of minutes.

We also prepared the queries for the 12 goals and implemented them in the "dbcli.py" python script. This script takes the arguments provided during the call in the command line: first argument is the number of the task, and second and third depends on the task. The script checks what number was entered as the first argument, runs a query that will answer the task, and prints out a message with the outputs. Additionally, we are calculating the times of execution of queries.

For goal 12, we limited the path length to 10, since otherwise it would run indefinetely. This number seemed to be the most optimal, but the bigger this number is, the more time it would take to execute the query.

------

## Prerequisites

- **Linux Computer:** Ensure you have a Linux computer with sufficient memory and processing power.

- **Python 3**: `python3.x --version` or `sudo apt install python3`

- **Python library 'neo4j'**: `pip3 install neo4j`

- **Neo4J 4.1** (can be installed from official cite).


---------

## Installation Guide

1. **Change configuration file**. After installing the software above, it is necessary to go to the configuration file of neo4j "neo4j.conf" that can be found in neo4j main directory (location depends on the environment), and change two lines:

    1. Allow files to be loaded from anywhere in the filesystem by commenting this line:
`#server.directories.import=import`
    2. To disable authentication, uncomment this line
`dbms.security.auth_enabled=false`

2. **Start Neo4J server**. Run command `neo4j start` (might require sudo access)

3. **Go to script directory**. In the terminal, change directory to the folder with all the files of this project: `importCSVfile.py`, `dbcli.py`.

4. **Add source CSV file**. Add `taxonomy_iw.csv` or any other csv of this sort to the directory with the python scripts.

5. **Populate the database**. Run `python3 importCSVfile.py`, wait until the database is cleared (if it wasn't) and then wait until the `.csv` file is loaded.

After completing these steps, now the main script can be run: `python3 dbcli.py`, following with the arguments depending on the task.

---------

## Sources

taxonomy_iw.csv.gz https://upel.agh.edu.pl/pluginfile.php/347249/mod_page/content/6/taxonomy_iw.csv.gz

Neo4J https://neo4j.com/download/

Python3 https://www.python.org/downloads/

-----------

## Result

The folowing resultes were obtained from running the scripts on a MacBook Air laptop with the following specifications:

CPU: Apple M1 8 cores
Memory: 16GB   
OS: macOS Ventura 13.5

To measure the time we are using the ```time``` command in the python scripts.  
  

| Goals | Execution time [s] |
|----------|----------|
|    Goal 1 | 0.012    |
|    Goal 2 |  0.026   |
|    Goal 3 |  0.025   |
|    Goal 4 |    0.0081 |
|    Goal 5 |  0.0093   |
|    Goal 6 |  0.0088   |
|    Goal 7 |   0.0064  |
|    Goal 8 |  0.0062   |
|    Goal 9 |   0.006  |
|   Goal 10 |   0.0083  |
|   Goal 11 |   0.026 |
|   Goal 12 | 0.0051  |
|   Data Import |  110  |  

<br>



------

## Self Evaluation

### Evaluation of Results

- All project objectives were successfully achieved.
- The data import time was drastically reduced from 12 hours to just a few minutes, demonstrating significant improvements in efficiency.
- The results were consistently reproduced on three different Unix machine setups.
- The time of execution can vary depending on the machine's CPU and current power settings. For instance, switching the machine to "power saving mode" nearly doubled the import times due to CPU limitations.
- Overall the execution times seem to be fast, even though we are using python scripts

### Efficiency improvement

##### Speed Efficiency

The data import proved to be the most challenging aspect of this project. Initially, using a basic import query for Neo4J, the process took over 12 hours. We gradually reduced the import times by incorporating constraints, indexes, periodic commits, and other techniques, but it still exceeded 5 hours. The significant breakthrough came after the implementation of python code to separate rows into batches. This innovation reduced the import time to under 3 minutes on our test setup. This phase consumed about 60% of our project time, primarily involving research and testing various import methods.

### Current Shortcomings and Future Improvements

- We believe further research can still improve the import time.
- The terminal application could be enhanced to offer a smoother user experience. At present, the command line interface is very basic and prints everythig in plain text. Every task has to be run seperately, and there can be errors if the amount of argumens is inconsistent with the required amount for the given task.
- The approach to make a python script file that manually creates temporary files to load into the database seems overly complicated. In the future, we could look into other methods to achieve the same result, or make the code cleaner.

--------

## Role of Students

### Katsiaryna Yakubava
1. Developed import script.
2. Developed cli script.

### Pravallika Mandavalli
1. Created installation documentation
2. Formulated Neo4J queries
3. Import query research

-------

<br>
