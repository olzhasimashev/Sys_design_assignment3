from neo4j import GraphDatabase

# Initialize Neo4j connection
uri = "bolt://localhost:7687"
driver = GraphDatabase.driver(uri, auth=("neo4j", "qeijbatmtk7e"))  # Replace 'password' with your neo4j password

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
