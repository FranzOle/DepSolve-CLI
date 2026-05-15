# DepSolve CLI 🔍

> **Package Dependency Resolver CLI** — Simulasi package manager modern berbasis Python dengan implementasi algoritma dan struktur data nyata.

---

## 📦 Deskripsi

**DepSolve CLI** adalah aplikasi command-line berbasis Python yang mensimulasikan cara kerja package manager modern seperti `npm`, `pip`, atau `apt`. Aplikasi ini dirancang sebagai tools edukatif yang menekankan penerapan **struktur data** dan **algoritma** secara nyata.

Setiap package dapat memiliki ketergantungan (dependency) terhadap package lain. Hubungan tersebut dimodelkan sebagai **directed graph** yang dianalisis menggunakan berbagai algoritma untuk menentukan urutan instalasi, mendeteksi circular dependency, dan memvalidasi kompatibilitas versi.

---

## ✨ Fitur Utama

| Fitur | Perintah | Deskripsi |
|---|---|---|
| Install Package | `depsolve install <package>` | Menginstal package beserta seluruh dependency-nya |
| Remove Package | `depsolve remove <package>` | Menghapus package jika tidak digunakan package lain |
| Dependency Tree | `depsolve tree <package>` | Menampilkan struktur dependency berbentuk tree |
| Conflict Detection | `depsolve conflicts` | Mendeteksi konflik dependency antar package |
| Circular Dependency | `depsolve check <package>` | Mendeteksi circular dependency menggunakan DFS |
| Package List | `depsolve list` | Menampilkan seluruh package yang terinstal |
| Version Validation | (otomatis saat install) | Memvalidasi kompatibilitas versi package |

### Contoh Output

```bash
$ depsolve install flask
[✓] Resolving dependencies for flask...
[✓] Installing werkzeug==3.0.1
[✓] Installing jinja2==3.1.0
[✓] Installing flask==3.0.0
Done! 3 package(s) installed.

$ depsolve tree django
django
├── pytz
├── sqlparse
└── asgiref

$ depsolve conflicts
[!] Conflict detected: package-a requires werkzeug>=2.0, but werkzeug==1.0 is installed.
```

---

## 🗂️ Struktur Data yang Digunakan

### 1. Graph (Adjacency List)
Struktur utama untuk merepresentasikan hubungan dependency antar package.
- Setiap **package** → node/vertex
- Setiap **dependency** → directed edge
- Disimpan sebagai adjacency list (lebih hemat memori dibanding adjacency matrix)

```
Flask -> [Werkzeug, Jinja2]
Django -> [pytz, sqlparse, asgiref]
```

### 2. Hash Map (Dictionary)
Digunakan untuk pencarian package dengan kompleksitas rata-rata **O(1)**.
- Lookup package berdasarkan nama
- Cache dependency
- Menyimpan versi dan status package

### 3. Stack (LIFO)
Digunakan dalam proses DFS dan cycle detection.
- Menyimpan node yang sedang diproses
- Mendeteksi node dalam recursion path

### 4. Queue (FIFO)
Digunakan dalam proses BFS traversal.
- Eksplorasi dependency level-by-level
- Antrian proses instalasi bertahap

---

## ⚙️ Algoritma yang Digunakan

| Algoritma | Fungsi | Kompleksitas |
|---|---|---|
| **DFS** (Depth First Search) | Traversal dependency, cycle detection | O(V + E) |
| **BFS** (Breadth First Search) | Eksplorasi dependency per level | O(V + E) |
| **Topological Sort** | Menentukan urutan instalasi yang benar | O(V + E) |
| **Cycle Detection** | Mendeteksi circular dependency | O(V + E) |

> `V` = jumlah package (node), `E` = jumlah dependency (edge)

### Contoh Topological Sort

```
Flask bergantung pada Werkzeug & Jinja2
→ Urutan instalasi: Werkzeug → Jinja2 → Flask
```

### Contoh Circular Dependency

```
A → B → C → A  ← TERDETEKSI! Instalasi dibatalkan.
```

---

## 🗄️ Skema Database

Seluruh data disimpan menggunakan **MySQL** yang diakses melalui **phpMyAdmin**.

