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
import json

# ═══════════════════════════════════════════════════════════════
# 🔥 RACORE PREMIUM ULTIMATE TAGGER BOT V2.0 🔥
# 👨‍💻 Author: Rzayeff Ağa
# 👥 Team: Rzayeffdi
# 🐍 Language: Python 3.x + Pyrogram + TgCrypto
# ⚡ Version: Premium Ultimate Edition
# ═══════════════════════════════════════════════════════════════

racore = Client(
    "RacorePremiumBot",
    api_id = config.API_ID,
    api_hash = config.API_HASH,
    bot_token = config.BOT_TOKEN
)



# Global dəyişənlər
chatQueue = []
stopProcess = False
isProcessing = False
START_TIME = datetime.utcnow()
START_TIME_ISO = START_TIME.replace(microsecond=0).isoformat()

# ═══════════════════════════════════════════════════════════════
# 📊 DATA MANAGEMENT FUNCTIONS
# ═══════════════════════════════════════════════════════════════

data_file = "racore_data.json"

def load_data():
    try:
        with open(data_file, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_data(data):
    with open(data_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

# ═══════════════════════════════════════════════════════════════
# 📈 MESSAGE STATISTICS TRACKER
# ═══════════════════════════════════════════════════════════════

@racore.on_message(filters.text & filters.group)
async def handle_message(client, message):
    try:
        chat_id = str(message.chat.id)
        user_id = message.from_user.id
        data = load_data()

        if chat_id not in data:
            data[chat_id] = {"messages": 0, "users": {}}

        data[chat_id]["messages"] += 1

        if str(user_id) not in data[chat_id]["users"]:
            data[chat_id]["users"][str(user_id)] = 0

        data[chat_id]["users"][str(user_id)] += 1
        save_data(data)
    except:
        pass

# ═══════════════════════════════════════════════════════════════
# 🎨 PREMIUM START COMMAND
# ═══════════════════════════════════════════════════════════════

@racore.on_message(filters.command("start") & filters.private)
async def start(client, message):
    user_name = message.from_user.first_name
    user_mention = message.from_user.mention
    
    start_text = f"""
╔═══════════════════════════╗
║   🌟 RACORE PREMIUM 🌟    ║
║      ULTIMATE TAGGER      ║
╚═══════════════════════════╝

👋 **Salam {user_name}!**

🔥 **Mən Racore Premium Ultimate Tagger Botuyam**

⚡ **Xüsusiyyətlərim:**
├ 🎯 Müxtəlif tag sistemləri
├ 📊 Detallı statistika sistemi
├ 🎨 Premium dizayn və interfeys
├ 🛡️ Admin idarəetmə paneli
├ 🤖 Ağıllı avtomatik funksiyalar
├ ⚙️ Qrup idarəetmə alətləri
└ 💎 VIP özəlliklər

🎭 **Versiya:** Premium Ultimate V2.0
👨‍💻 **Developer:** Rzayeff Ağa
👥 **Team:** Rzayeffdi
🐍 **Tech:** Python + Pyrogram + TgCrypto

┏━━━━━━━━━━━━━━━━━━━━━━━┓
┃  🚀 Gəlin Başlayaq! 🚀  ┃
┗━━━━━━━━━━━━━━━━━━━━━━━┛
"""
    
    buttons = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("📋 Əmrlər Menyusu", callback_data="main_commands"),
            InlineKeyboardButton("⚡ Tagger Menyusu", callback_data="tagger_menu")
        ],
        [
            InlineKeyboardButton("📊 Statistika", callback_data="statistics_menu"),
            InlineKeyboardButton("⚙️ Parametrlər", callback_data="settings_menu")
        ],
        [
            InlineKeyboardButton("ℹ️ Haqqında", callback_data="about_menu"),
            InlineKeyboardButton("💬 Dəstək Qrupu", url="https://t.me/rzayeffdi")
        ],
        [
            InlineKeyboardButton("👨‍💻 Developer", url="https://t.me/rzayeff"),
            InlineKeyboardButton("🌐 Kanal", url="https://t.me/rzayeffchannel")
        ]
    ])
    
    try:
        await message.reply_photo(
            photo="https://graph.org/file/racore-premium-logo.jpg",
            caption=start_text,
            reply_markup=buttons
        )
    except:
        await message.reply_text(
            start_text,
            reply_markup=buttons,
            disable_web_page_preview=True
        )

# ═══════════════════════════════════════════════════════════════
# 🎯 TAGGER MENU (INLINE)
# ═══════════════════════════════════════════════════════════════

@racore.on_message(filters.command(["tagger", "tmenu", "tagmenu"], prefixes=["/", ".", "!", "#"]) & filters.group)
async def tagger_menu_command(client, message):
    try:
        sender = await racore.get_chat_member(message.chat.id, message.from_user.id)
        has_permissions = sender.privileges
    except:
        has_permissions = message.sender_chat
    
    if not has_permissions:
        await message.reply("⛔ **Bu əmri yalnız adminlər istifadə edə bilər!**")
        return
    
    menu_text = """
╔═══════════════════════════╗
║   🎯 TAGGER MENYUSU 🎯    ║
╚═══════════════════════════╝

**🔥 Aşağıdakı düymələrdən istifadə edərək**
**istədiyiniz tag növünü seçin:**

⚡ **Aktiv Tag Sistemləri:**
├ 🎨 Gözəl ifadələrlə tag
├ ❓ Sual-cavab tag
├ 🔢 Sadə text tag
├ 👥 Qrup tag (10-luq)
└ ⏸️ Tag prosesini dayandır

💎 **Premium Ultimate Edition**
"""
    
    buttons = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🎨 Gözəl Tag", callback_data="tag_stag"),
            InlineKeyboardButton("❓ Sual Tag", callback_data="tag_qtag")
        ],
        [
            InlineKeyboardButton("📝 Text Tag", callback_data="tag_ttag"),
            InlineKeyboardButton("👥 Qrup Tag", callback_data="tag_otag")
        ],
        [
            InlineKeyboardButton("⏸️ Dayandır", callback_data="tag_stop"),
            InlineKeyboardButton("📊 Statistika", callback_data="tag_stats")
        ],
        [
            InlineKeyboardButton("❌ Bağla", callback_data="close_menu")
        ]
    ])
    
    await message.reply_text(menu_text, reply_markup=buttons)

# ═══════════════════════════════════════════════════════════════
# 📋 MAIN COMMANDS MENU
# ═══════════════════════════════════════════════════════════════

@racore.on_callback_query(filters.regex("main_commands"))
async def main_commands_menu(client, callback_query):
    commands_text = """
╔═══════════════════════════════════╗
║   📋 ƏMRLƏR MENYUSU 📋            ║
╚═══════════════════════════════════╝

**🎯 TAG ƏMRLƏRİ:**
├ `/tagger` - Tag menyusunu aç
├ `/stag` - Gözəl ifadələrlə tag
├ `/tag` - Sual-cavab ilə tag
├ `/ttag [mesaj]` - Text ilə tag
├ `/otag [mesaj]` - 10-luq qrup tag
└ `/stop` - Tag prosesini dayandır

**⚙️ İDARƏETMƏ:**
├ `/admins` - Adminlərin siyahısı
├ `/bots` - Botların siyahısı
├ `/remove` - Silinmiş hesabları at
└ `/banall` - Hamını qrupdan at (!) 

**📊 MƏLUMAT:**
├ `/stat` - Qrup statistikası
├ `/id` - ID məlumatı
├ `/info` - İstifadəçi məlumatı
├ `/ginfo` - Qrup məlumatı
├ `/ping` - Bot sürəti
└ `/uptime` - İşləmə müddəti

**💎 Premium Ultimate Edition**
**👨‍💻 Developer: Rzayeff Ağa**
**👥 Team: Rzayeffdi**
"""
    
    buttons = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("⚡ Tagger Menyu", callback_data="tagger_menu"),
            InlineKeyboardButton("📊 Statistika", callback_data="statistics_menu")
        ],
        [
            InlineKeyboardButton("⬅️ Geri", callback_data="back_to_start")
        ]
    ])
    
    await callback_query.message.edit_text(commands_text, reply_markup=buttons)

# ═══════════════════════════════════════════════════════════════
# ⚡ TAGGER MENU CALLBACKS
# ═══════════════════════════════════════════════════════════════

