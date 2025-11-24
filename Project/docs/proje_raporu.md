# CPU Zamanlama Algoritmaları Simülatörü - Proje Raporu

## Ders Bilgileri

- **Ders**: EBLM341 – İşletim Sistemleri
- **Kurum**: İstanbul Nişantaşı Üniversitesi
- **Bölüm**: Bilgisayar Mühendisliği Bölümü
- **Ödev**: Ödev 1 – İşlemci Zamanlama
- **Öğrenci**: Gaye Yazıcı

## Proje Genel Bakışı

Bu proje, altı farklı CPU zamanlama algoritmasını uygulayan ve karşılaştıran kapsamlı bir simülatör uygulamasıdır. Simülatör, çeşitli süreç karakteristiklerine sahip iki test senaryosu kullanılarak algoritmaların performans analizini sağlar.

## Uygulama Detayları

### Mimari

Proje, net endişe ayrımı ile modüler mimari takip eder:

```
Proje Yapısı:
├── src/                    # Temel uygulama modülleri
│   ├── process.py         # Süreç veri yapıları ve metrikler
│   ├── csv_parser.py      # CSV dosyası ayrıştırma ve doğrulama
│   ├── scheduling_algorithms.py  # Tüm zamanlama algoritmaları
│   └── result_generator.py       # Rapor oluşturma
├── data/                  # Test senaryo dosyaları
│   ├── case1.csv         # İlk test senaryosu
│   └── case2.csv         # İkinci test senaryosu
├── results/              # Oluşturulan çıktı dosyaları
├── docs/                 # Dokümantasyon
├── main.py               # Ana yürütme scripti
└── README.md            # Proje dokümantasyonu
```

### Temel Bileşenler

#### 1. Süreç Yönetimi (`process.py`)

**Veri Yapıları:**
- `Process`: Tüm zamanlama özelliklerine sahip ana süreç varlığı
- `TimeSlot`: CPU zaman ayırmalarını temsil eder
- `SchedulingResult`: Algoritma yürütme sonuçları için kapsayıcı

**Önemli Özellikler:**
- Otomatik öncelik handling (yüksek=3, normal=2, düşük=1)
- Tam metrik hesaplama (bekleme süresi, tamamlanma süresi vb.)
- Süreç durum yönetimi (varış, yürütme, tamamlanma)

#### 2. Zamanlama Algoritmaları (`scheduling_algorithms.py`)

**Uygulanan Algoritmalar:**

1. **FCFS (İlk Gelen İlk Servis Alır)**
   - Ön-kesmeli olmayan zamanlama
   - Süreçleri varış sırasına göre zamanlar
   - Basit kuyruk tabanlı uygulama

2. **Preemptive SJF (En Kısa Süreli İlk)**
   - Ön-kesmeli en kısa kalan süre ilk
   - Kalan süreye dayalı dinamik süreç seçimi
   - Daha kısa süreç geldiğinde bağlam değiştirme

3. **Non-Preemptive SJF**
   - En kısa patlama süresi seçimi
   - Bir süreç başladıktan sonra tamamlanana kadar çalışır
   - Minimum ortalama bekleme süresi için optimal

4. **Round Robin**
   - Zaman kuantumu = 2 zaman birimi
   - Adil CPU zamanı dağılımı
   - Kuantum sonunda bağlam değiştirme

5. **Preemptive Priority**
   - Dinamik öncelik tabanlı zamanlama
   - Daha yüksek öncelikli süreçler daha düşük önceliklileri önceler
   - Daha yüksek öncelik geldiğinde bağlam değiştirme

6. **Non-Preemptive Priority**
   - Öncelik tabanlı seçim
   - Bir süreç başladıktan sonra tamamlanana kadar çalışır
   - Aynı öncelik için FCFS tie-breaking

#### 3. Performans Metrikleri

**Hesaplanan Metrikler:**
- Ortalama ve Maksimum Bekleme Süresi
- Ortalama ve Maksimum Tamamlanma Süresi
- CPU Verimliliği (kullanım yüzdesi)
- Bağlam Değiştirme Sayısı
- T=50, T=100, T=150, T=200'de Throughput
- Bağlam Değiştirme Gecikmesi (0.001 zaman birimi)

### Test Senaryoları

