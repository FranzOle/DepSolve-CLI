import click
from src.cli.display import DisplayHelper
from src.services.install_service import InstallService
from src.services.remove_service import RemoveService
from src.commands.tree import TreeCommand
from src.database.connection import SessionLocal
from src.models.package import Package
from src.models.installed_package import InstalledPackage

# Inisialisasi Helper
ui = DisplayHelper()

@click.group()
def cli():
    """DepSolve CLI: Sistem Manajemen Dependensi Berbasis Graph (UAS Edition)"""
    pass

@cli.command()
@click.argument('package_name')
def install(package_name):
    """Menginstal paket beserta semua dependensinya secara otomatis."""
    ui.print_banner()
    service = InstallService()
    success = service.install_package(package_name)
    if not success:
        ui.print_error(f"Proses instalasi '{package_name}' dibatalkan.")

@cli.command()
@click.argument('package_name')
def remove(package_name):
    """Menghapus paket (Mencegah Broken Dependency)."""
    ui.print_banner()
    service = RemoveService()
    success = service.remove_package(package_name)
    if not success:
        ui.print_error(f"Gagal menghapus '{package_name}'.")

@cli.command()
@click.argument('package_name')
def tree(package_name):
    """Visualisasi hirarki dependensi menggunakan BFS."""
    ui.print_banner()
    cmd = TreeCommand()
    cmd.run(package_name)

@cli.command(name="list")
def list_installed():
    """Menampilkan semua paket yang sudah terpasang di sistem."""
    ui.print_banner()
    db = SessionLocal()
    try:
        # Query join untuk mendapatkan nama, versi, dan tanggal instalasi
        results = db.query(Package, InstalledPackage).join(
            InstalledPackage, Package.id == InstalledPackage.package_id
        ).all()

        packages_data = []
        for pkg, installed in results:
            packages_data.append({
                'id': pkg.id,
                'name': pkg.name,
                'version': pkg.version,
                'date': installed.install_date.strftime("%Y-%m-%d %H:%M")
            })
        
        ui.display_installed_table(packages_data)
    except Exception as e:
        ui.print_error(f"Gagal mengambil data dari database: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    cli()