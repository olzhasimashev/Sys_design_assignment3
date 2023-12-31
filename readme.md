# Group Members

| No | Name              |
|----|-------------------|
| 1  | Kaliyev Alikhan   |
| 2  | Kim Aleksandr     |
| 3  | Zhumash Imangali  |
| 4  | Imashev Olzhas    |
| 5  | Akhmullaev Sultan |
| 6  | Ayupov Zhandos    |
| 7  | Tolkachev Dmitriy |
| 8  | Ugai Artem        |

# Dependency Graph Analysis with Neo4j

## Prerequisites

- Docker
- Python 3.x
- Neo4j Python driver, pandas, and openpyxl

## Setup

1. **Install Docker:**
   - If Docker is not installed, download and install Docker from [here](https://www.docker.com/products/docker-desktop).

2. **Run Neo4j Docker Container:**
   - Open a terminal and execute the following command to pull and run the Neo4j Docker container:
     ```bash
     docker run \
       --name neo4j \
       -p7474:7474 -p7687:7687 \
       -d \
       neo4j
     ```

3. **Create virtual environment:**
   - Execute the following command to create a virtual environment. Replace 'name_of_venv' with tour desired name:
     ```bash
     python -m venv name_of_venv
     ```

4. **Install Required Python Libraries:**
   - Execute the following command to install the required libraries:
     ```bash
     pip install neo4j pandas openpyxl
     ```

## Execution

1. **Define Schema and Load Data:**
   - Create a new file named `load_data.py` and copy the code from below into the file:
     ```python
     from neo4j import GraphDatabase

     # Initialize Neo4j connection
     uri = "bolt://localhost:7687"
     driver = GraphDatabase.driver(uri, auth=("neo4j", "password"))  # Replace 'password' with your neo4j password

     def create_schema(tx):
         # Create nodes
         tx.run("CREATE (:Component {name: 'User Service'})")
         tx.run("CREATE (:Component {name: 'Tweet Service'})")
         tx.run("CREATE (:Component {name: 'Notification Service'})")
         # Create relationships
         tx.run("MATCH (a:Component {name: 'User Service'}), (b:Component {name: 'Tweet Service'}) CREATE (a)-[:DEPENDS_ON]->(b)")
         tx.run("MATCH (a:Component {name: 'User Service'}), (b:Component {name: 'Notification Service'}) CREATE (a)-[:DEPENDS_ON]->(b)")
         tx.run("MATCH (a:Component {name: 'Tweet Service'}), (b:Component {name: 'User Service'}) CREATE (a)-[:DEPENDS_ON]->(b)")
         tx.run("MATCH (a:Component {name: 'Notification Service'}), (b:Component {name: 'User Service'}) CREATE (a)-[:DEPENDS_ON]->(b)")
         tx.run("MATCH (a:Component {name: 'Notification Service'}), (b:Component {name: 'Tweet Service'}) CREATE (a)-[:DEPENDS_ON]->(b)")

     with driver.session() as session:
         session.execute_write(create_schema)
     ```
   - Run `load_data.py` by executing:
     ```bash
     python load_data.py
     ```

2. **Calculate Stability Metrics:**
   - Create a new file named `calculate_metrics.py` and copy the code from below into the file:
     ```python
     import pandas as pd
     from neo4j import GraphDatabase

     # Initialize Neo4j connection
     uri = "bolt://localhost:7687"
     driver = GraphDatabase.driver(uri, auth=("neo4j", "password"))  # Replace 'password' with your neo4j password

     def calculate_metrics(tx):
         # Fan-in and Fan-out
         query = """
         MATCH (a:Component)
         OPTIONAL MATCH (a)<-[:DEPENDS_ON]-(in)
         OPTIONAL MATCH (a)-[:DEPENDS_ON]->(out)
         RETURN a.name as Component, count(DISTINCT in) as Fan_in, count(DISTINCT out) as Fan_out
         """
         result = tx.run(query)
         return pd.DataFrame([dict(record) for record in result])

     with driver.session() as session:
         metrics_df = session.execute_write(calculate_metrics)

     # Calculate Instability
     metrics_df['I'] = metrics_df['Fan_out'] / (metrics_df['Fan_in'] + metrics_df['Fan_out'])

     # Save Metrics to Excel
     metrics_df.to_excel('metrics.xlsx', index=False)
     ```
   - Run `calculate_metrics.py` by executing:
     ```bash
     python calculate_metrics.py
     ```

## Output

- After running `calculate_metrics.py`, an Excel file named `metrics.xlsx` will be generated in the same directory, containing the calculated stability metrics for each component.
