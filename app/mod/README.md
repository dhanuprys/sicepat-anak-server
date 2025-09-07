# 🎯 Stunting Prediction Module

Modul Python untuk prediksi stunting menggunakan SVM (Support Vector Machine) dengan kernel linear. Modul ini dapat digunakan di webserver atau aplikasi Python lainnya.

## 📋 Fitur Utama

- ✅ **Machine Learning**: SVM dengan kernel linear untuk klasifikasi multiclass
- ✅ **Preprocessing**: StandardScaler dan LabelEncoder otomatis
- ✅ **API Ready**: Dapat digunakan di webserver (Flask, FastAPI, Django)
- ✅ **Model Persistence**: Save/load model yang sudah di-training
- ✅ **Smart Caching**: Cache otomatis untuk mempercepat loading model
- ✅ **Batch Prediction**: Prediksi multiple data sekaligus
- ✅ **Error Handling**: Validasi input dan error handling yang robust

## 🚀 Instalasi

### 1. Install Dependensi

```bash
pip install -r requirements.txt
```

### 2. Pastikan Dataset Tersedia

File `data_balita.xlsx` harus tersedia di folder yang sama dengan script Python.

## 📚 Cara Penggunaan

### Basic Usage

```python
from stunting_predictor import create_predictor_from_dataset

# Buat predictor dengan cache enabled (default)
predictor = create_predictor_from_dataset(use_cache=True)

# Prediksi single data
result = predictor.predict(umur=24, jenis_kelamin="Laki-laki", tinggi=85.5)
print(f"Hasil prediksi: {result['prediction']}")

# Batch prediction
test_data = [
    {"umur": 12, "jenis_kelamin": "Perempuan", "tinggi_badan": 70.2},
    {"umur": 36, "jenis_kelamin": "Laki-laki", "tinggi_badan": 95.8}
]
batch_results = predictor.batch_predict(test_data)
```

### Advanced Usage

```python
from stunting_predictor import StuntingPredictor

# Buat instance manual
predictor = StuntingPredictor()

# Load dataset dan training
df = predictor.load_dataset("path/to/dataset.xlsx")
X, y = predictor.preprocess_data(df)
metrics = predictor.train_model(X, y)

# Save model
predictor.save_model("model.pkl", "scaler.pkl", "encoder.pkl")

# Load model yang sudah ada
new_predictor = StuntingPredictor()
new_predictor.load_model("model.pkl", "scaler.pkl", "encoder.pkl")
```

## 🌐 Webserver Integration

### Flask Example

```python
from flask import Flask, request, jsonify
from stunting_predictor import create_predictor_from_dataset

app = Flask(__name__)
predictor = create_predictor_from_dataset()

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    result = predictor.predict(
        umur=data['umur'],
        jenis_kelamin=data['jenis_kelamin'],
        tinggi=data['tinggi_badan']
    )
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
```

### FastAPI Example

```python
from fastapi import FastAPI
from pydantic import BaseModel
from stunting_predictor import create_predictor_from_dataset

app = FastAPI()
predictor = create_predictor_from_dataset()

class PredictionInput(BaseModel):
    umur: int
    jenis_kelamin: str
    tinggi_badan: float

@app.post("/predict")
async def predict(input_data: PredictionInput):
    result = predictor.predict(
        umur=input_data.umur,
        jenis_kelamin=input_data.jenis_kelamin,
        tinggi=input_data.tinggi_badan
    )
    return result
```

## 📊 Format Input/Output

### Input Format

```json
{
    "umur": 24,
    "jenis_kelamin": "Laki-laki",
    "tinggi_badan": 85.5
}
```

### Output Format

```json
{
    "prediction": "Normal",
    "prediction_code": 0,
    "confidence": 0.85,
    "input_data": {
        "umur": 24,
        "jenis_kelamin": "Laki-laki",
        "tinggi_badan": 85.5
    },
    "available_classes": ["Severely Stunted", "Stunted", "Normal", "Tinggi"],
    "model_info": {
        "algorithm": "SVM (Linear Kernel)",
        "is_trained": true
    }
}
```

