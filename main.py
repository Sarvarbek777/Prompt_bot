import os
import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton, ChatMemberMember, ChatMemberAdministrator, ChatMemberOwner
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
CHANNELS = os.getenv("BOT_CHANNELS")
CHANNEL_LINK = os.getenv("BOT_CHANNEL_LINK")


bot = Bot(token=TOKEN)
dp = Dispatcher()

# --- OBUNANI TEKSHIRISH FUNKSIYASI ---
async def check_sub_status(user_id):
    for channel in CHANNELS:
        try:
            member = await bot.get_chat_member(chat_id=channel, user_id=user_id)
            # Agar foydalanuvchi a'zo, admin yoki yaratuvchi bo'lsa True qaytaradi
            if isinstance(member, (ChatMemberMember, ChatMemberAdministrator, ChatMemberOwner)):
                continue
            else:
                return False
        except Exception as e:
            logging.error(f"Xatolik: {e}")
            return False
    return True

# Obuna bo'lmaganlar uchun tugma
def get_sub_keyboard():
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="Obuna bo'lish ➕", url=CHANNEL_LINK))
    builder.add(InlineKeyboardButton(text="Tekshirish ✅", callback_data="check_subscription"))
    builder.adjust(1)
    return builder.as_markup()

# BARCHA MA'LUMOTLAR (PROMPTLAR)
PROMPTS_DATA = {
    "🎨 Rasm yaratish": {
        "Logo yaratish": "Minimalist vector logo design, [mavzu], flat design, white background, high resolution.",
        "Realistik Portret": "Hyper-realistic portrait of [mavzu], 8k resolution, cinematic lighting, detailed skin pores, shot on 85mm lens.",
        "Anime Uslubi": "Anime style illustration of [mavzu], Studio Ghibli colors, high quality, soft lighting, vibrant scenery.",
        "Arxitektura": "Modern luxury villa design, glass walls, sunset lighting, architectural photography, 8k render.",
        "3D Render": "Cute 3D character of [mavzu], Pixar style, high detail, soft shadows, colorful, 8k render."
    },
    "📝 Maqola va Matn": {
        "Blog Post": "Mavzu: [mavzu]. Ushbu mavzuda o'quvchini jalb qiladigan, qiziqarli va informatsion blog post yozib ber.",
        "Esse yozish": "Write a formal essay on [mavzu]. Include an introduction, 3 body paragraphs, and a conclusion.",
        "Email yozish": "Write a professional email to [kimga] about [mavzu]. Tone: Polite and formal.",
        "Xulosa qilish": "Ushbu matnni eng muhim nuqtalarini saqlab qolgan holda qisqacha xulosa qilib ber: [matnni joylang].",
        "Hikoya yozish": "Write a creative short story about [mavzu]. Genre: Sci-fi/Fantasy."
    },
    "📱 SMM va Kontent": {
        "Instagram Caption": "Instagram post uchun [mavzu] haqida qisqa, qiziqarli va emojilarga boy matn yozib ber.",
        "YouTube Ssenariy": "10 daqiqalik YouTube videosi uchun ssenariy rejasi tuzib ber. Mavzu: [mavzu].",
        "TikTok/Reels g'oya": "Create 5 viral video ideas for TikTok/Reels about [mavzu].",
        "Telegram Post": "Telegram kanal uchun [mavzu] haqida foydali va o'qishga oson post tayyorla."
    },
    "💻 Dasturlash va IT": {
        "Kod yozish": "Write a [til] function to [vazifa]. Explain how it works step by step.",
        "Xatoni topish": "Check this [til] code for bugs and fix them: [kodni joylang].",
        "SQL So'rovlar": "Write an SQL query to [vazifa] from a table named [jadval nomi].",
        "Kod tushuntirish": "Explain this code in simple terms for a beginner: [kodni joylang]."
    },
    "💼 Biznes va Marketing": {
        "Biznes Reja": "[Mavzu] bo'yicha startap uchun qisqa biznes reja va strategiya tuzib ber.",
        "Reklama matni": "Facebook Ads uchun [mahsulot] haqida sotuvchi (copywriting) matn yoz.",
        "Brending": "[Mavzu] biznesi uchun 10 ta o'ziga xos nom va shior (slogan) o'ylab top.",
        "Mijoz bilan aloqa": "Mijozning [e'tiroz] haqidagi shikoyatiga professional va xushmuomala javob matni tayyorla."
    },
    "🎓 Ta'lim va O'rganish": {
        "Til o'rganish": "Ingliz tilida [mavzu] bo'yicha eng ko'p ishlatiladigan 20 ta so'z va ularning tarjimasini ber.",
        "Oddiy tushuntirish": "Explain [murakkab mavzu] like I'm 5 years old (ELI5).",
        "Test savollari": "[Mavzu] bo'yicha bilimni tekshirish uchun 5 ta ko'p variantli (MCQ) test tuz."
    },
    "⚡️ Shaxsiy rivojlanish": {
        "Vaqt boshqaruvi": "Kunlik samarali ish rejasini tuzib ber. Maqsad: [maqsad].",
        "Sog'lom ovqatlanish": "1 hafta uchun [vazn] kg vazn tashlashga mo'ljallangan sog'lom taomnoma tuz.",
        "Motivatsiya": "O'z ustida ishlash va dangasalikni yengish bo'yicha amaliy maslahatlar ber."
    },
}

