# -*- coding: utf-8 -*-
"""Salinan dari rec_notebook_2.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1HR8M0jTCBOxlsfxAzLOMtOQx7Wh97JFh

# Proyek Diabetes Prediction

* Nama: Alif Khusain Bilfaqih
* Username: akbf_apotheosis
* Email: faqihkeren44@gmail.com

## Data Loading

**Import Library Yang DIbutuhkan**

Untuk mengolah dan memvisualisasikan data hingga membuat model, dibutuhkan library yang perlu sisiapkan, seperti pandas, numpy, seaborn, matplotlib, dan sebagainya.
"""

# Commented out IPython magic to ensure Python compatibility.
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
# %matplotlib inline
import seaborn as sns

"""**Import dataset**

Sebelum kita memulai semuanya, tentunya kita harus memasukkan dataset yang ingin kita gunakan.
Alamat dataset yang digunakan sebelumnya sudah di upload di github, lalu diambil dengan memasukan nama 'url' nya.
Dataset yang kita gunakan ada 2 file, yaitu 'credit' dan 'movies'.
"""

url_credits = "https://raw.githubusercontent.com/faqihkeren44/movie_recommendation/refs/heads/main/tmdb_5000_credits.csv"
url_movies = "https://raw.githubusercontent.com/faqihkeren44/movie_recommendation/refs/heads/main/tmdb_5000_movies.csv"

credits = pd.read_csv(url_credits)
movies = pd.read_csv(url_movies)

"""**Menggabungkan Dataset**

Agar lebih mudah mengolah data, kedua dataset kita gabungkan dengan memanfaatkan library pandas dengan menggunakan `.merge()`. Kedua dataset ini digabungkan sesuai kolom `title`.

Dataset sudah selesai kita masukan. Mari kita lihat isi 5 baris pertama dari dataset, dengan perintah `.head(3)`
"""

df = pd.merge(credits, movies, on='title')
df.head(3)

"""Untuk melihat beberapa informasi feature pada data, bisa memanfaatkan kode `.info()` dan `describe()`.

Dapat dilihat bahwa setiap kolom memiliki 100000 data. Dari data tersebut ada yang berupa kategorikal, dan ada yang numerical.
"""

df.info()

df.describe()

"""## Data Preparation

**Menangani missing data**

Beberapa kesalahan yang ada pada data adalah missing value atau nilai yang tidak ada, dan data yang terduplikasi. Agar tidak menjadi masalah pada saat menggali informasi, atau visualisasi, atau yang lainnya, dapat dilihat dengan menggunakan kode `.isna().sum()` dan `.duplicated().sum()`
"""

df.isnull().sum()

df.duplicated().sum()

"""Ternyata ada beberapa missing value, terutama pada kolom `homepage`. Namun kolom ini tidak akan kita gunakan, sehingga kita biarkan.

Data terduplikasi yang dicek dengan `.duplicated().sum()`, nilainya 0. Tapi sepertinya ada data terpulikasi yang tidak terhitung. Makanya kita cek judul yang sama di kolom `title`.
"""

df[df['title'].duplicated()].sort_values(by='title')

"""Ternyata benar, ada 3 judul yang sama dalam dataset kita. Mari kita persempit kolom dataset, dengan hanya melihat judul yang terduplikasi dan tanggal rilisnya."""

# df[df.duplicated(subset=['title', 'release_date'], keep=False)].sort_values(by='title')
duplicated_titles = df[df['title'].duplicated()]
duplicated_titles[['title', 'release_date']].sort_values(by='title')

"""Dari tabel di atas, kita dapat menyimpulkan mungkin film tersebut dibuat ulang di tahun berikutnya dan ditayangkan dengan nama yang sama. Oleh sebab itu, dari ketiga film yang sama ini, kita hapus 1 saja, dengan perintah `.dop.duplitaces(subset=['title', 'release_date'])`."""

df = df.drop_duplicates(subset=['title', 'release_date'])

drop_title = ['Batman', 'The Host', 'Out of the Blue']
duplicated_titles = df[df['title'].isin(drop_title)]
duplicated_titles[['title', 'release_date']]

"""**Menambahkan Judul Rilis Film**

Ada film dengan judul yang sama, namun memiliki tanggal rilis yang berbeda (Film remake). Agar tidak mengurangi film yang direkomendasikan dan tidak membuat model bingung (karena ada 2 data yang sama), kita tambahkna tahun rilis film itu setelah nama film.

Langkah pertama yaitu mengubah kolom 'release_date' menjadi tanggal dengan `.to_datetime()`, lalu mengubah formatnya menjadi tahun saja.
"""

