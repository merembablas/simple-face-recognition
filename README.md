# face-recognition

Face recognition sederhana. 

# Cara Menggunakan

Install module Python sesuai yang ada di requirements.txt

`$ pip install -r requirements.txt`

Untuk streaming dari webcam, cukup jalankan script dengan:

`$ python app.py`

Untuk streaming dari ipcam / file video, isi param `-v` dengan url ipcam atau path jika berupa file video:

`$ python app.py -v http://192.168.0.1:8080/video`

Untuk meload data wajah yg sudah disimpan, gunakan param `-d`, jika tidak otomatis menggunakan file `default`. File akan disimpan di folder data:

`$ python app.py -d keluarga`

Kemudian akan muncul window streaming video.

## Face Detector

tekan tombol `f` untuk menampilkan mode face detector, tekan `f` lagi untuk keluar dari mode face detector.

## Memasukkan label wajah

Tekan tombol `TAB` untuk menampilkan mode selector, video akan berhenti. Tekan `c` untuk cancel.

Drag kotak diatas gambar wajah yg diinginkan, tekan `ENTER`, kemudian akan keluar window untuk memasukkan label. Setelah memasukkan label, tekan `ENTER` kembali. 

Maka wajah tersebut akan dikenali jika masuk ke dalam mode face detector.


