# Temel Python imajını kullan
FROM python:3.13-slim

# Çalışma dizinini ayarla
WORKDIR /app

# Gereksinimler dosyasını çalışma dizinine kopyala
COPY requirements.txt .

# Python bağımlılıklarını yükle
RUN pip install --no-cache-dir -r requirements.txt

# Proje dosyalarını kopyala
COPY . .

# Projenizin kullandığı portu dışarıya aç
# Django server'ı 8000 portunda çalışıyor
EXPOSE 8000

# Django sunucusunu çalıştıracak komut
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]