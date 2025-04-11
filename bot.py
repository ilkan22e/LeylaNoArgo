from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
import asyncio

# Telegram API məlumatları
api_id = 24987920  # <-- Buraya öz API ID-ni yaz
api_hash = "ab67324974dbf85ef4f7e75712d4c746"  # <-- Buraya öz API HASH
bot_token = "7553414866:AAF7t6nlwjxl-5KC9AVIQ5wxnvStD2NawVA"  # <-- Buraya öz Bot Token

app = Client("no_söyüş_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

# Söyüş kökləri və şəkilçilər
söyüşlər = ["sikdir", "qehbe", "qəhbə", "anavı", "cındır", "blət","blet", "sikim", "oğraş", "dalbayov","osduraq", "boynu", "nın", "vı","va", "s2m", "Dalbek", "dalben","qandon", "dişi", "fayşə", "faişə","qehbe", "təpdir", "siydir", "siyim","qehbe", "qəhbə", "vz", "vzqırt","kiwi", "oğlancıq", "bacını", "xirtəyini","boşalıram", "verirəm", "real", "virtual","çal", "banan", "gala", "uç","hamilə", "donbal", "Dombale", "Dombal" ]
söyüş_şəkilçilər = ["nın", "vı", "vu", "sər", "m", "un", "ni", "nı"]

# Aktiv olan qruplar üçün saxlama
aktiv_qruplar = {}

# Söyüş yoxlama funksiyası
def söyüş_var(metin):
    metin = metin.lower().replace(" ", "")
    for söz in söyüşlər:
        if söz in metin:
            return True
        for şəkilçi in söyüş_şəkilçilər:
            if f"{söz}{şəkilçi}" in metin:
                return True
    return False

# No söyüş funksiyasını aç/bağla
@app.on_message(filters.command("noargo") & filters.group)
async def toggle_no_söyüş(_, message: Message):
    if len(message.command) < 2:
        await message.reply("İstifadə: /noargo  yes və ya /noargo no")
        return

    cmd = message.command[1].lower()
    if cmd == "yes":
        aktiv_qruplar[message.chat.id] = True
        await message.reply("No söyüş funksiyası artıq **aktiv edildi**.")
    elif cmd == "no":
        aktiv_qruplar.pop(message.chat.id, None)
        await message.reply("No söyüş funksiyası artıq **deaktiv edildi**.")
    else:
        await message.reply("Yanlış seçim, /nosöyüş aç və ya /nosöyüş bağla yaz.")

# Qrup mesajlarını yoxlayır
@app.on_message(filters.group & ~filters.command("nosöyüş"))
async def söyüş_yoxla(_, message: Message):
    if aktiv_qruplar.get(message.chat.id):
        if message.text and söyüş_var(message.text):
            await message.delete()
            await message.reply(f"Hörmətli {message.from_user.mention} Zəhmət olmasa Etikdadan kənar Argo kəlmələr istifadə etməyək,Əks halda ban oluna bilərsiniz😊 ")

# /start komandası üçün animasiya və info mesaj
@app.on_message(filters.command("start") & filters.private)
async def start_cmd(_, message: Message):
    user = message.from_user.first_name

    # 1. 🔞 mesajı
    step1 = await message.reply("🔞")
    await asyncio.sleep(1)
    await step1.delete()

    # 2. Leyla No Söyüş Aktifdir
    step2 = await message.reply("**`𝑵𝒐 𝑺𝒐𝒚𝒖𝒔 𝑨𝒌𝒕𝒊𝒇𝒅𝒊𝒓`**")
    await asyncio.sleep(1.5)
    await step2.delete()

    # 3. Əsas məlumat mesajı + şəkil olmadan
    await message.reply(
        f"**Salam {user}**👋\n"
        "Mən qruplarda **Na Layiq ifadələri və Söyüşləri** silə bilən botam🔞\n"
        "Daha ətraflı məlumat üçün /help komandasını yaz📜\n"
        "Məni Qrupuna əlavə edib **silmə yetkisi verin**🌟",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("➕ Məni qrupuna əlavə et", url="https://t.me/LeylaNoArgoBot?startgroup=true")],
            [
                InlineKeyboardButton("🇦🇿 Owner", url="https://t.me/SpeeditsMee"),
                InlineKeyboardButton("👨‍💻 Developer", url="https://t.me/Hakketdim")
            ],
            [InlineKeyboardButton("🔔 Kanal", url="https://t.me/Lcifsafed")]
        ])
    )

    # Mesajı silmək
    await message.delete()


# /help komandası üçün məlumat mesajı
@app.on_message(filters.command("help") & filters.private)
async def help_cmd(_, message: Message):
    await message.reply(
        "**📖 Bot haqqında məlumat:**\n\n"
        "Bu bot qruplarda **söyüşləri və nalayiq sözləri avtomatik silir**.\n"
        "Botun düzgün işləməsi üçün ona admin və **mesajları silmək** icazəsi verin.\n\n"
        "**Komandalar:**\n"
        "• `/noargo yes` - Söyüşləri avtomatik silməyi aktiv edin\n"
        "• `/noargo no` - Söyüşləri silməyi deaktiv edin\n"
        "• `/start` - Bot haqqında qısa info və start mesajı\n"
        "• `/help` - Bu yardım mesajı\n\n"
        "**🔔 Əlaqə:**\n"
        "🇦🇿 Owner: @SpeeditsMee\n"
        "👨‍💻 Developer: @Hakketdim\n"
        "📢 Kanal: @LeylaRobotlar",
        disable_web_page_preview=True
    )

# Botu işə sal
app.run()