df['release_date'] = pd.to_datetime(df['release_date'], errors='coerce').dt.year

"""Selanjutnya, kita gabungkan judul dengan tahun rilisnya. Tahun rilis ini akan dimasukan kedalam tanda kurung (). Jika pada kolom 'release_date' tidak ada, maka hanya akan menampilkan nama film saja."""

df['title'] = df.apply(
    lambda x: f"{x['title']} ({int(x['release_date'])})" if not pd.isna(x['release_date']) else x['title'],
    axis=1
)
df.head(3)

"""**Menyiapkan Dataset Baru**

Karena ada begitu banyak kolom, kita membuat dataframe baru dengan nama `main_df`, yang berisi beberapa kolom saja, yaitu 'movie_id', 'title', 'cast', 'crew', 'genres', dan 'keywords'.
"""

main_df = df[['movie_id', 'title', 'cast', 'crew', 'genres', 'keywords']].copy()
main_df.head()

"""Kolom cast, crew, keywords, dan genres berisi dictionary yang tidak kesemuanya dibutuhkan. Oleh sebab itu, kita akan mengubah list dictionary pada beberapa kolom tersebut.

Hal pertama adalah mengubahnya menjadi list.
"""

import ast

def convert (x):
  list = []
  for i in ast.literal_eval(x):
    list.append(i['name'])
  return list

"""Di atas sudah dibuatkan *function* untuk mengubah *dictionary* menjadi *list*, yang kita gunakan hanya untuk kolom 'genres' dan 'keywords'. Cara kerja *function* tersebut yaitu dengan mengambil kata dengan kata kunci 'name' dalam *dictionary*, dan memasukannya kedalam *list*. Hal itu terus berulang sampai semua kata dalam semua baris."""

main_df['genres'] = main_df['genres'].apply(convert)
main_df['keywords'] = main_df['keywords'].apply(convert)
main_df.head()

"""Sebelum kita menindak kolom 'cast', mari kita lihat salah 1 isinya, yaitu pada index ke 3."""

main_df['cast'].iloc[3]

"""Cast berisi nama karakter dalam film tersebut, dan aktor yang memerankannya, beserta id dan jenis kelamin. Biasanya, karakter penting seperti *main character* dan *main villain* berada di awal, kita ambil saja 5 nama karakter beserta aktor yang memerankannya.

Mari kita buat *function* untuk menjalankannya.
"""

def actor_convert (x):
  list = []
  for i in ast.literal_eval(x):
    if len(list) < 5:
      list.append(i['name'])
    else:
      break
  return list

def character_convert (x):
  list = []
  for i in ast.literal_eval(x):
    if len(list) < 5:
      list.append(i['character'])
    else:
      break
  return list

"""Setelah dibuat *function*, kita masukan datanya, yaitu kolom 'cast', dengan perintah `.apply()`.

Karakter dalam film akan dimasukan kedalam kolom baru bernama 'character', dan pemerannya dimasukan kedalam kolom 'actor'. Jika sudah, maka kolom 'cast' sudah tidak diperlukan lagi, dan bisa kita buang.
"""

main_df['actor'] = main_df['cast'].apply(actor_convert)
main_df['character'] = main_df['cast'].apply(character_convert)
main_df = main_df.drop('cast', axis=1)
main_df.head()

"""Terakhir adalah kolom 'cast'. Mari kita lihat salah satu isinya pada index pertama dengan `.iloc[0]`."""

main_df['crew'].iloc[0]

"""Banyak nama kru yang bertugas ada di dalam kolom 'crew', yang tidak semuanya penting. Karena tidak mungkin orang mencari film karena melihat siapa desain suaranya, kita hanya akan mengambil direkturnya saja."""

def director_convert (x):
  list = []
  for i in ast.literal_eval(x):
    if i['job'] == 'Director':
      list.append(i['name'])
      break
  return list

"""Di atas adalah *function* untuk mengambil nama direktur dalam film. Kita jalankan dengan perintah `.apply()`, dan menghapus kolom 'crew'.

Berikut adalah hasil akhirnya
"""

main_df['director'] = main_df['crew'].apply(director_convert)
main_df = main_df.drop('crew', axis=1)
main_df.head()

"""Setelah semua menjadi *list*, selanjutnya mari kita ubah menjadi string biasa dengan memisahkan setiap isinya dengan koma (,)."""

features = ['genres', 'keywords', 'actor', 'character', 'director']

