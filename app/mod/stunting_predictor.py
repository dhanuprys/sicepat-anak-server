"""
Modul Prediksi Stunting dengan SVM (Kernel Linear)
Modul ini berisi class untuk prediksi stunting tanpa GUI, dapat digunakan di webserver
"""

import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.svm import SVC
from typing import Dict, List, Union, Tuple
import joblib
import json


class StuntingPredictor:
    """
    Class untuk prediksi stunting menggunakan SVM dengan kernel linear
    Mendukung klasifikasi multiclass dan dapat digunakan di webserver
    """
    
    def __init__(self, model_path: str = None, scaler_path: str = None, encoder_path: str = None, 
                 cache_dir: str = "cache", auto_cache: bool = True):
        """
        Inisialisasi StuntingPredictor
        
        Args:
            model_path: Path ke file model yang sudah di-save (opsional)
            scaler_path: Path ke file scaler yang sudah di-save (opsional)
            encoder_path: Path ke file encoder yang sudah di-save (opsional)
            cache_dir: Directory untuk menyimpan cache model
            auto_cache: Apakah otomatis menggunakan cache jika tersedia
        """
        self.model = None
        self.scaler = None
        self.label_encoder = None
        self.gender_map = {"laki-laki": 1, "perempuan": 0}
        self.is_trained = False
        self.cache_dir = cache_dir
        self.auto_cache = auto_cache
        
        # Buat cache directory jika belum ada
        if not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir)
        
        # Load model yang sudah ada jika tersedia
        if model_path and scaler_path and encoder_path:
            self.load_model(model_path, scaler_path, encoder_path)
        elif self.auto_cache:
            # Coba load dari cache otomatis
            self.load_from_cache()
    
    def load_dataset(self, file_path: str = None) -> pd.DataFrame:
        """
        Load dataset dari file Excel
        
        Args:
            file_path: Path ke file Excel, jika None akan menggunakan default
            
        Returns:
            DataFrame yang sudah di-load
        """
        if file_path is None:
            # Gunakan path default
            base_dir = os.path.dirname(os.path.abspath(__file__))
            file_path = os.path.join(base_dir, "data_balita.xlsx")
        
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File tidak ditemukan di path: {file_path}")
        
        df = pd.read_excel(file_path)
        return df
    
    def preprocess_data(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.Series]:
        """
        Preprocessing data untuk training
        
        Args:
            df: DataFrame mentah dari dataset
            
        Returns:
            Tuple (X, y) dengan X sebagai fitur dan y sebagai target
        """
        # Copy dataframe untuk menghindari modifikasi original
        df_processed = df.copy()
        
        # Mapping Jenis Kelamin (menggunakan logika yang sama dengan program asli)
        df_processed['Jenis Kelamin'] = df_processed['Jenis Kelamin'].str.lower().map(self.gender_map)
        
        # Encode target menggunakan LabelEncoder (menggunakan logika yang sama dengan program asli)
        self.label_encoder = LabelEncoder()
        df_processed['Stunting'] = self.label_encoder.fit_transform(df_processed['Stunting'])
        
        # Fitur dan target (menggunakan nama kolom yang sama dengan program asli)
        X = df_processed[['Umur', 'Jenis Kelamin', 'Tinggi Badan']]
        y = df_processed['Stunting']
        
        return X, y
    
    def train_model(self, X: pd.DataFrame, y: pd.Series, test_size: float = 0.2, 
                   random_state: int = 42) -> Dict[str, float]:
        """
        Training model SVM
        
        Args:
            X: Fitur training
            y: Target training
            test_size: Proporsi data test
            random_state: Random seed untuk reproducibility
            
        Returns:
            Dictionary berisi metrics evaluasi
        """
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state, stratify=y
        )
        
        # Scaling
        self.scaler = StandardScaler()
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Training model
        self.model = SVC(kernel='linear', random_state=random_state)
        self.model.fit(X_train_scaled, y_train)
        
        # Evaluasi model (menggunakan logika yang sama dengan program asli)
        train_score = self.model.score(X_train_scaled, y_train)
        test_score = self.model.score(X_test_scaled, y_test)
        
        self.is_trained = True
        
        # Auto-save ke cache jika auto_cache enabled
        if self.auto_cache:
            self.save_to_cache()
        
        return {
            'train_accuracy': train_score,
            'test_accuracy': test_score,
            'n_samples': len(X),
            'n_features': X.shape[1],
            'n_classes': len(np.unique(y))
        }
    
    def predict(self, umur: int, jenis_kelamin: str, tinggi: float) -> Dict[str, Union[str, float, List[str]]]:
        """
        Prediksi stunting untuk data baru
        
        Args:
            umur: Umur dalam bulan
            jenis_kelamin: 'Laki-laki' atau 'Perempuan'
            tinggi: Tinggi badan dalam cm
            
        Returns:
            Dictionary berisi hasil prediksi dan informasi tambahan
        """
        if not self.is_trained:
            raise ValueError("Model belum di-training. Jalankan train_model() terlebih dahulu.")
        
        # Validasi input
        jenis_kelamin_lower = jenis_kelamin.strip().lower()
        if jenis_kelamin_lower not in self.gender_map:
            raise ValueError("Jenis kelamin harus 'Laki-laki' atau 'Perempuan'")
        
        if umur < 0 or umur > 60:
            raise ValueError("Umur harus antara 0-60 bulan")
        
        if tinggi < 0 or tinggi > 200:
            raise ValueError("Tinggi badan harus antara 0-200 cm")
        
        # Prepare data untuk prediksi (menggunakan nama kolom yang sama dengan training)
        input_data = pd.DataFrame({
            'Umur': [umur],
            'Jenis Kelamin': [self.gender_map[jenis_kelamin_lower]],
            'Tinggi Badan': [tinggi]
        })
        
        # Scaling
        input_scaled = self.scaler.transform(input_data)
        
        # Prediksi
        prediction = self.model.predict(input_scaled)[0]
        # SVM linear tidak selalu mendukung predict_proba, gunakan try-except
        try:
            prediction_proba = self.model.predict_proba(input_scaled)[0]
        except:
            prediction_proba = None
        
        # Decode hasil prediksi (menggunakan logika yang sama dengan program asli)
        predicted_label = self.label_encoder.inverse_transform([prediction])[0]
        
        # Dapatkan semua label yang tersedia
        available_labels = self.label_encoder.classes_.tolist()
        
        result = {
            'prediction': predicted_label,
            'prediction_code': int(prediction),
            'confidence': float(max(prediction_proba)) if prediction_proba is not None else None,
            'input_data': {
                'umur': umur,
                'jenis_kelamin': jenis_kelamin,
                'tinggi_badan': tinggi
            },
            'available_classes': available_labels,
            'model_info': {
                'algorithm': 'SVM (Linear Kernel)',
                'is_trained': self.is_trained
            }
        }
        
        return result
    
    def batch_predict(self, data_list: List[Dict]) -> List[Dict]:
        """
        Prediksi batch untuk multiple data
        
        Args:
            data_list: List of dictionaries dengan keys: 'umur', 'jenis_kelamin', 'tinggi_badan'
            
        Returns:
            List of prediction results
        """
        results = []
        for data in data_list:
            try:
                result = self.predict(
                    umur=data['umur'],
                    jenis_kelamin=data['jenis_kelamin'],
                    tinggi=data['tinggi_badan']  # Perbaiki: gunakan 'tinggi' bukan 'tinggi_badan'
                )
                results.append(result)
            except Exception as e:
                results.append({
                    'error': str(e),
                    'input_data': data
                })
        
        return results
    
    def save_model(self, model_path: str, scaler_path: str, encoder_path: str):
        """
        Save model, scaler, dan encoder ke file
        
        Args:
            model_path: Path untuk save model
            scaler_path: Path untuk save scaler
            encoder_path: Path untuk save encoder
        """
        if not self.is_trained:
            raise ValueError("Model belum di-training")
        
        # Save model
        joblib.dump(self.model, model_path)
        
        # Save scaler
        joblib.dump(self.scaler, scaler_path)
        
        # Save encoder
        joblib.dump(self.label_encoder, encoder_path)
    
    def load_model(self, model_path: str, scaler_path: str, encoder_path: str):
        """
        Load model, scaler, dan encoder dari file
        
        Args:
            model_path: Path ke file model
            scaler_path: Path ke file scaler
            encoder_path: Path ke file encoder
        """
        if not all(os.path.exists(path) for path in [model_path, scaler_path, encoder_path]):
            raise FileNotFoundError("Salah satu file model tidak ditemukan")
        
        self.model = joblib.load(model_path)
        self.scaler = joblib.load(scaler_path)
        self.label_encoder = joblib.load(encoder_path)
        self.is_trained = True
    
    def get_model_info(self) -> Dict:
        """
        Mendapatkan informasi model
        
        Returns:
            Dictionary berisi informasi model
        """
        if not self.is_trained:
            return {'status': 'Model belum di-training'}
        
        return {
            'status': 'Model sudah di-training',
            'algorithm': 'SVM (Linear Kernel)',
            'n_features': self.scaler.n_features_in_ if self.scaler else None,
            'n_classes': len(self.label_encoder.classes_) if self.label_encoder else None,
            'available_classes': self.label_encoder.classes_.tolist() if self.label_encoder else None,
            'gender_mapping': self.gender_map
        }
    
    def get_cache_paths(self) -> tuple:
        """
        Mendapatkan path untuk file cache
        
        Returns:
            Tuple (model_path, scaler_path, encoder_path, metadata_path)
        """
        model_path = os.path.join(self.cache_dir, "stunting_model.pkl")
        scaler_path = os.path.join(self.cache_dir, "stunting_scaler.pkl")
        encoder_path = os.path.join(self.cache_dir, "stunting_encoder.pkl")
        metadata_path = os.path.join(self.cache_dir, "stunting_metadata.json")
        return model_path, scaler_path, encoder_path, metadata_path
    
    def save_to_cache(self):
        """Save model ke cache directory"""
        if not self.is_trained:
            print("⚠️  Model belum di-training, tidak bisa disimpan ke cache")
            return False
        
        try:
            model_path, scaler_path, encoder_path, metadata_path = self.get_cache_paths()
            
            # Save model components
            joblib.dump(self.model, model_path)
            joblib.dump(self.scaler, scaler_path)
            joblib.dump(self.label_encoder, encoder_path)
            
            # Save metadata
            metadata = {
                'algorithm': 'SVM (Linear Kernel)',
                'n_features': self.scaler.n_features_in_ if self.scaler else None,
                'n_classes': len(self.label_encoder.classes_) if self.label_encoder else None,
                'available_classes': self.label_encoder.classes_.tolist() if self.label_encoder else None,
                'gender_mapping': self.gender_map,
                'cache_timestamp': pd.Timestamp.now().isoformat()
            }
            
            with open(metadata_path, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=2, ensure_ascii=False)
            
            print(f"✅ Model berhasil disimpan ke cache: {self.cache_dir}")
            return True
            
        except Exception as e:
            print(f"❌ Error saving to cache: {str(e)}")
            return False
    
    def load_from_cache(self) -> bool:
        """
        Load model dari cache directory
        
        Returns:
            True jika berhasil, False jika gagal
        """
        try:
            model_path, scaler_path, encoder_path, metadata_path = self.get_cache_paths()
            
            # Check if all cache files exist
            if not all(os.path.exists(path) for path in [model_path, scaler_path, encoder_path, metadata_path]):
                print("⚠️  Cache tidak lengkap, akan training dari awal")
                return False
            
            # Load model components
            self.model = joblib.load(model_path)
            self.scaler = joblib.load(scaler_path)
            self.label_encoder = joblib.load(encoder_path)
            
            # Load metadata
            with open(metadata_path, 'r', encoding='utf-8') as f:
                metadata = json.load(f)
            
            self.is_trained = True
            
            print(f"✅ Model berhasil di-load dari cache: {self.cache_dir}")
            print(f"📊 Cache info: {metadata.get('n_classes', 'Unknown')} classes, "
                  f"{metadata.get('n_features', 'Unknown')} features")
            print(f"⏰ Cache timestamp: {metadata.get('cache_timestamp', 'Unknown')}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error loading from cache: {str(e)}")
            return False
    
    def clear_cache(self):
        """Hapus semua file cache"""
        try:
            model_path, scaler_path, encoder_path, metadata_path = self.get_cache_paths()
            
            for path in [model_path, scaler_path, encoder_path, metadata_path]:
                if os.path.exists(path):
                    os.remove(path)
                    print(f"🗑️  Deleted: {path}")
            
            print("✅ Cache berhasil dibersihkan")
            
        except Exception as e:
            print(f"❌ Error clearing cache: {str(e)}")
    
    def cache_status(self) -> Dict:
        """
        Mendapatkan status cache
        
        Returns:
            Dictionary berisi status cache
        """
        model_path, scaler_path, encoder_path, metadata_path = self.get_cache_paths()
        
        cache_files = {
            'model': os.path.exists(model_path),
            'scaler': os.path.exists(scaler_path),
            'encoder': os.path.exists(encoder_path),
            'metadata': os.path.exists(metadata_path)
        }
        
        cache_complete = all(cache_files.values())
        
        if cache_complete:
            try:
                with open(metadata_path, 'r', encoding='utf-8') as f:
                    metadata = json.load(f)
                cache_info = metadata
            except:
                cache_info = {}
        else:
            cache_info = {}
        
        return {
            'cache_enabled': self.auto_cache,
            'cache_directory': self.cache_dir,
            'cache_complete': cache_complete,
            'cache_files': cache_files,
            'cache_info': cache_info
        }
    
    def retrain_from_dataset(self, file_path: str = None, **kwargs) -> Dict[str, float]:
        """
        Retrain model dari dataset baru
        
        Args:
            file_path: Path ke dataset baru
            **kwargs: Parameter tambahan untuk train_model
            
        Returns:
            Dictionary berisi metrics evaluasi
        """
        df = self.load_dataset(file_path)
        X, y = self.preprocess_data(df)
        return self.train_model(X, y, **kwargs)


