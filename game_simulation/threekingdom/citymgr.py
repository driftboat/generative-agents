from .city import City
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import networkx as nx
from .powermgr import PowerMgr
class CityMgr:
    def __init__(self):
        self.cities = {}

    def add_city(self, city):
        self.cities[city.name] = city
        
    def create_cities(self, powerMgr):
        cities = ["洛阳", "凉州", "北京", "许昌", "长沙", "成都", "建业", "交趾","汉中"]
        powers = ["魏", "魏", "魏", "魏", "蜀", "蜀", "吴", "吴", "张鲁"]

        for city_name, power in zip(cities, powers):
            city = City(city_name, 20000, 10000, 20000, 2000, powerMgr.get_power(power))   
            self.add_city(city)
         
        loyang = self.get_city("洛阳")
        liangzhou = self.get_city("凉州")
        beijing = self.get_city("北京")
        xuchang = self.get_city("许昌")
        hanzhong = self.get_city("汉中")
        changsha = self.get_city("长沙")
        chengdu = self.get_city("成都")
        jianye = self.get_city("建业")
        jiaozhi = self.get_city("交趾")
        
        self.addconnection(loyang, xuchang)
        self.addconnection(loyang, liangzhou)  
        self.addconnection(liangzhou, hanzhong)
        self.addconnection(beijing, xuchang)
        self.addconnection(xuchang, hanzhong)
        self.addconnection(xuchang, changsha)
        self.addconnection(xuchang, jianye)
        self.addconnection(changsha, hanzhong)
        self.addconnection(changsha, jianye)
        self.addconnection(changsha, jiaozhi)
        self.addconnection(changsha, chengdu)
        self.addconnection(chengdu, hanzhong)
        self.addconnection(jianye, jiaozhi)

    def draw(self):
        fromcities = []
        tocities = []
        names = []
        powers = []
        for city in self.cities.values():
            surrounding_cities = city.get_surrounding_city()
            names.append(city.name)
            powers.append(city.power.id - 1)
            for neighbor in surrounding_cities:
                fromcities.append(city.name)
            
                tocities.append(neighbor.name)

        
        relationships = pd.DataFrame({'from': fromcities, 
                                    'to':   tocities})

        carac = pd.DataFrame({ "cities":cities, 
                      'powers':powers})


        G = nx.from_pandas_edgelist(relationships, 'from', 'to', create_using=nx.Graph())
        carac = carac.set_index('cities')
        carac = carac.reindex(G.nodes())
   
        # Specify colors
        cmap = matplotlib.colors.ListedColormap(['blue', 'green','red',"orange"])

        # Set node_color
        nx.draw(G, with_labels=True,  node_color=carac['powers'], cmap=cmap)
        plt.show()

    
    def addconnection(self, src, target):
        src.add_surrounding_city(target)
        target.add_surrounding_city(src)
    
    def get_city(self, city_name):
        return self.cities.get(city_name)

        



