import json
import networkx as nx
from agents.agent import Agent
from locations.locations import Locations
from utils.text_generation import summarize_simulation
from  threekingdom.citymgr import CityMgr
from  threekingdom.powermgr import PowerMgr
from memories.memory_type import MemoryType
from datetime import datetime, timedelta
import locale 
locale.setlocale(locale.LC_TIME, 'zh_CN')  
# Set default value for prompt_meta if not defined elsewhere
prompt_meta = '### Instruction:\n{}\n### Response:'

# Initialize global time and simulation variables
global_time = 0
repeats = 5

log_locations = False
log_actions = True
log_plans = False
log_ratings = False
log_memories = False

print_locations = True
print_actions = True
print_plans = True
print_ratings = True
print_memories = False 

use_openai=False

# Start simulation loop
whole_simulation_output = ""
powerMgr = PowerMgr()
powerMgr.create_powers()
cityMgr = CityMgr()
cityMgr.create_cities(powerMgr)

# Load town areas and people from JSON file
with open('simulation_config.json', 'r', encoding='UTF-8') as f:
    town_data = json.load(f)

town_people = town_data['town_people']

# Initialize agents and locations
agents = []
locations = Locations()

 
now = datetime(214, 1, 1)
for name, people in town_people.items():
    starting_location = people['starting_location']
    des_arr = people['description'].split(";")
    agent = Agent(name,40, starting_location, use_openai)
    for des in des_arr: 
        agent.add_memory_with_importance(now,des, MemoryType.OBSERVATION,10,prompt_meta)
    agent.gen_summary(prompt_meta)
    agents.append(agent)

for repeat in range(repeats):
    #log_output for one repeat
    log_output = ""

    print(f"====================== REPEAT {repeat} ======================\n")
    log_output += f"====================== REPEAT {repeat} ======================\n"
    for agent in agents:
        daily_plan = agent.retrive_cur_daily_plain(now)
        if daily_plan == None:
            if repeat != 0:
                agent.gen_reflection(prompt_meta)
            daily_plan = agent.gen_daily_plan(now,prompt_meta)
            log_output += f"{agent.name} daily plan: {daily_plan.description}\n"
        hour_plan = agent.retrive_cur_hour_plain(now)
        if hour_plan == None:
            hour_plan = agent.gen_hour_plan(now, prompt_meta)
            log_output += f"{agent.name} hour plan: {hour_plan.description}\n"
        action = agent.retrive_cur_action(now)
        if action == None:
            action = agent.gen_action(now,30, prompt_meta)
            log_output += f"{agent.name} action: {action.description}\n"


    whole_simulation_output += log_output

    # Increment time
    now +=  timedelta(minutes=30)
    global_time += 1

# Write log output to file
with open('simulation_log.txt', 'w', encoding='UTF-8') as f:
    f.write(whole_simulation_output)