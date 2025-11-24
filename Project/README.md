# CPU Zamanlama Algoritmaları Simülatörü

İstanbul Nişantaşı Üniversitesi EBLM341 İşletim Sistemleri dersi için kapsamlı bir Python CPU zamanlama algoritmaları uygulaması.

## Özellikler

### Uygulanan Algoritmalar
- ✅ **FCFS (İlk Gelen İlk Servis Alır)** - Ön-kesmeli olmayan zamanlama
- ✅ **Preemptive SJF** - En kısa kalan süre ilk
- ✅ **Non-Preemptive SJF** - En kısa patlama süresi seçimi
- ✅ **Round Robin** - Zaman kuantumu = 2 zaman birimi
- ✅ **Preemptive Priority** - Dinamik öncelikli zamanlama
- ✅ **Non-Preemptive Priority** - Öncelik tabanlı seçim

### Performans Metrikleri
- Maksimum ve Ortalama Bekleme Süresi
- Maksimum ve Ortalama Tamamlanma Süresi
- CPU Verimliliği ve Kullanımı
- Bağlam Değiştirme Sayısı ve Gecikmesi
- Throughput Analizi (T=50, 100, 150, 200)
- Detaylı Zaman Tabloları

### Bonus Özellikler
- ✅ **Multi-threading Desteği** - Daha hızlı sonuçlar için paralel çalışma
- ✅ **Kapsamlı Raporlama** - Bireysel ve karşılaştırmalı raporlar
- ✅ **Esnek Girdi** - Özel CSV dosyaları desteği
- ✅ **İnteraktif Arayüz** - Komut satırı ve interaktif modlar

## Hızlı Başlangıç

### Temel Kullanım
```bash
# Her iki test senaryosunu çalıştır
python3 main.py --both

# Multi-threading ile daha hızlı çalıştır
python3 main.py --both --threading

# Özel dosya çalıştır
python3 main.py --file benim_sureclerim.csv
```

### İnteraktif Mod
```bash
python3 main.py
```

## Proje Yapısı

```
Project/
├── src/                    # Ana modüller
│   ├── process.py         # Veri yapıları
│   ├── csv_parser.py      # Girdi ayrıştırma
│   ├── scheduling_algorithms.py  # Tüm algoritmalar
│   └── result_generator.py       # Rapor oluşturma
├── data/                  # Test senaryoları
│   ├── case1.csv         # 200 süreç, sıralı
│   └── case2.csv         # 100 süreç, değişken
├── results/              # Oluşturulan raporlar
├── docs/                 # Dokümantasyon
│   ├── user_manual.md    # Tam kullanım kılavuzu
│   └── project_report.md # Teknik uygulama detayları
├── main.py               # Ana çalıştırma scripti
└── README.md            # Bu dosya
```

## Gereksinimler

- Python 3.7+
- Harici bağımlılık yok (sadece standart kütüphane)
- Sonuçlar için 50MB disk alanı

## Girdi Formatı

CSV dosyaları şu sütunları içermelidir:
```csv
Process_ID,Arrival_Time,CPU_Burst_Time,Priority
P001,0,4,high
P002,2,7,normal
```

## Oluşturulan Raporlar

Her algoritma ve senaryo için:
- **Bireysel Sonuçlar**: Performans metrikleri ve zaman tabloları
- **Karşılaştırma Raporları**: Algoritma sıralamaları ve analizi
- **Genel Özet**: Tüm metriklerde en iyi performans gösterenler

## Dokümantasyon

- 📖 **[Kullanıcı Kılavuzu](docs/user_manual.md)** - Tam kullanım talimatları
- 📊 **[Proje Raporu](docs/project_report.md)** - Teknik uygulama detayları

## Akademik Bilgiler

- **Ders**: EBLM341 – İşletim Sistemleri
- **Kurum**: İstanbul Nişantaşı Üniversitesi
- **Ödev**: CPU Zamanlama Algoritmaları (Ödev 1)

## Örnek Çıktı

```
CPU ZAMANLAMA ALGORİTMALARI - GENEL ÖZET RAPORU
================================================================================

SENARYO: CASE2
----------------------------------------
En iyi performans gösteren algoritmalar:
  En Düşük Ortalama Bekleme Süresi: Preemptive SJF (267.869)
  En Düşük Ortalama Tamamlanma Süresi: Preemptive SJF (278.369)
  En Yüksek CPU Verimliliği: Preemptive Priority (100.00%)
  T=100'de En Yüksek Throughput: Preemptive SJF (20 süreç)

SENARYO: CASE1
----------------------------------------
En iyi performans gösteren algoritmalar:
  En Düşük Ortalama Bekleme Süresi: Preemptive SJF (537.016)
  En Düşük Ortalama Tamamlanma Süresi: Preemptive SJF (547.516)
  En Yüksek CPU Verimliliği: Preemptive Priority (99.95%)
  T=100'de En Yüksek Throughput: Preemptive SJF (22 süreç)
```

## Performans Analizi

Simülatör kapsamlı analiz sunarak gösteriyor:
- **SJF algoritmaları** optimal bekleme süreleri elde eder
- **Öncelikli zamanlama** en yüksek CPU verimliliği sağlar
- **Round Robin** adil zaman dağılımı sunar
- **FCFS** uzun süreçlerde konvoy etkisi gösterir

## Lisans

Bu proje İşletim Sistemi dersi kapsamında eğitim amaçlıdır.

---

**Toplam Uygulama**: ~1500+ satır Python kodu
**Geliştirme Süresi**: ~8 saat
**Test Kapsamı**: 2 kapsamlı senaryo (toplam 300 süreç)# EBLM341-ODEV1-GAYEYAZICI
# EBLM341-ODEV1-GAYEYAZICI
# EBLM341-ODEV1-GAYEYAZICI
