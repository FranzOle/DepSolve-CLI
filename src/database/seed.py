from src.database.connection import SessionLocal, engine, Base
from src.models.package import Package
from src.models.dependency import Dependency
from src.models.installed_package import InstalledPackage

def seed_data():
    db = SessionLocal()
    try:
        db.query(InstalledPackage).delete()
        db.query(Dependency).delete()
        db.query(Package).delete()
        db.commit()

        p1 = Package(name="Flask", version="3.0.0")
        p2 = Package(name="Werkzeug", version="3.0.1")
        p3 = Package(name="Jinja2", version="3.1.0")
        p4 = Package(name="MarkupSafe", version="2.1.0")
        
        db.add_all([p1, p2, p3, p4])
        db.commit() 
        db.add_all([
            Dependency(package_id=p1.id, dependency_id=p2.id, min_version=">=2.0"),
            Dependency(package_id=p1.id, dependency_id=p3.id, min_version=">=3.0"),
            Dependency(package_id=p3.id, dependency_id=p4.id, min_version=">=2.0")
        ])
        installed = InstalledPackage(package_id=p4.id)
        db.add(installed)
        
        db.commit()
        print("✅ Database SEEDING LENGKAP!")
        print(f"Master: {p1.name}, {p2.name}, {p3.name}, {p4.name}")
        print(f"Status: {p4.name} sudah terhitung sebagai 'Installed'")

    except Exception as e:
        print(f"❌ Error saat seeding: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()