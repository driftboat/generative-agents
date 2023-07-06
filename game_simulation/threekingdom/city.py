class City:
    def __init__(self,name, population, army, food, money, power):
        self.name = name
        self.population = population
        self.army = army
        self.food = food
        self.money = money
        self.power = power
        self.tavern = Tavern()
        self.barracks = Barracks()
        self.market = Market()
        self.town_hall = TownHall()
        self.farm = Farm()
        self.surrounding_cities = []

    def add_surrounding_city(self, city):
        self.surrounding_cities.append(city)


 