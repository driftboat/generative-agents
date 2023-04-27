import numpy as np
from utils.text_generation import similar
class Memory:
    def __init__(self,mem_type,description,creat_at,access_at,importance,embedding_vec):
        self.mem_type = mem_type
        self.description = description
        self.create_at = creat_at
        self.access_at = access_at
        self.imprtance = importance
        self.embedding_vec = embedding_vec 

    def retieval_score(self,retriev_at,query_vec):
        
        recency = pow(0.99,(retriev_at - self.access_at).total_seconds() / 3600)
        𝑟𝑒𝑙𝑒𝑣𝑎𝑛𝑐𝑒 = similar(self.embedding_vec , query_vec)
        return recency + self.imprtance + relevance


   