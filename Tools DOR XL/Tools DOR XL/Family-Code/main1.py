from dotenv import load_dotenv
from datetime import datetime

load_dotenv() 

import sys
from app.menus.util import clear_screen, pause
from app.client.engsel import *
from app.service.auth import AuthInstance
from app.menus.bookmark import show_bookmark_menu
from app.menus.account import show_account_menu
from app.menus.package import fetch_my_packages, get_packages_by_family

# Daftar family code yang sudah ditentukan
FAMILY_CODES = [
    {"name": "Special For You", "code": "6fda76ee-e789-4897-89fb-9114da47b805", "is_enterprise": False},
    {"name": "Akrab 2Kb", "code": "340be7a9-9ab8-d23e5-3059-70b81ec984e", "is_enterprise": False},
    {"name": "Bonus Flex Rp.0", "code": "1b42d4f6-a76e-4986-aa5c-e2979da952f4", "is_enterprise": False},
    {"name": "Kuota Bersama Rp 0", "code": "434a1449-1d18-43f8-b059-10b3d5e3f5c3", "is_enterprise": False},
    {"name": "Addon Hotrod/Xcs 8gb", "code": "74eb925a-4a05-4ede-b04b-edd90786419b", "is_enterprise": False},
    {"name": "Xcs Flex Ori", "code": "4a1acab0-da54-462c-84b1-25fd0efa9318", "is_enterprise": False},
    {"name": "EduCoference Ori", "code": "5d63dddd-4f90-4f4c-8438-2f005c20151f", "is_enterprise": False},
    {"name": "Mastif Bundling Setahun", "code": "6bcc96f4-f196-4e8f-969f-e45a121d21bd", "is_enterprise": False},
    {"name": "Paket XL Point", "code": "784be350-9364-4f03-8efa-e7cf31e8baa2", "is_enterprise": False},
    {"name": "Paket Bonus MyRewards", "code": "07461ed8-8a81-4d89-a8f2-4dd0271efdde", "is_enterprise": False},
    {"name": "Addon XCP 2GB", "code": "580c1f94-7dc4-416e-96f6-8faf26567516", "is_enterprise": False},
    {"name": "Addon XCP 15GB", "code": "45c3a622-8c06-4bb1-8e56-bba1f3434600", "is_enterprise": False},
    {"name": "Bebas Puas", "code": "d0a349a7-0b3a-4552-bc1d-3fd9ac0a17ee", "is_enterprise": False},
    {"name": "XCP OLD 10GB", "code": "364d5764-77d3-41b8-9c22-575b555bf9df", "is_enterprise": False},
    {"name": "XCP VIP", "code": "23b71540-8785-4abe-816d-e9b4efa48f95", "is_enterprise": False},
    {"name": "Biz starter", "code": "20342db0-e03e-4dfd-b2d0-cd315d7ddc36", "is_enterprise": True},
    {"name": "EduCoference Rp 0", "code": "fcf982c8-523b-4748-9258-5fca2c0b703d", "is_enterprise": True},
    {"name": "Biz data+", "code": "53de8ac3-521d-43f5-98ce-749ad0481709", "is_enterprise": True},
    # Kode baru yang ditambahkan
    {"name": "Hotrod special DKK", "code": "96d99f87-8963-40e4-a522-8bea86504fee", "is_enterprise": False},
    {"name": "combo plus", "code": "e0f9605b-5dad-486e-a378-cf40d5b7f2ba", "is_enterprise": False},
    {"name": "combo mini", "code": "ad176860-49d4-4bdd-9161-ab38dc6a631b", "is_enterprise": False},
    {"name": "ShopeePay 9.9 3.5GB", "code": "a95ff678-d7aa-48a5-9ab5-103bcc295e92", "is_enterprise": False},
    {"name": "akrab", "code": "6e469cb2-443d-402f-ba77-681b032ead6a", "is_enterprise": False},
    {"name": "xtra on", "code": "5cc06efb-cdc4-4656-afdc-0c1597245c9e", "is_enterprise": False},
    {"name": "kuota utama 2gb", "code": "b903c49b-04bb-41cc-bdce-d103f151bd5c", "is_enterprise": False},
    {"name": "sosialmedia", "code": "2f2ecdb9-0766-4e15-b4de-000b2d6ce359", "is_enterprise": False},
    {"name": "Video & Music Youtube", "code": "05c159a8-5f64-4bb5-9ec3-7b47c8dfb7c5", "is_enterprise": False},
    {"name": "booster akrab", "code": "5452eed8-91f3-4e9c-b7bb-0985759d5440", "is_enterprise": False},
    {"name": "game", "code": "fc77cc03-4b05-4e79-8e42-5308c3f81fd1", "is_enterprise": False},
    {"name": "kuota malam", "code": "64e63f53-6889-4d12-a0b4-ef9ea77b9efc", "is_enterprise": False},
    {"name": "Navigasi Google Maps + Waze", "code": "971dd733-602a-4440-abdd-9dbe9bfa951d", "is_enterprise": False},
    {"name": "XL PASS XL", "code": "fff99b6b-5a5d-4ba4-a55b-38f6aca6f91d", "is_enterprise": False},
    {"name": "umroh", "code": "7360a68a-737c-467d-b617-3022ff0a9235", "is_enterprise": False},
    {"name": "XL PASS LITE", "code": "7fed7aa1-946f-44ce-9eb4-488a7e15c68a", "is_enterprise": False},
    {"name": "Fav Roaming", "code": "eff1d7c3-b780-40f5-88cd-5e2c7f34ccd3", "is_enterprise": False},
    {"name": "Umroh dan Haji", "code": "8358dc90-0717-45e8-8fb1-7ca8470d6562", "is_enterprise": False},
    {"name": "Vision+ Premium Sports", "code": "6abdce39-3f45-46b0-8cbe-f760e774101e", "is_enterprise": False},
    {"name": "Vidio Ultimate All Screen", "code": "e2dbb9ed-bc4c-4d09-9e1f-78d54ec9917d", "is_enterprise": False},
    {"name": "Vidio Platinum Extra Mobile", "code": "ce36962f-c56d-4568-9195-24cc61d4d703", "is_enterprise": False},
    {"name": "Vidio Platinum All Screen", "code": "18d5ea5c-c1bf-4450-9f3e-43b40ef69dad", "is_enterprise": False},
    {"name": "Viu Premium Viu", "code": "2faefba5-6d74-45fe-abcd-9517c6d1697d", "is_enterprise": False},
]


