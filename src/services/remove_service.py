from src.database.connection import SessionLocal
from src.models.package import Package
from src.models.installed_package import InstalledPackage
from src.models.dependency import Dependency
from src.graph.graph_builder import GraphBuilder

class RemoveService:
    def __init__(self):
        self.db = SessionLocal()
        self.builder = GraphBuilder()

    def remove_package(self, package_name):
        target_pkg = self.db.query(Package).filter(Package.name == package_name).first()
        
        if not target_pkg:
            print(f"❌ Error: Paket '{package_name}' tidak ditemukan di repository.")
            return False

        is_installed = self.db.query(InstalledPackage).filter(
            InstalledPackage.package_id == target_pkg.id
        ).first()

        if not is_installed:
            print(f"❌ Error: Paket '{package_name}' memang belum terinstal di sistem.")
            return False

        installed_ids = self.db.query(InstalledPackage.package_id).all()
        installed_ids = [r[0] for r in installed_ids]

        dependents = self.db.query(Package.name).join(
            Dependency,
            Package.id == Dependency.package_id
        ).filter(
            Dependency.dependency_id == target_pkg.id,
            Package.id.in_(installed_ids)
        ).all()

        if dependents:
            dep_names = [d[0] for d in dependents]
            print(f"🚫 Gagal menghapus '{package_name}'!")
            print(f"⚠️ Paket ini masih dibutuhkan oleh: {', '.join(dep_names)}")
            print("Pesan: Hapus paket-paket di atas terlebih dahulu.")
            return False

        try:
            self.db.delete(is_installed)
            self.db.commit()
            print(f"🗑️ Berhasil menghapus paket: {package_name}")
            return True

        except Exception as e:
            self.db.rollback()
            print(f"❌ Terjadi kesalahan database: {e}")
            return False

        finally:
            self.db.close()

if __name__ == "__main__":
    service = RemoveService()

    print("--- Test 1: Hapus dependency yang masih dipakai ---")
    service.remove_package("Jinja2")

    print("\n--- Test 2: Hapus paket paling atas ---")
    service.remove_package("Flask")