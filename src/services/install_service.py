from datetime import datetime
from src.database.connection import SessionLocal
from src.models.package import Package
from src.models.installed_package import InstalledPackage
from src.resolver.dependency_resolver import DependencyResolver
from sqlalchemy.exc import OperationalError

class InstallService:
    def __init__(self):
        # Kita tidak langsung buka session di __init__ agar tidak hang jika DB mati
        self.resolver = DependencyResolver()

    def _get_session(self):
        return SessionLocal()

    def install_package(self, package_name):
        """
        Eksekusi instalasi paket secara atomik dan profesional.
        """
        db = self._get_session()
        try:
            # 1. Cek Koneksi DB dulu (Safety First)
            db.execute("SELECT 1")
            
            # 2. Dapatkan antrian dari Resolver
            # Kita panggil resolver untuk hitung urutan & validasi versi
            queue, message = self.resolver.resolve_installation(package_name)

            if not queue:
                print(message)
                return False

            print(f"\n📦 [PHASE 1] Memulai instalasi: {package_name}")
            print(f"🔗 Menghitung dependensi... Ditemukan {len(queue)} paket.")

            # 3. Proses Instalasi (Looping Queue hasil Topological Sort)
            for pkg_name in queue:
                # Cari ID paket di repository (tabel packages)
                pkg = db.query(Package).filter(Package.name == pkg_name).first()
                
                if pkg:
                    # Cek apakah sudah terinstall (double check)
                    exists = db.query(InstalledPackage).filter(
                        InstalledPackage.package_id == pkg.id
                    ).first()
                    
                    if not exists:
                        # Sesuai ERD: package_id dan install_date
                        new_install = InstalledPackage(
                            package_id=pkg.id,
                            install_date=datetime.now() # Isi otomatis waktu skrg
                        )
                        db.add(new_install)
                        print(f"   ✅ Installed: {pkg_name} (v{pkg.version})")
                    else:
                        print(f"   ℹ️  Skipped: {pkg_name} (Sudah ada)")

            # 4. Finalisasi
            db.commit()
            print(f"\n✨ [SUCCESS] {package_name} siap digunakan!")
            return True

        except OperationalError:
            print("❌ DATABASE ERROR: Tidak bisa terhubung ke MySQL.")
            print("👉 Pastikan XAMPP/MySQL sudah dinyalakan (Status: Running).")
            return False
        except Exception as e:
            db.rollback()
            print(f"❌ SYSTEM ERROR: {str(e)}")
            return False
        finally:
            db.close()

if __name__ == "__main__":
    service = InstallService()
    # Tes Install Flask (Pastikan database SEEDING sudah dijalankan sebelumnya)
    service.install_package("Flask")