@racore.on_callback_query(filters.regex("tagger_menu"))
async def tagger_menu_callback(client, callback_query):
    menu_text = """
╔═══════════════════════════╗
║   🎯 TAGGER MENYUSU 🎯    ║
╚═══════════════════════════╝

**🔥 Tag sistemləri:**

🎨 **Gözəl Tag** - Motivasiya sözləri
❓ **Sual Tag** - Maraqlı suallar
📝 **Text Tag** - Öz mesajınız
👥 **Qrup Tag** - 10-luq tag sistemi

**💡 Məsləhət:**
Qrupda tag etmək üçün admin olmalısınız!

💎 **Premium Ultimate Edition**
"""
    
    buttons = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🎨 Gözəl Tag (/stag)", callback_data="info_stag"),
            InlineKeyboardButton("❓ Sual Tag (/tag)", callback_data="info_qtag")
        ],
        [
            InlineKeyboardButton("📝 Text Tag (/ttag)", callback_data="info_ttag"),
            InlineKeyboardButton("👥 Qrup Tag (/otag)", callback_data="info_otag")
        ],
        [
            InlineKeyboardButton("⬅️ Geri", callback_data="main_commands")
        ]
    ])
    
    await callback_query.message.edit_text(menu_text, reply_markup=buttons)

# ═══════════════════════════════════════════════════════════════
# 📊 STATISTICS MENU
# ═══════════════════════════════════════════════════════════════

@racore.on_callback_query(filters.regex("statistics_menu"))
async def statistics_menu_callback(client, callback_query):
    data = load_data()
    total_chats = len(data)
    total_messages = sum(chat_data.get("messages", 0) for chat_data in data.values())
    
    stats_text = f"""
╔═══════════════════════════════════╗
║   📊 STATİSTİKA MENYUSU 📊        ║
╚═══════════════════════════════════╝

**📈 Ümumi Statistika:**
├ 💬 Ümumi qruplar: **{total_chats}**
├ 📨 Ümumi mesajlar: **{total_messages}**
└ ⚡ Status: **Aktiv**

**🤖 Bot Məlumatları:**
├ 🔥 Versiya: Premium Ultimate V2.0
├ 👨‍💻 Developer: Rzayeff Ağa
├ 👥 Team: Rzayeffdi
└ 🐍 Tech: Python + Pyrogram

**💎 Premium Ultimate Edition**
"""
    
    buttons = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🔄 Yenilə", callback_data="statistics_menu"),
            InlineKeyboardButton("⬅️ Geri", callback_data="back_to_start")
        ]
    ])
    
    await callback_query.message.edit_text(stats_text, reply_markup=buttons)

# ═══════════════════════════════════════════════════════════════
# ℹ️ ABOUT MENU
# ═══════════════════════════════════════════════════════════════

@racore.on_callback_query(filters.regex("about_menu"))
async def about_menu_callback(client, callback_query):
    about_text = """
╔═══════════════════════════════════╗
║   ℹ️ HAQQINDA ℹ️                  ║
╚═══════════════════════════════════╝

**🔥 RACORE PREMIUM ULTIMATE TAGGER**

**🎯 Bot Haqqında:**
Racore - Telegram üçün hazırlanmış
ən güclü və funksional tagger botudur.

**⚡ Xüsusiyyətlər:**
├ 🎨 Premium dizayn
├ 🚀 Sürətli performans
├ 🛡️ Təhlükəsiz sistem
├ 📊 Detallı statistika
├ 💎 VIP funksiyalar
└ 🔧 Asan istifadə

**👨‍💻 Developer Məlumatları:**
├ 👤 Ad: Rzayeff Ağa
├ 👥 Team: Rzayeffdi
├ 🐍 Dil: Python 3.x
├ 📚 Framework: Pyrogram
├ 🔐 Security: TgCrypto
└ 📅 Versiya: Premium Ultimate V2.0

**📞 Əlaqə:**
├ 💬 Dəstək: @rzayeffdi
├ 👨‍💻 Developer: @rzayeff
└ 🌐 Kanal: @rzayeffchannel

**🌟 Premium Ultimate Edition**
**© 2024 Rzayeffdi Team**
"""
    
    buttons = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("💬 Dəstək", url="https://t.me/rzayeffdi"),
            InlineKeyboardButton("👨‍💻 Developer", url="https://t.me/rzayeff")
        ],
        [
            InlineKeyboardButton("⬅️ Geri", callback_data="back_to_start")
        ]
    ])
    
    await callback_query.message.edit_text(about_text, reply_markup=buttons)

# ═══════════════════════════════════════════════════════════════
# 🔙 BACK TO START
# ═══════════════════════════════════════════════════════════════

@racore.on_callback_query(filters.regex("back_to_start"))
async def back_to_start_callback(client, callback_query):
    user_name = callback_query.from_user.first_name
    
    start_text = f"""
╔═══════════════════════════╗
║   🌟 RACORE PREMIUM 🌟    ║
║      ULTIMATE TAGGER      ║
╚═══════════════════════════╝

👋 **Salam {user_name}!**

🔥 **Mən Racore Premium Ultimate Tagger Botuyam**

⚡ **Xüsusiyyətlərim:**
├ 🎯 Müxtəlif tag sistemləri
├ 📊 Detallı statistika sistemi
├ 🎨 Premium dizayn və interfeys
├ 🛡️ Admin idarəetmə paneli
├ 🤖 Ağıllı avtomatik funksiyalar
├ ⚙️ Qrup idarəetmə alətləri
└ 💎 VIP özəlliklər

🎭 **Versiya:** Premium Ultimate V2.0
👨‍💻 **Developer:** Rzayeff Ağa
👥 **Team:** Rzayeffdi
🐍 **Tech:** Python + Pyrogram + TgCrypto

┏━━━━━━━━━━━━━━━━━━━━━━━┓
┃  🚀 Gəlin Başlayaq! 🚀  ┃
┗━━━━━━━━━━━━━━━━━━━━━━━┛
"""
    
    buttons = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("📋 Əmrlər Menyusu", callback_data="main_commands"),
            InlineKeyboardButton("⚡ Tagger Menyusu", callback_data="tagger_menu")
        ],
        [
            InlineKeyboardButton("📊 Statistika", callback_data="statistics_menu"),
            InlineKeyboardButton("⚙️ Parametrlər", callback_data="settings_menu")
        ],
        [
            InlineKeyboardButton("ℹ️ Haqqında", callback_data="about_menu"),
            InlineKeyboardButton("💬 Dəstək Qrupu", url="https://t.me/rzayeffdi")
        ],
        [
            InlineKeyboardButton("👨‍💻 Developer", url="https://t.me/rzayeff"),
            InlineKeyboardButton("🌐 Kanal", url="https://t.me/rzayeffchannel")
        ]
    ])
    
    await callback_query.message.edit_text(start_text, reply_markup=buttons)

# ═══════════════════════════════════════════════════════════════
# ❌ CLOSE MENU
# ═══════════════════════════════════════════════════════════════

@racore.on_callback_query(filters.regex("close_menu"))
async def close_menu_callback(client, callback_query):
    await callback_query.message.delete()

# ═══════════════════════════════════════════════════════════════
# 📊 STAT COMMAND
# ═══════════════════════════════════════════════════════════════

@racore.on_message(filters.command("stat"))
async def show_stats(client, message):
    chat_id = str(message.chat.id)
    data = load_data()

    if chat_id not in data:
        await message.reply("**📊 Bu qrup üçün statistik məlumat yoxdur.**")
        return

    group_data = data[chat_id]
    total_messages = group_data["messages"]
    user_stats = group_data["users"]

    if not user_stats:
        await message.reply("**📊 Heç bir istifadəçi məlumatı yoxdur.**")
        return

    # Top 5 users
    sorted_users = sorted(user_stats.items(), key=lambda x: x[1], reverse=True)[:5]
    
    stats_text = f"""
╔═══════════════════════════════════╗
║   📊 QRUP STATİSTİKASI 📊         ║
╚═══════════════════════════════════╝

**📈 Ümumi Məlumat:**
└ 💬 Ümumi mesajlar: **{total_messages}**

**🏆 Top 5 Aktiv İstifadəçilər:**
"""
    
    medals = ["🥇", "🥈", "🥉", "🎖️", "🏅"]
    for idx, (user_id, msg_count) in enumerate(sorted_users):
        try:
            user = await client.get_users(int(user_id))
            user_name = user.first_name
            stats_text += f"{medals[idx]} **{user_name}** - {msg_count} mesaj\n"
        except:
            stats_text += f"{medals[idx]} İstifadəçi {user_id} - {msg_count} mesaj\n"
    
    stats_text += "\n**💎 Premium Ultimate Edition**"
    
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔄 Yenilə", callback_data=f"refresh_stats_{chat_id}")]
    ])
    
    await message.reply(stats_text, reply_markup=buttons)

