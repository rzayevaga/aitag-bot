import asyncio
import random
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
import json
from bp import beautiful_phrases
# Botun məlumatları
API_ID = 123456  # Telegram API ID
API_HASH = ""  # Telegram API Hash
BOT_TOKEN = ""  # Bot Token

# Bot müştərisi
rzayeff = Client("tag_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Tağ etmə prosesinin dayandırılması üçün flag
tagging_in_progress = False

# Inline düymələri göndərən menyu
@rzayeff.on_message(filters.command(["tag", "tağ", "tagger", "menu", "menyu"], prefixes=["/", "!", "."]) & filters.group)
async def show_menu(client: Client, message: Message):
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("😍 Sözlərlə tağ", callback_data="tag_with_phrases"),
                InlineKeyboardButton("😉 Beş'li tağ", callback_data="tag_five"),
            ],
            [
                InlineKeyboardButton("☑️ Tağı dayandır", callback_data="stop_tagging"),
            ]
        ]
    )
    await message.reply_text("Salam, Tağ Menyusu:", reply_markup=keyboard)

# Callback data-ları idarə edən funksiya
@rzayeff.on_callback_query()
async def handle_callbacks(client: Client, callback_query):
    global tagging_in_progress
    data = callback_query.data
    chat_id = callback_query.message.chat.id

    if data == "tag_with_phrases":
        await tag_with_phrases(client, callback_query.message)
    elif data == "tag_five":
        await tag_five(client, callback_query.message)
    elif data == "stop_tagging":
        tagging_in_progress = False
        await callback_query.message.reply_text("Tağ prosesi dayandırıldı.")
    await callback_query.answer()

# Sözlərlə tağ edən funksiya
async def tag_with_phrases(client: Client, message: Message):
    global tagging_in_progress
    chat_id = message.chat.id

    if tagging_in_progress:
        await message.reply_text("Tağ prosesi artıq davam edir. Lütfən, bitməsini gözləyin.")
        return

    tagging_in_progress = True
    await message.reply_text("Sözlərlə tağ prosesi başladı...")

    async for member in client.get_chat_members(chat_id):
        if not tagging_in_progress:
            await message.reply_text("Tağ prosesi dayandırıldı.")
            return

        if member.user.is_bot:
            continue

        phrase = random.choice(beautiful_phrases)
        user_tag = (
            f"@{member.user.username}"
            if member.user.username
            else f"[{member.user.first_name}](tg://user?id={member.user.id})"
        )
        tag_message = f"{user_tag}, {phrase}"
        await client.send_message(chat_id, tag_message, disable_web_page_preview=True)
        await asyncio.sleep(3)

    tagging_in_progress = False
    await message.reply_text("Tağ prosesi tamamlandı!")

# Beş'li tağ edən funksiya
async def tag_five(client: Client, message: Message, custom_message=None):
    global tagging_in_progress
    chat_id = message.chat.id

    if tagging_in_progress:
        await message.reply_text("Tağ prosesi artıq davam edir. Lütfən, bitməsini gözləyin.")
        return

    tagging_in_progress = True
    await message.reply_text("Beş'li tağ prosesi başladı...")

    members = []
    async for member in client.get_chat_members(chat_id):
        if member.user.is_bot:
            continue
        user_tag = (
            f"@{member.user.username}"
            if member.user.username
            else f"[{member.user.first_name}](tg://user?id={member.user.id})"
        )
        members.append(user_tag)

    for i in range(0, len(members), 5):
        if not tagging_in_progress:
            await message.reply_text("Tağ prosesi dayandırıldı.")
            return

        tag_group = members[i:i+5]
        tag_message = " ".join(tag_group)
        if custom_message:
            tag_message += f"\n\n{custom_message}"

        await client.send_message(chat_id, tag_message, disable_web_page_preview=True)
        await asyncio.sleep(3)

    tagging_in_progress = False
    await message.reply_text("Beş'li tağ prosesi tamamlandı!")

# /btag əmri ilə beş'li tağ
@rzayeff.on_message(filters.command("btag", prefixes=["/", "!", "."]) & filters.group)
async def btag_command(client: Client, message: Message):
    custom_message = message.text.split(maxsplit=1)[1] if len(message.text.split()) > 1 else None
    await tag_five(client, message, custom_message)


