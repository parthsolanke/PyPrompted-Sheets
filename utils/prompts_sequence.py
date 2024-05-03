from string import Template
from pathlib import Path
from dotenv import load_dotenv
import openai
import time
import os

env_path = Path.cwd() / '.env'
load_dotenv(dotenv_path=env_path)
openai.api_key = os.getenv("OPENAI_API_KEY")

class OpenAIChat:
    def __init__(self, model="gpt-3.5-turbo", max_retries=15, sleep_time=2):
        self.model = model
        self.max_retries = max_retries
        self.sleep_time = sleep_time

    def query_chat(self, query) -> str:
        """
        Queries the GPT-3.5 Turbo model with a given message history and returns the response content.

        Args:
            message_history (list): A list of messages exchanged in the conversation.

        Returns:
            str: The content of the response from the GPT-3.5 Turbo model.

        Raises:
            Exception: If the maximum number of retries is exceeded without a successful response.
        """
        retries = 0
        message = [{"role": "system", "content": query}]

        while retries < self.max_retries:
            try:
                response = openai.chat.completions.create(
                    model=self.model,
                    messages=message
                )
                content = response.choices[0].message.content
                if content:
                    return content
            except Exception as e:
                print(f"Error querying GPT-3.5 Turbo: {e}")
                retries += 1
                time.sleep(self.sleep_time)

        raise Exception("Maximum retries exceeded")

prompt1 = Template(
    """
    Here's the raw homepage information of my target company. 

    I need you to convert this into a 200 word summary that is organized in the following manner:

    - Company overview 
    - Product and service offering recap
    - Potential target industries for this company 
    - What is their core USP 
    - How many times have they used the word "AI" in their homepage. 


    Here's the homepage information:
    {homepage_info} 
    """
)

prompt2 = Template(
    """
    I will give you the company overivew of a target company I'm trying to pitch to.

    Can you read through their offering and create a potential sales opportunity for me?

    My company offers custom HR training and modules

    Your potential sales opportunity analysis should be 150 words
    It should have mutliple bullet points and tell me how I can posit my solution 
    Ensure it is hihgy custom built and includes the target companies industry terminology 


    Here's the summary:

    {prompt1_output}
    """
)

prompt3 = Template(
    """
    I will give you a potential sales opportunity analysis for a company I'm targeting 

    You have to create a custom 100 word sales email 

    The email has to look at elements about what the company offers from ###Company overivew### 

    and should include potential sales hooks from ###sales opportunity analysis### 


    Keep the text extremely human and to the point. 


    ###Company overivew### 
    {prompt1_output}

    ###sales opportunity analysis### 
    {prompt2_output}
    """

)

def get_prompt1(homepage_info: str) -> str:
    """
    Generates a prompt for summarizing the raw homepage information of a target company.

    Parameters:
    - homepage_info (str): The raw homepage information of the target company.

    Returns:
    str: The generated prompt for summarizing the homepage information.
    """
    return prompt1.substitute(homepage_info=homepage_info)

def get_prompt2(prompt1_output: str) -> str:
    """
    Generates a prompt for creating a potential sales opportunity based on a company's overview.

    Parameters:
    - prompt2_output (str): The company overview to analyze for potential sales opportunities.

    Returns:
    str: The generated prompt for analyzing the company overview.
    """
    return prompt2.substitute(prompt1_output=prompt1_output)

def get_prompt3(prompt1_output: str, prompt2_output: str) -> str:
    """
    Generates a prompt for creating a custom sales email based on a company's overview and sales opportunity analysis.

    Parameters:
    - prompt1_output (str): The company overview to include in the sales email.
    - prompt2_output (str): The sales opportunity analysis to include in the sales email.

    Returns:
    str: The generated prompt for creating a custom sales email.
    """
    return prompt3.substitute(prompt1_output=prompt1_output, prompt2_output=prompt2_output)