# ═══════════════════════════════════════════════════════════════
# 🎨 STAG COMMAND (Beautiful Phrases Tag)
# ═══════════════════════════════════════════════════════════════

@racore.on_message(filters.command(["stag"], prefixes=["/", "!", "%", ",", ".", "@", "#"]))
async def stag(client, message):
    global stopProcess, chatQueue
    try:
        try:
            sender = await racore.get_chat_member(message.chat.id, message.from_user.id)
            has_permissions = sender.privileges
        except:
            has_permissions = message.sender_chat
        
        if not has_permissions:
            await message.reply("**⛔ Bu əmri yalnız adminlər istifadə edə bilər!**")
            return
        
        if len(chatQueue) > 30:
            await message.reply("**⛔ Maksimum 30 söhbət limiti aşılıb. Zəhmət olmasa gözləyin.**")
            return
        
        if message.chat.id in chatQueue:
            await message.reply("**🚫 Bu çatda artıq tag prosesi davam edir. `/stop` əmri ilə dayandırın.**")
            return
        
        chatQueue.append(message.chat.id)
        
        # Progress message
        progress_msg = await message.reply("**🎨 Gözəl ifadələrlə tag başladı...**\n⏳ Hazırlanır...")
        
        membersList = []
        async for member in racore.get_chat_members(message.chat.id):
            if not member.user.is_bot and not member.user.is_deleted:
                membersList.append(member.user)
        
        total_members = len(membersList)
        if total_members == 0:
            await progress_msg.edit("**❌ Tag ediləcək istifadəçi tapılmadı.**")
            chatQueue.remove(message.chat.id)
            return
        
        i = 0
        stopProcess = False
        
        while membersList and not stopProcess:
            user = membersList.pop(0)
            random_phrase = random.choice(beautiful_phrases)
            text = f"**🎨 {random_phrase}**\n\n👤 {user.mention}"
            
            try:
                await racore.send_message(message.chat.id, text)
                i += 1
                
                # Update progress every 10 tags
                if i % 10 == 0:
                    await progress_msg.edit(f"**🎨 Tag davam edir...**\n✅ Tamamlanan: {i}/{total_members}")
                
                await asyncio.sleep(3)
            except FloodWait as e:
                await asyncio.sleep(e.value)
            except Exception:
                continue
        
        if stopProcess:
            await progress_msg.edit(f"**⏸️ Tag dayandırıldı!**\n✅ Tamamlanan: **{i}/{total_members}**")
        else:
            await progress_msg.edit(f"**✅ Tag tamamlandı!**\n👥 Ümumi: **{i}** istifadəçi")
        
        chatQueue.remove(message.chat.id)
    
    except FloodWait as e:
        await asyncio.sleep(e.value)
    except Exception as e:
        await message.reply(f"**❌ Xəta: {str(e)}**")
        if message.chat.id in chatQueue:
            chatQueue.remove(message.chat.id)

# ═══════════════════════════════════════════════════════════════
# ❓ TAG COMMAND (Question Tag)
# ═══════════════════════════════════════════════════════════════

@racore.on_message(filters.command(["tag"], prefixes=["/", "!", "%", ",", ".", "@", "#"]))
async def tag(racore_client, message):
    global stopProcess, chatQueue
    try:
        try:
            sender = await racore.get_chat_member(message.chat.id, message.from_user.id)
            has_permissions = sender.privileges
        except:
            has_permissions = message.sender_chat

        if not has_permissions:
            await message.reply("**⛔ Bu əmri yalnız adminlər istifadə edə bilər!**")
            return

        if len(chatQueue) > 30:
            await message.reply("**⛔ Maksimum 30 söhbət limiti aşılıb. Zəhmət olmasa gözləyin.**")
            return

        if message.chat.id in chatQueue:
            await message.reply("**🚫 Bu çatda artıq tag prosesi davam edir. `/stop` əmri ilə dayandırın.**")
            return

        chatQueue.append(message.chat.id)
        
        progress_msg = await message.reply("**❓ Sual-cavab tag başladı...**\n⏳ Hazırlanır...")

        membersList = []
        async for member in racore.get_chat_members(message.chat.id):
            if not member.user.is_bot and not member.user.is_deleted:
                membersList.append(member.user)

        total_members = len(membersList)
        if total_members == 0:
            await progress_msg.edit("**❌ Tag ediləcək istifadəçi tapılmadı.**")
            chatQueue.remove(message.chat.id)
            return

        i = 0
        stopProcess = False

        while membersList and not stopProcess:
            user = membersList.pop(0)
            random_question = random.choice(sual_db)
            text = f"**❓ {random_question}**\n\n👤 {user.mention}"
            
            try:
                await racore.send_message(message.chat.id, text)
                i += 1
                
                if i % 10 == 0:
                    await progress_msg.edit(f"**❓ Tag davam edir...**\n✅ Tamamlanan: {i}/{total_members}")
                
                await asyncio.sleep(3)
            except FloodWait as e:
                await asyncio.sleep(e.value)
            except Exception:
                continue

        if stopProcess:
            await progress_msg.edit(f"**⏸️ Tag dayandırıldı!**\n✅ Tamamlanan: **{i}/{total_members}**")
        else:
            await progress_msg.edit(f"**✅ Tag tamamlandı!**\n👥 Ümumi: **{i}** istifadəçi")

        chatQueue.remove(message.chat.id)

    except FloodWait as e:
        await asyncio.sleep(e.value)
    except Exception as e:
        await message.reply(f"**❌ Xəta: {str(e)}**")
        if message.chat.id in chatQueue:
            chatQueue.remove(message.chat.id)

# ═══════════════════════════════════════════════════════════════
# 📝 TTAG COMMAND (Text Tag)
# ═══════════════════════════════════════════════════════════════

@racore.on_message(filters.command("ttag", prefixes=["/", ".", "!", "#"]))
async def ttag(racore_client, message):
    global stopProcess, isProcessing, chatQueue

    if isProcessing:
        await message.reply("**⚠️ Hal-hazırda başqa tag prosesi davam edir. Gözləyin.**")
        return

    try:
        chat_member = await racore.get_chat_member(message.chat.id, message.from_user.id)
        if chat_member.status not in ["administrator", "creator"]:
            await message.reply("**❌ Bu əmri yalnız adminlər istifadə edə bilər!**")
            return
    except:
        await message.reply("**❌ Admin yoxlaması uğursuz oldu!**")
        return

    if len(message.command) < 2:
        await message.reply("**📝 İstifadə: `/ttag [mesaj]`**\n\nMisal: `/ttag Salam hamıya!`")
        return

    try:
        input_text = " ".join(message.command[1:])
        
        progress_msg = await message.reply("**📝 Text tag başladı...**\n⏳ Hazırlanır...")

        members = []
        async for member in racore.get_chat_members(message.chat.id):
            if not member.user.is_bot and not member.user.is_deleted:
                members.append(member.user)

        total = len(members)
        if total == 0:
            await progress_msg.edit("**❌ Tag ediləcək istifadəçi tapılmadı.**")
            return

        i = 0
        stopProcess = False
        isProcessing = True
        
        while members and not stopProcess:
            user = members.pop(0)
            try:
                await racore.send_message(
                    message.chat.id, f"**📝 {input_text}**\n\n👤 {user.mention}"
                )
                i += 1
                
                if i % 10 == 0:
                    await progress_msg.edit(f"**📝 Tag davam edir...**\n✅ Tamamlanan: {i}/{total}")
                
                await asyncio.sleep(3)
            except FloodWait as e:
                await asyncio.sleep(e.value)
            except Exception:
                continue

        if stopProcess:
            await progress_msg.edit(f"**⏸️ Tag dayandırıldı!**\n✅ Tamamlanan: **{i}/{total}**")
        else:
            await progress_msg.edit(f"**✅ Tag tamamlandı!**\n👥 Ümumi: **{i}** istifadəçi")
    
    except Exception as e:
        await message.reply(f"**❌ Xəta: {str(e)}**")
    finally:
        isProcessing = False

