from flask import Flask, redirect, send_file, request
import requests
from io import BytesIO
import random

app = Flask(__name__)

# Define the proxy list
proxy_list = [
    "107.181.132.224:6202:secureUsername:securePassword",
    "45.43.71.63:6661:secureUsername:securePassword",
    "86.38.236.82:6366:secureUsername:securePassword",
    "45.43.82.111:6105:secureUsername:securePassword",
    "45.43.70.192:6479:secureUsername:securePassword",
    "89.116.71.66:6032:secureUsername:securePassword",
    "107.181.130.229:5850:secureUsername:securePassword",
    "217.69.126.81:5951:secureUsername:securePassword",
    "178.159.34.164:6111:secureUsername:securePassword",
    "45.43.83.38:6321:secureUsername:securePassword",
    "45.43.68.151:5791:secureUsername:securePassword",
    "86.38.236.106:6390:secureUsername:securePassword",
    "198.105.101.220:5849:secureUsername:securePassword",
    "45.43.83.37:6320:secureUsername:securePassword",
    "45.43.68.242:5882:secureUsername:securePassword",
    "107.181.142.68:5661:secureUsername:securePassword",
    "154.92.114.72:5767:secureUsername:securePassword",
    "206.232.13.231:5897:secureUsername:securePassword",
    "154.85.124.54:5915:secureUsername:securePassword",
    "103.99.33.15:6010:secureUsername:securePassword",
    "64.43.89.239:6498:secureUsername:securePassword",
    "198.105.111.212:6890:secureUsername:securePassword",
    "107.181.154.95:5773:secureUsername:securePassword",
    "198.105.100.13:6264:secureUsername:securePassword"
]

def get_random_proxy():
    proxy = random.choice(proxy_list)
    ip, port, user, password = proxy.split(':')
    proxy_auth = f"http://{user}:{password}@{ip}:{port}"
    print(proxy_auth)
    return {
        "http": proxy_auth,
        "https": proxy_auth
    }


@app.route('/asset/<int:asset_id>')
def get_asset(asset_id):
    params = {
        'assetIds': asset_id,  # Use the provided asset_id
        'size': '420x420',
        'format': 'Png'
    }
    response = requests.get('https://thumbnails.roblox.com/v1/assets', params=params, proxies=get_random_proxy()).json()
    print(response)
    image_url = response["data"][0]["imageUrl"]

    return redirect(image_url)  # Redirect to the obtained image URL

@app.route('/users/<int:user_id>', methods=['GET'])
def get_avatar_bust(user_id):
    if not user_id:
        return {"error": "userId parameter is required"}, 400

    url = f"https://thumbnails.roblox.com/v1/users/avatar-bust?userIds={user_id}&size=420x420&format=Png&isCircular=false"
    response = requests.get(url, proxies=get_random_proxy())

    if response.status_code != 200:
        return {"error": "Failed to retrieve data from Roblox API"}, response.status_code

    data = response.json()
    if 'data' not in data or not data['data']:
        return {"error": "Invalid response from Roblox API"}, 500

    image_url = data['data'][0]['imageUrl']
    image_response = requests.get(image_url, proxies=get_random_proxy())

    if image_response.status_code != 200:
        return {"error": "Failed to retrieve image from Roblox CDN"}, image_response.status_code

    image_bytes = BytesIO(image_response.content)
    return send_file(image_bytes, mimetype='image/png', as_attachment=False, download_name=f"{user_id}.png")

@app.route('/groups/<int:group_id>', methods=['GET'])
def get_group_pic(group_id):
    if not group_id:
        return {"error": "group id parameter is required"}, 400

    url = f"https://thumbnails.roblox.com/v1/groups/icons?groupIds={group_id}&size=420x420&format=Png&isCircular=false"
    response = requests.get(url, proxies=get_random_proxy())

    if response.status_code != 200:
        return {"error": "Failed to retrieve data from Roblox API"}, response.status_code

    data = response.json()
    if 'data' not in data or not data['data']:
        return {"error": "Invalid response from Roblox API"}, 500

    image_url = data['data'][0]['imageUrl']
    image_response = requests.get(image_url, proxies=get_random_proxy())

    if image_response.status_code != 200:
        return {"error": "Failed to retrieve image from Roblox CDN"}, image_response.status_code

    image_bytes = BytesIO(image_response.content)
    return send_file(image_bytes, mimetype='image/png', as_attachment=False, download_name=f"{group_id}.png")

if __name__ == '__main__':
    app.run(debug=True)
