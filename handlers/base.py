import aiohttp
from config import http_api


async def user_get(user_id):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{http_api}/user/?user_id={user_id}") as resp:
            data  = await resp.json()
            if resp.status == 200 and len(data) > 0:
                return data
            else:
                return False
            


async def get_users():
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{http_api}/user/") as resp:
            data =  await resp.json()
            user_id = [response['user_id'] for response in data]
            return user_id


async def user_post(data):
    async with aiohttp.ClientSession() as session:
        async with session.post(f"{http_api}/user/", data=data) as resp:
            if resp.status == 201:
                return True
            else:
                return False

async def keyword_kb():
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{http_api}/keywordcategories/") as resp:
            data = await resp.json()
            keyword = '\n'.join([response['name'] for response in data])
            return keyword


async def post_channels(data):
    async with aiohttp.ClientSession() as session:
        async with session.post(f"{http_api}/channels/", data=data) as resp:
            if resp.status == 201:
                return True
            else:
                return False

async def get_channels():
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{http_api}/channels/") as resp:
            data = await resp.json()
            # result = []
            channels = [response['channel_id'] for response in data]
            # result.append(channels)
            # print(result)
    
            return channels


async def get_agents():
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{http_api}/bot/") as resp:
            data = await resp.json()
            agents = [response['bot_id'] for response in data]
            
            return agents







async def add_channels(channels: str, channel_id=0):
    async with aiohttp.ClientSession() as session:
        async with session.post(f"{http_api}/channels/", data={'name': channels, 'channel_id': channel_id}) as resp:

            if resp.status == 200:
                return True
            else:
                return False

            

async def get_keyword_categories(keywords):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{http_api}/keywordcategories/?name={keywords}") as resp:
            data = await resp.json()
            keyword = [response for response in data]
            if resp.status == 200 and len(keyword)>0:
                return keyword
            else:
                return False
          

async def get_keyword_web():
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{http_api}/keywordcategories/?name=WEB-разработка") as resp:
            data = await resp.json()
            keyword = [response for response in data]
            if resp.status == 200 and len(keyword)>0:
                return keyword
            else:
                return False
            
async def get_keyword_marketplace():
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{http_api}/keywordcategories/?name=MARKETPLACES") as resp:
            data = await resp.json()
            keyword = [response for response in data]
            if resp.status == 200 and len(keyword)>0:
                return keyword
            else:
                return False
            

async def get_keyword_currency():
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{http_api}/keywordcategories/?name=Обмен валют") as resp:
            data = await resp.json()
            keyword = [response for response in data]
            if resp.status == 200 and len(keyword)>0:
                return keyword
            else:
                return False
        
async def get_admin(admin_id):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{http_api}/user/?user_id={admin_id}&is_admin=True") as resp:
            data =  await resp.json()
            user_id = [response['user_id'] for response in data]
            if resp.status == 200 and len(user_id)>0:
                return user_id
            
            else:
                return False
        

async def post_subscribe(data):
    async with aiohttp.ClientSession() as session:
        async with session.post(f"{http_api}/subscription/", data=data) as resp:
    
            if resp.status == 201:
                return True
            else:
                return False
            
async def get_subscribe(user_id):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{http_api}/subscription/?user__user_id={user_id}") as resp:
            data = await resp.json()
            subscribe = [response for response in data]
            if resp.status == 200 and len(subscribe)>0:
                return subscribe

            else:
                return False

            
async def get_subscribe_kw():
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{http_api}/subscription/") as resp:
            data = await resp.json()
            subscribe = [response['keyword'] for response in data]
            if resp.status == 200 and len(subscribe)>0:
          
                return subscribe

            else:
                return False
            
async def get_active_sub(user_id, keyword):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{http_api}/activesubscription/?user__user_id={user_id}&keyword__name={keyword}") as resp:
            data = await resp.json()
            subscribe = [response for response in data]
            if resp.status == 200 and len(subscribe)>0:
                return subscribe
            else:
                return False
            
async def get_check_sub(user_id, keyword):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{http_api}/subscription/?user__user_id={user_id}&keyword__name={keyword}") as resp:
            data = await resp.json()
            subscribe = [response for response in data]
            if resp.status == 200 and len(subscribe)>0:
                return subscribe
            else:
                return False
            
async def patch_sub(id_user, duration_days):
    #отправляем патч запрос
    async with aiohttp.ClientSession() as session:
        async with session.patch(f"{http_api}/subscription/{id_user}/", json ={'duration_days': duration_days}) as resp:
            if resp.status == 200:
                return True
            else:
                return False
            

async def get_active_subscriptions(user_id):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{http_api}/subscription/?user__user_id={user_id}") as resp:
            data = await resp.json()
            subscribe = [response for response in data]
            if resp.status == 200 and len(subscribe) > 0:
                return subscribe
            else:
                return False
            
async def get_active_kyword(keyword):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{http_api}/activesubscription/?keyword__name={keyword}") as resp:
            data = await resp.json()
            subscribe = [response['user_id'] for response in data]
        
            return subscribe
            