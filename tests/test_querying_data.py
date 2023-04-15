import random
import pytest
import asyncio

# Define the possible tokens
tokens = [
    "id",
    "address",
    "chainId",
    "name",
    "symbol",
    "type",
    "totalSupply",
    "decimals",
    "baseURI",
    "lastTransferTimestamp",
    "lastTransferBlock",
    "lastTransferHash",
    "contractMetaData { description }",
    "logo { medium original }",
    "tokenBalances { tokenId amount blockchain }"
]

# Define the common variables for both test cases
variables = {
    "input": {
        "blockchain": "ethereum",
        "limit": 1,
        "cursor": "",
        "filter": {
            "address": {
                "_eq": "0x60e4d786628fea6478f785a6d7e704777c86a7c6"
            }
        }
    }
}

# Define the query for single object

query_token = '''
query Test1($input: TokensInput!) {
  Tokens(input: $input) {
    Token {
      %s
    }
  }
}
'''

# Define the test case for querying a single object
@pytest.mark.asyncio
async def test_query_single_object(gql_client):
    # Choose a random token from the list of tokens
    random_token = random.choice(tokens)

    # Create the query with the randomly chosen token
    query = query_token % random_token

    print("\nselected_token-", random_token, "\n")

    print("\nquery-", query, "\n")

    # Execute the query with the variables
    response_data = await gql_client(query, variables)

    # Print the response data
    print("\nResponse data:", response_data,"\n")

    # Verify that only one object is returned
    assert len(response_data["Tokens"]["Token"]) == 1

    # Verify that the returned object has the expected token
    assert random_token.split(' ')[0] in response_data["Tokens"]["Token"][0]

# Define the test case for querying multiple objects
@pytest.mark.asyncio
async def test_query_multiple_objects(gql_client):
    # Choose a random number between 1 and 15 for the number of tokens to choose
    num_tokens = random.randint(1, 15)

    # Choose that many tokens randomly from the list of tokens without repetition
    chosen_tokens = random.sample(tokens, num_tokens)

    print("\nselected_token-", chosen_tokens, "\n")

    # Create the query with the chosen tokens
    query = query_token % ", ".join(chosen_tokens)

    print("\nqyery-", query, "\n")

    # Execute the query with the variables
    response_data = await gql_client(query, variables)

    # Print the response data
    print("\nResponse data:", response_data,"\n")

    # Verify that at least one object is returned
    assert len(response_data["Tokens"]["Token"]) > 0

    # Verify that all the requested tokens are present in the returned objects
    for token in chosen_tokens:
        found = False
        split_token = token.split(' ')[0]
        for obj in response_data["Tokens"]["Token"]:
            if split_token in obj:
                found = True
                break
        assert found == True

# Define the test case for querying nested objects
@pytest.mark.asyncio
async def test_query_nested_objects(gql_client):
    # Select the nested tokens
    nested_tokens = [
        "contractMetaData { description }",
        "logo { medium, original }",
        "tokenBalances { tokenId, amount, blockchain }"
    ]

    print("\nselected_token-", nested_tokens, "\n")

    # Create the query with the nested tokens
    query = query_token % ", ".join(nested_tokens)

    print("\nqyery-", query, "\n")

    # Execute the query with the variables
    response_data = await gql_client(query, variables)
    

    # Print the response data
    print("Response data:", response_data)

    # Verify that at least one object is returned
    assert len(response_data["Tokens"]["Token"]) > 0

    # Verify that all the requested nested tokens are present in the returned objects
    for token in nested_tokens:
        found = False
        split_token = token.split(' ')[0]
        for obj in response_data["Tokens"]["Token"]:
            if split_token in obj:
                found = True
                break
        assert found == True


#Define the test case for load testing
@pytest.mark.asyncio
async def test_load_testing(gql_client):
    # Number of times to call each test function concurrently
    num_concurrent_tests = 20

    async def run_test(test_func, client):
        return await test_func(client)

    test_funcs = [
        test_query_single_object,
        test_query_multiple_objects,
        test_query_nested_objects,
    ]

    tasks = [
        run_test(test_func, gql_client) for test_func in test_funcs for _ in range(num_concurrent_tests)
    ]

    # Use asyncio.gather to run tasks concurrently
    await asyncio.gather(*tasks)
