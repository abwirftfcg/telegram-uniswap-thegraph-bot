from python_graphql_client import GraphqlClient

client = GraphqlClient(endpoint="https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v2")

def get_token_info(token):
  query = """
    query getPrice($symbol: String) {
      tokens(where: {symbol: $symbol}) {
        id
        derivedETH
        name
        txCount
        totalLiquidity
        totalSupply
      }
    }
  """
  data = client.execute(query=query, variables={"symbol":token})
  return data['data']['tokens']

def get_euro_eth():
  query = """
    query getTokens {
      tokens (where: {id: "0x9f378bd16932ce3388cc237133fd7a3ea13f0c81"}) {
        derivedETH
      }
    }
  """
  data = client.execute(query=query)
  return float(data['data']['tokens'][0]['derivedETH'])