### Tabel `packages`
| Field | Tipe | Keterangan |
|---|---|---|
| id | INT | Primary key |
| name | VARCHAR(100) | Nama package |
| version | VARCHAR(20) | Versi package |

### Tabel `dependencies`
| Field | Tipe | Keterangan |
|---|---|---|
| id | INT | Primary key |
| package_id | INT | Foreign key → packages.id |
| dependency_id | INT | Foreign key → packages.id |
| min_version | VARCHAR(20) | Versi minimum yang dibutuhkan |

### Tabel `installed_packages`
| Field | Tipe | Keterangan |
|---|---|---|
| id | INT | Primary key |
| package_id | INT | Foreign key → packages.id |
| install_date | DATETIME | Waktu instalasi |

---

## 🛠️ Teknologi yang Digunakan

| Teknologi | Fungsi |
|---|---|
| **Python** | Bahasa utama aplikasi |
| **MySQL** | Database penyimpanan package |
| **phpMyAdmin** | Database management GUI |
| **Click / Argparse** | CLI framework |
| **SQLAlchemy** | ORM untuk koneksi database |
| **Rich** | Tampilan terminal yang interaktif & berwarna |

---

## 🚀 Cara Instalasi & Menjalankan

### 1. Clone Repository

```bash
git clone https://github.com/username/depsolve-cli.git
cd depsolve-cli
```

### 2. Buat Virtual Environment

```bash
python -m venv venv
source venv/bin/activate        # Linux/Mac
venv\Scripts\activate           # Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Konfigurasi Database

Pastikan MySQL sudah berjalan, lalu buat database dan import skema:

```bash
mysql -u root -p < database/schema.sql
```

Edit file konfigurasi koneksi database di `config.py`:

```python
DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "your_password"
DB_NAME = "depsolve"
```

### 5. Jalankan Aplikasi

```bash
python main.py --help
```

---

---

## 🔄 Alur Sistem (Install Package)

```
User → depsolve install flask
         │
         ▼
  Cek package di database
         │
         ▼
  Bangun dependency graph
         │
         ▼
  Cycle detection (DFS)
    ├─ Ada cycle? → ERROR, batalkan
    └─ Tidak ada → lanjut
         │
         ▼
  Topological Sort
         │
         ▼
  Install dependency satu per satu
         │
         ▼
  Install package utama (flask)
         │
         ▼
  Simpan ke tabel installed_packages
```

---

## 📊 Mapping Fitur → Struktur Data & Algoritma

| Fitur | Struktur Data | Algoritma |
|---|---|---|
| Install Package | Graph, Hash Map, Queue | DFS, Topological Sort |
| Remove Package | Hash Map, Graph | Traversal, Validasi Dependents |
| Dependency Tree | Graph, Stack, Tree | DFS |
| Conflict Detection | Graph, Hash Map | Traversal + Perbandingan Versi |
| Circular Dependency | Graph, Stack | DFS Cycle Detection |
| Package List | List, Hash Map | Query Database |
| Version Validation | Hash Map | Perbandingan Versi |

---

## 🎓 Relevansi Mata Kuliah

Project ini dikembangkan sebagai implementasi nyata dari mata kuliah **Struktur Data**, mencakup:

- ✅ Graph & representasi adjacency list
- ✅ DFS (Depth First Search)
- ✅ BFS (Breadth First Search)
- ✅ Stack & Queue
- ✅ Hash Map / Dictionary
- ✅ Topological Sort
- ✅ Cycle Detection
- ✅ Rekursi

---

## 🔮 Potensi Pengembangan

- [ ] Semantic versioning (`^1.2.0`, `~1.2`, `>=1.0 <2.0`)
- [ ] Online repository simulation
- [ ] Package publishing
- [ ] Auto update
- [ ] Dependency locking (`depsolve.lock`)
- [ ] Local cache system
- [ ] Package integrity hash (checksum)
- [ ] Multi-user repository

---

## 👨‍💻 Tim Pengembang

| Nama | NIM | Role |
|---|---|---|
| Lionel Jevon Chrismana Putra | 25091397019| Full Stack |

---

## 📄 Lisensi

Project ini dibuat untuk keperluan akademik dan idle.

---

<div align="center">
  <strong>DepSolve CLI</strong> — Built with 🐍 Python & ❤️ Data Structures
</div>
