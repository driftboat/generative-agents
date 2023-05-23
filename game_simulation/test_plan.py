import datetime
import unittest

from utils.text_generation import generate 

class TestPlan(unittest.TestCase): 
    def test_daily_plan(self):
        summary = "Name: Eddy Lin (age: 19)\nInnate traits: friendly, outgoing, hospitable Eddy Lin is a student at Oak Hill College studying music theory and composition. He loves to explore different musical styles and is always looking for ways to expand his knowledge. Eddy Lin is working on a composition project for his college class. He is also taking classes to learn more about music theory. Eddy Lin is excited about the new composition\nhe is working on but he wants to dedicate more hours in the day to work on it in the coming days"
        des = "Today is Wednesday February 13. Here is Eddy’s plan today in broad strokes: 1)"
        pre_daily_plan = "On Tuesday February 12, Eddy 1) woke up and completed the morning routine at 7:00 am,2) go to Oak Hill College to take classes starting 10:00 am, 3) have lunch at 12:00 am,4) work on his new music composition from 1:00 pm to 5:00 pm,5) have dinner at 5:30 pm,6) got ready to sleep around 10 pm."
        prompt = f"{summary}\n{pre_daily_plan}\n{des}"
        res = generate(prompt,False)
        print(res)
        self.assertIsNotNone(res)

        summary = "Name: John Lin (40)\nJohn Lin is a compassionate pharmacist who values meaningful relationships with others and works hard to make the shopping experience at the Willow Market and Pharmacy as easy and seamless as possible for customers. He also is a good listener and will help customers understand how their medications will affect their health and safety.\nJohn Lin is a shopkeeper at the Willow Market and Pharmacy and he spends most of his time meeting and getting to know his various neighbors and their respective stories.\nJohn Lin is optimistic about his recent progress in life. He has achieved a great deal in terms of making meaningful connections with family and friends, creating meaningful relationships with co-workers and neighbors, and gaining knowledge in the local area. John is also grateful for the opportunities that his job at the Willows Market and Pharmacy has presented for him to develop new relationships."
        des = "Today is Monday May 08. Here is John Lin’s plan today in broad strokes: 1)"
        pre_daily_plan =  "On Sunday May 07, John Lin 1) woke up and completed the morning routine at 7:00 am,2) watch tv starting 10:00 am, 3) have lunch at 12:00 am,4) visit the zoo from 1:00 pm to 5:00 pm,5) have dinner at 5:30 pm,6) got ready to sleep around 10 pm."
        prompt = f"{summary}\n{pre_daily_plan}\n{des}"
        res = generate(prompt,False)
        print(res)

unittest.main()