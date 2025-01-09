import requests

BASE_URL = "https://tg-dex-api.overdone.it"
TOKEN = "PFhkWFXpG6afktPsT9w6GrfgFZA8hQmXFvD"

def get_auth_params():
    url = f"{BASE_URL}/auth/params"
    headers = {"Authorization": TOKEN}
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error fetching parameters: {response.status_code} - {response.text}")
            return None
    except requests.RequestException as e:
        print(f"Request error: {e}")
        return None

def get_trade_history():
    url = f"{BASE_URL}/auth/history"
    headers = {"Authorization": TOKEN}
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            trades = response.json()
            sorted_trades = sorted(
                [
                    {
                        "id": trade.get("id"),
                        "is_success": trade.get("is_success"),
                        "mint": trade.get("mint"),
                        "tx_hash": trade.get("tx_hash"),
                        "error": trade.get("error"),
                        "created_at": trade.get("created_at")
                    }
                    for trade in trades
                ],
                key=lambda trade: trade["created_at"],
                reverse=False
            )
            return sorted_trades[-1:]
        else:
            print(f"Error fetching trade history: {response.status_code} - {response.text}")
            return None
    except requests.RequestException as e:
        print(f"Request error: {e}")
        return None


def edit_auth_params(sol_lamports, slippage):
    url = f"{BASE_URL}/auth/edit"
    headers = {"Authorization": TOKEN, "Content-Type": "application/json"}
    data = {
        "sol_lamports": int(sol_lamports),
        "slippage": int(slippage)
    }
    try:
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            return response.text
        else:
            print(f"Error updating parameters: {response.status_code} - {response.text}")
            return None
    except requests.RequestException as e:
        print(f"Request error: {e}")
        return None

def perform_swap(token_mint):
    url = f"{BASE_URL}/auth/swap"
    headers = {"Authorization": TOKEN, "Content-Type": "application/json"}
    data = {
        "token_mint": token_mint
    }
    try:
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            return response.text
        else:
            print(f"Error performing swap: {response.status_code} - {response.text}")
            return None
    except requests.RequestException as e:
        print(f"Request error: {e}")
        return None
