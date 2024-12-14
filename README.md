# Laporan Proyek Machine Learning Rekomendasi Film - Alif Khusain Bilfaqih

## Project Overview

Laju informasi saat ini sudah tidak terkendali. Pada tahun 2024, diperkirakan sekitar 402,89 juta terabyte data dibuat, ditangkap, atau dikonsumsi setiap harinya. Fenomena ini dikenal dengan sebutan "*information overload*" atau "kelebihan informasi". Untuk mengatasi *information overload*, sistem rekomendasi memainkan peran penting, termasuk dalam industri hiburan seperti film.

Dengan semakin banyaknya film yang dirilis setiap tahun, penonton sering merasa kesulitan dan menghabiskan banyak waktu untuk memilih film yang sesuai dengan keinginan mereka. Sebuah survei oleh *CivicScience* pada tahun 2020 menunjukkan bahwa rata-rata pengguna menghabiskan sekitar 18 menit hanya untuk memilih apa yang akan mereka tonton di platform streaming. Banyak juga penonton merasa lebih nyaman memilih film setelah membaca sinopsis, ulasan, atau menonton *trailer*.

Proyek ini dibuat dengan tujuan untuk mengembangkan sistem rekomendasi film berbasis machine learning, yang dapat memberikan saran yang relevan bagi pengguna. Sehingga dapat menjadi solusi untuk mengurangi waktu pencarian hingga 50%.

Platform video yang populer seperti Netflix dan YouTube juga menerapkan teknologi sistem rekomendasi. Terbukti di Netflix, lebih dari 60% film yang ditonton berasal dari fitur rekomendasi yang ada di halaman awal. Ini menunjukkan efektivitas sistem rekomendasi dalam menarik dan mempertahankan pengguna.

Dari segi ekonomi, relevansi rekomendasi yang dipersonalisasi juga mendukung strategi bisnis melalui retensi pelanggan. Dampak baik dari retensi pelanggan diantaranya:
- Pelanggan yang puas dan setia lebih mungkin merekomendasikan kepada orang lain.
- Pelanggan yang terus kembali cenderung menghasilkan pendapatan yang lebih konsisten bagi perusahaan.
- Mendapatkan pelanggan baru sering kali lebih mahal daripada mempertahankan pelanggan yang sudah ada. Oleh karena itu, retensi pelanggan dapat menghemat biaya pemasaran.