# ═══════════════════════════════════════════════════════════════
# 👥 OTAG COMMAND (Group Tag - 10 users per message)
# ═══════════════════════════════════════════════════════════════

@racore.on_message(filters.command(["otag"], prefixes=["/", "!", "%", ",", ".", "@", "#"]))
async def otag(client, message):
    global stopProcess, chatQueue
    try:
        try:
            sender = await racore.get_chat_member(message.chat.id, message.from_user.id)
            has_permissions = sender.privileges
        except:
            has_permissions = message.sender_chat
        
        if not has_permissions:
            await message.reply("**⛔ Bu əmri yalnız adminlər istifadə edə bilər!**")
            return
        
        if len(chatQueue) > 30:
            await message.reply("**⛔ Maksimum 30 söhbət limiti aşılıb. Zəhmət olmasa gözləyin.**")
            return
        
        if message.chat.id in chatQueue:
            await message.reply("**🚫 Bu çatda artıq tag prosesi davam edir. `/stop` əmri ilə dayandırın.**")
            return
        
        chatQueue.append(message.chat.id)
        
        if len(message.command) > 1:
            inputText = " ".join(message.command[1:])
        else:
            inputText = "👥 **Qrup Tağı**"
        
        progress_msg = await message.reply("**👥 Qrup tag başladı...**\n⏳ Hazırlanır...")
        
        membersList = []
        async for member in racore.get_chat_members(message.chat.id):
            if not member.user.is_bot and not member.user.is_deleted:
                membersList.append(member.user)
        
        total_members = len(membersList)
        if total_members == 0:
            await progress_msg.edit("**❌ Tag ediləcək istifadəçi tapılmadı.**")
            chatQueue.remove(message.chat.id)
            return
        
        i = 0
        stopProcess = False
        
        while membersList and not stopProcess:
            j = 0
            text1 = f"**{inputText}**\n\n"
            
            try:
                while j < 10 and membersList:
                    user = membersList.pop(0)
                    if user.username:
                        text1 += f"@{user.username} "
                    else:
                        text1 += f"{user.mention} "
                    j += 1
                
                try:
                    await racore.send_message(message.chat.id, text1)
                except Exception:
                    pass
                
                await asyncio.sleep(10)
                i += j
                
                if i % 50 == 0:
                    await progress_msg.edit(f"**👥 Tag davam edir...**\n✅ Tamamlanan: {i}/{total_members}")
            
            except Exception:
                pass
        
        if stopProcess:
            await progress_msg.edit(f"**⏸️ Tag dayandırıldı!**\n✅ Tamamlanan: **{i}/{total_members}**")
        else:
            await progress_msg.edit(f"**✅ Tag tamamlandı!**\n👥 Ümumi: **{i}** istifadəçi\n❌ Botlar və silinmiş hesablar rədd edildi")
        
        chatQueue.remove(message.chat.id)
    
    except FloodWait as e:
        await asyncio.sleep(e.value)
    except Exception as e:
        await message.reply(f"**❌ Xəta: {str(e)}**")
        if message.chat.id in chatQueue:
            chatQueue.remove(message.chat.id)

# ═══════════════════════════════════════════════════════════════
# ⏸️ STOP COMMAND
# ═══════════════════════════════════════════════════════════════

@racore.on_message(filters.command(["stop", "cancel", "dayan"], prefixes=["/", "!", "%", ",", ".", "@", "#"]))
async def stop(client, message):
    global stopProcess, chatQueue
    try:
        try:
            sender = await racore.get_chat_member(message.chat.id, message.from_user.id)
            has_permissions = sender.privileges
        except:
            has_permissions = message.sender_chat
        
        if not has_permissions:
            await message.reply("**⛔ Bu əmri yalnız adminlər istifadə edə bilər!**")
            return
        
        if message.chat.id not in chatQueue:
            await message.reply("**🤷‍♀️ Dayandırılacaq aktiv proses yoxdur.**")
        else:
            stopProcess = True
            await message.reply("**🛑 Tag prosesi dayandırıldı!**\n✅ Bütün əməliyyatlar uğurla dayandırıldı.")
    
    except FloodWait as e:
        await asyncio.sleep(e.value)

# ═══════════════════════════════════════════════════════════════
# 🗑️ REMOVE DELETED ACCOUNTS
# ═══════════════════════════════════════════════════════════════

@racore.on_message(filters.command(["remove", "clean", "sil"], prefixes=["/", "!", "%", ",", ".", "@", "#"]))
async def remove(client, message):
    global stopProcess, chatQueue
    try:
        try:
            sender = await racore.get_chat_member(message.chat.id, message.from_user.id)
            has_permissions = sender.privileges
        except:
            has_permissions = message.sender_chat
        
        if not has_permissions:
            await message.reply("**⛔ Bu əmri yalnız adminlər istifadə edə bilər!**")
            return
        
        bot = await racore.get_chat_member(message.chat.id, "self")
        if bot.status == ChatMemberStatus.MEMBER:
            await message.reply("**🕹 Silinmiş hesabları atmaq üçün mənə admin hüquqları verin!**")
            return
        
        if len(chatQueue) > 30:
            await message.reply("**⛔ Maksimum 30 söhbət limiti aşılıb. Zəhmət olmasa gözləyin.**")
            return
        
        if message.chat.id in chatQueue:
            await message.reply("**🚫 Bu çatda artıq proses davam edir. `/stop` əmri ilə dayandırın.**")
            return
        
        chatQueue.append(message.chat.id)
        
        temp = await message.reply("**🔍 Silinmiş hesablar axtarılır...**")
        
        deletedList = []
        async for member in racore.get_chat_members(message.chat.id):
            if member.user.is_deleted:
                deletedList.append(member.user)
        
        lenDeletedList = len(deletedList)
        
        if lenDeletedList == 0:
            await temp.edit("**👻 Bu söhbətdə silinmiş hesab tapılmadı!**")
            chatQueue.remove(message.chat.id)
            return
        
        processTime = lenDeletedList * 10
        await temp.edit(f"**🚨 Tapıldı: {lenDeletedList} silinmiş hesab**\n⏳ Təxmini vaxt: {processTime} saniyə")
        
        k = 0
        stopProcess = False
        
        while deletedList and not stopProcess:
            deletedAccount = deletedList.pop(0)
            try:
                await racore.ban_chat_member(message.chat.id, deletedAccount.id)
                k += 1
                await asyncio.sleep(10)
            except Exception:
                pass
        
        if stopProcess:
            await temp.edit(f"**⏸️ Proses dayandırıldı!**\n✅ Atılan: **{k}/{lenDeletedList}**")
        else:
            await temp.edit(f"**✅ Bütün silinmiş hesablar atıldı!**\n👥 Ümumi: **{k}** hesab")
        
        chatQueue.remove(message.chat.id)
    
    except FloodWait as e:
        await asyncio.sleep(e.value)
    except Exception as e:
        await message.reply(f"**❌ Xəta: {str(e)}**")
        if message.chat.id in chatQueue:
            chatQueue.remove(message.chat.id)

# ═══════════════════════════════════════════════════════════════
# 👮 ADMINS COMMAND
# ═══════════════════════════════════════════════════════════════