## 🔧 Testing

### Test Cache System

```bash
python cache_example.py
```

### Test Modul Utama

```bash
python stunting_predictor.py
```

### Test Webserver

```bash
python webserver_simple.py
```

Kemudian buka browser di `http://localhost:8000`

## 📁 File Structure

```
stunting/
├── data_balita.xlsx          # Dataset (harus tersedia)
├── stunting_predictor.py     # Modul utama dengan cache system
├── cache_example.py          # Contoh penggunaan cache
├── webserver_simple.py       # Contoh webserver
├── requirements.txt           # Dependensi
├── cache/                    # Cache directory (otomatis dibuat)
│   ├── stunting_model.pkl    # Cached model
│   ├── stunting_scaler.pkl   # Cached scaler
│   ├── stunting_encoder.pkl  # Cached encoder
│   └── stunting_metadata.json # Cache metadata
└── README.md                 # Dokumentasi ini
```

## 🐛 Troubleshooting

### Error: "File tidak ditemukan"

Pastikan file `data_balita.xlsx` tersedia di folder yang sama dengan script Python.

### Error: "Model belum di-training"

Jalankan `create_predictor_from_dataset()` atau `train_model()` terlebih dahulu.

### Error: "Jenis kelamin harus 'Laki-laki' atau 'Perempuan'"

Pastikan input jenis kelamin menggunakan format yang benar (case-insensitive).

### Error: "Cache tidak lengkap"

Cache mungkin rusak atau tidak lengkap. Gunakan `predictor.clear_cache()` untuk reset.

### Error: "Model belum di-training"

Pastikan `use_cache=True` atau jalankan training manual. Check cache status dengan `predictor.cache_status()`.

## 📈 Model Performance

Model SVM dengan kernel linear memberikan:
- **Accuracy**: Biasanya 85-95% tergantung dataset
- **Speed**: Prediksi cepat untuk real-time applications
- **Interpretability**: Model yang mudah diinterpretasi

## 🚀 Smart Caching System

Modul ini dilengkapi dengan sistem cache otomatis yang mempercepat loading model secara signifikan.

### Cache Features

- ✅ **Auto-cache**: Model otomatis disimpan ke cache setelah training
- ✅ **Fast Loading**: Load model dari cache dalam hitungan detik
- ✅ **Metadata Tracking**: Informasi lengkap tentang cached model
- ✅ **Cache Management**: Fungsi untuk manage cache (clear, status, dll)

### Cache Usage

```python
# Default: menggunakan cache (recommended untuk production)
predictor = create_predictor_from_dataset(use_cache=True)

# Tanpa cache: training ulang setiap kali (untuk development/testing)
predictor = create_predictor_from_dataset(use_cache=False)

# Custom cache directory
predictor = create_predictor_from_dataset(use_cache=True, cache_dir="my_cache")
```

### Cache Management

```python
# Check cache status
cache_status = predictor.cache_status()
print(json.dumps(cache_status, indent=2))

# Clear cache (force retraining)
predictor.clear_cache()

# Manual save to cache
predictor.save_to_cache()

# Load from cache
predictor.load_from_cache()
```

### Performance Comparison

- **Training dari dataset**: 10-30 detik (tergantung dataset size)
- **Loading dari cache**: 0.1-1 detik
- **Speedup**: 10-100x lebih cepat dengan cache!

## 🔄 Retraining Model

```python
# Retrain dengan dataset baru
metrics = predictor.retrain_from_dataset("new_dataset.xlsx")
print(f"New accuracy: {metrics['test_accuracy']:.4f}")

# Save model baru (otomatis ke cache)
predictor.save_to_cache()

# Atau save manual
predictor.save_model("new_model.pkl", "new_scaler.pkl", "new_encoder.pkl")
```

## 📞 Support

Jika ada masalah atau pertanyaan, periksa:
1. Error message yang muncul
2. Format input data
3. Dataset yang digunakan
4. Dependensi yang terinstall

## 📝 License

Modul ini dibuat untuk keperluan akademis dan penelitian. Gunakan dengan bijak.
