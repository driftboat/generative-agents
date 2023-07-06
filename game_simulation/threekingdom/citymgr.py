class CityMgr:
    def __init__(self):
        self.cities = {}

    def add_city(self, city):
        self.cities[city.name] = city
        
    def create_cities(self):
        cities = ["洛阳", "凉州", "北京", "许昌", "长沙", "成都", "建业", "交趾","汉中"]
        powers = ["魏", "魏", "魏", "魏", "蜀", "蜀", "吴", "吴", "张鲁"]

        for city_name, power in zip(cities, powers):
            city = City(city_name, 20000, 10000, 20000, 2000, power)  # Initialize population, army, food, money to 0
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
        self.addconnection(changsha, chengdu)
        self.addconnection(chengdu, hanzhong)
        self.addconnection(changsha, jiaozhi)

    
    def addconnection(self, src, target):
        src.add_surrounding_city(target)
        target.add_surrounding_city(src)
    
    def get_city(self, city_name):
        return self.cities.get(city_name)

        