# Fungsi utility untuk webserver
def create_predictor_from_dataset(file_path: str = None, use_cache: bool = True, 
                                cache_dir: str = "cache") -> StuntingPredictor:
    """
    Factory function untuk membuat StuntingPredictor dan training dari dataset
    
    Args:
        file_path: Path ke dataset Excel
        use_cache: Apakah menggunakan cache
        cache_dir: Directory untuk cache
        
    Returns:
        StuntingPredictor instance yang sudah di-training
    """
    predictor = StuntingPredictor(auto_cache=use_cache, cache_dir=cache_dir)
    
    # Jika cache tersedia dan enabled, model sudah di-load otomatis
    if predictor.is_trained:
        print("🚀 Model loaded dari cache, siap digunakan!")
        return predictor
    
    # Jika tidak ada cache, training dari dataset
    print("📊 Training model dari dataset...")
    df = predictor.load_dataset(file_path)
    X, y = predictor.preprocess_data(df)
    predictor.train_model(X, y)
    
    print("✅ Model berhasil di-training dan disimpan ke cache!")
    return predictor


def predict_single(umur: int, jenis_kelamin: str, tinggi: float, 
                  model_path: str, scaler_path: str, encoder_path: str) -> Dict:
    """
    Fungsi utility untuk prediksi single data tanpa membuat instance
    
    Args:
        umur: Umur dalam bulan
        jenis_kelamin: 'Laki-laki' atau 'Perempuan'
        tinggi: Tinggi badan dalam cm
        model_path: Path ke file model
        scaler_path: Path ke file scaler
        encoder_path: Path ke file encoder
        
    Returns:
        Dictionary berisi hasil prediksi
    """
    predictor = StuntingPredictor()
    predictor.load_model(model_path, scaler_path, encoder_path)
    return predictor.predict(umur, jenis_kelamin, tinggi)


