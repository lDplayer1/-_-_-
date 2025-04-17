from classes.super_class import superclass
import random
from SPARQLWrapper import SPARQLWrapper, JSON

class country(superclass):
    def __init__(self):
        super().__init__()
        self.name = "Country"
        self.filters = {'populationTotal': '(?populationTotal > 30000000)'}
        self.opt = "capital"
        self.wrongOpt = "City"
    
def query_cities_of_country(country):
    query = f"""
    SELECT ?city WHERE {{
      ?city rdf:type <http://dbpedia.org/ontology/City>.
      ?city <http://dbpedia.org/ontology/country> <http://dbpedia.org/resource/{country}>.
    }}
    """
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    
    cities = [result["city"]["value"].split("/")[-1].replace('_',' ') for result in results["results"]["bindings"]]
    
    if len(cities) < 4:
        return False
    else:
        return cities
