from flask import Flask, send_file, request
import requests
from io import BytesIO
import random
from flask_caching import Cache
import os


app = Flask(__name__)

# Configure Flask-Caching
cache = Cache(app, config={'CACHE_TYPE': 'simple'})

# Define the proxy list
proxy_list = [
    "45.43.82.141:6135:secureUsername:securePassword",
    "45.43.84.77:6702:secureUsername:securePassword",
    "154.92.114.24:5719:secureUsername:securePassword",
    "64.43.90.123:6638:secureUsername:securePassword",
    "198.105.101.219:5848:secureUsername:securePassword",
    "45.135.139.123:6426:secureUsername:securePassword",
    "45.43.64.77:6335:secureUsername:securePassword",
    "45.43.71.112:6710:secureUsername:securePassword",
    "154.92.116.249:6561:secureUsername:securePassword",
    "107.181.152.115:5152:secureUsername:securePassword",
    "107.181.148.47:5907:secureUsername:securePassword",
    "154.92.112.205:5226:secureUsername:securePassword",
    "107.181.128.66:5078:secureUsername:securePassword",
    "154.92.116.177:6489:secureUsername:securePassword",
    "107.181.143.45:6176:secureUsername:securePassword",
    "107.181.141.170:6567:secureUsername:securePassword",
    "104.143.224.102:5963:secureUsername:securePassword",
    "45.43.83.250:6533:secureUsername:securePassword",
    "45.43.65.191:6705:secureUsername:securePassword",
    "107.181.154.7:5685:secureUsername:securePassword",
    "138.128.153.14:5048:secureUsername:securePassword",
    "155.254.49.221:6781:secureUsername:securePassword",
    "154.85.125.194:6405:secureUsername:securePassword",
    "89.116.71.47:6013:secureUsername:securePassword",
    "104.239.53.22:7440:secureUsername:securePassword",
    "64.43.89.19:6278:secureUsername:securePassword",
    "86.38.26.12:6177:secureUsername:securePassword",
    "64.137.93.46:6503:secureUsername:securePassword",
    "198.105.111.120:6798:secureUsername:securePassword",
    "45.135.139.73:6376:secureUsername:securePassword",
    "217.69.121.9:5674:secureUsername:securePassword",
    "217.69.127.74:6695:secureUsername:securePassword",
    "107.181.130.225:5846:secureUsername:securePassword",
    "107.181.143.162:6293:secureUsername:securePassword",
    "155.254.49.16:6576:secureUsername:securePassword",
    "45.43.82.150:6144:secureUsername:securePassword",
    "206.232.127.70:6032:secureUsername:securePassword",
    "154.92.114.87:5782:secureUsername:securePassword",
    "86.38.236.172:6456:secureUsername:securePassword",
    "45.43.65.233:6747:secureUsername:securePassword",
    "204.217.245.51:6642:secureUsername:securePassword",
    "216.173.111.127:6837:secureUsername:securePassword",
    "104.143.224.101:5962:secureUsername:securePassword",
    "107.181.130.189:5810:secureUsername:securePassword",
    "217.69.121.50:5715:secureUsername:securePassword",
    "107.181.141.82:6479:secureUsername:securePassword",
    "154.85.124.203:6064:secureUsername:securePassword",
    "89.116.71.89:6055:secureUsername:securePassword",
    "204.217.245.121:6712:secureUsername:securePassword",
    "138.128.153.114:5148:secureUsername:securePassword",
    "86.38.234.10:6464:secureUsername:securePassword",
    "154.92.114.8:5703:secureUsername:securePassword",
    "104.143.226.243:5846:secureUsername:securePassword",
    "89.116.71.239:6205:secureUsername:securePassword",
    "45.43.81.231:5878:secureUsername:securePassword",
    "216.173.111.94:6804:secureUsername:securePassword",
    "89.116.78.96:5707:secureUsername:securePassword",
    "154.92.114.113:5808:secureUsername:securePassword",
    "107.181.148.218:6078:secureUsername:securePassword",
    "198.105.101.238:5867:secureUsername:securePassword",
    "138.128.153.74:5108:secureUsername:securePassword",
    "107.181.143.158:6289:secureUsername:securePassword",
    "217.69.121.105:5770:secureUsername:securePassword",
    "45.43.68.157:5797:secureUsername:securePassword",
    "217.69.127.203:6824:secureUsername:securePassword",
    "107.181.152.8:5045:secureUsername:securePassword",
    "154.92.112.76:5097:secureUsername:securePassword",
    "154.92.114.201:5896:secureUsername:securePassword",
    "64.137.92.20:6219:secureUsername:securePassword",
    "198.105.108.71:6093:secureUsername:securePassword",
    "45.43.84.95:6720:secureUsername:securePassword",
    "64.137.93.187:6644:secureUsername:securePassword",
    "216.173.111.172:6882:secureUsername:securePassword",
    "107.181.142.249:5842:secureUsername:securePassword",
    "107.181.143.134:6265:secureUsername:securePassword",
    "45.43.71.30:6628:secureUsername:securePassword",
    "64.137.92.25:6224:secureUsername:securePassword",
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

redis_url = "redis://default:4n6yVVMesJeLzkXMmLaNWltNEkSuHEc1@redis-18765.c263.us-east-1-2.ec2.redns.redis-cloud.com:18765"
if redis_url:
    cache_config = {
        'CACHE_TYPE': 'RedisCache',
        'CACHE_REDIS_URL': redis_url,
        'CACHE_DEFAULT_TIMEOUT': 3600  # Cache timeout in seconds (1 hour)
    }
    cache = Cache(app, config=cache_config)


def get_random_proxy():
    proxy = random.choice(proxy_list)
    ip, port, user, password = proxy.split(':')
    proxy_auth = f"http://{user}:{password}@{ip}:{port}"
    return {
        "http": proxy_auth,
        "https": proxy_auth
    }

def cache_image(cache_key, image_url):
    image_response = requests.get(image_url, proxies=get_random_proxy())
    if image_response.status_code == 200:
        image_bytes = image_response.content
        cache.set(cache_key, image_bytes)
        print(f"Caching new image for {cache_key}")
        return image_bytes
    else:
        return None

@app.route('/asset/<int:asset_id>')
def get_asset(asset_id):
    cache_key = f"asset_{asset_id}"
    cached_image = cache.get(cache_key)
    
    if cached_image is None:
        print(f"Fetching new image for asset ID {asset_id}")
        params = {
            'assetIds': asset_id,
            'size': '420x420',
            'format': 'Png'
        }
        response = requests.get('https://thumbnails.roblox.com/v1/assets', params=params, proxies=get_random_proxy()).json()
        image_url = response["data"][0]["imageUrl"]
        cached_image = cache_image(cache_key, image_url)
        if cached_image is None:
            return {"error": "Failed to retrieve image from Roblox CDN"}, 500
    else:
        print(f"Serving cached image for asset ID {asset_id}")

    image_bytes = BytesIO(cached_image)
    return send_file(image_bytes, mimetype='image/png', as_attachment=False, download_name=f"{asset_id}.png")

@app.route('/users/<int:user_id>', methods=['GET'])
def get_avatar_bust(user_id):
    cache_key = f"user_avatar_{user_id}"
    cached_image = cache.get(cache_key)
    
    if cached_image is None:
        print(f"Fetching new image for user ID {user_id}")
        url = f"https://thumbnails.roblox.com/v1/users/avatar-bust?userIds={user_id}&size=420x420&format=Png&isCircular=false"
        response = requests.get(url, proxies=get_random_proxy())
        
        if response.status_code != 200:
            return {"error": "Failed to retrieve data from Roblox API"}, response.status_code

        data = response.json()
        if 'data' not in data or not data['data']:
            return {"error": "Invalid response from Roblox API"}, 500

        image_url = data['data'][0]['imageUrl']
        cached_image = cache_image(cache_key, image_url)
        if cached_image is None:
            return {"error": "Failed to retrieve image from Roblox CDN"}, 500
    else:
        print(f"Serving cached image for user ID {user_id}")

    image_bytes = BytesIO(cached_image)
    return send_file(image_bytes, mimetype='image/png', as_attachment=False, download_name=f"{user_id}.png")

@app.route('/groups/<int:group_id>', methods=['GET'])
def get_group_pic(group_id):
    cache_key = f"group_pic_{group_id}"
    cached_image = cache.get(cache_key)
    
    if cached_image is None:
        print(f"Fetching new image for group ID {group_id}")
        url = f"https://thumbnails.roblox.com/v1/groups/icons?groupIds={group_id}&size=420x420&format=Png&isCircular=false"
        response = requests.get(url, proxies=get_random_proxy())
        
        if response.status_code != 200:
            return {"error": "Failed to retrieve data from Roblox API"}, response.status_code

        data = response.json()
        if 'data' not in data or not data['data']:
            return {"error": "Invalid response from Roblox API"}, 500

        image_url = data['data'][0]['imageUrl']
        cached_image = cache_image(cache_key, image_url)
        if cached_image is None:
            return {"error": "Failed to retrieve image from Roblox CDN"}, 500
    else:
        print(f"Serving cached image for group ID {group_id}")

    image_bytes = BytesIO(cached_image)
    return send_file(image_bytes, mimetype='image/png', as_attachment=False, download_name=f"{group_id}.png")

if __name__ == '__main__':
    app.run(debug=True)