# --- KLAVIATURALAR ---
def get_main_keyboard():
    builder = InlineKeyboardBuilder()
    for category in PROMPTS_DATA.keys():
        builder.add(InlineKeyboardButton(text=category, callback_data=f"cat_{category}"))
    builder.adjust(2)
    return builder.as_markup()

def get_sub_keyboard_internal(category):
    builder = InlineKeyboardBuilder()
    for sub in PROMPTS_DATA[category].keys():
        builder.add(InlineKeyboardButton(text=sub, callback_data=f"sub_{category}_{sub}"))
    builder.add(InlineKeyboardButton(text="⬅️ Orqaga", callback_data="back_to_main"))
    builder.adjust(1)
    return builder.as_markup()

# --- HANDLERLAR ---

@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    # Obunani tekshirish
    is_sub = await check_sub_status(message.from_user.id)
    if not is_sub:
        await message.answer(
            f"❌ **Kechirasiz!** Botdan foydalanish uchun kanalimizga obuna bo'lishingiz kerak:",
            reply_markup=get_sub_keyboard(),
            parse_mode="Markdown"
        )
        return

    await message.answer(
        "👋 **Xush kelibsiz!** Bo'limni tanlang:",
        reply_markup=get_main_keyboard(),
        parse_mode="Markdown"
    )

# "Tekshirish ✅" tugmasi bosilganda
@dp.callback_query(F.data == "check_subscription")
async def check_button(callback: types.CallbackQuery):
    is_sub = await check_sub_status(callback.from_user.id)
    if is_sub:
        await callback.answer("Rahmat, obuna tasdiqlandi! ✅")
        await callback.message.edit_text(
            "👋 **Xush kelibsiz!** Bo'limni tanlang:",
            reply_markup=get_main_keyboard(),
            parse_mode="Markdown"
        )
    else:
        await callback.answer("Hali obuna bo'lmagansiz! ❌", show_alert=True)

@dp.callback_query(F.data == "back_to_main")
async def back_to_main(callback: types.CallbackQuery):
    if not await check_sub_status(callback.from_user.id):
        await callback.message.edit_text("Botdan foydalanish uchun kanalga a'zo bo'ling!", reply_markup=get_sub_keyboard())
        return

    await callback.message.edit_text(
        "Bo'limni tanlang:",
        reply_markup=get_main_keyboard()
    )

@dp.callback_query(F.data.startswith("cat_"))
async def process_category(callback: types.CallbackQuery):
    if not await check_sub_status(callback.from_user.id):
        await callback.answer("Avval kanalga a'zo bo'ling!", show_alert=True)
        return

    category = callback.data.split("_", 1)[1]
    await callback.message.edit_text(
        f"📂 **{category}** bo'limi.\nYo'nalishni tanlang:",
        reply_markup=get_sub_keyboard_internal(category),
        parse_mode="Markdown"
    )

@dp.callback_query(F.data.startswith("sub_"))
async def process_prompt(callback: types.CallbackQuery):
    if not await check_sub_status(callback.from_user.id):
        await callback.answer("Avval kanalga a'zo bo'ling!", show_alert=True)
        return


    data = callback.data.split("_", 2)
    category = data[1]
    sub = data[2]
    prompt_text = PROMPTS_DATA[category][sub]

    response = (
        f"📍 **Yo'nalish:** {sub}\n"
        f"📝 **Prompt:**\n\n"
        f"`{prompt_text}`\n\n"
        f"👆 _Nusxa olish uchun matn ustiga bosing._"
    )

    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="⬅️ Orqaga", callback_data=f"cat_{category}"))
    await callback.message.edit_text(response, reply_markup=builder.as_markup(), parse_mode="Markdown")

async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot to'xtatildi")