import httpx
from utils import load_tokens
from config import BASE_URL
from datetime import datetime
from languages import get_message

def translate_items(items_str: str, lang: str) -> str:
    """Translate symptoms or medications from English to the target language"""
    if not items_str or lang == 'en':
        return items_str
        
    # Create translation dictionaries from SYMPTOM_OPTIONS and MEDICATION_OPTIONS
    translations = {}
    
    # Add symptom translations
    for en_list, fa_list in zip(SYMPTOM_OPTIONS['en'], SYMPTOM_OPTIONS['fa']):
        for en, fa in zip(en_list, fa_list):
            if en not in ['Write Custom Symptoms', 'Done']:
                translations[en] = fa
                
    # Add medication translations
    for en_list, fa_list in zip(MEDICATION_OPTIONS['en'], MEDICATION_OPTIONS['fa']):
        for en, fa in zip(en_list, fa_list):
            if en not in ['Write Custom Medication', 'Done']:
                translations[en] = fa
    
    # Split items and translate each one
    items = [item.strip() for item in items_str.split(',')]
    translated_items = []
    
    for item in items:
        translated_items.append(translations.get(item, item))  # Use original if no translation
        
    return ', '.join(translated_items)

async def fetch_periods(update, context):
    """Fetch and display period history"""
    lang = context.user_data.get('language', 'en')
    chat_id = str(update.message.chat_id)
    
    # Get access token from user_tokens
    from bot import user_tokens
    if chat_id not in user_tokens or "access" not in user_tokens[chat_id]:
        await update.message.reply_text(get_message(lang, 'auth', 'login_required'))
        return
        
    access_token = user_tokens[chat_id]["access"]
    headers = {"Authorization": f"Bearer {access_token}"}
    
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/api/periods/", headers=headers)

        if response.status_code == 401:  # Token expired
            new_token = await refresh_token(chat_id, user_tokens)
            if new_token:
                headers["Authorization"] = f"Bearer {new_token}"
                response = await client.get(f"{BASE_URL}/api/periods/", headers=headers)

        if response.status_code == 200:
            periods = response.json()
            
            if not periods:
                await update.message.reply_text(get_message(lang, 'errors', 'no_history'))
                return
            
            # Add RTL mark for Persian
            rtl_mark = '\u200F' if lang == 'fa' else ''
            ltr_mark = '\u200E' if lang == 'fa' else ''
            
            formatted_periods = f"{get_message(lang, 'period_history', 'title')}\n\n"
            
            for idx, period in enumerate(sorted(periods, key=lambda x: x["start_date"], reverse=True), start=1):
                start_date = period["start_date"]
                end_date = period["end_date"]
                predicted_end_date = period.get("predicted_end_date")
                
                # Translate symptoms and medications
                symptoms = translate_items(period['symptoms'], lang) if period['symptoms'] else get_message(lang, 'period_history', 'none_noted')
                medications = translate_items(period['medication'], lang) if period['medication'] else get_message(lang, 'period_history', 'none_taken')
                
                if lang == 'fa':
                    symptoms = f"{rtl_mark}{symptoms}"
                    medications = f"{rtl_mark}{medications}"
                
                formatted_periods += (
                    f"{rtl_mark}{get_message(lang, 'period_history', 'cycle', idx)}\n"
                    f"┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈\n\n"
                    f"{rtl_mark}🗓 {ltr_mark}*{start_date}* → *{end_date}*\n"
                    f"{rtl_mark}{get_message(lang, 'period_history', 'predicted')}: {ltr_mark}*{predicted_end_date}*\n"
                    f"{rtl_mark}{get_message(lang, 'period_history', 'duration')}: {ltr_mark}*{calculate_duration(start_date, end_date, lang)}*{rtl_mark}{get_message(lang, 'period_history', 'days')}\n\n"
                    f"{rtl_mark}{get_message(lang, 'period_history', 'symptoms_title')}\n"
                    f"{rtl_mark}• {symptoms}\n\n"
                    f"{rtl_mark}{get_message(lang, 'period_history', 'medicine_title')}\n"
                    f"{rtl_mark}• {medications}\n\n"
                    f"•°•°•°•°•°•°•°•°•°\n\n"
                )

            await update.message.reply_text(formatted_periods, parse_mode="Markdown")
        else:
            await update.message.reply_text(get_message(lang, 'errors', 'fetch_failed'))

def calculate_duration(start_date, end_date, lang):
    """Calculate the duration between start and end date"""
    if not start_date or not end_date:
        return get_message(lang, 'errors', 'unknown_duration')
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    return (end - start).days + 1

