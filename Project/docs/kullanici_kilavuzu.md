# CPU Zamanlama Simülatörü - Kullanıcı Kılavuzu

## Genel Bakış

CPU Zamanlama Simülatörü, altı farklı CPU zamanlama algoritmasını uygulayan ve karşılaştıran kapsamlı bir Python uygulamasıdır. Bu simülatör, öğrencilerin ve geliştiricilerin farklı zamanlama algoritmalarının çeşitli koşullar altında nasıl performans gösterdiğini anlamasına yardımcı olmak için tasarlanmıştır.

## Desteklenen Algoritmalar

1. FCFS (İlk Gelen İlk Servis Alır) - Süreçleri geldikleri sırayla zamanlayan ön-kesmeli olmayan algoritma
2. Preemptive SJF (En Kısa Süreli İlk) - En kısa kalan süreye sahip süreci önceliklendiren ön-kesmeli algoritma
3. Non-Preemptive SJF - Tüm gelen süreçler arasında en kısa patlama süresine sahip süreci seçen algoritma
4. Round Robin - Her sürece sabit bir zaman kuantumu (varsayılan: 2 zaman birimi) ayıran algoritma
5. Preemptive Priority - En yüksek önceliğe sahip süreci dinamik olarak zamanlayan algoritma
6. Non-Preemptive Priority - Gelen süreçler arasından en yüksek önceliğe sahip süreci seçen algoritma

## Sistem Gereksinimleri

- Python 3.7 veya üzeri
- İşletim Sistemi: Windows, macOS veya Linux
- Bellek: Minimum 512MB RAM
- Disk Alanı: Sonuçlar ve veri dosyaları için 50MB

## Kurulum

### Ön Koşullar

Sisteminizde Python'un kurulu olduğundan emin olun. Python sürümünü kontrol edebilirsiniz:

```bash
python --version
```

veya

```bash
python3 --version
```

### Kurulum

1. Projeyi yerel makinenize klonlayın veya indirin
2. Proje dizinine gidin
3. Proje sadece standart Python kütüphanelerini kullandığı için ek kurulum gerekmez

## Kullanım

### Temel Kullanım

#### Her İki Test Senaryosunu Çalıştırma

Simülatörü sağlanan iki test senaryosu ile çalıştırmak için:

```bash
python main.py --both
```

#### Multi-threading Kullanımı (Bonus Özellik)

Daha hızlı yürütme için multi-threading desteği ile:

```bash
python main.py --both --threading
```

#### Özel CSV Dosyası Çalıştırma

Kendi süreç verilerinizle simülatörü çalıştırmak için:

```bash
python main.py --file dosya_yolu/surecler.csv
```
### İnteraktif Mod

Hiçbir argüman olmadan `python main.py` çalıştırırsanız, program interaktif moda geçer ve seçenekler üzerinden size rehberlik eder.

## Girdi Dosyası Formatı

Simülatör, CSV dosyalarını aşağıdaki sütunlarla bekler:

```
Process_ID,Arrival_Time,CPU_Burst_Time,Priority
P001,0,4,high
P002,2,7,normal
P003,4,10,low
```

### Sütun Açıklamaları

-Process_ID: Her sürecin benzersiz tanımlayıcısı (örneğin, P001, P002)
- Arrival_Time: Sürecin hazır kuyruğa geldiği zaman (sayısal)
- CPU_Burst_Time: Sürecin gerektirdiği CPU zamanı (sayısal)
- Priority: Sürecin önceliği (high, normal, low)

### Öncelik Seviyeleri

- high: En yüksek öncelik (değer = 3)
- normal: Orta öncelik (değer = 2)
- low: En düşük öncelik (değer = 1)

## Çıktı Dosyaları

Simülatör `results/` dizininde çeşitli çıktı dosyaları oluşturur:

### Bireysel Algoritma Sonuçları

Her algoritma, aşağıdaki adlandırma kuralına sahip detaylı bir sonuç dosyası oluşturur:
```
{senaryo_adı}_{algoritma_adı}_sonuclari.txt
```

Örnek: `case1_fcfs_sonuclari.txt`

Bu dosyalar içerir:
- Performans Metrikleri: Ortalama ve maksimum bekleme/tamamlanma süreleri
- Throughput Metrikleri: Farklı zaman aralıklarında tamamlanan süreç sayıları
- Zaman Tablosu: Detaylı yürütme zaman çizelgesi
- Özet İstatistikler Genel performans değerlendirmesi

### Karşılaştırma Raporları

#### Senaryo Özel Karşılaştırma
```
{senaryo_adi}_karsilastirma_raporu.txt
```

İçerir:
- Tüm algoritmaların karşılaştırma tablosu
- Metriklere göre algoritma sıralamaları
- Performans analizi

#### Genel Özet
```
genel_ozet.txt
```

