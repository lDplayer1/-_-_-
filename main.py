from generator import method_1, method_2, method_4, method_5
from classes.country import country, query_cities_of_country
from classes.book import book
from classes.film import film


def main():
    ##method函数填写参数：类的生成，问题数量
    method_5(film(),10)
    method_5(country(),10)
    method_5(book(),10)
    """method_2(film(),10)
    method_4(film(),10)
    method_5(film(),10)
    pass"""

if __name__ == "__main__" :
    main()