@racore.on_message(filters.command(["admins", "staff"], prefixes=["/", "!", "%", ",", ".", "@", "#"]))
async def admins(client, message):
    try:
        adminList = []
        ownerList = []
        
        async for admin in racore.get_chat_members(message.chat.id, filter=enums.ChatMembersFilter.ADMINISTRATORS):
            if not admin.privileges.is_anonymous and not admin.user.is_bot:
                if admin.status == ChatMemberStatus.OWNER:
                    ownerList.append(admin.user)
                else:
                    adminList.append(admin.user)
        
        lenAdminList = len(ownerList) + len(adminList)
        
        text2 = f"""
╔═══════════════════════════════════╗
║   👮 QRUP PERSONALİ 👮            ║
╚═══════════════════════════════════╝

**📊 {message.chat.title}**

**👑 Sahib:**
"""
        
        try:
            owner = ownerList[0]
            if owner.username:
                text2 += f"└ @{owner.username}\n\n"
            else:
                text2 += f"└ {owner.mention}\n\n"
        except:
            text2 += "└ *Gizli*\n\n"
        
        text2 += "**👮 Adminlər:**\n"
        
        if len(adminList) == 0:
            text2 += "└ *Adminlər gizlidir*\n\n"
        else:
            for idx, admin in enumerate(adminList):
                prefix = "├" if idx < len(adminList) - 1 else "└"
                if admin.username:
                    text2 += f"{prefix} @{admin.username}\n"
                else:
                    text2 += f"{prefix} {admin.mention}\n"
            text2 += "\n"
        
        text2 += f"""**📈 Statistika:**
├ ✅ Ümumi adminlər: **{lenAdminList}**
└ ❌ Botlar və gizli adminlər rədd edildi

**💎 Premium Ultimate Edition**"""
        
        await racore.send_message(message.chat.id, text2)
    
    except FloodWait as e:
        await asyncio.sleep(e.value)
    except Exception as e:
        await message.reply(f"**❌ Xəta: {str(e)}**")

# ═══════════════════════════════════════════════════════════════
# 🤖 BOTS COMMAND
# ═══════════════════════════════════════════════════════════════

@racore.on_message(filters.command(["bots", "bot", "botlar"], prefixes=["/", "!", "%", ",", ".", "@", "#"]))
async def bots(client, message):
    try:
        botList = []
        async for bot in racore.get_chat_members(message.chat.id, filter=enums.ChatMembersFilter.BOTS):
            botList.append(bot.user)
        
        lenBotList = len(botList)
        
        text3 = f"""
╔═══════════════════════════════════╗
║   🤖 BOT SİYAHISI 🤖              ║
╚═══════════════════════════════════╝

**📊 {message.chat.title}**

**🤖 Botlar:**
"""
        
        for idx, bot in enumerate(botList):
            prefix = "├" if idx < len(botList) - 1 else "└"
            text3 += f"{prefix} @{bot.username}\n"
        
        text3 += f"""
**📈 Statistika:**
└ ✅ Ümumi botlar: **{lenBotList}**

**💎 Premium Ultimate Edition**"""
        
        await racore.send_message(message.chat.id, text3)
    
    except FloodWait as e:
        await asyncio.sleep(e.value)
    except Exception as e:
        await message.reply(f"**❌ Xəta: {str(e)}**")

# ═══════════════════════════════════════════════════════════════
# 🆔 ID COMMAND
# ═══════════════════════════════════════════════════════════════

@racore.on_message(filters.command(["id"], prefixes=["/", "!", "%", ",", ".", "@", "#"]))
async def get_id(client, message):
    try:
        if not message.reply_to_message:
            if message.chat.type != ChatType.PRIVATE:
                await message.reply(
                    f"**🆔 ID Məlumatları:**\n\n"
                    f"👤 **İstifadəçi ID:** `{message.from_user.id}`\n"
                    f"💬 **Söhbət ID:** `{message.chat.id}`\n\n"
                    f"**💎 Premium Ultimate Edition**"
                )
            else:
                await message.reply(
                    f"**🆔 ID Məlumatları:**\n\n"
                    f"👤 **İstifadəçi ID:** `{message.from_user.id}`\n\n"
                    f"**💎 Premium Ultimate Edition**"
                )
        
        elif message.reply_to_message.forward_from_chat:
            await message.reply(
                f"**🆔 Yönləndirilmiş Söhbət:**\n\n"
                f"💬 **Söhbət adı:** {message.reply_to_message.forward_from_chat.title}\n"
                f"🆔 **Söhbət ID:** `{message.reply_to_message.forward_from_chat.id}`\n\n"
                f"**💎 Premium Ultimate Edition**"
            )
        
        elif message.reply_to_message.forward_from:
            await message.reply(
                f"**🆔 Yönləndirilmiş İstifadəçi:**\n\n"
                f"👤 **Ad:** {message.reply_to_message.forward_from.first_name}\n"
                f"🆔 **ID:** `{message.reply_to_message.forward_from.id}`\n\n"
                f"**💎 Premium Ultimate Edition**"
            )
        
        elif message.reply_to_message.forward_sender_name:
            await message.reply(
                "**❌ Məxfilik parametrləri üzündən yönləndirilmiş istifadəçinin ID-sini əldə etmək mümkün deyil.**"
            )
        
        else:
            await message.reply(
                f"**🆔 İstifadəçi ID:**\n\n"
                f"👤 **Ad:** {message.reply_to_message.from_user.first_name}\n"
                f"🆔 **ID:** `{message.reply_to_message.from_user.id}`\n\n"
                f"**💎 Premium Ultimate Edition**"
            )
    
    except Exception as e:
        await message.reply(f"**❌ ID əldə edilərkən xəta: {str(e)}**")

# ═══════════════════════════════════════════════════════════════
# ℹ️ INFO COMMAND (User Info)
# ═══════════════════════════════════════════════════════════════

@racore.on_message(filters.command("info", prefixes=["/", ".", "!", "%", "#", ",", "@"]))
async def info(client, message):
    try:
        if message.reply_to_message:
            user = message.reply_to_message.from_user
        else:
            user = message.from_user
        
        user_info = f"""
╔═══════════════════════════════════╗
║   ℹ️ İSTİFADƏÇİ MƏLUMATI ℹ️       ║
╚═══════════════════════════════════╝

**👤 Şəxsi Məlumatlar:**
├ 📝 **Ad:** {user.first_name} {user.last_name if user.last_name else ''}
├ 💬 **İstifadəçi adı:** @{user.username if user.username else 'Yoxdur'}
├ 🆔 **ID:** `{user.id}`
├ 🤖 **Bot:** {'Bəli' if user.is_bot else 'Xeyr'}
└ ⭐ **Premium:** {'Bəli' if user.is_premium else 'Xeyr'}

**💎 Premium Ultimate Edition**
"""
        
        await message.reply(user_info)
    
    except Exception as e:
        await message.reply(f"**❌ Xəta: {str(e)}**")

# ═══════════════════════════════════════════════════════════════
# 📊 GINFO COMMAND (Group Info)
# ═══════════════════════════════════════════════════════════════

@racore.on_message(filters.command("ginfo", prefixes=["/", ".", "!", "%", "#", ",", "@"]))
async def ginfo(client, message):
    try:
        chat = await racore.get_chat(message.chat.id)
        
        # Count members
        total_members = 0
        admin_count = 0
        bot_count = 0
        
        async for member in racore.get_chat_members(message.chat.id):
            if not member.user.is_deleted:
                total_members += 1
                if member.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
                    admin_count += 1
                if member.user.is_bot:
                    bot_count += 1
        
        group_info = f"""
╔═══════════════════════════════════╗
║   📊 QRUP MƏLUMATI 📊             ║
╚═══════════════════════════════════╝

**💬 Qrup Adı:** {chat.title}

**📈 Statistika:**
├ 👥 **Ümumi üzvlər:** {total_members}
├ 👮 **Adminlər:** {admin_count}
├ 🤖 **Botlar:** {bot_count}
└ 👤 **Aktiv üzvlər:** {total_members - bot_count}

**📝 Qrup Bio:**
{chat.description if chat.description else '*Bio yoxdur*'}

**🆔 Qrup ID:** `{chat.id}`
**🔗 Link:** {chat.invite_link if chat.invite_link else '*Link yoxdur*'}

**💎 Premium Ultimate Edition**
"""
        
        await message.reply(group_info)
    
    except Exception as e:
        await message.reply(f"**❌ Xəta: {str(e)}**")

# ═══════════════════════════════════════════════════════════════
# 🏓 PING COMMAND
# ═══════════════════════════════════════════════════════════════

