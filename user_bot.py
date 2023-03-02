import asyncio
import telethon
from config import *
from telethon import TelegramClient, events
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.functions.messages import ImportChatInviteRequest
from telethon.tl.types import PeerUser
from telethon import TelegramClient, events
from telethon import types
from http_req import get_channels_req, get_required_word, get_stop_word
from base import *




# for user in users:
# client = TelegramClient(user['SESSION_NAME'], user['API_ID'], user['API_HASH'])
client = TelegramClient(SESSION_NAME, API_ID, API_HASH)
client.start()


listen_channels= get_channels_req()

listen_channels.append(BOT_ID_MAIN)


async def join_group(link, client=client):
    if 'https://t.me/' in link:
        if '+' in link:
            return await client(ImportChatInviteRequest(link.split('/')[-1][1:]))
        else:
            return await client(JoinChannelRequest(link))
    else:
        return await client(JoinChannelRequest(f"https://t.me/{link}"))


# print(join_group("https://t.me/istanbul_expats"))


def check_required_message(text: str):
    text = text.lower()
    required_list = get_required_word()

    for required in required_list:
        if required.lower() in text:
            break
    else:
        return False

    stop_list = get_stop_word()
    for stop in stop_list:
        if stop.lower() in text:
            return False

    return True




async def custom_filter(event: events.NewMessage.Event):
    channel_id = event.chat_id
    result = await get_channels()

    if int(channel_id) in [*result, BOT_ID_MAIN]:
        return True
    else:
        return False

print('Running!')


@client.on(events.NewMessage(func=custom_filter))
async def check_new_message(event: events.NewMessage.Event):

    # Если сообщение от канала
    if type(event.message.peer_id) == telethon.types.PeerChannel:
        user_id = event.message.peer_id.channel_id
    else:
        try:
            user_id = event.message.peer_id.user_id
        except Exception as e:
            admin = await get_admin()
            for admins in admin:
                await client.send_message(admins, message=f'[AGENT] Ошибка, {e}')
            return

    message_text = event.message.message
    # Если бот дал команду входа
    if user_id == BOT_ID_MAIN:


        for link in message_text.replace('\n', ' ').split(' '):
            
            try:
                group = await join_group(link)

            except telethon.errors.rpcerrorlist.FloodWaitError as error:
                admin = await get_admin()
                for admins in admin:
                    await client.send_message(admins, message=f'[AGENT] не сможет войти в группу через {error.seconds} секунд!')
                group = None
            except telethon.errors.rpcerrorlist.UserAlreadyParticipantError:
                admin = await get_admin()
                for admins in admin:
                    await client.send_message(admins, message=f'[AGENT] Уже стоит в группе!')
                group = None
            except Exception:
                continue

#             # Если данные группы доступны
            if group:
              
                group_id = (await client.get_peer_id(link))
                if not str(group_id).startswith('-100'):
                    group_id = int('-100',group_id)
                listen_channels.append(group_id)
                
                data = {
                    'name': link,
                    'channel_id': group_id,

                }
                post = await post_channels(data)
                if post:
                    admin = await get_admin()
                    for admins in admin:
                        await client.send_message(admins,f'[AGENT] Присоединился к группе `{link}`', parse_mode='Markdown')
                else:
                    admin = await get_admin()
                    for admins in admin:
                        await client.send_message(admins,f'[AGENT] Присоединился к группе `{link}`', parse_mode='Markdown')
    

            else:
                admin = await get_admin()
                for admins in admin:
                    await client.send_message( f'[AGENT] Не удалось присоединиться к группе!')
            await asyncio.sleep(3)

        return
    if not check_required_message(message_text): return
    message_sent = False
    try:
        entity = (await client.get_participants(user_id))
        entity = entity[0]


        chat = await client.get_entity(event.chat_id)
        group_link = f"https://t.me/{chat.username}"
        message_text = f"{event.message.message}\n\nСообщение пришло с этой группы: {group_link}"
        for bot_id in BOT_ID:
            await client.forward_messages(bot_id, event.message)
            if not message_sent:
                await client.send_message(1937696257, message_text)
                message_sent = True
          
    
        db = await get_channels()
        for channel in db:
            group_message = await client.get_messages(channel, 1)
            group_message = group_message[0]
        return
    except Exception:
        return



client.run_until_disconnected()


