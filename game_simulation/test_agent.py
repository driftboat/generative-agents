import datetime
import unittest
from agents.agent import Agent 
from utils.text_generation import embedding

class TestAgent(unittest.TestCase):
    def test_importance(self):
        prompt_meta = '### Instruction:\n{}\n### Response:'
        agent = Agent("sa",40, "starting_location", "world_graph", False)
        im1 = agent.description_importance("cleanup the room",prompt_meta)
        im2 = agent.description_importance("asking your crush out on a date.",prompt_meta)
        print(im1)
        print(im2)
        self.assertGreater(5,im1)
        self.assertGreater(im2,5)
    
    def test_summary(self):
        prompt_meta = '### Instruction:\n{}\n### Response:'
        now = datetime.datetime.now()
        agent = Agent("John Lin",40, "starting_location", "world_graph", False)
        #initial memories
        description = "John Lin is a pharmacy shopkeeper at the Willow Market and Pharmacy who loves to help people. He is always looking for ways to make the process of getting medication easier for his customers; John Lin is living with his wife, Mei Lin, who is a college professor, and son, Eddy Lin, who is a student studying music theory; John Lin loves his family very much; John Lin has known the old couple next-door, Sam Moore and Jennifer Moore, for a few years; John Lin thinks Sam Moore is a kind and nice man; John Lin knows his neighbor, Yuriko Yamamoto, well; John Lin knows of his neighbors, Tamara Taylor and Carmen Ortiz, but has not met them before; John Lin and Tom Moreno are colleagues at The Willows Market and Pharmacy; John Lin and Tom Moreno are friends and like to discuss local politics together; John Lin knows the Moreno family somewhat well — the husband Tom Moreno and the wife Jane Moreno"
        des_arr = description.split(";")
        for des in des_arr:
            des_vec = embedding(des,False)
            agent.add_memory(now,des,des_vec,prompt_meta)
        agent.gen_summary(prompt_meta)
        print(agent.summary)
        self.assertIsNotNone(agent.summary)

unittest.main()