def show_normal_codes_menu():
    """Menampilkan daftar Family Code (normal) dan memproses pilihan pengguna."""
    while True:
        clear_screen()
        print("---------------------------------")
        print("Pilih Paket dari Daftar Family Code (Normal)")
        print("---------------------------------")
        # Mengambil hanya paket non-enterprise
        normal_codes = [pkg for pkg in FAMILY_CODES if not pkg["is_enterprise"]]
        
        for i, pkg in enumerate(normal_codes, 1):
            print(f"{i}. {pkg['name']}")
        print("---------------------------------")
        print("0. Kembali ke menu utama")
        print("---------------------------------")
        
        try:
            choice = int(input("Pilih nomor paket: "))
            if choice == 0:
                return
            
            if 1 <= choice <= len(normal_codes):
                selected_pkg = normal_codes[choice - 1]
                print(f"Memilih paket: {selected_pkg['name']}")
                get_packages_by_family(selected_pkg["code"], is_enterprise=False)
                pause()
                return
            else:
                print("Pilihan tidak valid. Silakan coba lagi.")
                pause()
        except ValueError:
            print("Pilihan tidak valid. Masukkan angka.")
            pause()


def show_enterprise_codes_menu():
    """Menampilkan daftar Family Code (Enterprise) dan memproses pilihan pengguna."""
    while True:
        clear_screen()
        print("---------------------------------")
        print("Pilih Paket dari Daftar Family Code (Enterprise)")
        print("---------------------------------")
        # Mengambil hanya paket enterprise
        enterprise_codes = [pkg for pkg in FAMILY_CODES if pkg["is_enterprise"]]
        
        for i, pkg in enumerate(enterprise_codes, 1):
            print(f"{i}. {pkg['name']}")
        print("---------------------------------")
        print("0. Kembali ke menu utama")
        print("-----------------")
        
        try:
            choice = int(input("Pilih nomor paket: "))
            if choice == 0:
                return
            
            if 1 <= choice <= len(enterprise_codes):
                selected_pkg = enterprise_codes[choice - 1]
                print(f"Memilih paket: {selected_pkg['name']}")
                get_packages_by_family(selected_pkg["code"], is_enterprise=True)
                pause()
                return
            else:
                print("Pilihan tidak valid. Silakan coba lagi.")
                pause()
        except ValueError:
            print("Pilihan tidak valid. Masukkan angka.")
            pause()


