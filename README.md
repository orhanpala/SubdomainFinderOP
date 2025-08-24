# SubdomainFinder ORHAN PALA
# SubdomainFinderOP

Basit ve hızlı bir **Subdomain Finder** aracı.  
Wordlist ile brute-force yapar, DNS resolve eder ve isteğe bağlı HTTP probe gerçekleştirir.  

---

## 🚀 Özellikler
- Wordlist üzerinden subdomain brute-force
- DNS resolve (opsiyonel IP gösterimi)
- HTTP/HTTPS probe (alive kontrolü)
- Çok iş parçacıklı (threading) hızlı tarama
- JSON veya TXT çıktı kaydı
- Minimum bağımlılık (sadece `requests` kütüphanesi)

----------------------------------------------------------------------------------

## 🔧 Kurulum

```bash
git clone https://github.com/orhanpala/SubdomainFinderOP.git
cd SubdomainFinderOP

# Sanal ortam oluşturma (opsiyonel)
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux / macOS
source .venv/bin/activate

# Bağımlılıkları yükle
pip install -r requirements.txt

----------------------------------------------------------------------------------
# Temel kullanım
python subfinder.py -d example.com -w wordlists/subdomains_small.txt

# Daha detaylı kullanım
python subfinder.py -d example.com -w subs.txt -t 50 --timeout 3 --show-ips -o results.json

# DNS'i atla, sadece HTTP probe
python subfinder.py -d example.com -w subs.txt --skip-dns

# HTTP probe'u atla, sadece DNS
python subfinder.py -d example.com -w subs.txt --skip-http
-----------------------------------------------------------------------------



## Lisans
MIT
