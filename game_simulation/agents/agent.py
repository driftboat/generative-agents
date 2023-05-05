import datetime
import random
from memories.memory_type import MemoryType
from utils.text_generation import embedding, generate, get_rating
from memories.memory import Memory
import networkx as nx

class Agent:
     
    """
    A class to represent an individual agent in a simulation similar to The Sims.

    Attributes:
    -----------
    name : str
        The name of the agent.
    age: int
        The age of the agent.
    description : str
        A brief description of the agent.
    location : str
        The current location of the agent in the simulated environment.
    memories : list
        A list of memories the agent has about their interactions.
    compressed_memories : list
        A list of compressed memories that summarize the agent's experiences.
    plans : str
        The agent's daily plans, generated at the beginning of each day.
    
    summary : str
        The agent’s name, age, and traits are concatenated with these three
summaries as the cached summary.



    Methods:
    --------
    plan(global_time, town_people, prompt_meta):
        Generates the agent's daily plan.
    
    execute_action(other_agents, location, global_time, town_areas, prompt_meta):
        Executes the agent's action based on their current situation and interactions with other agents.
    
    update_memories(other_agents, global_time, action_results):
        Updates the agent's memories based on their interactions with other agents.
    
    compress_memories(memory_ratings, global_time, MEMORY_LIMIT=10):
        Compresses the agent's memories to a more manageable and relevant set.
    
    rate_locations(locations, town_areas, global_time, prompt_meta):
        Rates different locations in the simulated environment based on the agent's preferences and experiences.
    """
     
    def __init__(self, name, age , starting_location, world_graph, use_openai):
        self.name = name
        self.age = age 
        self.location = starting_location
        self.memory_ratings = []
        self.memories = []
        self.compressed_memories = []
        self.plans = ""
        self.world_graph = world_graph
        self.use_openai = use_openai
        
    def __repr__(self):
        return f"Agent({self.name}, {self.location})"
    
    def plan(self, global_time, prompt_meta):
        """
        Generates the agent's daily plan.
        
        Parameters:
        -----------
        global_time : int
            The current time in the simulation.
        prompt_meta : str
            The prompt used to generate the plan.
        """

        prompt = "You are {}. The following is your description: {} You just woke up. What is your goal for today? Write it down in an hourly basis, starting at {}:00. Write only one or two very short sentences. Be very brief. Use at most 50 words.".format(self.name, self.description, str(global_time))
        self.plans = generate(prompt_meta.format(prompt), self.use_openai)
    
    def execute_action(self, other_agents, location, global_time, town_areas, prompt_meta):

        """Executes the agent's action based on their current situation and interactions with other agents.
        
        Parameters:
        -----------
        other_agents : list
            A list of other Agent objects in the simulation.
        location : Location
            The current Location object where the agent is located.
        global_time : int
            The current time in the simulation.
        town_areas : dict
            A dictionary of Location objects representing different areas in the simulated environment.
        prompt_meta : str
            The prompt used to generate the action.

        Returns:
        --------
        action : str
            The action executed by the agent.
        """

        people = [agent.name for agent in other_agents if agent.location == location]
        
        prompt = "You are {}. Your plans are: {}. You are currently in {} with the following description: {}. It is currently {}:00. The following people are in this area: {}. You can interact with them.".format(self.name, self.plans, location.name, town_areas[location.name], str(global_time), ', '.join(people))
        
        people_description = [f"{agent.name}: {agent.description}" for agent in other_agents if agent.location == location.name]
        prompt += ' You know the following about people: ' + '. '.join(people_description)
        
        prompt += "What do you do in the next hour? Use at most 10 words to explain."
        action = generate(prompt_meta.format(prompt), self.use_openai)
        return action
    
    def update_memories(self, other_agents, global_time, action_results):
        
        """
        Updates the agent's memories based on their interactions with other agents.
        
        Parameters:
        -----------
        other_agents : list
            A list of other Agent objects in the simulation.
        global_time : int
            The current time in the simulation.
        action_results : dict
            A dictionary of the results of each agent's action.
        """

        for agent in other_agents:
            if agent.location == self.location:
                self.memories.append('[Time: {}. Person: {}. Memory: {}]\n'.format(str(global_time), agent.name, action_results[agent.name]))

    def compress_memories(self, global_time, MEMORY_LIMIT=10):

        """
        Compresses the agent's memories to a more manageable and relevant set.
        
        Parameters:
        -----------
        global_time : int
            The current time in the simulation.
        MEMORY_LIMIT : int, optional
            The maximum number of memories to compress. Default is 10.

        Returns:
        --------
        memory_string : str
            The compressed memory string.
        """

        memories_sorted = sorted(self.memory_ratings, key=lambda x: x[1], reverse=True)
        relevant_memories = memories_sorted[:MEMORY_LIMIT]
        memory_string_to_compress = '.'.join([a[0] for a in relevant_memories])
        return '[Recollection at Time {}:00: {}]'.format(str(global_time), memory_string_to_compress)
    
    def rate_memories(self, locations, global_time, prompt_meta):

        """
         Rates the agent's memories based on their relevance and importance.
        
        Parameters:
        -----------
        locations : Locations
            The Locations object representing different areas in the simulated environment.
        global_time : int
            The current time in the simulation.
        prompt_meta : str
            The prompt used to rate the memories.

        Returns:
        --------
        memory_ratings : list
            A list of tuples representing the memory, its rating, and the generated response.
        """

        memory_ratings = []
        for memory in self.memories:
            prompt = "You are {}. Your plans are: {}. You are currently in {}. It is currently {}:00. You observe the following: {}. Give a rating, between 1 and 5, to how much you care about this.".format(self.name, self.plans, locations.get_location(self.location), str(global_time), memory)
            res = generate(prompt_meta.format(prompt), self.use_openai)
            rating = get_rating(res)
            max_attempts = 2
            current_attempt = 0
            while rating is None and current_attempt < max_attempts:
                rating = get_rating(res)
                current_attempt += 1
            if rating is None:
                rating = 0
            memory_ratings.append((memory, rating, res))
        self.memory_ratings = memory_ratings
        return memory_ratings


    def rate_locations(self, locations, global_time, prompt_meta):

        """
        Rates different locations in the simulated environment based on the agent's preferences and experiences.
        
        Parameters:
        -----------
        locations : Locations
            The Locations object representing different areas in the simulated environment.
        global_time : int
            The current time in the simulation.
        prompt_meta : str
            The prompt used to rate the locations.

        Returns:
        --------
        place_ratings : list
            A list of tuples representing the location, its rating, and the generated response.

        """

        place_ratings = []
        for location in locations.locations.values():
            prompt = "You are {}. Your plans are: {}. It is currently {}:00. You are currently at {}. How likely are you to go to {} next?".format(self.name, self.plans, str(global_time), locations.get_location(self.location), location.name)
            res = generate(prompt_meta.format(prompt), self.use_openai)
            rating = get_rating(res)
            max_attempts = 2
            current_attempt = 0
            while rating is None and current_attempt < max_attempts:
                res = generate(prompt_meta.format(prompt), self.use_openai)
                rating = get_rating(res)
                current_attempt += 1
            if rating is None:
                rating = 0
            place_ratings.append((location.name, rating, res))
        self.place_ratings = place_ratings
        return sorted(place_ratings, key=lambda x: x[1], reverse=True)
    
    def move(self, new_location_name):

        if new_location_name == self.location:
            return self.location

        try:
            path = nx.shortest_path(self.world_graph, source=self.location, target=new_location_name)
            self.location = new_location_name
        except nx.NetworkXNoPath:
            print(f"No path found between {self.location} and {new_location_name}")
            return self.location

        return self.location
    
    def description_importance(self,description, prompt_meta):
        prompt = "On the scale of 1 to 10, where 1 is purely mundane(e.g., brushing teeth, making bed) and 10 is extremely poignant (e.g., a break up, college acceptance),rate the likely poignancy of the following piece of memory.\n Memory:{} \n ".format(description)
        res = generate(prompt_meta.format(prompt), self.use_openai)
        
        rating = get_rating(res)
        max_attempts = 2
        current_attempt = 0
        while rating is None and current_attempt < max_attempts:
            res = generate(prompt_meta.format(prompt), self.use_openai)
            rating = get_rating(res)
            current_attempt += 1
        if rating is None:
            rating = 0
        return rating
    
    def add_memory(self, time,description,description_vec, prompt_meta):
        importance = self.description_importance(description,prompt_meta)
        description_vec = embedding(description,self.use_openai)
        mem = Memory(MemoryType.OBSERVATION, description, time,time,importance,description_vec )
        self.memories.append(mem)

    def retrieve_memories(self, query, MEMORY_LIMIT=20):
        query_vec = embedding(query,self.use_openai)
        now = datetime.datetime.now()
        sorted_memories = sorted(self.memories, key=lambda x:x.retieval_score(now,query_vec), reverse=True)
        retrieved = sorted_memories[:MEMORY_LIMIT]
        return retrieved
    
    def gen_summary_for(self,summary_des, prompt_meta):
        mems = self.retrieve_memories(f"{self.name}’s {summary_des}")
        query = f"How would one describe {self.name}’s {summary_des}\ngiven the following statements?"
        mem_des_arr = [mem.description for mem in mems ]
        memsstr = "\n-".join(mem_des_arr)
        query = f"{query}\n-{memsstr}"
        res = generate(prompt_meta.format(query), self.use_openai)
        return res
    
    def gen_summary(self, prompt_meta):
        name = f"Name: {self.name} ({self.age})"
        core_characteristics = self.gen_summary_for("core characteristics", prompt_meta)
        daily_occupation = self.gen_summary_for("current daily occupation", prompt_meta)
        recent_progress = self.gen_summary_for("feeling about his recent progress in life", prompt_meta)
        self.summary = f"{name}\n{core_characteristics}\n{daily_occupation}\n{recent_progress}"
  