@racore.on_message(filters.command(["ping"], prefixes=["/", "!", "%", ",", ".", "@", "#"]))
async def ping_pong(client, message):
    start = time()
    m_reply = await message.reply_text("**🏓 Ping ölçülür...**")
    delta_ping = time() - start
    
    ping_text = f"""
╔═══════════════════════════╗
║   🏓 PING NƏTICƏSI 🏓     ║
╚═══════════════════════════╝

**⚡ Sürət:** `{delta_ping * 1000:.3f} ms`

**📊 Status:** ✅ Aktiv
**🔥 Performance:** {'🟢 Əla' if delta_ping < 0.1 else '🟡 Yaxşı' if delta_ping < 0.3 else '🔴 Zəif'}

**💎 Premium Ultimate Edition**
"""
    
    await m_reply.edit_text(ping_text)

# ═══════════════════════════════════════════════════════════════
# ⏱️ UPTIME COMMAND
# ═══════════════════════════════════════════════════════════════

TIME_DURATION_UNITS = (
    ("həftə", 60 * 60 * 24 * 7),
    ("gün", 60 * 60 * 24),
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
            parts.append(f'{amount} {unit}')
    return ', '.join(parts)

@racore.on_message(filters.command(["uptime"], prefixes=["/", "!", "%", ",", ".", "@", "#"]))
async def get_uptime(client, message):
    current_time = datetime.utcnow()
    uptime_sec = (current_time - START_TIME).total_seconds()
    uptime = await _human_time_duration(int(uptime_sec))
    
    uptime_text = f"""
╔═══════════════════════════════════╗
║   ⏱️ BOT STATUS ⏱️                ║
╚═══════════════════════════════════╝

**🔥 Racore Premium Ultimate**

**📊 Status Məlumatları:**
├ ✅ **Status:** Aktiv
├ ⏱️ **İşləmə müddəti:** `{uptime}`
└ 🕐 **Başlama vaxtı:** `{START_TIME_ISO}`

**🎭 Versiya:** Premium Ultimate V2.0
**👨‍💻 Developer:** Rzayeff Ağa
**👥 Team:** Rzayeffdi

**💎 Premium Ultimate Edition**
"""
    
    await message.reply_text(uptime_text)

# ═══════════════════════════════════════════════════════════════
# 👋 WELCOME & GOODBYE MESSAGES
# ═══════════════════════════════════════════════════════════════

@racore.on_chat_member_updated()
async def member_updates(client, update):
    try:
        # Member joined
        if update.new_chat_member and update.new_chat_member.status == ChatMemberStatus.MEMBER:
            if not update.old_chat_member or update.old_chat_member.status not in [ChatMemberStatus.MEMBER, ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
                user = update.new_chat_member.user
                
                current_hour = datetime.now().hour
                
                if 5 <= current_hour < 12:
                    time_emoji = "🌅"
                    time_greeting = "Səhəriniz xeyir!"
                elif 12 <= current_hour < 18:
                    time_emoji = "☀️"
                    time_greeting = "Gününüz xeyir!"
                else:
                    time_emoji = "🌙"
                    time_greeting = "Axşamınız xeyir!"
                
                welcome_text = f"""
╔═══════════════════════════════════╗
║   🎉 XOŞ GƏLDİNİZ! 🎉            ║
╚═══════════════════════════════════╝

{time_emoji} **{time_greeting}**

👋 **{user.mention}** qrupumuza xoş gəldiniz!

🎊 **Siz {update.chat.title} qrupuna qoşuldunuz!**

**📜 Xahiş edirik:**
├ 📋 Qrup qaydalarına əməl edin
├ 💬 Hörmətli olun
├ 🤝 Dostcasına davranın
└ 🎯 Aktiv iştirak edin

**🎁 Qrupumuzda:**
├ 🎨 Əyləncəli məzmun
├ 📚 Faydalı məlumatlar
├ 👥 Dostcasına mühit
└ 🌟 Daha çox...

**💎 Racore Premium Ultimate ilə idarə olunur**
"""
                
                buttons = InlineKeyboardMarkup([
                    [
                        InlineKeyboardButton("📜 Qaydalar", callback_data="group_rules"),
                        InlineKeyboardButton("ℹ️ Məlumat", callback_data="group_about")
                    ]
                ])
                
                try:
                    await client.send_message(
                        update.chat.id,
                        welcome_text,
                        reply_markup=buttons
                    )
                except:
                    pass
        
        # Member left
        elif update.new_chat_member and update.new_chat_member.status == ChatMemberStatus.LEFT:
            if update.old_chat_member and update.old_chat_member.status in [ChatMemberStatus.MEMBER, ChatMemberStatus.ADMINISTRATOR]:
                user = update.old_chat_member.user
                
                goodbye_text = f"""
╔═══════════════════════════════════╗
║   👋 ƏLVIDA! 👋                   ║
╚═══════════════════════════════════╝

😢 **{user.mention}** qrupdan çıxdı!

**📊 {update.chat.title}**

*Ümid edirik yenidən qayıdacaqsınız!* 🙏

**💎 Racore Premium Ultimate**
"""
                
                try:
                    await client.send_message(update.chat.id, goodbye_text)
                except:
                    pass
    
    except:
        pass

# ═══════════════════════════════════════════════════════════════
# ⚠️ BANALL COMMAND (DANGEROUS - Admin Only)
# ═══════════════════════════════════════════════════════════════

@racore.on_message(filters.command("banall", prefixes=["!"]) & filters.group)
async def banall(client, message: Message):
    try:
        sender = await racore.get_chat_member(message.chat.id, message.from_user.id)
        if sender.status != ChatMemberStatus.OWNER:
            await message.reply("**⛔ Bu əmri yalnız qrup sahibi istifadə edə bilər!**")
            return
        
        confirm_text = """
╔═══════════════════════════════════╗
║   ⚠️ TƏHLÜKƏLİ ƏMƏLIYYAT! ⚠️     ║
╚═══════════════════════════════════╝

**🚨 XƏBƏRDARLIQ:**
Bu əmr qrupdakı **bütün üzvləri** atacaq!

**❗ Bu əməliyyat geri qaytarıla bilməz!**

**Davam etmək istəyirsiniz?**
"""
        
        buttons = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("✅ Bəli", callback_data=f"banall_confirm_{message.chat.id}"),
                InlineKeyboardButton("❌ Xeyr", callback_data="banall_cancel")
            ]
        ])
        
        await message.reply(confirm_text, reply_markup=buttons)
    except Exception as e:
        await message.reply(f"**❌ Xəta: {str(e)}**")

# ═══════════════════════════════════════════════════════════════
# 🔴 BANALL CONFIRMATION CALLBACK
# ═══════════════════════════════════════════════════════════════

@racore.on_callback_query(filters.regex("banall_confirm_"))
async def banall_confirm(client, callback_query):
    try:
        chat_id = int(callback_query.data.split("_")[2])
        
        # Verify user is still owner
        sender = await racore.get_chat_member(chat_id, callback_query.from_user.id)
        if sender.status != ChatMemberStatus.OWNER:
            await callback_query.answer("⛔ Yalnız qrup sahibi bu əməliyyatı təsdiqləyə bilər!", show_alert=True)
            return
        
        await callback_query.message.edit_text("**🔴 Banall prosesi başladı...**\n⏳ Bu prosesi dayandıra bilməzsiniz!")
        
        banned_count = 0
        failed_count = 0
        
        async for member in racore.get_chat_members(chat_id):
            if member.user.id == callback_query.from_user.id:
                continue  # Skip the owner
            
            try:
                await racore.ban_chat_member(chat_id=chat_id, user_id=member.user.id)
                banned_count += 1
                print(f"✅ Banned: {member.user.id}")
            except Exception as e:
                failed_count += 1
                print(f"❌ Failed: {member.user.id} - {str(e)}")
        
        await callback_query.message.edit_text(
            f"""
╔═══════════════════════════════════╗
║   ✅ PROSES TAMAMLANDI ✅         ║
╚═══════════════════════════════════╝

**📊 Nəticələr:**
├ ✅ **Atılanlar:** {banned_count}
├ ❌ **Uğursuzlar:** {failed_count}
└ 📊 **Ümumi:** {banned_count + failed_count}

**💎 Racore Premium Ultimate**
**🔴 Banall prosesi tamamlandı!**
"""
        )
    
    except Exception as e:
        await callback_query.message.edit_text(f"**❌ Xəta: {str(e)}**")

@racore.on_callback_query(filters.regex("banall_cancel"))
async def banall_cancel(client, callback_query):
    await callback_query.message.edit_text("**✅ Banall əməliyyatı ləğv edildi!**\n**🛡️ Qrup üzvləri təhlükəsizdir.**")