# Contoh penggunaan untuk testing
if __name__ == "__main__":
    # Contoh penggunaan modul dengan cache
    try:
        print("🚀 Testing StuntingPredictor dengan Cache System")
        print("=" * 60)
        
        # Test 1: Buat predictor dengan cache enabled
        print("\n📊 Test 1: Membuat predictor dengan cache...")
        predictor = create_predictor_from_dataset(use_cache=True, cache_dir="model")
        
        # Test 2: Check cache status
        print("\n📋 Test 2: Cache status...")
        cache_status = predictor.cache_status()
        print(json.dumps(cache_status, indent=2, ensure_ascii=False))
        
        # Test 3: Single prediction
        print("\n🎯 Test 3: Single prediction...")
        result = predictor.predict(24, "Laki-laki", 85.5)
        print(f"Hasil prediksi: {result['prediction']}")
        
        # Test 4: Batch prediction
        print("\n📦 Test 4: Batch prediction...")
        test_data = [
            {"umur": 12, "jenis_kelamin": "Perempuan", "tinggi_badan": 70.2},
            {"umur": 36, "jenis_kelamin": "Laki-laki", "tinggi_badan": 95.8}
        ]
        
        batch_results = predictor.batch_predict(test_data)
        for i, result in enumerate(batch_results):
            if 'error' in result:
                print(f"Data {i+1}: ❌ {result['error']}")
            else:
                print(f"Data {i+1}: ✅ {result['prediction']}")
        
        # Test 5: Test cache performance (kedua kalinya)
        print("\n⚡ Test 5: Testing cache performance...")
        print("Membuat predictor kedua kalinya (seharusnya dari cache)...")
        
        predictor2 = create_predictor_from_dataset(use_cache=True)
        print(f"Predictor 2 trained: {predictor2.is_trained}")
        
        # Test 6: Manual save/load
        # print("\n💾 Test 6: Manual save/load...")
        # predictor.save_model("manual_model.pkl", "manual_scaler.pkl", "manual_encoder.pkl")
        # print("Model berhasil disimpan manual!")
        
        # Test 7: Cache management
        print("\n🔧 Test 7: Cache management...")
        print("Cache directory:", predictor.cache_dir)
        print("Cache files:", os.listdir(predictor.cache_dir))
        
        print("\n🎉 Semua test berhasil!")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