for col in features:
  main_df[col] = main_df[col].apply(lambda x: ', '.join(x) if isinstance(x, list) else x)
main_df.head(3)

"""Setelah semuanya selesai, kita buat kolom baru dengan nama 'tags' ynag berisi dari gabungan semua kolom yang ada. Isi/nilai dri kolom 'tags' ini yang akan kita gunakan untuk menghitung rekomendasi yang tepat."""

main_df['tags'] = main_df['genres'] + main_df['keywords'] + main_df['actor'] + main_df['character'] + main_df['director']
main_df['tags'].iloc[0]

"""Berikut adalah dataframe baru, yang bernama `new_df`, yang hanya berisi judul film (title), dan kolom 'tags'."""

new_df = main_df[['title', 'tags']]
new_df.head(3)

"""Agar tidak ada perbedaan, kita buat semua kata pada kolom 'tags' menjadi huruf kecil atau *undercase*."""

new_df['tags'] = new_df['tags'].apply(lambda x: x.lower())
new_df['tags']

"""## Modeling and Result

Karena kita menggunakan TF-IDF, mari kita import library, lalu diinisialisasi dengan nama 'tf'.
"""

from sklearn.feature_extraction.text import TfidfVectorizer
tf = TfidfVectorizer()

"""Hal pertama yang dilakukan adalah menghitung IDF pada kolom 'tags' dengan `tf.fit()`. Jika sudah, mari kita mapping array dari fitur index integer ke fitur utama dengan `tf.get_feature_names_out()`."""

tf.fit(main_df['tags'])
tf.get_feature_names_out()

"""Setelah berhasil, kita *fit* kolom 'tags', dan mentranfsormasikannya kedalam bentuk matrix 2 dimensi. Kita bisa melihat ukurannya dengan perintah `.shape`."""

tfidf_matrix = tf.fit_transform(new_df['tags'])
tfidf_matrix.shape

"""Kita juga bisa melihat matriks tf-idf yang sudah kita buat dengan `tfidf_matrix.todense()`. Bisa juga kita buatkan dataframe agar lebih nyaman dilihatnya. Di bawah adalah contohnya, dengan sample acak (15 kolom dari 'tags', dan 10 baris nama film)."""

pd.DataFrame(
    tfidf_matrix.todense(),
    columns = tf.get_feature_names_out(),
    index = main_df.title
).sample(15, axis=1).sample(10, axis=0)

"""### Cosine Similarity

Di atas, kita berhasil mengidentifikasi korelasi antara film dengan kolom 'tags'. Sekarang kita hitung derajat kesamaannya. Di sini, kita menggunakan `cosine_similarity` dari librarby `sklearn`.
"""

from sklearn.metrics.pairwise import cosine_similarity
# from sklearn.metrics.pairwise import linear_kernel

cosine_sim = cosine_similarity(tfidf_matrix)
cosine_sim

"""Untuk membuat struktur data yang memungkinkan kita mencari index dari sebuah judul film dengan cepat, kita buat data baru dengan nama `indices`."""

indices = pd.Series(main_df.index, index = new_df['title']).drop_duplicates()

"""Selanjutnya, mari kita lihat matriks kesamaan setiap resto dengan menampilkan nama film dalam 5 sampel kolom (axis = 1) dan 10 sampel baris (axis=0). Jalankan kode berikut."""

cosine_sim_df = pd.DataFrame(cosine_sim, index = new_df['title'], columns = new_df['title'])
cosine_sim_df.sample(5, axis = 1).sample(10, axis = 0)

"""### Mendapatkan Rekomendasi

Setelah kita memiliki data similarity (kesamaan) antar film, langkah terakhir adalah membuat fungsi agar sistem dapat menampilkan rekondasi film sesuai judul yang dimasukan.
"""

def get_recommendations(title, cosine_sim=cosine_sim):
    # Mencari semua judul film yang cocok tanpa tahun
    matched_titles = main_df[main_df['title'].str.contains(title, case=False, na=False)]

    if matched_titles.empty:
        return f"Film dengan judul '{title}' tidak ditemukan dalam dataset."

    # Jika hanya ada satu film yang cocok
    if len(matched_titles) == 1:
        idx = matched_titles.index[0]
    else:
        # Menampilkan daftar film dengan tahun rilis untuk pemilihan
        print("Ditemukan beberapa judul film dengan nama yang sama:")
        print(matched_titles['title'])
        choice = input("Masukkan indeks film yang ingin direkomendasikan: ")

        try:
            idx = int(choice)
            if idx not in matched_titles.index:
                return "Indeks yang dimasukkan tidak valid."
        except ValueError:
            return "Harap masukkan indeks yang valid."

    # Mendapatkan skor kemiripan berdasarkan indeks
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:11]  # Mengambil 10 film teratas
    movie_indices = [i[0] for i in sim_scores]

    return main_df['title'].iloc[movie_indices]