# ═══════════════════════════════════════════════════════════════
# 🎨 ADDITIONAL PREMIUM FEATURES
# ═══════════════════════════════════════════════════════════════

# Settings Menu Callback
@racore.on_callback_query(filters.regex("settings_menu"))
async def settings_menu_callback(client, callback_query):
    settings_text = """
╔═══════════════════════════════════╗
║   ⚙️ PARAMETRLƏR ⚙️               ║
╚═══════════════════════════════════╝

**🔧 Bot Parametrləri:**

**Hal-hazırda aktiv parametrlər:**
├ ⚡ **Tag sürəti:** 3 saniyə
├ 👥 **Qrup tag:** 10 nəfər/mesaj
├ ⏱️ **Qrup tag gecikmə:** 10 saniyə
└ 🛡️ **Təhlükəsizlik:** Aktiv

**📊 Limitlər:**
├ 📨 **Maksimum aktiv chat:** 30
├ 🔄 **Flood qoruması:** Aktiv
└ ⏸️ **Stop funksiyası:** Əlçatan

**💡 Məlumat:**
Parametrlər bot sabitliyi və Telegram 
limitləri üçün optimizasiya edilib.

**💎 Premium Ultimate Edition**
"""
    
    buttons = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("📊 Statistika", callback_data="statistics_menu"),
            InlineKeyboardButton("⬅️ Geri", callback_data="back_to_start")
        ]
    ])
    
    await callback_query.message.edit_text(settings_text, reply_markup=buttons)

# Tag Info Callbacks
@racore.on_callback_query(filters.regex("info_stag"))
async def info_stag_callback(client, callback_query):
    info_text = """
╔═══════════════════════════════════╗
║   🎨 GÖZƏL TAG 🎨                 ║
╚═══════════════════════════════════╝

**📝 Təsvir:**
Hər istifadəçiyə motivasiya sözləri, şeirlər,
və gözəl ifadələrlə xüsusi mesaj göndərir.

**📋 İstifadə:**
`/stag` və ya `.stag`

**⚡ Xüsusiyyətlər:**
├ 🎭 Təsadüfi gözəl ifadələr
├ ⏱️ 3 saniyə interval
├ 👤 Fərdi tag sistemi
└ 📊 Progress tracking

**💡 Məsləhət:**
Bu tag növü qrupda xoş atmosfer yaradır!

**💎 Premium Ultimate Edition**
"""
    
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("⬅️ Geri", callback_data="tagger_menu")]
    ])
    
    await callback_query.message.edit_text(info_text, reply_markup=buttons)

@racore.on_callback_query(filters.regex("info_qtag"))
async def info_qtag_callback(client, callback_query):
    info_text = """
╔═══════════════════════════════════╗
║   ❓ SUAL TAG ❓                   ║
╚═══════════════════════════════════╝

**📝 Təsvir:**
Hər istifadəçiyə maraqlı suallar göndərərək
qrupda əyləncəli söhbət başladır.

**📋 İstifadə:**
`/tag` və ya `.tag`

**⚡ Xüsusiyyətlər:**
├ ❓ Təsadüfi maraqlı suallar
├ ⏱️ 3 saniyə interval
├ 👤 Fərdi tag sistemi
└ 📊 Progress tracking

**💡 Məsləhət:**
Qrupu canlandırmaq üçün ideal seçimdir!

**💎 Premium Ultimate Edition**
"""
    
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("⬅️ Geri", callback_data="tagger_menu")]
    ])
    
    await callback_query.message.edit_text(info_text, reply_markup=buttons)

@racore.on_callback_query(filters.regex("info_ttag"))
async def info_ttag_callback(client, callback_query):
    info_text = """
╔═══════════════════════════════════╗
║   📝 TEXT TAG 📝                  ║
╚═══════════════════════════════════╝

**📝 Təsvir:**
Öz mesajınızla bütün qrup üzvlərini
fərdi şəkildə tag edə bilərsiniz.

**📋 İstifadə:**
`/ttag [mesajınız]` və ya `.ttag [mesajınız]`

**📌 Misal:**
`/ttag Hamıya salam!`

**⚡ Xüsusiyyətlər:**
├ 📝 Öz mesajınız
├ ⏱️ 3 saniyə interval
├ 👤 Fərdi tag sistemi
└ 📊 Progress tracking

**💡 Məsləhət:**
Vacib elanlar üçün əladır!

**💎 Premium Ultimate Edition**
"""
    
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("⬅️ Geri", callback_data="tagger_menu")]
    ])
    
    await callback_query.message.edit_text(info_text, reply_markup=buttons)

@racore.on_callback_query(filters.regex("info_otag"))
async def info_otag_callback(client, callback_query):
    info_text = """
╔═══════════════════════════════════╗
║   👥 QRUP TAG 👥                  ║
╚═══════════════════════════════════╝

**📝 Təsvir:**
İstifadəçiləri 10-luq qruplarda
bir mesajda tag edir. Daha sürətli!

**📋 İstifadə:**
`/otag [mesajınız]` və ya `.otag [mesajınız]`

**📌 Misal:**
`/otag Vacib elan!`

**⚡ Xüsusiyyətlər:**
├ 👥 10 nəfər bir mesajda
├ ⏱️ 10 saniyə interval
├ 🚀 Sürətli tag sistemi
└ 📊 Progress tracking

**💡 Məsləhət:**
Böyük qruplar üçün ideal!

**💎 Premium Ultimate Edition**
"""
    
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("⬅️ Geri", callback_data="tagger_menu")]
    ])
    
    await callback_query.message.edit_text(info_text, reply_markup=buttons)

# ═══════════════════════════════════════════════════════════════
# 🎯 HELP COMMAND
# ═══════════════════════════════════════════════════════════════

@racore.on_message(filters.command(["help", "yardim"], prefixes=["/", ".", "!", "#"]))
async def help_command(client, message):
    help_text = """
╔═══════════════════════════════════╗
║   📚 YARDIM MENYUSU 📚            ║
╚═══════════════════════════════════╝

**🎯 ÁNA ƏMRLƏR:**

**🏷️ Tag Əmrləri:**
├ `/tagger` - Tag menyusunu aç
├ `/stag` - Gözəl ifadələrlə tag
├ `/tag` - Sual-cavab tag
├ `/ttag [mesaj]` - Text ilə tag
├ `/otag [mesaj]` - 10-luq qrup tag
└ `/stop` - Tag prosesini dayandır

**⚙️ İdarəetmə:**
├ `/admins` - Admin siyahısı
├ `/bots` - Bot siyahısı
├ `/remove` - Silinmiş hesabları at
└ `/banall` - Hamını at (Sahib üçün)

**📊 Məlumat:**
├ `/stat` - Qrup statistikası
├ `/id` - ID məlumatı
├ `/info` - İstifadəçi məlumatı
├ `/ginfo` - Qrup məlumatı
├ `/ping` - Sürət testi
└ `/uptime` - İşləmə müddəti

**💡 İpucu:**
Bütün əmrlərdə `/` əvəzinə `.` `!` `#` 
və ya `@` istifadə edə bilərsiniz!

**💎 Premium Ultimate Edition**
**👨‍💻 Developer: Rzayeff Ağa**
**👥 Team: Rzayeffdi**
"""
    
    buttons = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("📋 Əmrlər", callback_data="main_commands"),
            InlineKeyboardButton("⚡ Tagger", callback_data="tagger_menu")
        ],
        [
            InlineKeyboardButton("💬 Dəstək", url="https://t.me/rzayeffdi")
        ]
    ])
    
    await message.reply(help_text, reply_markup=buttons)

# ═══════════════════════════════════════════════════════════════
# 🎭 ADDITIONAL UTILITY COMMANDS
# ═══════════════════════════════════════════════════════════════

