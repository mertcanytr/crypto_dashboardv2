import logging
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Telegram Bot API token'ınızı buraya girin
TELEGRAM_BOT_TOKEN = "API_KEY"

# Django uygulamanızın çalıştığı URL
# Eğer localde çalışıyorsa http://127.0.0.1:8000/
DJANGO_API_URL = "http://127.0.0.1:8000" 

# Log ayarları
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

# /start komutu için fonksiyon
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Merhaba! Kripto verilerini almak için komutları kullanın.\n"
        "Örn: /wavg BTCUSDT 1 BUY\n"
        "Örn: /market BTCUSDT"
    )

# /wavg komutu için fonksiyon
async def get_wavg(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        # Komut argümanlarını ayrıştırma
        if len(context.args) != 3:
            await update.message.reply_text("Kullanım: /wavg <symbol> <quantity> <side>\n"
                                            "Örn: /wavg BTCUSDT 1 BUY")
            return
        
        symbol, quantity, side = context.args
        
        # Django API'nize GET isteği gönderme
        api_endpoint = f"{DJANGO_API_URL}/api/wavg/{symbol}/{quantity}/{side}/"
        response = requests.get(api_endpoint)
        response.raise_for_status() # Hata durumunda istisna fırlatır
        
        data = response.json()
        
        if "error" in data:
            await update.message.reply_text(f"Hata: {data['error']}")
        else:
            avg_price = data.get("average_price")
            message = f"**{symbol} Ağırlıklı Ortalama Fiyat**\n" \
                      f"İşlem Miktarı: {quantity}\n" \
                      f"İşlem Yönü: {side}\n" \
                      f"Ortalama Fiyat: {avg_price}"
            await update.message.reply_text(message)
            
    except requests.exceptions.RequestException as e:
        await update.message.reply_text(f"API bağlantı hatası: {e}")
    except Exception as e:
        await update.message.reply_text(f"Bir hata oluştu: {e}")

# /market komutu için fonksiyon
async def get_market(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        # Komut argümanlarını ayrıştırma
        if len(context.args) != 1:
            await update.message.reply_text("Kullanım: /market <symbol>\n"
                                            "Örn: /market BTCUSDT")
            return
            
        symbol = context.args[0]
        
        # Django API'nize GET isteği gönderme
        api_endpoint = f"{DJANGO_API_URL}/api/market/{symbol}/"
        response = requests.get(api_endpoint)
        response.raise_for_status()
        
        data = response.json()
        
        if "error" in data:
            await update.message.reply_text(f"Hata: {data['error']}")
        else:
            oi = data.get("open_interest")
            ls_ratio = data.get("long_short_ratio")
            fr = data.get("funding_rate")
            timestamp = data.get("timestamp")
            
            message = f"**{symbol} Piyasa Verileri**\n" \
                      f"Open Interest: {oi:,.2f}\n" \
                      f"Long/Short Ratio: {ls_ratio:.4f}\n" \
                      f"Funding Rate: {(fr * 100):.4f} %"
            await update.message.reply_text(message)
            
    except requests.exceptions.RequestException as e:
        await update.message.reply_text(f"API bağlantı hatası: {e}")
    except Exception as e:
        await update.message.reply_text(f"Bir hata oluştu: {e}")

def main() -> None:
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    
    # Komut işleyicilerini ekleme
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("wavg", get_wavg))
    application.add_handler(CommandHandler("market", get_market))
    
    # Botu çalıştırma
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
