from telethon.sync import TelegramClient
from telethon.tl.functions.channels import InviteToChannelRequest
from telethon.errors import rpcerrorlist

from time import sleep
from os import listdir
from colorama import Fore, init

from configparser import ConfigParser
from argparse import ArgumentParser


# colorama initialization
init(autoreset=True)

# configparser initialization
config = ConfigParser() 


# global variable
configfile = 'config.ini'

def delay():
    for i in reversed(range(5)):
        print(f'\r{Fore.GREEN}[*] {Fore.WHITE}mohon tunggu selama {i} detik...', end='')
        sleep(1)

# main program
def main():
    if not configfile in listdir():
        print(f'{Fore.RED}[!] {Fore.WHITE} tolong buat konfigurasi terlebih dahulu')
        print(f'{Fore.YELLOW}[*] {Fore.WHITE} python main.py --setup')
        exit()

    config.read(configfile)
    phone = config['user']['phone']
    api_id = 2998038
    api_hash = "1f9dee0586edc9a175e004ef8ee6d9ec"
    client = TelegramClient(phone, api_id, api_hash)
    client.connect()

    if not client.is_user_authorized():
        client.send_code_request(phone)
        client.sign_in(phone, input(f'{Fore.YELLOW}[?] {Fore.WHITE}Enter the code: '))

    print('\n')
    print(f'{Fore.YELLOW}[-] {Fore.WHITE}Masukan username grub/channel yang akan Anda tambahkan anggotanya ke grub/channel Anda')
    input_target = input(f'{Fore.YELLOW}[?] username grub/channel: ')
    try:
        target = client.get_entity(input_target)
        print(f'{Fore.GREEN}[•] {target.title}')
    except ValueError:
        print(f'{Fore.RED}[!] Tidak dapat menemukan grub/channel dengan username {input_target}')
        exit()
    print()
    try:
        input_to = config['user']['group']
        to = client.get_entity(input_to)
        print(f'{Fore.YELLOW}[•] {Fore.WHITE}Akan menambahkan anggota ke {Fore.GREEN}{to.title}')
        sleep(3)
    except ValueError:
        print(f'{Fore.RED}[!] Tidak dapat menemukan grub/channel dengan username {input_to}')
        exit()

    print()
    user_list = client.iter_participants(entity=target)
    failed    = 0
    success   = 0
    for user in user_list:
        try:
            user_to_add = client.get_input_entity(user.username)
            client(InviteToChannelRequest(
                to,
                [user_to_add]
            ))
            print(f'\r{Fore.GREEN}[+] {Fore.WHITE}Menambahkan {Fore.GREEN}{user.username}')
            success += 1
            delay()
        except rpcerrorlist.PeerFloodError:
            print(f'{Fore.RED}[!] {Fore.WHITE} akun Anda dibatasi, kirim pesan pribadi ke {Fore.GREEN}@SpamBot{Fore.WHITE} untuk info lebih lanjut')
            break
        except rpcerrorlist.UserChannelsTooMuchError:
            pass
        except rpcerrorlist.UserPrivacyRestrictedError:
            failed += 1
            print(f'\r{Fore.RED}[!] {Fore.WHITE}Tidak dapat mengundang {Fore.RED}{user.username}')
            pass
        except TypeError:
            pass
        except Exception as e:
            print(f'\r{Fore.RED}{e}')

        print(f'\r{Fore.YELLOW}[*] {Fore.GREEN}berhasil: {success} {Fore.RED}gagal: {failed}', end='')


def setup():
    print('[!] masukan nomor telepon Anda dengan awalan +62, contoh: +6281234567890')
    phone = input('[?] nomor telepon: ')
    print()
    print('[!] Masukan username group yang akan Anda tambah anggotanya')
    group = input('[?] username group: ')

    config.add_section('user')
    config['user']['phone'] = phone
    config['user']['group'] = group

    with open('./config.ini', 'w') as configfile:
        config.write(configfile)

    print()
    print('[!] berhasil mengubah konfigurasi')

if __name__ == "__main__":
    argparse = ArgumentParser()
    argparse.add_argument('--run', help='run the program', action='store_true')
    argparse.add_argument('--setup', help='change configuration', action='store_true')

    args = argparse.parse_args()

    if args.run:
        main()
    elif args.setup:
        setup()
    else:
        print('usage: main.py [-h]')
