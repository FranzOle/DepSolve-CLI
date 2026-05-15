import re

class VersionValidator:
    @staticmethod
    def parse_version(version_str):
        """
        Mengubah string '1.2.3' menjadi tuple (1, 2, 3) 
        agar bisa dibandingkan secara numerik.
        """
        if not version_str:
            return (0, 0, 0)
        numbers = re.findall(r'\d+', version_str)
        return tuple(map(int, numbers))

    @staticmethod
    def is_compatible(current_version, required_min_version):
        """
        Mengecek apakah current_version >= required_min_version.
        Contoh input: current='3.0.0', required='>=2.1.0'
        """
        if not required_min_version:
            return True
        
        # Bersihkan simbol operator jika ada
        clean_required = required_min_version.replace(">=", "").replace("==", "").strip()
        
        v_current = VersionValidator.parse_version(current_version)
        v_required = VersionValidator.parse_version(clean_required)
        
        return v_current >= v_required

if __name__ == "__main__":
    validator = VersionValidator()

    print(f"3.0.0 >= 2.0.0? {validator.is_compatible('3.0.0', '>=2.0.0')}") 
    print(f"1.5.0 >= 2.0.0? {validator.is_compatible('1.5.0', '>=2.0.0')}")
    print(f"2.1.0 >= 2.1.0? {validator.is_compatible('2.1.0', '>=2.1.0')}")