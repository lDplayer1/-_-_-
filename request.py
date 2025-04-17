from SPARQLWrapper import SPARQLWrapper, JSON
import numpy as np
import pandas as pd
import random
sparql = SPARQLWrapper("http://dbpedia.org/sparql")


def table_generator(classtype):
    """
    参数：自定义的类
    返回：关键字的表和选项
    """

    classname = classtype.name
    filter_dict = classtype.filters
    option = classtype.opt
    query = f"""
    SELECT ?{classname} ?{option} WHERE {{
    ?{classname} rdf:type <http://dbpedia.org/ontology/{classname}>.
    """
    for filter_key, filter_value in filter_dict.items():
        if filter_key.find('undefined') < 0:
            query += f"""
            ?{classname} <http://dbpedia.org/ontology/{filter_key}> ?{filter_key}.
            """
        query += f""" 
        FILTER {filter_value}
        """
    query += f"""
    OPTIONAL {{?{classname} <http://dbpedia.org/ontology/{option}> ?{option}.
    }}
    }}
    """
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    quiz_dict = {}
    ## 字典中，key是问题主题，值是正确答案
    for result in results["results"]["bindings"]:
        quizText = result[classname]["value"].split("/")[-1].replace("_", " ")
        if quizText.find("History") >= 0:
            continue
        try:
            rightOpt = result[option]["value"].split("/")[-1].replace("_", " ")
        except KeyError:
            continue
        quiz_dict[quizText] = rightOpt
    return quiz_dict

def get_official_languages(country_name):
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    
    # 构建 SPARQL 查询
    # 这里假设我们用国家的英文名称来做检索，并且匹配 rdfs:label 为 "xxx"@en
    query = f"""
    PREFIX dbo: <http://dbpedia.org/ontology/>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    
    SELECT DISTINCT ?language
    WHERE {{
        ?country a dbo:Country ;
                 rdfs:label "{country_name}"@en ;
                 dbo:officialLanguage ?language .
    }}
    """
    
    # 设置查询和返回格式
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    
    # 执行查询
    results = sparql.query().convert()
    
    # 解析结果
    languages = []
    for result in results["results"]["bindings"]:
        languages.append(result["language"]["value"])
    
    return languages

if __name__ == "__main__":
    country = "China"  # 你可以换成其它国家英文名，例如 "France"、"Germany" 等
    official_languages = get_official_languages(country)
    print(f"Official languages of {country}: {official_languages}")