import pytest

query_single_object = '''
query Test1($input: TokensInput!) {
  Tokens(input: $input) {
    Token {
      id
    }
  }
}
'''

@pytest.mark.asyncio
@pytest.mark.parametrize(
    "variables",
    [
        {
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
        },
        # Add more test cases if needed
    ]
)
async def test_query_single_object(gql_client, variables):
    response_data = await gql_client(query_single_object, variables)
    tokens = response_data["Tokens"]["Token"]

    # Print the response data
    print("Response data:", response_data)

    # Verify that only one object is returned
    assert len(tokens) == 1

    # Verify that the returned object has the expected id
    token_id = tokens[0]["id"]
    assert token_id == "10x60e4d786628fea6478f785a6d7e704777c86a7c6"
