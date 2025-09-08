# crypto_dashboard

Crypto Dashboard V2

Crypto Dashboard V2, kullanıcıların kripto para birimlerinin anlık fiyatlarını, piyasa verilerini ve ticaret hacmini görsel olarak takip edebileceği modern bir web uygulamasıdır. Bu proje, Python, Django ve Docker kullanılarak geliştirilmiştir ve kullanıcı dostu bir arayüz sunmaktadır.

Özellikler

Anlık Kripto Para Verileri: Kullanıcılar, CoinGecko API'si aracılığıyla kripto para birimlerinin güncel fiyatlarını ve piyasa verilerini görüntüleyebilirler.

Veritabanı Entegrasyonu: SQLite veritabanı kullanılarak, kullanıcıların tercihleri ve geçmiş verileri saklanabilir.

Bot Entegrasyonu: bot.py dosyası, belirli aralıklarla veri çekme ve işlem yapma gibi otomatik görevleri yerine getirebilir.

Docker Desteği: Proje, Docker ile konteynerize edilmiştir, böylece uygulamanın kurulumu ve dağıtımı kolaylaştırılmıştır.

Teknolojiler

Backend: Python, Django

Veritabanı: SQLite

API Entegrasyonu: CoinGecko API

Otomasyon: Python betikleri

Konteynerizasyon: Docker

Kurulum
Gereksinimler

Python 3.8 veya üzeri

Docker (isteğe bağlı)

Adımlar

Depoyu klonlayın:

git clone https://github.com/mertcanytr/crypto_dashboardv2.git

cd crypto_dashboardv2


Gerekli Python paketlerini yükleyin:

pip install -r requirements.txt


Veritabanını hazırlayın:

python manage.py migrate


Uygulamayı başlatın:

python manage.py runserver


Alternatif olarak, Docker kullanarak uygulamayı çalıştırabilirsiniz:

docker build -t crypto_dashboard .
docker run -p 8000:8000 crypto_dashboard


Uygulama, http://localhost:8000
 adresinde çalışacaktır.

