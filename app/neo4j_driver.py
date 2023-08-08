import os
from neo4j import GraphDatabase

host = os.environ.get('bolt://44.200.13.113:7687')
user = os.environ.get('neo4j')
password = os.environ.get('fund-rest-umbrella')
driver = GraphDatabase.driver(host, auth=(user, password))


def run_query(query, params={}):
    with driver.session() as session:
        result = session.run(query, params)
        response = [r.values()[0] for r in result]
        return response


if __name__ == '__main__':
    print(run_query("""
    MATCH (m:Movie {title:"Copycat"})<-[:ACTED_IN]-(a)
    RETURN {actor: a.name} AS result;
    """))
