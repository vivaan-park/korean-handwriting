# © 2021 지성. all rights reserved.
# <llllllllll@kakao.com>
# MIT License

def dec_to_hex(n):
    return hex(n).replace('0x', '').upper()

def hex_to_kr(h):
    return chr(int(h, 16))