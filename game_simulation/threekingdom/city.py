from .tavern import Tavern
from .barracks import Barracks
from .market import Market
from .farm import Farm
from .townhall import TownHall
class City:
    def __init__(self,name, population, army, food, money, power):
        self.name = name
        self.population = population
        self.army = army
        self.food = food
        self.money = money
        self.power = power
        self.tavern = Tavern(1)
        self.barracks = Barracks(1)
        self.market = Market(1)
        self.town_hall = TownHall(1)
        self.farm = Farm(1)
        self.surrounding_cities = []

    def add_surrounding_city(self, city):
        self.surrounding_cities.append(city)

    def get_surrounding_city(self):
        return self.surrounding_cities

 