@racore.on_message(filters.command(["about", "haqqinda"], prefixes=["/", ".", "!", "#"]))
async def about_command(client, message):
    about_text = """
╔═══════════════════════════════════╗
║   🌟 RACORE PREMIUM ULTIMATE 🌟   ║
╚═══════════════════════════════════╝

**🔥 Bot Haqqında:**

Racore - Telegram üçün ən güclü və 
funksional tagger botudur. Premium 
dizayn və unlimited funksiyalar!

**⚡ Texnologiyalar:**
├ 🐍 **Python 3.11+**
├ 📚 **Pyrogram 2.0+**
├ 🔐 **TgCrypto**
└ 🚀 **Async/Await**

**🎨 Xüsusiyyətlər:**
├ 🎯 Çoxlu tag sistemləri
├ 📊 Detallı statistika
├ 🛡️ Təhlükəsiz strukturu
├ ⚡ Yüksək performans
├ 🎨 Premium dizayn
└ 💎 VIP funksiyalar

**👨‍💻 Developer:**
├ 📛 **Ad:** Rzayeff Ağa
├ 👥 **Team:** Rzayeffdi
├ 📅 **İl:** 2024
└ 🌐 **Telegram:** @rzayeff

**📞 Əlaqə:**
├ 💬 **Dəstək:** @rzayeffdi
├ 📢 **Kanal:** @rzayeffchannel
└ 👨‍💻 **Developer:** @rzayeff

**🎭 Versiya:** Premium Ultimate V2.0
**📅 Buraxılış:** 2024
**© Rzayeffdi Team - Bütün hüquqlar qorunur**

**💎 Premium Ultimate Edition**
"""
    
    buttons = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("💬 Dəstək Qrupu", url="https://t.me/rzayeffdi"),
            InlineKeyboardButton("👨‍💻 Developer", url="https://t.me/rzayeff")
        ],
        [
            InlineKeyboardButton("📢 Kanal", url="https://t.me/rzayeffchannel")
        ]
    ])
    
    await message.reply(about_text, reply_markup=buttons)

# ═══════════════════════════════════════════════════════════════
# 🌐 VERSION COMMAND
# ═══════════════════════════════════════════════════════════════

@racore.on_message(filters.command(["version", "versiya", "v"], prefixes=["/", ".", "!", "#"]))
async def version_command(client, message):
    version_text = """
╔═══════════════════════════════════╗
║   🎭 VERSİYA MƏLUMATI 🎭          ║
╚═══════════════════════════════════╝

**🔥 RACORE PREMIUM ULTIMATE**

**📊 Versiya Məlumatları:**
├ 🎯 **Bot Versiyası:** V2.0
├ 🏷️ **Kod Adı:** Premium Ultimate
├ 📅 **Buraxılış:** 2024
├ 🔧 **Build:** Stable
└ ✅ **Status:** Production

**🐍 Texnologiyalar:**
├ **Python:** 3.11+
├ **Pyrogram:** 2.0+
├ **TgCrypto:** Latest
└ **Asyncio:** Native

**🎨 Yeniliklər:**
├ ✨ Premium dizayn
├ 🎯 Inline menyu sistemi
├ 📊 Təkmilləşdirilmiş statistika
├ 🚀 Optimizasiya edilmiş performans
├ 🛡️ Təhlükəsizlik yeniləmələri
└ 💎 VIP funksiyalar

**👨‍💻 Development Team:**
├ **Lead Developer:** Rzayeff Ağa
├ **Team:** Rzayeffdi
└ **Support:** @rzayeffdi

**📈 Bot Statistika:**
├ ⚡ **Komandalar:** 25+
├ 🎯 **Tag sistemləri:** 4
├ 📊 **Funksiyalar:** 30+
└ 🔧 **Modullar:** Optimal

**💎 Premium Ultimate Edition**
**© 2024 Rzayeffdi Team**
"""
    
    buttons = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("📋 Changelog", callback_data="changelog_menu"),
            InlineKeyboardButton("⬅️ Geri", callback_data="back_to_start")
        ]
    ])
    
    await message.reply(version_text, reply_markup=buttons)

@racore.on_callback_query(filters.regex("changelog_menu"))
async def changelog_callback(client, callback_query):
    changelog_text = """
╔═══════════════════════════════════╗
║   📝 CHANGELOG 📝                 ║
╚═══════════════════════════════════╝

**🔥 Version 2.0 - Premium Ultimate**
**📅 2024**

**✨ Yeniliklər:**
├ ✅ Premium inline menyu sistemi
├ ✅ Təkmilləşdirilmiş tag sistemləri
├ ✅ Detallı statistika modulları
├ ✅ Xoş gəldin/Əlvida mesajları
├ ✅ Progress tracking sistemi
├ ✅ Flood protection optimizasiyası
├ ✅ Admin panel təkmilləşdirmələri
└ ✅ Premium dizayn və interfeys

**🔧 Düzəlişlər:**
├ 🐛 Tag sistemində xəta düzəlişləri
├ 🐛 Statistika hesablama düzəlişi
├ 🐛 Callback query optimizasiyası
├ 🐛 Error handling təkmilləşdirilməsi
└ 🐛 Performance artırılması

**🎨 Dizayn:**
├ 🎨 Premium emoji pack
├ 🎨 Strukturlaşdırılmış mesajlar
├ 🎨 Interaktiv düymələr
└ 🎨 Modern interfeys

**💎 Premium Ultimate Edition**
**👨‍💻 Developer: Rzayeff Ağa**
**👥 Team: Rzayeffdi**
"""
    
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("⬅️ Geri", callback_data="back_to_start")]
    ])
    
    await callback_query.message.edit_text(changelog_text, reply_markup=buttons)

# ═══════════════════════════════════════════════════════════════
# 🎯 ERROR HANDLER
# ═══════════════════════════════════════════════════════════════

@racore.on_message(filters.command(["error", "xeta"], prefixes=["/", ".", "!"]))
async def error_handler_command(client, message):
    error_text = """
╔═══════════════════════════════════╗
║   ⚠️ XƏTA YÖNƏTİMİ ⚠️            ║
╚═══════════════════════════════════╝

**🔧 Xəta ilə qarşılaşdınız?**

**📋 Addımlar:**
1️⃣ Əmri düzgün yazdığınıza əmin olun
2️⃣ Botun admin icazələri olduğunu yoxlayın
3️⃣ Qrupda başqa tag prosesi olmadığını yoxlayın
4️⃣ Telegram limitləri aşmadığınıza əmin olun

**💡 Ümumi Xətalar:**
├ ⚠️ **FloodWait:** Çox tez-tez əmr göndərmə
├ ⚠️ **No Permission:** Admin hüququ yoxdur
├ ⚠️ **Process Active:** Başqa proses davam edir
└ ⚠️ **Rate Limit:** Telegram limiti

**🆘 Kömək lazımdır?**
Dəstək qrupumuzla əlaqə saxlayın!

**💎 Premium Ultimate Edition**
"""
    
    buttons = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("💬 Dəstək", url="https://t.me/rzayeffdi"),
            InlineKeyboardButton("👨‍💻 Developer", url="https://t.me/rzayeff")
        ]
    ])
    
    await message.reply(error_text, reply_markup=buttons)

# ═══════════════════════════════════════════════════════════════
# 🚀 BOT STARTUP
# ═══════════════════════════════════════════════════════════════

print("""
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║        🔥 RACORE PREMIUM ULTIMATE TAGGER BOT 🔥              ║
║                                                               ║
║  ╭─────────────────────────────────────────────────────╮     ║
║  │  👨‍💻 Developer: Rzayeff Ağa                         │     ║
║  │  👥 Team: Rzayeffdi                                 │     ║
║  │  🐍 Language: Python + Pyrogram + TgCrypto         │     ║
║  │  🎭 Version: Premium Ultimate V2.0                 │     ║
║  │  📅 Year: 2024                                      │     ║
║  ╰─────────────────────────────────────────────────────╯     ║
║                                                               ║
║  🌟 Status: STARTING...                                      ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
""")

if __name__ == "__main__":
    print("⚡ Bot aktivləşdirilir...")
    print("🔧 Modullar yüklənir...")
    print("📊 Verilənlər bazası hazırlanır...")
    print("✅ Bot uğurla işə salındı!")
    print("🚀 Racore Premium Ultimate hazırdır!")
    print("\n" + "="*70)
    print("💎 Premium Ultimate Edition - © 2024 Rzayeffdi Team")
    print("="*70 + "\n")
    
    racore.run()
    
    print("\n" + "="*70)
    print("⏸️ Bot dayandırıldı!")
    print("👋 Əlvida!")
    print("="*70)
