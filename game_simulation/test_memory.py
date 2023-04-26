import sys 
import unittest
import datetime

from utils.text_generation import embedding
from memories.memory import Memory
from memories.memory_type import MemoryType
class TestMemory(unittest.TestCase):
    def test_retieval_score(self):
        now = datetime.datetime.now() 
        memtime = now - datetime.timedelta(hours = 30)

        description = "John Lin is living with his wife, Mei Lin, who is a college professor, and son, Eddy Lin, who is a student studying music theory"
        query = "What is John Lin’s relationship with the Eddy Lin?"
        query2 = "What topic is Klaus Mueller passionate about?"
        embedding_description = embedding(description,False)
        embedding_query = embedding(query,False)
        embedding_query2 = embedding(query2,False)

        mem = Memory(MemoryType.OBSERVATION,"Klaus Mueller is writing a research paper",memtime,memtime,1,embedding_description)
        score1 = mem.retieval_score(now,embedding_query)
        score2 = mem.retieval_score(now,embedding_query2)
        print(score1)
        print(score2)
        self.assertGreater(score1,score2)
 
unittest.main()