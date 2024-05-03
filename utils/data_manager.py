import os
from pathlib import Path
from dotenv import load_dotenv
import requests
import pandas as pd

env_path = Path.cwd() / '.env'
load_dotenv(dotenv_path=env_path)

class DataManager:
    """
    A class that manages data retrieval and manipulation.

    Attributes:
        data (dict): A dictionary to store the retrieved data.
        df (pandas.DataFrame): A DataFrame to store the data in tabular format.

    Methods:
        get_data: Retrieves data from a specified endpoint.
        get_dataframe: Converts the retrieved data into a DataFrame.
        update_data: Updates the Google Sheet with the new data.

    """

    def __init__(self):
        self.data = {}
        self.df = pd.DataFrame()

    def get_data(self):
        """
        Retrieves data from a specified endpoint.

        Returns:
            dict: The retrieved data.

        Raises:
            requests.exceptions.HTTPError: If the request to the endpoint fails.

        """
        try:
            response = requests.get(url=os.environ.get("SHEETY_API"))
            response.raise_for_status()
            sheet = response.json()
            self.data = sheet.get("targetCompanyData", {})
            return self.data
        except requests.RequestException as e:
            print(f"Error retrieving data: {e}")
            return {}

    def get_dataframe(self):
        """
        Converts the retrieved data into a DataFrame.

        Returns:
            pandas.DataFrame: The data in tabular format.

        """
        self.df = pd.DataFrame(self.get_data())
        return self.df
    
    def save_dataframe(self, df, path):
        """
        Saves the DataFrame to a CSV file.

        Args:
            df (pandas.DataFrame): The DataFrame to be saved.
            path (str): The path to save the CSV file.

        """
        df.to_csv(path, index=False)
        print(f"Data saved to {path}")
        
    def update_data(self, df):
        """
        Updates the Google Sheet with the new data.

        Args:
            df (pandas.DataFrame): The new DataFrame containing the updated data.

        Returns:
            requests.models.Response: The response from the Google Sheet API.

        """
        try:
            headers = {
                "Content-Type": "application/json"
            }
            endpoint = os.environ.get('SHEETY_API')
            
            batch_size = 10
            num_batches = len(df) // batch_size + (1 if len(df) % batch_size != 0 else 0)

            responses = []
            for batch_num in range(num_batches):
                start_index = batch_num * batch_size
                end_index = min((batch_num + 1) * batch_size, len(df))
                
                batch_data = []
                for index, row in df.iloc[start_index:end_index].iterrows():
                    content = str(row["content"])
                    batch_data.append({
                        "targetCompanyData": {
                            "content": content,
                        }
                    })

                response = requests.put(url=endpoint, headers=headers, json=batch_data)
                response.raise_for_status()
                responses.append(response)

            return responses
        except requests.RequestException as e:
            print(f"Error updating data: {e}")
            return None