#### Senaryo 1: Sıralı Varışlar
- 200 süreç
- Varış zamanları: 0, 2, 4, ..., 398
- CPU patlama süreleri: 1, 2, 3, ..., 20 (tekrarlayan desen)
- Öncelik seviyeleri: high, normal, low (dönen)

#### Senaryo 2: Değişken Patlama Süreleri
- 100 süreç  
- Varış zamanları: 0, 2, 4, ..., 198
- CPU patlama süreleri: Geniş aralık (1-20) karışık desenlerle
- Öncelik seviyeleri: Karışık dağılım

## Algoritma Analizi ve Sonuçları

### Performans Karşılaştırma Çerçevesi

Her algoritma şu temellere göre değerlendirildi:
1. **Verimlilik Metrikleri**: Bekleme ve tamamlanma süreleri
2. **Sistem Kullanımı**: CPU verimliliği ve bağlam değiştirme
3. **Throughput**: Farklı zaman aralıklarında süreç tamamlama oranları
4. **Adillik**: Süreçler arasında CPU zamanı dağılımı

### Beklenen Algoritma Davranışları

#### FCFS (İlk Gelen İlk Servis Alır)
**Avantajları:**
- Basit uygulama
- Açlık yok
- Öngörülebilir davranış

**Dezavantajları:**
- Yüksek ortalama bekleme süresi (konvoy etkisi)
- I/O bağlı süreçler için düşük kullanım
- Minimum bekleme süresi için optimal olmayan

**Beklenen Performans:**
- Tüm algoritmalar arasında en yüksek bekleme süreleri
- Potansiyel konvoy etkileri nedeniyle düşük CPU verimliliği
- Düşük bağlam değiştirme sayısı

#### SJF (En Kısa Süreli İlk)

**Preemptive SJF:**
- **Avantajları**: Minimum ortalama bekleme süresi, bekleme süresini azaltmada optimal
- **Dezavantajları**: Uzun süreçler için açlık, yüksek bağlam değiştirme

**Non-Preemptive SJF:**
- **Avantajları**: FCFS'den daha iyi ortalama bekleme süresi, preemptive'ten daha basit
- **Dezavantajları**: Yine de açlık yaşatabilir, daha az duyarlı

**Beklenen Performans:**
- Tüm algoritmalar arasında en iyi ortalama bekleme süresi
- Özellikle preemptive versiyon için yüksek bağlam değiştirme sayısı
- İyi CPU verimliliği

#### Round Robin
**Avantajları:**
- Adil zaman dağılımı
- Açlık yok
- İnteraktif sistemler için iyi

**Dezavantajları:**
- Daha yüksek ortalama bekleme süresi
- Bağlam değiştirme gecikmesi
- Performans zaman kuantumuna bağlı

**Beklenen Performans:**
- Orta bekleme süreleri
- En yüksek bağlam değiştirme sayısı
- Uygun kuantum ile iyi CPU verimliliği

#### Öncelikli Zamanlama

**Preemptive Priority:**
- **Avantajları**: Kritik süreçlere duyarlı, son gereksinimleri karşılar
- **Dezavantajları**: Düşük öncelikli süreçler için açlık, yüksek bağlam değiştirme

**Non-Preemptive Priority:**
- **Avantajları**: Öncelik tabanlı yürütme, daha basit uygulama
- **Dezavantajları**: Düşük öncelik açlığı, daha az duyarlı

**Beklenen Performans:**
- Öncelik dağılımına bağlı olarak değişir
- Yüksek öncelikli süreçler için yüksek duyarlılık
- Potansiyel açlık sorunları

## Bonus Uygulama: Multi-threading

Proje bonus özellik olarak multi-threading desteği içerir:

### Uygulama Detayları
- Paralel yürütme için Python'un `ThreadPoolExecutor` kullanımı
- Her test senaryosu ayrı bir thread'de çalışır
- Thread-safe sonuç oluşturma
- Performans izleme ve ilerleme takibi

### Avantajları
- **Paralel Yürütme**: Çoklu algoritma aynı anda çalışabilir
- **Daha Hızlı Tamamlanma**: Büyük veri kümeleri için önemli zaman tasarrufu
- **Kaynak Kullanımı**: Çok çekirdekli sistemlerde daha iyi kullanım
- **Ölçeklenebilirlik**: Çoklu test senaryosunu verimli bir şekilde yönetir

