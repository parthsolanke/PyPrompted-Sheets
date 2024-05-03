from utils.data_manager import DataManager
from utils.data_scraper import DataScraper
from utils.prompts_sequence import *

SAVE_PATH = "./data/output.csv"

def main():
    data_scraper = DataScraper()
    data_manager = DataManager()
    openai_chat = OpenAIChat()
    
    df = data_manager.get_dataframe()
    df["content"] = ""
    df["response1"] = ""
    df["response2"] = ""
    df["response3"] = ""
    
    for url, content in zip(df["companywebsite"].tolist(), df["content"].tolist()):
        if not content:
            content = data_scraper.scrape_content(url)
            if content == "N/A":
                df.loc[df["companywebsite"] == url, "content"] = "N/A"
                df.loc[df["companywebsite"] == url, "response1"] = "N/A"
                df.loc[df["companywebsite"] == url, "response2"] = "N/A"
                df.loc[df["companywebsite"] == url, "response3"] = "N/A"
                continue
            else:
                df.loc[df["companywebsite"] == url, "content"] = content
    
                prompt1 = get_prompt1(content)
                response1 = openai_chat.query_chat(prompt1)
                df.loc[df["content"] == content, "response1"] = response1
                
                prompt2 = get_prompt2(response1)
                response2 = openai_chat.query_chat(prompt2)
                df.loc[df["content"] == content, "response2"] = response2
                
                prompt3 = get_prompt3(response1, response2)
                response3 = openai_chat.query_chat(prompt3)
                df.loc[df["content"] == content, "response3"] = response3
        
    data_manager.save_dataframe(df, SAVE_PATH)
    
    
if __name__ == "__main__":
    main()
    
    