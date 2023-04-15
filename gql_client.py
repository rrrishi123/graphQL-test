import os
import httpx
from dotenv import load_dotenv

load_dotenv()

GRAPHQL_API_ENDPOINT = os.getenv("GRAPHQL_API_ENDPOINT")

# Define the headers for the GraphQL request
headers = {
    "Content-Type": "application/json",
    "Accept": "application/json",
}

async def execute_gql_query(query, variables=None):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            GRAPHQL_API_ENDPOINT,
            json={"query": query, "variables": variables},
            headers=headers
        )
    
    if response.status_code != 200:
        raise Exception(f"GraphQL API request failed with status code {response.status_code}")

    json_response = response.json()

    if "errors" in json_response:
        raise Exception(f"GraphQL API request returned errors: {json_response['errors']}")

    return json_response["data"]