# JSON faylını oxumaq və yazmaq üçün funksiyalar
def load_data():
    try:
        with open("data.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_data(data):
    with open("data.json", "w") as file:
        json.dump(data, file, indent=4)

# Botun əsas funksiyası (Qrupda edilən söhbətləri izləmək)
@rzayeff.on_message(filters.text)
def handle_message(client, message):
    data = load_data()

    # Qrupda edilən söhbətləri toplayırıq
    if message.chat.type == "supergroup":
        user = message.from_user.username or message.from_user.first_name
        text = message.text
        
        # İstifadəçi tərəfindən verilən cavabları və sözləri qeyd edirik
        if message.reply_to_message:
            replied_text = message.reply_to_message.text
            if replied_text:
                if replied_text not in data:
                    data[replied_text] = []
                data[replied_text].append(text)
        else:
            if text not in data:
                data[text] = []
        
        # İstifadəçi tərəfindən əlavə edilən sözləri saxlayırıq
        if user not in data:
            data[user] = []
        data[user].append(text)


# JSON faylını oxumaq və yazmaq üçün funksiyalar
def load_data():
    try:
        with open("data.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {"welcome_messages": {}, "user_words": {}}  # Əgər fayl yoxdursa, başlanğıc dəyəri

def save_data(data):
    with open("data.json", "w") as file:
        json.dump(data, file, indent=4)

# Welcome mesajı
@rzayeff.on_message(filters.new_chat_members)
async def welcome(client, message):
    chat_id = message.chat.id
    data = load_data()  # Data faylını yükləyirik
    for member in message.new_chat_members:
        # Xoş gəldin mesajını JSON-dan alırıq
        welcome_text = data["welcome_messages"].get(str(chat_id), "Xoş gəldiniz!")
        await message.reply_text(f"{welcome_text}, {member.mention}!")

# Welcome mesajını təyin et
@rzayeff.on_message(filters.command("setwelcome") & filters.group)
async def set_welcome(client, message):
    # Qrup admini olub-olmadığını yoxlayaq
    if not message.from_user.id in [admin.user.id for admin in await message.chat.get_members(filters="administrator")]:
        await message.reply_text("Bu əmri yalnız qrup adminləri icra edə bilər!")
        return

    if len(message.command) < 2:
        await message.reply_text("Xahiş edirəm, yeni Xoş Gəldin mesajını daxil edin.")
        return
    chat_id = message.chat.id
    welcome_text = " ".join(message.command[1:])
    
    # Data faylını yükləyirik və yeni mesajı saxlayırıq
    data = load_data()
    data["welcome_messages"][str(chat_id)] = welcome_text
    save_data(data)
    
    await message.reply_text("Qarşılama mesajı uğurla təyin edildi!")

# Qrup daxilində edilən söhbətləri toplayırıq və istifadəçi tərəfindən əlavə edilən sözləri saxlayırıq
@rzayeff.on_message(filters.text)
def handle_message(client, message):
    data = load_data()

    # Qrupda edilən söhbətləri toplayırıq
    if message.chat.type == "supergroup":
        user = message.from_user.username or message.from_user.first_name
        text = message.text
        
        # İstifadəçi tərəfindən verilən cavabları və sözləri qeyd edirik
        if message.reply_to_message:
            replied_text = message.reply_to_message.text
            if replied_text:
                if replied_text not in data["user_words"]:
                    data["user_words"][replied_text] = []
                data["user_words"][replied_text].append(text)
        else:
            if text not in data["user_words"]:
                data["user_words"][text] = []
        
        # İstifadəçi tərəfindən əlavə edilən sözləri saxlayırıq
        if user not in data["user_words"]:
            data["user_words"][user] = []
        data["user_words"][user].append(text)

    save_data(data)

# İstifadəçilərin öz sözlərini əlavə etməsi üçün komanda
@rzayeff.on_message(filters.command("addsoz"))
def add_word(client, message):
    data = load_data()

    # Komanda strukturu /addsoz <söz> - <tərcümə>
    if len(message.text.split()) > 2:
        word, translation = message.text.split(" ", 2)[1], message.text.split(" ", 2)[2]
        if word not in data["user_words"]:
            data["user_words"][word] = []
        data["user_words"][word].append(translation)
        save_data(data)
        message.reply(f"'{word}' sözü əlavə edildi!")
    else:
        message.reply("Zəhmət olmasa, düzgün formatda daxil edin: /addsoz <söz> - <tərcümə>")

# İstifadəçilərin əlavə etdiyi sözləri göstərmək üçün komanda
@rzayeff.on_message(filters.command("sözlər"))
def list_words(client, message):
    data = load_data()
    user = message.from_user.username or message.from_user.first_name
    if user in data["user_words"]:
        words = "\n".join([f"{word}: {', '.join(translations)}" for word, translations in data["user_words"][user].items()])
        message.reply(f"Sənin əlavə etdiyin sözlər:\n{words}")
    else:
        message.reply("Heç bir söz əlavə etməmisiniz.")

# İstifadəçilərin əlavə etdiyi sözləri silmək üçün komanda
@rzayeff.on_message(filters.command("silsoz"))
def delete_word(client, message):
    data = load_data()

    # Komanda strukturu /silsoz <söz>
    if len(message.text.split()) > 1:
        word = message.text.split(" ", 1)[1]
        user = message.from_user.username or message.from_user.first_name
        
        # Yalnız istifadəçinin öz əlavə etdiyi sözləri silmək
        if user in data["user_words"] and word in data["user_words"][user]:
            del data["user_words"][user][word]  # İstifadəçinin sözünü silirik
            if not data["user_words"][user]:  # İstifadəçi artıq heç bir söz əlavə etməyibsə, onu silirik
                del data["user_words"][user]
            save_data(data)
            message.reply(f"'{word}' sözü silindi!")
        else:
            message.reply(f"'{word}' sözü tapılmadı və ya bu söz sizin tərəfinizdən əlavə edilməyib.")
    else:
        message.reply("Zəhmət olmasa, silmək istədiyiniz sözü daxil edin: /silsoz <söz>")

# Botun avtomatik cavab verməsi
@rzayeff.on_message(filters.text)
def auto_reply(client, message):
    data = load_data()
    text = message.text

    # Bot, istifadəçinin yazdığı sözə cavab verir
    if text in data["user_words"]:
        reply = data["user_words"][text]
        if reply:
            # Bu zaman "Bu sözə cavab" mesajı olmadan, sadəcə cavabı göndəririk
            message.reply(f"{', '.join(reply)}")

    # "söz" yazıldığında inline button göndəririk
    if "söz" in text.lower():
        keyboard = [
            [InlineKeyboardButton("➕ Öz Sözünü Əlavə Et ➕", callback_data="add_word")],
            [InlineKeyboardButton("Sənin Əlavə etdiyin sözlər", callback_data="my_words")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        message.reply("Bu sözə cavab olaraq öz sözünü əlavə edə bilərsən:", reply_markup=reply_markup)

# Inline button-a basıldığında istifadəçiyə söz əlavə etməsi üçün komanda göndəririk
@rzayeff.on_callback_query(filters.regex("add_word"))
def on_button_click(client, callback_query):
    callback_query.answer()
    callback_query.message.reply("Zəhmət olmasa, əlavə etmək istədiyiniz sözü daxil edin: /addsoz <söz> - <tərcümə>")

# "Sənin Əlavə etdiyin sözlər" buttonuna basıldığında istifadəçiyə öz sözlərini göstəririk
@rzayeff.on_callback_query(filters.regex("my_words"))
def on_my_words_button_click(client, callback_query):
    data = load_data()
    user = callback_query.from_user.username or callback_query.from_user.first_name
    callback_query.answer()

    if user in data["user_words"]:
        words = "\n".join([f"{word}: {', '.join(translations)}" for word, translations in data["user_words"][user].items()])
        callback_query.message.reply(f"Sənin əlavə etdiyin sözlər:\n{words}")
    else:
        callback_query.message.reply("Heç bir söz əlavə etməmisiniz.")


# Botu işə salırıq
if __name__ == "__main__":
    rzayeff.run()
