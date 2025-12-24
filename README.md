# 🚦 YOLOv8 ile Nesne Tespiti (Dur – Yaya Geçidi)

Bu projede, **YOLOv8n nesne tespit modeli** kullanılarak trafik levhalarının görüntüler üzerinde tespit edilmesi gerçekleştirilmiştir.  
Model, gerçek ortamdan elde edilen ve manuel olarak etiketlenen trafik levhası görüntüleri ile eğitilmiştir.

---

## 📌 Proje Amacı

- Trafik levhalarını görüntü üzerinde **bounding box** ile tespit etmek
- `dur` ve `yaya_gecidi` sınıflarını ayırt edebilmek
- YOLOv8 kullanarak uçtan uca bir nesne tespit süreci oluşturmak
- Eğitilen modeli bir GUI uygulamasında kullanmak

---

## 📂 Proje İçeriği

- Veri seti hazırlama
- Görüntü etiketleme
- YOLOv8 model eğitimi
- Performans değerlendirme (mAP, loss)
- Eğitilmiş model (`best.pt`)
- PyQt5 tabanlı GUI uygulaması

---

## 🗂️ Veri Seti Bilgileri

### Sınıflar
- `dur`
- `yaya_gecidi`

### Toplam Görsel Sayısı
- **Toplam:** 220
  - Dur: 111
  - Yaya Geçidi: 109

### Train / Validation Bölünmesi
- **Train (170):**
  - 85 dur
  - 85 yaya
- **Validation (50):**
  - 26 dur
  - 24 yaya

> Train ve validation setleri **sınıf dengesi korunarak** oluşturulmuştur.

---

## 📸 Görsel Kaynağı

-Kendi çektiğim gerçek trafik levhası görüntüleri
- Görseller Google Maps üzerinden farklı açılardan görüntüler
- Farklı mesafe, açı ve ışık koşulları içermektedir
- Etiketleme sırasında **ham (kırpılmamış)** görseller kullanılmıştır

---

## 🏷️ Etiketleme Süreci

- Etiketleme işlemi **makesense.ai** web aracı kullanılarak yapılmıştır
- Her trafik levhası için bounding box çizilmiştir
- Etiketler **YOLO formatında (.txt)** oluşturulmuştur

---

## 📁 YOLOv8 Klasör Yapısı

```text
dataset/
├── images/
│   ├── train/
│   └── val/
├── labels/
│   ├── train/
│   └── val/
└── data.yaml
```
---

## 🖥️ PyQt5 Tabanlı Nesne Tespit Arayüzü

Eğitilen YOLOv8 modeli (`best.pt`) kullanılarak, trafik levhalarını tespit edebilen **PyQt5 tabanlı bir masaüstü uygulaması** geliştirilmiştir.

Bu arayüz sayesinde model, yalnızca notebook ortamında değil, **gerçek bir kullanıcı arayüzü üzerinden** test edilebilmektedir.

---

### ⚙️ Uygulama Özellikleri

- YOLOv8 modeli (`best.pt`) uygulama başlatıldığında yüklenir
- Kullanıcı bilgisayarından:
  - Görsel seçebilir
  - Video dosyası seçebilir
  - Webcam üzerinden canlı tespit yapabilir
- Orijinal görüntü ve tespit sonucu **yan yana** gösterilir
- Tespit edilen nesneler:
  - Bounding box ile işaretlenir
  - Sınıf isimleri görüntü üzerine yazdırılır
- Tespit edilen sınıflar ve adetleri metin alanında listelenir
- İşlenmiş (etiketli) görüntü diske kaydedilebilir

---

### 🧩 Arayüz Yapısı

- **Sol panel:** Orijinal görüntü / video / kamera akışı
- **Sağ panel:** YOLOv8 tarafından etiketlenmiş çıktı
- **Alt bölüm:**
  - Resim seçme
  - Tespit işlemi başlatma
  - Sonucu kaydetme
  - Video seçme
  - Webcam başlatma / durdurma

---

### 🧠 Model Entegrasyonu

- YOLOv8 modeli `ultralytics` kütüphanesi kullanılarak yüklenmiştir
- Görsel tespiti için `model(image)` yöntemi kullanılmıştır
- Video ve kamera işlemlerinde:
  - `model.track()` fonksiyonu tercih edilmiştir
- Bounding box çizimleri YOLOv8’in kendi `plot()` fonksiyonu ile alınmıştır

---

### ▶️ Uygulamanın Çalıştırılması

Uygulama aşağıdaki komut ile çalıştırılabilir:

```bash
python main.py
```
---
## 📌 Notlar

- Tüm kodlar açıklamalı markdown hücreleri ile desteklenmiştir.
- Notebook adım adım ilerleyecek şekilde düzenlenmiştir.
- Okunabilirlik ve anlaşılabilirlik ön planda tutulmuştur.

---

## 👤 Öğrenci Bilgileri

- **Ad:** Yusuf  
- **Soyad:** Tunç  
- **Okul No:** 2012721024  

---
