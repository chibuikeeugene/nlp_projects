from smolagents import CodeAgent, DuckDuckGoSearchTool, FinalAnswerTool, load_tool, tool, HfApiModel
import requests
from datetime import datetime as dt
import pytz
import yaml


# create a time tool
@tool
def get_current_time_in_timezone(timezone:str) -> str:
    """A tool that fetches the current local time in a specified timezone
    
    Args:
    * timezone -  a string representing a valid timezone.(e.g., America/New_york)"""

    try:
        # get the timezone
        timezone = pytz.timezone(timezone)

        # get the time of the timezone
        time = dt.now(timezone).strftime( "%d/%m/%Y %H:%M:%S")

        return f'The current time in this zone {timezone} is: {time}'
    except Exception as e:
        return f'Unable to fetch the time for {timezone} due to {str(e)}'


# create a final answer tool
final_answer = FinalAnswerTool()

# create llm model object
model = HfApiModel(
    max_tokens = 2096,
    temperature = 0.5
)

with open('prompts.yaml', mode='r') as stream:
    prompt_template = yaml.safe_load(stream)

# create the code agent
agent = CodeAgent(
    tools=[get_current_time_in_timezone],
    model=model,
    max_steps =6,
    prompt_templates=prompt_template,
    grammar=None,

)