def show_main_menu(number, balance, balance_expired_at):
    clear_screen()
    phone_number = number
    remaining_balance = balance
    expired_at = balance_expired_at
    # Mengonversi timestamp ke format tanggal yang mudah dibaca
    expired_at_dt = datetime.fromtimestamp(expired_at / 1000).strftime("%Y-%m-%d %H:%M:%S")
    
    print("--------------------------")
    print("Informasi Akun")
    print(f"Nomor: {phone_number}")
    print(f"Pulsa: Rp {remaining_balance}")
    print(f"Masa aktif: {expired_at_dt}")
    print("--------------------------")
    print("Menu:")
    print("1. Login/Ganti akun")
    print("2. Lihat Paket Saya")
    print("3. Beli Paket XUT")
    print("4. Beli Paket dari Daftar Pilihan (Normal)")
    print("5. Beli Paket dari Daftar Pilihan (Enterprise)")
    print("00. Bookmark Paket")
    print("99. Tutup aplikasi")
    print("--------------------------")

show_menu = True
def main():
    
    while True:
        active_user = AuthInstance.get_active_user()

        # Logged in
        if active_user is not None:
            balance = get_balance(AuthInstance.api_key, active_user["tokens"]["id_token"])
            balance_remaining = balance.get("remaining")
            balance_expired_at = balance.get("expired_at")

            show_main_menu(active_user["number"], balance_remaining, balance_expired_at)

            choice = input("Pilih menu: ")
            if choice == "1":
                selected_user_number = show_account_menu()
                if selected_user_number:
                    AuthInstance.set_active_user(selected_user_number)
                else:
                    print("No user selected or failed to load user.")
                continue
            elif choice == "2":
                fetch_my_packages()
                continue
            elif choice == "3":
                # XUT 
                get_packages_by_family("08a3b1e6-8e78-4e45-a540-b40f06871cfe")
            elif choice == "4":
                show_normal_codes_menu()
            elif choice == "5":
                show_enterprise_codes_menu()
            elif choice == "00":
                show_bookmark_menu()
            elif choice == "99":
                print("Exiting the application.")
                sys.exit(0)
            elif choice == "9":
                # Playground
                pass
                # data = get_package(
                #     AuthInstance.api_key,
                #     active_user["tokens"],
                #     "U0NfX8A08oQLUQuLplGhfT_FXQokJ9GFF9kAKRiV5trm6BfbRoxrsizKkWIVNxM0az6lroT92FYXnWmTXRXZOl1Meg",
                #     ""
                #     ""
                #     )
                # print(json.dumps(data, indent=2))
                # pause()
            else:
                print("Invalid choice. Please try again.")
                pause()
        else:
            # Not logged in
            selected_user_number = show_account_menu()
            if selected_user_number:
                AuthInstance.set_active_user(selected_user_number)
            else:
                print("No user selected or failed to load user.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting the application.")
    except Exception as e:
        print(f"An error occurred: {e}")