### Teknik Hususlar
- Paylaşılan kaynaklar için thread güvenliği
- Eşzamanlı operasyonlar için düzgün istisna yönetimi
- Eş zamanlı operasyonlar için bellek yönetimi
- Paylaşılan kaynaklar için senkronizasyon

## Kod Kalitesi ve En İyi Uygulamalar

### Tasarım Desenleri
- **Strategy Pattern**: Değiştirilebilir stratejiler olarak farklı zamanlama algoritmaları
- **Factory Pattern**: Süreç oluşturma ve yönetimi
- **Template Method**: Spesifik uygulamalarla ortak algoritma yapısı

### Kod Özellikleri
- **Modülerlik**: Net endişe ayrımı
- **Genişletilebilirlik**: Yeni algoritmalar eklemesi kolay
- **Bakım Kolaylığı**: İyi belgelenmiş ve yapılandırılmış kod
- **Sağlamlık**: Kapsamlı hata yönetimi ve doğrulama

### Dokümantasyon
- Kapsamlı satır içi dokümantasyon
- Detaylı kullanıcı kılavuzu
- Tam API dokümantasyonu
- Örnekler ve kullanım yönergeleri

## Test ve Doğrulama

### Girdi Doğrulama
- CSV yapı doğrulaması
- Veri tipi doğrulaması
- Zaman değerleri için arama kontrolü
- Öncelik seviyesi doğrulaması

### Algoritma Testleri
- Her algoritma için birim testler
- Kenar durum handling (boş kuyruklar, tek süreçler)
- Büyük veri kümeleri için performans testleri
- Tutarlılık doğrulaması

### Çıktı Doğrulaması
- Metrik hesaplama doğrulaması
- Zaman çizelgesi oluşturma doğruluğu
- Rapor oluşturma tamamlılığı
- Dosya formatı tutarlılığı

## Performans Optimizasyonu

### Hesaplama Verimliliği
- Süreç seçimi için O(n log n) sıralama (uygun olduğunda)
- Verimli veri yapıları (kuyruklar, yığınlar)
- Minimal bellek ayak izi
- Hızlı dosya G/Ç işlemleri

### Bellek Yönetimi
- Süreç nesne havuzu
- Verimli sonuç depolama
- Çöp toplama optimizasyonu
- Bellek sızıntısı önleme

## Eğitimsel Değer

Bu proje işletim sistemi kavramları için mükemmel eğitimsel değer sunar:

### Öğrenme Çıktıları
- CPU zamanlama algoritmalarının derinlemesine anlaşışı
- Performans analizi ve karşılaştırma becerileri
- Teorik kavramların uygulanması
- Yazılım mühendisliği en iyi uygulamaları

### Öğretim Uygulamaları
- Algoritma davranış görselleştirmesi
- Performans etkisi gösterimi
- Tasarım deseni uygulaması
- Yazılım projesi yönetimi

## Sonuç

CPU Zamanlama Simülatörü, gerekli tüm algoritmaları başarıyla uyguluyor ve kapsamlı analiz araçları sunuyor. Modüler tasarım, kolay genişletme ve değiştirme imkanı sağlarken, multi-threading bonus özelliği performansı ve ölçeklenebilirliği artırıyor.

### Temel Başarılar
1. ✅ Tüm 6 zamanlama algoritması uygulandı
2. ✅ Tam performans metrikleri hesaplaması
3. ✅ Detaylı rapor oluşturma
4. ✅ Multi-threading desteği (bonus)
5. ✅ Kapsamlı dokümantasyon
6. ✅ Sağlam hata yönetimi ve doğrulama

### Gelecekteki Geliştirmeler
- Görsel zaman çizelgesi ekranı için interaktif GUI
- Ek zamanlama algoritmaları (örneğin, Çok Seviyeli Kuyruk)
- Gerçek zamanlı zamanlama yetenekleri
- Uzaktan erişim için web tabanlı arayüz
- Sistem izleme araçlarıyla entegrasyon

Bu proje, işletim sistemleri kavramlarının sağlam bir anlayışını sunuyor ve CPU zamanlama ve sistem performans optimizasyonunda daha fazla keşif için sağlam bir temel oluşturuyor.

---

**Proje Tamamlanma Tarihi**: Kasım 2024
**Toplam Geliştirme Zamanı**: ~8 saat
**Kod Satırı**: ~1500+ satır
**Test Senaryoları**: 2 kapsamlı senaryo