İçerir:
- Her senaryo için en iyi performans gösteren algoritmalar
- Genel özet ve tavsiyeler

### Örnek Çıktı Yapısı

```
results/
├── case1_fcfs_sonuclari.txt
├── case1_preemptive_sjf_sonuclari.txt
├── case1_non_preemptive_sjf_sonuclari.txt
├── case1_round_robin_sonuclari.txt
├── case1_preemptive_priority_sonuclari.txt
├── case1_non_preemptive_priority_sonuclari.txt
├── case1_karsilastirma_raporu.txt
├── case2_*.txt (benzer yapı)
└── genel_ozet.txt
```

## Performans Metriklerinin Açıklaması

### Bekleme Süresi
Bir sürecin yürütülmeye başlamadan önce hazır kuyrukta geçirdiği süre.

### Tamamlanma Süresi (Turnaround Time)
Bir sürecin varış zamanından tamamlanma zamanına kadar geçen toplam süre.

### CPU Verimliliği
CPU'nun süreçleri yürütmeyle meşgul olduğu zaman yüzdesi (boş zaman ve bağlam değişiklikleri hariç).

### Throughput
Belirli zaman aralıklarında (T=50, T=100, T=150, T=200) tamamlanan süreç sayısı.

### Bağlam Değiştirmeleri
CPU'nun bir sürec diğerine geçiş yapma sayısı.

## Sorun Giderme

### Yaygın Sorunlar

1. Dosya Bulunamadı Hatası
   ```
   Hata: CSV dosyası bulunamadı: data/case1.csv
   ```
   Çözüm: CSV dosyalarının `data/` dizininde doğru isimlerle var olduğundan emin olun.

2. Geçersiz CSV Yapısı
   ```
   Hata: CSV'de eksik required sütun: Process_ID
   ```
   Çözüm: CSV dosyanızın tüm gerekli sütunları doğru isimlerle içerdiğini doğrulayın.

3.İzin Reddedildi
   Çözüm: Proje dizinine ve `results/` klasörüne yazma izinlerinizin olduğundan emin olun.

4. Bellek Sorunları
   Çözüm: Çok büyük veri kümeleri için bir seferde tek algoritma çalıştırmayı veya sistem belleğini artırmayı düşünün.

### Doğrulama

Simülatör dahili doğrulama içerir:
- CSV yapısı doğrulaması
- Veri tipi doğrulaması
- Sayısal değerler için arama kontrolü
- Öncelik seviyesi doğrulaması

## Gelişmiş Kullanım

### Özel Bağlam Değiştirme Süresi

Bağlam değiştirme gecikmesini değiştirmek için:

```bash
python main.py --both --context-switch 0.005
```

### Büyük Veri Kümelerini İşleme

Çok sayıda sürec içeren veri kümeleri için:
- `--threading` seçeneğini paralel yürütme için kullanın
- Sistem kaynaklarını izleyin
- Tek seferde tek bir algoritma çalıştırmayı düşünün

### Simülatörü Genişletme

Simülatör genişletilebilir şekilde tasarlanmıştır:
- `src/scheduling_algorithms.py` dosyasını değiştirerek yeni algoritmalar ekleyin
- `src/process.py` dosyasında performans metriklerini değiştirin
- `src/result_generator.py` dosyasında çıktı formatlarını özelleştirin

## Örnekler

### Örnek 1: Sağlanan Verilerle Hızlı Test

```bash
# Varsayılan ayarlarla her iki test senaryosunu çalıştır
python main.py --both

# Sonuçları kontrol et
ls results/
```

### Örnek 2: Özel Süreç Dosyası

`benim_sureclerim.csv` oluştur:
```csv
Process_ID,Arrival_Time,CPU_Burst_Time,Priority
PROG1,0,5,high
PROG2,1,3,normal
PROG3,3,8,low
```

Simülasyonu çalıştır:
```bash
python main.py --file benim_sureclerim.csv
```

### Örnek 3: Performans Karşılaştırması

```bash
# Daha hızlı yürütme için multi-threading ile çalıştır
python main.py --both --threading

# Karşılaştırma raporunu görüntüle
cat results/case1_karsilastirma_raporu.txt
```

## Destek

Sorunlar veya sorular için:
1. Sorun giderme adımlarını kontrol edin
2. Girdi dosyası formatını doğrulayın
3. Sistem gereksinimlerinin karşılandığından emin olun
4. Oluşturulan hata mesajlarını dikkatle inceleyin

## Akademik Kullanım

Bu simülatör eğitim amaçlı tasarlanmıştır ve şu konular;
- Zamanlama algoritması davranış görselleştirmesi
- Performans analizi ve karşılaştırma çalışmaları
- Teorik kavramların uygulanması
- Yazılım mühendisliği en iyi uygulamaları

---

