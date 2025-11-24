# CPU Zamanlama Algoritmaları Simülatörü

## Özellikler

### Uygulanan Algoritmalar
- FCFS (İlk Gelen İlk Servis Alır) - Ön-kesmeli olmayan zamanlama
- Preemptive SJF - En kısa kalan süre ilk
- Non-Preemptive SJF - En kısa patlama süresi seçimi
- Round Robin - Zaman kuantumu = 2 zaman birimi
- Preemptive Priority - Dinamik öncelikli zamanlama
- Non-Preemptive Priority - Öncelik tabanlı seçim

### Performans Metrikleri
- Maksimum ve Ortalama Bekleme Süresi
- Maksimum ve Ortalama Tamamlanma Süresi
- CPU Verimliliği ve Kullanımı
- Bağlam Değiştirme Sayısı ve Gecikmesi
- Throughput Analizi (T=50, 100, 150, 200)
- Detaylı Zaman Tabloları


- Multi-threading Desteği - Daha hızlı sonuçlar için paralel çalışma
- Kapsamlı Raporlama - Bireysel ve karşılaştırmalı raporlar
- Esnek Girdi - Özel CSV dosyaları desteği
- İnteraktif Arayüz - Komut satırı ve interaktif modlar

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

## Girdi Formatı

CSV dosyaları şu sütunları içermelidir:
```csv
Process_ID,Arrival_Time,CPU_Burst_Time,Priority
P001,0,4,high
P002,2,7,normal
```

## Oluşturulan Raporlar

Her algoritma ve senaryo için:
- Bireysel Sonuçlar: Performans metrikleri ve zaman tabloları
- Karşılaştırma Raporları: Algoritma sıralamaları ve analizi
- Genel Özet: Tüm metriklerde en iyi performans gösterenler

## Dokümantasyon

-  [Kullanıcı Kılavuzu](docs/user_manual.md) - Tam kullanım talimatları
-  [Proje Raporu](docs/project_report.md) - Teknik uygulama detayları