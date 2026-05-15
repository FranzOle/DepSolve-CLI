from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.theme import Theme

# Kustomisasi tema agar warna konsisten di seluruh aplikasi
custom_theme = Theme({
    "info": "cyan",
    "warning": "yellow",
    "error": "bold red",
    "success": "bold green",
    "header": "bold magenta"
})

class DisplayHelper:
    def __init__(self):
        self.console = Console(theme=custom_theme)

    def print_banner(self):
        """Menampilkan banner utama aplikasi saat dijalankan."""
        banner_text = Text("DEPSOLVE CLI", style="header")
        banner_text.append("\nPackage Dependency Resolver - UAS Edition", style="italic white")
        
        self.console.print(Panel(
            banner_text,
            expand=False,
            border_style="magenta",
            subtitle="v1.0.0"
        ))

    def print_success(self, message):
        self.console.print(f"[success]✅ SUCCESS:[/success] {message}")

    def print_error(self, message):
        self.console.print(f"[error]❌ ERROR:[/error] {message}")

    def print_info(self, message):
        self.console.print(f"[info]💡 INFO:[/info] {message}")

    def display_installed_table(self, packages_data):
        """
        Menampilkan tabel paket yang terinstal.
        Expects: List of dicts [{'id': 1, 'name': 'Flask', 'version': '3.0.0', 'date': '...'}]
        """
        table = Table(title="Daftar Paket Terinstal", border_style="cyan")

        table.add_column("ID", justify="right", style="dim")
        table.add_column("Package Name", style="bold white")
        table.add_column("Version", justify="center", style="green")
        table.add_column("Installation Date", style="dim")

        if not packages_data:
            table.add_row("-", "Tidak ada paket", "-", "-")
        else:
            for pkg in packages_data:
                table.add_row(
                    str(pkg['id']),
                    pkg['name'],
                    pkg['version'],
                    pkg['date']
                )

        self.console.print(table)

# --- TEST TAMPILAN ---
if __name__ == "__main__":
    ui = DisplayHelper()
    ui.print_banner()
    ui.print_success("Ini adalah contoh pesan sukses.")
    ui.print_error("Ini adalah contoh pesan error.")
    
    # Simulasi data dari Database
    dummy_data = [
        {'id': 1, 'name': 'Flask', 'version': '3.0.0', 'date': '2023-12-01 10:00'},
        {'id': 2, 'name': 'Jinja2', 'version': '3.1.2', 'date': '2023-12-01 10:01'}
    ]
    ui.display_installed_table(dummy_data)