Informasi selengkapnya dapat dilihat pada artikel:
[An overview of video recommender systems](https://www.frontiersin.org/journals/big-data/articles/10.3389/fdata.2023.1281614/full#B47)

## Business Understanding

### Problem Statements

**1. Information Overload di dunia industri (termasuk film)**

Dengan semakin banyaknya film yang dirilis setiap tahunnya, pengguna sering kali menghadapi kesulitan memilih konten yang sesuai dengan keinginan mereka. Masalah ini diperburuk oleh banyaknya informasi pada platform streaming, seperti ada sinopsis, ulasan, rating, *trailer*, *genre*, dsb. Ini membuat penonton bingung dan menghabiskan banyak waktu.

**2. Waktu dan Efisiensi dalam Menemukan Konten**

Meski platform seperti Netflix menawarkan ribuan pilihan, pengguna tetap harus melihat trailer, membaca sinopsis, atau mencari ulasan sebelum membuat keputusan. Proses ini tidak hanya memakan waktu tetapi juga mengurangi kepuasan pengalaman pengguna.

### Goals

**1. Menyempitkan informasi film**

Membuat sistem rekomendasi berbasis machine learning yang memberikan rekomendasi sesuai personal pengguna, sehingga informasi yang tidak ditampilkan memang bukan informasi yang dibutuhkan atau diinginkan pengguna.

Sistem rekomendasi ini menjadi salah satu solusi *information overload* yang paling banyak disarankan. Beberapa buku dan literatur yang menyarankan diantaranya:

- **"The Filter Bubble: What the Internet Is Hiding from You" oleh Eli Pariser**.
Buku ini mengeksplorasi bagaimana algoritma rekomendasi digunakan oleh platform online untuk menyaring informasi berdasarkan preferensi pengguna. Pariser menjelaskan bahwa meskipun sistem ini membantu pengguna mengatasi kelebihan informasi, ada juga risiko penyempitan pandangan (filter bubble). Namun, dia mengakui bahwa tanpa sistem rekomendasi, pengguna akan kewalahan menghadapi data yang terlalu banyak.

- **"Recommender Systems: An Introduction" oleh Jannach, Zanker, Felfernig, dan Friedrich**.
Buku ini membahas bagaimana kelebihan informasi dapat menghambat produktivitas dan pengambilan keputusan. Rekomendasi konten disebut sebagai salah satu solusi penting yang dapat memprioritaskan data relevan, terutama dalam lingkungan digital.

**2. Mengurangi Waktu Pencarian Film**

Mengembangkan sistem rekomendasi berbasis machine learning yang dapat menyarankan film atau serial yang relevan secara personal untuk mengurangi waktu pencarian hingga 50%.

### Solution statements

Untuk membuat sistem rekomendasi yang dapat menyempitkan informasi film dengan lebih personal dan mengurangi waktu mencari film yang diminati, berikut adalah *solution statement* yang akan digunakan;

**1. *Content Based Filtering***

Ide dari sistem rekomendasi berbasis konten (*content-based filtering*) adalah merekomendasikan item yang mirip dengan item yang disukai pengguna di masa lalu. Jiks pengguna menyukai film Ada Apa dengan Cinta, sistem akan merekomendasikan film dengan aktor utama Nicholas Saputra atau Dian Sastrowardoyo. Sistem juga akan merekomendasikan film dengan genre drama lainnya.

*Content-based filtering* mempelajari profil minat pengguna baru berdasarkan data dari objek yang telah dinilai pengguna. Algoritma ini bekerja dengan menyarankan item serupa yang pernah disukai di masa lalu atau sedang dilihat di masa kini kepada pengguna. Semakin banyak informasi yang diberikan pengguna, semakin baik akurasi sistem rekomendasi.

**2. Membuat model di bawah 1 detik**

Waktu sangatlah berharga. Oleh karena itu, setelah model berhasil dibuat dan sudah mengeluarkan hasilnya, akan ada evaluasi yang mneghitung berapa lama model memberikan rekomendasinya. Jika waktu yang diperlukan kurang dari 1 detik, maka dianggap cukup cepat.

## Data Understanding

Dataset yang digunakan diambil dari platform kaggle.com, dan di-*upload* oleh The Movie Database (TMDB). Versi asli dari dataset ini sudah dihapus karena permintaan sesuai [DMCA](https://en.wikipedia.org/wiki/Digital_Millennium_Copyright_Act) dari IMDB. Namun demikian, dampaknya sudah diminimalisir dengan mengganti film dan data yang sesuai dengan [ketentuan penggunaan](https://www.themoviedb.org/api-terms-of-use).

Berikut adalah dataset yang digunakan: [TMDB 5000 Movie Dataset](https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata?select=tmdb_5000_movies.csv)

Tidak sesuai judulnya, dataset ini hanya memilki 4800 judul film. Selain itu, terdapat banyak *missing value* pada kolom `homepage`, yaitu 3096 baris, ada juga pada `tagline` berjumlah 844, dan kolom `overview`, `runtime`, dan `release_date` hanya ada kurang dari 5 baris *missing value*. Selain *missing_value*, tidak ada masalah lain pada data, seperti outlier atau duplikat.

Adapun *feature* pada dataset ini dibagi menjadi 2 file, yaitu `tmdb_5000_credits.csv`, dan `tmdb_5000_movies.csv`. Berikut adalah penjelasan setiap *features*:
1. File `tmdb_5000_credits.csv`
    - movie_id : Nomor unik setiap yang diberikan pada setiap film
    - title : Nama judul film 
    - cast : Nama karakter yang ada dalam film, beserta nama aktor yang memerankannya, dan jenis kelaminnya.
    - credit : Kru yang bertugas dalam pembuatan film, yang dibagi berdasarkan departemen dan *job* atau pekerjaan.
2. File `tmdb_5000_movies.csv`
    - title : Nama judul film.
    - budget : Total pengeluaran yang digunakan dalam pembuatan film.
    - genres : Kategori film.
    - homepage : Situs yang menayangkan film tersebut.
    - id : Nomor unik setiap yang diberikan pada setiap film.
    - keywords : Kata kunci yang diberikan untuk menerangkan film tersebut.
    - original_language : Bahasa asli yang digunakan dalam film.
    - original_title : Judul nama film sebelum di-*translate*
    - overview : Ringkasan tentang apa isi film tersebut.
    - popularity : Tingkat populer film di dunia.
    - production_companies : Perusahaan yang menggarap film.
    - production_countries : Negara yang menggarap film
    - release_date : Tanggal perilisan film.
    - revenue : Total pemasukan film tersebut.
    - runtime : Status keberlanjutan film.
    spoken_languages : Bahasa asli yang digunakan untuk dialog atau percakapan dalam film.
    - tagline : Garis besar atau ide inti isi cerita.
    - vote_average : Hasil rata-rata voting penilaian film.
    - vote_count : Jumlah pengguna yang memberikan penilaian.

## Data Preparation

### Menangani missing data

Beberapa kesalahan yang ada pada data adalah missing value atau nilai yang tidak ada, dan data yang terduplikasi. Agar tidak menjadi masalah pada saat menggali informasi, atau visualisasi, atau yang lainnya, dapat dilihat dengan menggunakan kode `.isna().sum()` dan `.duplicated().sum()`.
Ada beberapa missing value, terutama pada kolom `homepage`. Namun kolom ini tidak akan kita gunakan, sehingga kita biarkan.

Data terduplikasi yang dicek dengan `.duplicated().sum()`, nilainya 0. Tapi ada data terpulikasi yang tidak terhitung, dapat dilihat dengan mengecek judul yang sama di kolom `title`, dengan `release_date` yang sama. Selanjutnya, hapus dengan `.drop_duplicates(subset=['title', 'release_date'])`

### Menambahkan Judul Rilis Film

Pada dataset, terdapat film yang dibuat ulang pada tanggal berbeda, namun dengan nama yang sama. Ini dapat menyebabkan error saat akan menampilkan rekomendasi. Agar tidak mengurangi film yang direkomendasikan, tahun rilis film akan ditambahkan setelah nama film.
Caranya yaitu dengan mengubah format tanggal pada kolom `release_date` agar hanya menampilkan tahunnya saja. Llau, tambahkan tahun rilis sesuai pada kolom `release_date` pada akhir nama film.

### Menyiapkan Dataset Baru

Karena ada begitu banyak kolom yang tidak dipakai, dibuat dataframe baru dengan nama `main_df`, yang berisi beberapa kolom saja, yaitu 'movie_id', 'title', 'cast', 'crew', 'genres', dan 'keywords'.

### *Convert* kolom

Kolom cast, crew, keywords, dan genres berupa *dictionary*. Oleh sebab itu, kita akan mengubah list dictionary pada beberapa kolom tersebut dengan menggunakan *function*.
- Untuk kolom 'genres' dan 'keywords', cara kerjanya yaitu dengan mengambil kata dengan kata kunci 'name' dalam *dictionary*, dan memasukannya kedalam *list*. Hal itu terus berulang sampai semua kata dalam semua baris.
- Cast berisi nama karakter dalam film tersebut, dan aktor yang memerankannya, beserta id dan jenis kelamin. Biasanya, karakter penting seperti *main character* dan *main villain* berada di awal, kita ambil saja 5 nama karakter beserta aktor yang memerankannya.
- Nama kru yang bertugas ada di dalam kolom 'crew' sangatlah bnayak, yang tidak semuanya penting. Karena tidak mungkin orang mencari film karena melihat siapa desain suaranya, kita hanya akan mengambil direkturnya saja.
- Setelah semua menjadi *list*, selanjutnya mari kita ubah menjadi string biasa dengan memisahkan setiap isinya dengan koma (,) menggunakan `lambda`.
- Memasukkan ke dalam kolom baru bernama 'tags'.

### Menyiapkan Dataset Yang Digunakan

Untuk dataset yang digunakan hanya berisi kolom 'tags' yang berisi nama film, dan 'tags' yang memberikan informasi tentang film. Data ini disimpan dengan nama `new_df`. Selain itu, kolom tags juga diubah menjadi hufur kecil semua (*undercase*) menggunakan `.apply(lambda x: x.lower())`.

## Modeling

Model yang digunakan berbasis konten (content-based filtering), yaitu merekomendasikan item yang mirip dengan item yang disukai pengguna di masa lalu.

### Kelebihan

- *Content based filtering* memberikan rekomendasi berdasarkan fitur yang telah diketahui, seperti genre, aktor, direktur, dan *keywords*. Hal ini memungkinkan sistem untuk memberikan rekomendasi yang lebih relevan sesuai.
- Sistem dapat mempelajari preferensi pengguna secara individual, sehingga lebih personal dan cocok dengan apa yang sudah disukai atau ditonton oleh pengguna sebelumnya.
- Sistem ini tidak bergantung pada data pengguna lain untuk memberikan rekomendasi. Artinya, bahkan jika tidak ada data atau interaksi pengguna lain (cold start problem) sistem tetap bisa memberikan rekomendasi berdasarkan konten item itu sendiri.

### Kekurangan

- Sistem hanya dapat merekomendasikan item yang mirip dengan yang telah disukai atau dikonsumsi sebelumnya. Ini dapat mengurangi variasi film dan eksplorasi pengguna.
- Agar sistem content-based filtering efektif, proses ekstraksi fitur harus akurat dan mencakup informasi penting. Jika fitur yang digunakan tidak relevan atau tidak mencakup seluruh aspek konten, sistem mungkin akan memberikan rekomendasi yang kurang tepat.

### Proses

Hal pertama yang dilakukan adalah menghitung IDF pada kolom 'tags' yang berisi *features* film dengan menggunakan `tf.fit()`. Jika sudah, *mapping* array dari fitur index integer ke fitur utama dengan `tf.get_feature_names_out()`, lalu transformasikan agar menjadi matriks 2D.

Hal selanjutnya adalah menghitung derajat kesamaan (similarity degree) antara film dengan kolom 'tags' menggunakan teknik cosine similarity. Untuk membuat struktur data yang memungkinkan kita mencari index dari sebuah judul film dengan cepat, kita buat data baru dengan nama `indices`.

Jika sudah memiliki data similarity (kesamaan) antar film, tandanya pembuatan model sudah hampir selesai. Tahap terakhir adalah membuat fungsi yang menampilkan rekomendasi. Berikut tahapan lengkap pada fungsi yang dibuat:
- Mencari semua judul film yang sesuai pada data tanpa tahun rilisnya. Jika tidak ada, maka sistem akan mengeluarkan teks 'Film dengan judul ... tidak ditemukan dalam dataset'.
- Jika judul film yang dimasukan hanya sesuai dengan 1 film, maka index dari film tersebut akan disimpan di `idx`.
- Jika ada lebih dari 1 film yang cocok dengan nama film dimasukan, maka sistem akan menampilkan pesan 'Ditemukan beberapa judul film dengan nama yang sama:' beserta nama-nama film yang sesuai. Selain itu, akan ada *input text* untuk memasukan nomor index dari film yang dimaksud.
- Jika ada lebih dari 1 film yang cocok, lalu memasukan nomor index yang tidak ada pada pilihan yang ditampilkan sistem, akan muncul pesan 'Indeks yang dimasukkan tidak valid'. Namun jika nomor index yang dimasukkan sesuai, proses rekomendasi akan dilanjutkan.
- Pada tahap ini, `cosine_sim[idx]` akan memberikan daftar nilai kesamaan antara film yang di-*input* dengan semua film lainnya dalam dataset, lalu diubah menjadi pasangan (index, value).
- Hasil `enumerate()` diubah menjadi sebuah daftar sesuai nilai kesamaan film. Hasil ini disimpan pada `sim_scores`.
- Selanjutnya, nilai `sim_scores` diurutkan secara menurun, sehingga film dengan kesamaan tertinggi akan muncul di urutan pertama, lalu `sim_scores` hanya menyimpan 10 film teratas.
- Membuat `movie_indices` yang berisi daftar indeks film yang memiliki kesamaan tertinggi dengan film yang dipilih.
- Mengembalikan atau menampilkan nama film pada kolom 'title' sesuai index `movie_indices`.

### Hasil

Berikut adalah daftar rekomendasi yang diberikan sistem untuk film 'Batman (1989)'

| No  | Title                                             |
|-----|---------------------------------------------------|
| 1   | Batman (1966)                                     |
| 2   | Batman & Robin (1997)                             |
| 3   | Batman Returns (1992)                             |
| 4   | The Dark Knight (2008)                            |
| 5   | Batman Begins (2005)                              |
| 6   | Batman: The Dark Knight Returns, Part 2 (2013)    |
| 7   | The Dark Knight Rises (2012)                      |
| 8   | Batman v Superman: Dawn of Justice (2016)         |
| 9   | Batman Forever (1995)                             |
| 10  | Man of Steel (2013)                               |

## Evaluation

### Evalusi Hasil

Jenis evaluasi yang digunakan adalah `precision`, `recall`, dan `f1-score`. Ini adalah metrik yang sering digunakan untuk mengevaluasi performa sistem rekomendasi, terutama ketika fokusnya adalah pada relevansi rekomendasi yang dihasilkan. Karena keterbatasan data pengguna, evaluasi ini dilakukan berdasarkan data histori saya sendiri, yaitu setelah menonton film 'Spider-Man'.

Berikut penjelasan matriks yang digunakan:
- `precision`: mengukur seberapa relevan item yang direkomendasikan dari total item yang direkomendasikan. *Precision* tinggi berarti sebagian besar rekomendasi yang diberikan kepada pengguna relevan.
- `recall` mengukur seberapa baik sistem dapat menemukan semua item relevan dari dataset. Recall tinggi berarti sistem berhasil mencakup sebagian besar film relevan yang bisa direkomendasikan.
- `f1_score` menggabungkan precision dan recall menjadi satu metrik tunggal dengan membagi hasil perkalian precision dengan recall, dan penjumlahan precision dengan recall. F1-Score menunjukan rata-rata harmonik antara *Precision* dan *Recall*.

Adapun hasil dari evaluasi adalah sebagai berikut

Precision: 0.4, Recall: 0.8, F1-Score: 0.53

Penjelasan:
- Precision = 0.4: Sistem cenderung memberikan banyak rekomendasi yang tidak relevan (hanya 40% yang relevan). Ini menunjukkan bahwa sistem cenderung terlalu banyak memberikan rekomendasi yang salah, yang perlu diperbaiki agar hanya memberikan rekomendasi yang relevan.
- Recall = 0.8: Sistem cukup baik dalam menemukan sebagian besar item yang relevan (80% relevan ditemukan), tetapi masih ada 20% dari item relevan yang tidak ditemukan atau tidak direkomendasikan.
- F1-Score = 0.53: F1-Score yang relatif lebih rendah menunjukkan bahwa meskipun recall cukup baik, precision perlu ditingkatkan untuk mencapai keseimbangan yang lebih baik antara keduanya. Sistem memberikan banyak rekomendasi yang salah (menurunkan precision), meskipun sebagian besar item relevan sudah ditemukan (meningkatkan recall).

### Evaluasi Waktu

Target waktu pada proyek ini adalah kurang dari 1 detik. Untuk mengevaluasi waktu pada proyek ini, menggunakan *magic command* `%timeit`. Maka secara otomatis menjalankan kode beberapa kali dan memberikan waktu rata-rata eksekusi.
Hasilnya, tertulis '27 ms ± 3.3 ms per loop (mean ± std. dev. of 7 runs, 10 loops each)'. Artinya, secara rata-rata, setiap eksekusi 1 loop membutuhkan sekitar 27 *milisecond*, dengan variasi sekitar 3.3 *milisecond*. Waktu ini diperoleh dari pengujian yang diulang sebanyak 7 kali, masing-masing dengan 10 loop.