"""Berikut penjelasannya:
- skor kemiripan film dimasukan kedalam list `sim_scores`.
- `enumerate`: Menambahkan index (0, 1, 2, ...) ke skor kemiripan sehingga setiap film memiliki pasangan.
- Mengurutkan daftar film berdasarkan kemiripan dalam urutan menurun (Skor tertinggi di atas)
- Hanya menampilkan 10 film dengan skor kemiripan tertinggi
- Membuat `movie_indices` yang berisi `i[0]`, yaitu hanya mengambil index dari pasangan (`index`, `similarity_score`)
- Terakhir, `return` atau mengembalikan judul film seuai *index* yang dihitung sebelumya.

Sekarang, mari kita coba menampilkan rekomendasi film Superman dan Avatar
"""

get_recommendations('Batman')

get_recommendations('Avatar')

get_recommendations('Avengers')

"""## Evaluation

Evaluasi sistem rekomendasi berbasis *Content-Based Filtering* seperti yang kita buat dilakukan untuk mengukur seberapa baik sistem memberikan rekomendasi yang relevan bagi pengguna. Pengukuran metode ini berdasarkan *history* pribadi saya setelah menonton film 'Spider-Man' yang mungkin akan saya rekomendasikan juga pada orang lain.
"""

def evaluate(recommended, actual):
    recommended_set = set(recommended)
    actual_set = set(actual)

    true_positives = len(recommended_set & actual_set)
    precision = true_positives / len(recommended_set) if recommended_set else 0
    recall = true_positives / len(actual_set) if actual_set else 0
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

    return precision, recall, f1

"""Di atas merupakan fungsi untuk mengukur metrik evaluasi *precision*, *recall*, dan *f1*. Daftar film hasil rekomendasi dan pengalaman pribadi saya diubah menjadi set, karena set memiliki kelebihan, yaitu hanya menyimpan elemen unik dan mendukung operasi himpunan, seperti union, intersection, dan difference, yang akan berguna untuk menghitung true positives.

- *precision* membagi jumlah yang film yang sama dengan total rekomendasi yang diberikan oleh sistem. Jika `recommended_set` kosong, maka bernilai 0.
- *recall* menghitung seberapa banyak item yang relevan yang ditemukan oleh sistem dari keseluruhan item yang relevan.
- *f1* menggabungkan precision dan recall menjadi satu metrik tunggal dengan membagi hasil perkalian *precision* dengan *recall*, dan penjumlahan *precision* dengan *recall*

Di bawah merupakan hasil setelah menjalankan fungsi `evaluate`, dengan membandingkan film hasil rekomendasi film 'Spider-Man' tahun 2002, dengan pengalaman saya pribadi.
"""

recommended = get_recommendations('Spider-Man').tolist()
actual = ['Spider-Man 3 (2007)', 'The Amazing Spider-Man 2 (2014)',
          'Spider-Man 2 (2004)', 'The Amazing Spider-Man (2012)',
          'Avengers: Age of Ultron (2015)']
precision, recall, f1 = evaluate(recommended, actual)
print(f"Precision: {precision}, Recall: {recall}, F1-Score: {f1}")

"""Dari hasil evaluasi di atas, sistem sudah cukup baik dalam menemukan sebagian besar item yang relevan (80% relevan ditemukan), namun hanya 40% yang relevan. Nilai f1-Score yang relatif lebih rendah (0.533) menunjukkan bahwa meskipun recall cukup baik, precision perlu ditingkatkan untuk mencapai keseimbangan yang lebih baik antara keduanya."""

# Commented out IPython magic to ensure Python compatibility.
# %timeit get_recommendations('Avatar')

"""Terakhir adalah evaluasi waktu yang dibutuhkan sistem untuk menampilkan rekomendasi.

Di sini kita mencoba dengan membuat sistem menampilkan rekomendasi film 'Avatar' 10x, lalu menghitung jumlah rata-rata waktu yang dibutuhkan.

Dapat dilihat rata-rata waktu yang dibutuhkan untuk menjalankan 1 loop adalah 27 *milisecond*, dengan vasiari 3.3 *milisecond*.
"""