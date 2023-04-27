import unittest
from agents.agent import Agent 

class TestAgent(unittest.TestCase):
    def test_importance(self):
        prompt_meta = '### Instruction:\n{}\n### Response:'
        agent = Agent("sa", "simple agent", "starting_location", "world_graph", False)
        im1 = agent.description_importance("cleanup the room",prompt_meta)
        im2 = agent.description_importance("asking your crush out on a date.",prompt_meta)
        print(im1)
        print(im2)
        self.assertGreater(5,im1)
        self.assertGreater(im2,5)

unittest.main()