import datetime
import unittest
from agents.agent import Agent
from memories.memory_type import MemoryType
from utils.text_generation import embedding

class TestAgent(unittest.TestCase):
    def setUp(self):
        prompt_meta = '### Instruction:\n{}\n### Response:'
        now = datetime.datetime.now()
        agent = Agent("John Lin",40, "starting_location", "world_graph", True)
        #initial memories
        description = "John Lin is a pharmacy shopkeeper at the Willow Market and Pharmacy who loves to help people. He is always looking for ways to make the process of getting medication easier for his customers; John Lin is living with his wife, Mei Lin, who is a college professor, and son, Eddy Lin, who is a student studying music theory; John Lin loves his family very much; John Lin has known the old couple next-door, Sam Moore and Jennifer Moore, for a few years; John Lin thinks Sam Moore is a kind and nice man; John Lin knows his neighbor, Yuriko Yamamoto, well; John Lin knows of his neighbors, Tamara Taylor and Carmen Ortiz, but has not met them before; John Lin and Tom Moreno are colleagues at The Willows Market and Pharmacy; John Lin and Tom Moreno are friends and like to discuss local politics together; John Lin knows the Moreno family somewhat well — the husband Tom Moreno and the wife Jane Moreno"
        des_arr = description.split(";")
        for des in des_arr: 
            agent.add_memory(now,des, MemoryType.OBSERVATION,prompt_meta)
        agent.gen_summary(prompt_meta)
        print(agent.summary)
        self.assertIsNotNone(agent.summary)
        self.agent = agent
        self.prompt_meta = prompt_meta
        
    def test_importance(self): 
        im1 = self.agent.description_importance("cleanup the room",self.prompt_meta)
        im2 = self.agent.description_importance("asking your crush out on a date.",self.prompt_meta)
        print(im1)
        print(im2)
        self.assertGreater(im2,im1) 

    def test_plan(self):
        now = datetime.datetime.now()
        daily_plan = self.agent.gen_daily_plan(now,self.prompt_meta)
        self.assertIsNotNone(daily_plan)
        print("==============daily plan================")
        print(daily_plan.description)
        hour_plan = self.agent.gen_hour_plan(now,self.prompt_meta)
        self.assertIsNotNone(hour_plan)
        print("==============hour plan================")
        print(hour_plan.description)
        action_plan = self.agent.gen_action(now,5,self.prompt_meta)
        self.assertIsNotNone(action_plan)
        print("==============action plan================")
        print(action_plan.description)
        three_minutes_later = now + datetime.timedelta(minutes=3)        
        cur_atcion_plan = self.agent.retrive_cur_action(three_minutes_later)
        self.assertIsNotNone(cur_atcion_plan)
        print("==============current action================")
        print(action_plan.description)
    

unittest.main()