# SubdomainFinder

Basit ve hızlı bir **Subdomain Finder** aracı. Wordlist ile brute-force yapar, DNS resolve eder ve isteğe bağlı HTTP probe gerçekleştirir.

> ⚠️ **Yasal Uyarı**: Bu aracı sadece **izin verilen** hedeflerde kullanın. Tüm sorumluluk kullanıcıya aittir.

## Özellikler
- Wordlist'den subdomain denemesi
- DNS resolve (IP'leri opsiyonel gösterme)
- HTTP/HTTPS probe (alive kontrolü)
- Çok iş parçacıklı (threading) hızlı tarama
- JSON veya TXT çıktı kaydı
- Sıfır ek bağımlılık (sadece `requests`)

## Kurulum
```bash
git clone https://github.com/YOUR_USERNAME/SubdomainFinder.git
cd SubdomainFinder
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Kullanım
```bash
# Temel kullanım
python subfinder.py -d example.com -w wordlists/subdomains_small.txt

# Daha detaylı
python subfinder.py -d example.com -w subs.txt -t 50 --timeout 3 --show-ips -o results.json

# DNS'i atla, sadece HTTP probe
python subfinder.py -d example.com -w subs.txt --skip-dns

# HTTP probe'u atla, sadece DNS
python subfinder.py -d example.com -w subs.txt --skip-http
```

Örnek çıktı:
```
[+] api.example.com 203.0.113.10
[+] dev.example.com 203.0.113.20

Done. Found 2 subdomains in 3.4s.
Saved results to: results.json
```

## Wordlist
Projedeki küçük bir başlangıç wordlist’i için: `wordlists/subdomains_small.txt`

Daha büyük listeler için SecLists kullanabilirsiniz:
- https://github.com/danielmiessler/SecLists (DNS/subdomains listeleri)

## Yol Haritası
- AsyncIO ile çok daha hızlı sürüm
- Wildcard DNS tespiti ve eleme
- `crt.sh` ve `hackertarget` gibi kaynaklardan pasif subdomain toplama
- HTML raporu

## Lisans
MIT