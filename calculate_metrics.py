import pandas as pd
from neo4j import GraphDatabase

# Initialize Neo4j connection
uri = "bolt://localhost:7687"
driver = GraphDatabase.driver(uri, auth=("neo4j", "qeijbatmtk7e"))  # Replace 'password' with your neo4j password

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
