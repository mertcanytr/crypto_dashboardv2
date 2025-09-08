# Temel Python imajını kullan
FROM python:3.13-slim

# Çalışma dizinini ayarla
WORKDIR /app

# Gereksinimler dosyasını çalışma dizinine kopyala
COPY requirements.txt ./

# Python bağımlılıklarını yükle
RUN pip install --no-cache-dir -r requirements.txt

# Proje dosyalarını kopyala
COPY . ./

# Projenizin kullandığı portu dışarıya aç
# Django uygulaması, heroku'da dinamik portu kullanacaktır
EXPOSE 8000

# Django sunucusunu Gunicorn ile çalıştıracak komut
CMD ["gunicorn", "crypto_backend.wsgi:application", "--bind", "0.0.0.0:$PORT"]