import sys
from neo4j import GraphDatabase
import time

queryNum = sys.argv[1]
if len(sys.argv) >2:
    inputForQuery = sys.argv[2]
    if len(sys.argv) >3:
        secondInput = sys.argv[3]

uri = "bolt://localhost:7687"  
user = "" 
password = "" 

driver = GraphDatabase.driver(uri, auth=(user, password))

if queryNum == '1':
    with driver.session() as session:
        start_time = time.time()
        result = session.run(f"""
                MATCH (parent {{name: "{inputForQuery}" }})-[:HAS_SUBCATEGORY]->(child)
                RETURN child;
            """)
        print(f"Here are all the children of this node: {inputForQuery}")
        end_time = time.time()
        for record in result:
            print(record["child"]["name"])
        print("Execution time for the query (in seconds): ", end_time - start_time)


if queryNum == '2':
    with driver.session() as session:
        start_time = time.time()
        result = session.run(f"""
                MATCH (parent {{name: "{inputForQuery}" }})-[:HAS_SUBCATEGORY]->(child)
                RETURN COUNT(child) AS numChildren;
            """)
        end_time = time.time()
        print(f"Here is the amount of children of this node: {inputForQuery}")
        for record in result:
            print(record["numChildren"])
        print("Execution time for the query for the query (in seconds): ", end_time - start_time)


if queryNum == '3':
    with driver.session() as session:
        start_time = time.time()
        result = session.run(f"""
                MATCH (node:Category {{name: "{inputForQuery}" }})-[:HAS_SUBCATEGORY*2]->(grandchild:Category)
                RETURN grandchild

            """)
        end_time = time.time()
        print(f"Here are all the grand children of this node: {inputForQuery}")
        for record in result:
            print(record["grandchild"]["name"])
        print("Execution time for the query (in seconds): ", end_time - start_time)


if queryNum == '4':
    with driver.session() as session:
        start_time = time.time()
        result = session.run(f"""
                MATCH (parent)-[:HAS_SUBCATEGORY]->(child {{name: "{inputForQuery}" }})
                RETURN parent;
            """)
        end_time = time.time()
        print(f"Here are all the parents of the node {inputForQuery}")
        for record in result:
            print(record["parent"]["name"])
        print("Execution time for the query (in seconds): ", end_time - start_time)


if queryNum == '5':
    with driver.session() as session:
        start_time = time.time()
        result = session.run(f"""
                MATCH (parent)-[:HAS_SUBCATEGORY]->(child {{name: "{inputForQuery}" }})
                RETURN COUNT(parent) AS numParents;
            """)
        end_time = time.time()
        print(f"Here is the amount of parents of the node {inputForQuery}")
        for record in result:
            print(record["numParents"])
        print("Execution time for the query (in seconds): ", end_time - start_time)


if queryNum == '6':
    with driver.session() as session:
        start_time = time.time()
        result = session.run(f"""
                MATCH (node:Category {{name: "{inputForQuery}" }})<-[:HAS_SUBCATEGORY*2]-(grandparent:Category)
                RETURN grandparent;
                """)
        end_time = time.time()
        print(f"Here are all the grand parents of the node {inputForQuery}")
        for record in result:
            print(record["grandparent"]["name"])
        print("Execution time for the query (in seconds): ", end_time - start_time)


if queryNum == '7':
    with driver.session() as session:
        start_time = time.time()
        result = session.run(f"""
                MATCH (n)
                RETURN COUNT(DISTINCT n.name) AS uniqueNamesCount;           
                """)
        end_time = time.time()
        print(f"Here is the number of distinct nodes: ")
        for record in result:
            print(record["uniqueNamesCount"])
        print("Execution time for the query (in seconds): ", end_time - start_time)


if queryNum == '8':
    with driver.session() as session:
        start_time = time.time()
        result = session.run(f"""
                MATCH (n)
                WHERE NOT (n)<-[:HAS_SUBCATEGORY]-()
                RETURN n;           
                """)
        end_time = time.time()
        print(f"Here is the number of root nodes: ")
        for record in result:
            print(record["n"]["name"])
        print("Execution time for the query (in seconds): ", end_time - start_time)


if queryNum == '9':
    with driver.session() as session:
        start_time = time.time()
        result = session.run(f"""
                MATCH (parent)-[:HAS_SUBCATEGORY]->(child)
                WITH parent, COUNT(child) AS numChildren

                ORDER BY numChildren DESC
                LIMIT 1
                WITH numChildren

                MATCH (parent)-[:HAS_SUBCATEGORY]->(child)
                WITH parent, COUNT(child) AS numChildren, numChildren AS maxChildren
                WHERE numChildren = maxChildren

                RETURN parent, numChildren       
                """)
        end_time = time.time()
        print(f"Here are nodes with the most children (and child count): ")
        for record in result:
            print(record["parent"]["name"], record["numChildren"])
        print("Execution time for the query (in seconds): ", end_time - start_time)




if queryNum == '10':
    with driver.session() as session:
        start_time = time.time()
        result = session.run(f"""
                PROFILE
                MATCH (parent)-[:HAS_SUBCATEGORY]->(child)
                WITH parent, COUNT(child) AS numChildren
                WHERE numChildren > 0 
                             
                WITH parent, numChildren
                ORDER BY numChildren ASC
                LIMIT 1
                WITH numChildren AS minChildren

                MATCH (parent)-[:HAS_SUBCATEGORY]->(child)
                WITH parent, COUNT(child) AS numChildren, minChildren
                WHERE numChildren = minChildren

                RETURN parent, numChildren;
                """)
        end_time = time.time()
        print(f"Here are nodes with the least children (and child count): ")
        for record in result:
            print(record["parent"]["name"], record["numChildren"])
        print("Execution time for the query (in seconds): ", end_time - start_time)


if queryNum == '11':
    with driver.session() as session:
        start_time = time.time()
        result = session.run(f"""
                MATCH (n {{name: "{inputForQuery}" }})
                SET n.name = '{secondInput}'
                RETURN n;
                """)
        end_time = time.time()
        print(f"Renamed node {inputForQuery}")
        for record in result:
            print("to ", record["n"]["name"])

        print("Execution time for the query (in seconds): ", end_time - start_time)


if queryNum == '12':
    with driver.session() as session:
        start_time = time.time()
        result = session.run(f"""
                MATCH (startNode:Category {{name: "{inputForQuery}" }}), (endNode:Category {{name: "{secondInput}" }})
                MATCH path = ((startNode)-[*..10]->(endNode))
                RETURN path;
                """)
        end_time = time.time()
        print(f"All paths between {inputForQuery} and {secondInput}:")
        path_count = 0
        for record in result:
            path_count += 1
            path = record["path"]
            nodes_in_path = [node["name"] for node in path.nodes]
            print(f"{path_count}. {' -> '.join(nodes_in_path)}")
        print("Execution time for the query (in seconds): ", end_time - start_time)