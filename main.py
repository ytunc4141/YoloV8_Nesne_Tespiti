import os

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
os.environ["MKL_THREADING_LAYER"] = "GNU"

import sys
import cv2

from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, QFileDialog, 
                             QTextEdit, QMessageBox, QGroupBox)
from PyQt5.QtGui import QPixmap, QImage, QFont
from PyQt5.QtCore import Qt, QTimer
from ultralytics import YOLO

class NesneTespitUygulamasi(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("YOLOv8 Nesne Tespiti - Dur ve Yaya Geçidi")
        self.setGeometry(100, 100, 1200, 700)
        self.model_yolu = "best.pt"

        self.cap = None 
        self.timer = QTimer()
        self.timer.timeout.connect(self.kare_guncelle)
        
        self.secilen_resim_yolu = None
        self.islenmis_goruntu = None
        
        self.initUI()
        
        self.modeli_yukle()

    def modeli_yukle(self):
        """YOLOv8 modelini yükler."""
        try:
            self.durum_cubugu.setText("Model yükleniyor...")
            self.model = YOLO(self.model_yolu)
            self.durum_cubugu.setText(f"Model yüklendi: {self.model_yolu}")
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Model yüklenirken hata oluştu!\n{str(e)}\nLütfen 'best.pt' dosyasının yan yana olduğundan emin olun.")

    def initUI(self):
        """Grafik Arayüz (GUI) elemanlarını oluşturur."""
        merkez_widget = QWidget()
        self.setCentralWidget(merkez_widget)
        
        ana_duzen = QVBoxLayout()
        
        baslik = QLabel("Trafik İşareti Tespit Sistemi")
        baslik.setAlignment(Qt.AlignCenter)
        baslik.setFont(QFont("Arial", 20, QFont.Bold))
        ana_duzen.addWidget(baslik)

        resim_paneli_duzeni = QHBoxLayout()

        gb_orijinal = QGroupBox("Orijinal Görüntü")
        gb_orijinal_layout = QVBoxLayout()
        self.lbl_orijinal = QLabel("Resim Seçilmedi")
        self.lbl_orijinal.setAlignment(Qt.AlignCenter)
        self.lbl_orijinal.setStyleSheet("background-color: #dcdcdc; border: 1px solid gray;")
        self.lbl_orijinal.setFixedSize(500, 400)
        gb_orijinal_layout.addWidget(self.lbl_orijinal)
        gb_orijinal.setLayout(gb_orijinal_layout)

        gb_sonuc = QGroupBox("Tespit Sonucu (Tagged Image)")
        gb_sonuc_layout = QVBoxLayout()
        self.lbl_sonuc = QLabel("Henüz işlem yapılmadı")
        self.lbl_sonuc.setAlignment(Qt.AlignCenter)
        self.lbl_sonuc.setStyleSheet("background-color: #dcdcdc; border: 1px solid gray;")
        self.lbl_sonuc.setFixedSize(500, 400)
        gb_sonuc_layout.addWidget(self.lbl_sonuc)
        gb_sonuc.setLayout(gb_sonuc_layout)

        resim_paneli_duzeni.addWidget(gb_orijinal)
        resim_paneli_duzeni.addWidget(gb_sonuc)
        ana_duzen.addLayout(resim_paneli_duzeni)

        self.txt_bilgi = QTextEdit()
        self.txt_bilgi.setMaximumHeight(100)
        self.txt_bilgi.setReadOnly(True)
        self.txt_bilgi.setPlaceholderText("Tespit edilen nesnelerin sayısı ve sınıfları burada listelenecek...")
        ana_duzen.addWidget(self.txt_bilgi)

        buton_duzeni = QHBoxLayout()
        
        btn_sec = QPushButton("1. Resim Seç")
        btn_sec.setFont(QFont("Arial", 11))
        btn_sec.clicked.connect(self.resim_sec)
        
        btn_test = QPushButton("2. Test Et (Detect)")
        btn_test.setFont(QFont("Arial", 11, QFont.Bold))
        btn_test.setStyleSheet("background-color: #4CAF50; color: white;")
        btn_test.clicked.connect(self.test_et)
        
        btn_kaydet = QPushButton("3. Sonucu Kaydet")
        btn_kaydet.setFont(QFont("Arial", 11))
        btn_kaydet.clicked.connect(self.resmi_kaydet)

        buton_duzeni.addWidget(btn_sec)
        buton_duzeni.addWidget(btn_test)
        buton_duzeni.addWidget(btn_kaydet)
        ana_duzen.addLayout(buton_duzeni)

        btn_layout_video = QHBoxLayout()
        
        btn_video_sec = QPushButton("🎬 Video Dosyası Seç")
        btn_video_sec.setStyleSheet("background-color: #FF9800; color: white; font-weight: bold;")
        btn_video_sec.clicked.connect(self.video_sec)

        btn_kamera = QPushButton("Webcam Başlat")
        btn_kamera.setStyleSheet("background-color: #2196F3; color: white; font-weight: bold;")
        btn_kamera.clicked.connect(self.kamera_baslat)

        btn_durdur = QPushButton("⛔ DURDUR")
        btn_durdur.setStyleSheet("background-color: #f44336; color: white; font-weight: bold;")
        btn_durdur.clicked.connect(self.video_durdur)

        btn_layout_video.addWidget(btn_video_sec)
        btn_layout_video.addWidget(btn_kamera)
        btn_layout_video.addWidget(btn_durdur)
        ana_duzen.addLayout(btn_layout_video)

        self.durum_cubugu = QLabel("Hazır")
        ana_duzen.addWidget(self.durum_cubugu)

        merkez_widget.setLayout(ana_duzen)

    def resim_sec(self):
        """Kullanıcının bilgisayarından resim seçmesini sağlar."""
        dosya_yolu, _ = QFileDialog.getOpenFileName(self, "Resim Seç", "", "Resim Dosyaları (*.jpg *.jpeg *.png)")
        
        if dosya_yolu:
            self.secilen_resim_yolu = dosya_yolu
            
            cv_img = cv2.imread(dosya_yolu)
            self.resmi_goster(cv_img, self.lbl_orijinal)

            self.lbl_sonuc.setText("Tespit bekleniyor...")
            self.lbl_sonuc.setPixmap(QPixmap())
            self.txt_bilgi.clear()
            self.durum_cubugu.setText(f"Resim seçildi: {os.path.basename(dosya_yolu)}")

    def test_et(self):
        """Seçilen resim üzerinde nesne tespiti yapar."""
        if not self.secilen_resim_yolu:
            QMessageBox.warning(self, "Uyarı", "Lütfen önce bir resim seçiniz!")
            return

        self.durum_cubugu.setText("Tespit yapılıyor...")
        QApplication.processEvents()

        results = self.model(self.secilen_resim_yolu)
        sonuc = results[0]

        self.islenmis_goruntu = sonuc.plot()

        self.resmi_goster(self.islenmis_goruntu, self.lbl_sonuc)

        nesne_sayilari = {}
        sinif_isimleri = sonuc.names
        
        for box in sonuc.boxes:
            sinif_id = int(box.cls[0])
            isim = sinif_isimleri[sinif_id]
            nesne_sayilari[isim] = nesne_sayilari.get(isim, 0) + 1
        
        rapor = f"SONUÇ RAPORU:\n----------------\n"
        toplam = 0
        if nesne_sayilari:
            for isim, adet in nesne_sayilari.items():
                rapor += f"• {isim.upper()}: {adet} adet\n"
                toplam += adet
            rapor += f"\nTOPLAM NESNE: {toplam}"
        else:
            rapor += "Hiçbir nesne tespit edilemedi."
            
        self.txt_bilgi.setText(rapor)
        self.durum_cubugu.setText("İşlem tamamlandı.")

    def resmi_kaydet(self):
        """İşlenmiş (kutulu) resmi diske kaydeder."""
        if self.islenmis_goruntu is None:
            QMessageBox.warning(self, "Uyarı", "Kaydedilecek işlenmiş bir görüntü yok! Önce 'Test Et' butonuna basınız.")
            return

        kayit_yolu, _ = QFileDialog.getSaveFileName(self, "Resmi Kaydet", "sonuc.jpg", "Resim Dosyaları (*.jpg *.png)")
        
        if kayit_yolu:
            cv2.imwrite(kayit_yolu, self.islenmis_goruntu)
            QMessageBox.information(self, "Başarılı", f"Resim başarıyla kaydedildi:\n{kayit_yolu}")

    def resmi_goster(self, cv_img, label_widget):
        """OpenCV resmini PyQt QLabel içinde gösterir."""

        rgb_img = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_img.shape
        bytes_per_line = ch * w
        qt_img = QImage(rgb_img.data, w, h, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qt_img)

        label_widget.setPixmap(pixmap.scaled(label_widget.width(), label_widget.height(), Qt.KeepAspectRatio))

    def video_sec(self):
        self.video_durdur()
        dosya_yolu, _ = QFileDialog.getOpenFileName(self, "Video Seç", "", "Video Dosyaları (*.mp4 *.avi *.mov)")
        if dosya_yolu:
            self.cap = cv2.VideoCapture(dosya_yolu)
            self.timer.start(30)
            self.durum_cubugu.setText("Video oynatılıyor...")

    def kamera_baslat(self):
        self.video_durdur()
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            QMessageBox.warning(self, "Hata", "Kamera bulunamadı!")
            return
        self.timer.start(30)
        self.durum_cubugu.setText("Kamera başlatıldı...")

    def kare_guncelle(self):
        """Zamanlayıcı tarafından sürekli çağrılan fonksiyon"""
        if self.cap is None: return
        ret, frame = self.cap.read()
        if ret:
            self.resmi_goster(frame, self.lbl_orijinal)

            results = self.model.track(frame, persist=True, verbose=False)
            res = results[0]
            
            self.islenmis_goruntu = res.plot()
            self.resmi_goster(self.islenmis_goruntu, self.lbl_sonuc)
        else:
            self.video_durdur()

    def video_durdur(self):
        self.timer.stop()
        if self.cap:
            self.cap.release()
        self.lbl_orijinal.clear()
        self.lbl_orijinal.setText("Durduruldu")
        self.lbl_sonuc.clear()
        self.lbl_sonuc.setText("Durduruldu")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    pencere = NesneTespitUygulamasi()
    pencere.show()

    sys.exit(app.exec_())
