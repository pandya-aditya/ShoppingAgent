from google.adk.agents import Agent
from pydantic import BaseModel, Field
import pandas as pd


def filter_products(price: float, condition: str, dataset: list) -> dict:
    """
    Filters the inventory for items that are above or below a specific price.
    
    Args:
        price: The numeric price threshold (e.g., 50.0).
        condition: Must be either "above" or "below".
        dataset: The list of items to filter.
        
    Returns:
        dict: A dictionary containing the status and the list of matching items.
    """

    results = []
    
    for item in dataset:
        if condition == "below" and item["price"] < price:
            results.append(item)
        elif condition == "above" and item["price"] > price:
            results.append(item)
    print(results)
    return {
        "items": results
    }

class ShoppingOutput(BaseModel):
    response: str = Field(
        description="The subject line of the email. Should be concise and descriptive."
    )
    items: list = Field(
        description="List of all of the items in the json format as specified in the instruction."
    )

df = pd.read_json('data.json')

data = df.to_dict(orient='records')

root_agent = Agent(
    name="greeting_agent",
    model="gemini-2.0-flash",
    description="Categorization agent",
    instruction="""
    You are a tool that categorizes the dataset {data} based on user queries and answers questions about the categorized dataset. 
    Once you determine the categroy and the list of items that fit that category, you may use the tool 'filter_products' to filter items based on price if the user requests it.
    Pass the price that the are filtering based on, pass whether its looking for products above or below that price and pass the list of items that match the user's query

    IMPORTANT: Your response MUST be valid JSON matching this structure:
        {
            "response": "A friendly salesman like response to the user's query witha. focus on selling the products. Using classic sales tatics to persuade you to buy",
            "items": [
                {
                    "id": 0,
                    "name": "Name of item",
                    "description": "Description of item.",
                    "price": price_value,
                    "image": "image_url_here"
                },
                ...
            ]
        }

        Make sure the response in the output comes off very friendly and the response should be formatted such that it should come off as natural language. There shouldn't be
        unecessary asterisks or markdown formatting in the output. The output should be concise and to the point.
        DO NOT include any explanations or additional text outside the JSON response. IMPORTANT: the items list maintains perfect list formatting without any extra characters

    """,
    # tools=[filter_products],
    output_schema=ShoppingOutput,    
)
