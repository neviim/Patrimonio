from flask import Flask, request, jsonify
from neo4j import GraphDatabase
import sys
import pandas as pd

class Neo4jCRUDAPI:
    def __init__(self, uri="bolt://localhost:7687", user="neo4j", password="#neo4jcn*"):
        """
        Initialize the Neo4j connection for CRUD operations.
        
        :param uri: Neo4j database URI
        :param user: Neo4j username
        :param password: Neo4j password
        """
        try:
            self.driver = GraphDatabase.driver(uri, auth=(user, password))
            self.driver.verify_connectivity()
        except Exception as e:
            print(f"Erro ao conectar ao Neo4j: {str(e)}")
            sys.exit(1)

    def create_node(self, label, properties):
        """
        Create a new node in the database.
        
        :param label: Node label (e.g., 'Patrimonio', 'Setor')
        :param properties: Dictionary of node properties
        :return: Created node details
        """
        with self.driver.session() as session:
            try:
                # Construct the Cypher query dynamically based on properties
                property_string = ', '.join([f"n.{k} = ${k}" for k in properties.keys()])
                query = f"""
                CREATE (n:{label})
                SET {property_string}
                RETURN n
                """
                
                result = session.run(query, properties)
                record = result.single()
                
                if record:
                    node = record['n']
                    return {
                        'id': node.id,
                        'labels': list(node.labels),
                        'properties': dict(node)
                    }
                return None
            except Exception as e:
                print(f"Erro ao criar nó: {str(e)}")
                return None

    def read_nodes(self, label=None, filter_properties=None, limit=100):
        """
        Read nodes from the database with optional filtering.
        
        :param label: Optional node label to filter
        :param filter_properties: Optional dictionary of properties to filter
        :param limit: Maximum number of nodes to return
        :return: List of nodes matching the criteria
        """
        with self.driver.session() as session:
            try:
                # Construct the base query
                base_query = "MATCH (n"
                if label:
                    base_query += f":{label}"
                base_query += ")"
                
                # Add WHERE clause for filtering if properties are provided
                where_clauses = []
                if filter_properties:
                    where_clauses = [f"n.{k} = ${k}" for k in filter_properties.keys()]
                    base_query += " WHERE " + " AND ".join(where_clauses)
                
                # Add return and limit
                base_query += f" RETURN n LIMIT {limit}"
                
                # Run the query
                result = session.run(base_query, filter_properties or {})
                
                # Process results
                nodes = []
                for record in result:
                    node = record['n']
                    nodes.append({
                        'id': node.id,
                        'labels': list(node.labels),
                        'properties': dict(node)
                    })
                
                return nodes
            except Exception as e:
                print(f"Erro ao ler nós: {str(e)}")
                return []

    def update_node(self, node_id, new_properties):
        """
        Update an existing node's properties.
        
        :param node_id: Internal Neo4j node ID
        :param new_properties: Dictionary of properties to update
        :return: Updated node details or None
        """
        with self.driver.session() as session:
            try:
                # Construct the update query dynamically
                property_string = ', '.join([f"n.{k} = ${k}" for k in new_properties.keys()])
                query = f"""
                MATCH (n)
                WHERE id(n) = $node_id
                SET {property_string}
                RETURN n
                """
                
                # Prepare properties dictionary
                properties = new_properties.copy()
                properties['node_id'] = node_id
                
                result = session.run(query, properties)
                record = result.single()
                
                if record:
                    node = record['n']
                    return {
                        'id': node.id,
                        'labels': list(node.labels),
                        'properties': dict(node)
                    }
                return None
            except Exception as e:
                print(f"Erro ao atualizar nó: {str(e)}")
                return None

    def delete_node(self, node_id):
        """
        Delete a node from the database.
        
        :param node_id: Internal Neo4j node ID
        :return: Boolean indicating success or failure
        """
        with self.driver.session() as session:
            try:
                query = """
                MATCH (n)
                WHERE id(n) = $node_id
                DETACH DELETE n
                RETURN count(n) as deleted_count
                """
                
                result = session.run(query, {'node_id': node_id})
                record = result.single()
                
                return record['deleted_count'] > 0
            except Exception as e:
                print(f"Erro ao deletar nó: {str(e)}")
                return False

    def close(self):
        """
        Close the Neo4j driver connection.
        """
        if self.driver:
            self.driver.close()

# Flask API Setup
app = Flask(__name__)
neo4j_crud = Neo4jCRUDAPI()

@app.route('/node', methods=['POST'])
def create_node():
    """
    Create a new node
    Expects JSON with 'label' and 'properties'
    """
    data = request.json
    if not data or 'label' not in data or 'properties' not in data:
        return jsonify({"error": "Invalid request. Requires 'label' and 'properties'"}), 400
    
    result = neo4j_crud.create_node(data['label'], data['properties'])
    if result:
        return jsonify(result), 201
    return jsonify({"error": "Failed to create node"}), 500

@app.route('/node', methods=['GET'])
def read_nodes():
    """
    Read nodes with optional filtering
    Supports query params: label, limit
    Supports JSON body for complex filtering
    """
    label = request.args.get('label')
    limit = int(request.args.get('limit', 100))
    
    # Check if there's a JSON body for filtering
    filter_properties = request.json if request.is_json else None
    
    result = neo4j_crud.read_nodes(label, filter_properties, limit)
    return jsonify(result)

@app.route('/node/<int:node_id>', methods=['PUT'])
def update_node(node_id):
    """
    Update an existing node
    Expects JSON with new properties
    """
    data = request.json
    if not data:
        return jsonify({"error": "No update properties provided"}), 400
    
    result = neo4j_crud.update_node(node_id, data)
    if result:
        return jsonify(result)
    return jsonify({"error": "Failed to update node"}), 500

@app.route('/node/<int:node_id>', methods=['DELETE'])
def delete_node(node_id):
    """
    Delete a node by its ID
    """
    result = neo4j_crud.delete_node(node_id)
    if result:
        return jsonify({"message": "Node deleted successfully"}), 200
    return jsonify({"error": "Failed to delete node"}), 500

# Graceful shutdown
@app.teardown_appcontext
def close_db(error):
    """
    Close Neo4j connection when Flask app shuts down
    """
    neo4j_crud.close()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)