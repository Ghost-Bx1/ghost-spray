# Ghost-Spray

**Password Spraying & Credential Attacks**  
By Gh0st-Bx1 | github.com/Ghost-Bx1

---

## Descricao

Ghost-Spray e uma ferramenta de ataques de credenciais com password spraying inteligente, credential stuffing, verificacao de senhas padrao, quebra de hash por dicionario+regras e vault local criptografado. Construido com stdlib Python 3 - sem dependencias externas.

## Recursos

- **Password Spray** - Uma senha por vez para todos os usuarios (evita lockout)
- **Credential Stuffing** - Suporte a breach DBs em multiplos formatos
- **Default Credentials** - 40+ credenciais padrao de fabricantes conhecidos
- **Hash Cracker** - Quebra MD5/SHA1/SHA256/SHA512 por dicionario + regras
- **Lockout Detection** - Pausa automatica ao detectar possivel lockout
- **Vault Criptografado** - Armazenamento local de credenciais com XOR + SHA-256

## Modos

### spray - Password Spraying

```bash
python ghost-spray.py spray -t <alvo> --userlist <arquivo> [opcoes]
```

| Argumento | Descricao |
|-----------|-----------|
| `-t, --target` | URL ou host:porta |
| `--protocol` | http, https, smtp, ldap, ssh (padrao: http) |
| `--userlist` | Arquivo com lista de usuarios |
| `--passlist` | Arquivo com lista de senhas (padrao: lista interna) |
| `--delay` | Delay entre tentativas em segundos (padrao: 1.0) |
| `--threads` | Threads simultaneas por senha (padrao: 3) |
| `--vault-pass` | Senha do vault para salvar credenciais validas |
| `-o, --output` | Salvar resultados em JSON |

```bash
# Spray HTTP Basic Auth
python ghost-spray.py spray -t http://alvo.com/admin --protocol http \
  --userlist usuarios.txt --delay 2.0

# Spray SMTP com lista de senhas customizada
python ghost-spray.py spray -t mail.alvo.com:587 --protocol smtp \
  --userlist emails.txt --passlist senhas.txt --delay 3.0 --vault-pass s3cr3t

# Spray LDAP
python ghost-spray.py spray -t 192.168.1.10:389 --protocol ldap \
  --userlist usuarios.txt --threads 5
```

### stuff - Credential Stuffing

```bash
python ghost-spray.py stuff -t <alvo> --breach-file <arquivo> [opcoes]
```

Formatos suportados de breach DB:
- `usuario:senha`
- `email:senha`
- `{"email":"...","password":"..."}` (JSON)
- Separadores: `:` `;` `\t` `|`

```bash
# Credential stuffing com breach DB
python ghost-spray.py stuff -t http://alvo.com/login --breach-file dump.txt

# Com vault e output JSON
python ghost-spray.py stuff -t http://alvo.com/api/auth \
  --breach-file breach.json --vault-pass s3cr3t -o achados.json
```

### defaults - Default Credentials

```bash
python ghost-spray.py defaults -t <alvo> --protocol <protocolo>
```

Fabricantes incluidos: D-Link, TP-Link, Netgear, Cisco, Juniper, Mikrotik, Ubiquiti, Hikvision, Dahua, Axis, VMware ESXi, Citrix, IPMI/BMC, PostgreSQL, MySQL, Redis, MongoDB, Jenkins, Tomcat, Grafana, Kibana, Jupyter, Jira, Confluence, e mais.

```bash
# Testar credenciais padrao em painel web
python ghost-spray.py defaults -t http://192.168.1.1/admin --protocol http

# Testar credenciais padrao LDAP
python ghost-spray.py defaults -t 192.168.1.10:389 --protocol ldap
```

### hash - Hash Cracker

```bash
python ghost-spray.py hash --hash <hash> [--wordlist <arquivo>]
```

Tipos suportados: MD5 (32), SHA1 (40), SHA224 (56), SHA256 (64), SHA384 (96), SHA512 (128)

Regras aplicadas automaticamente:
- Capitalizacao, MAIUSCULA, minuscula
- Sufixos numericos (1, 12, 123, 1234, 2024, 2025)
- Simbolos (@, !, #)
- Substituicoes leet (a->@, e->3, i->1, o->0)

```bash
# Quebrar MD5 com lista interna
python ghost-spray.py hash --hash 5f4dcc3b5aa765d61d8327deb882cf99

# Com wordlist customizada
python ghost-spray.py hash --hash <sha256> --wordlist rockyou.txt --verbose
```

### vault - Gerenciar Vault

```bash
python ghost-spray.py vault --action <acao> --vault-pass <senha>
```

| Acao | Descricao |
|------|-----------|
| `list` | Listar credenciais salvas |
| `clear` | Limpar vault |
| `export` | Exportar para vault_export.json |

```bash
# Listar credenciais no vault
python ghost-spray.py vault --action list --vault-pass s3cr3t

# Exportar vault para JSON
python ghost-spray.py vault --action export --vault-pass s3cr3t
```

## Lockout Detection

O Ghost-Spray monitora automaticamente tentativas falhas por usuario. Ao detectar 5+ falhas em 60 segundos para o mesmo usuario, pausa automaticamente por 300 segundos antes de continuar.

Use `--delay` para adicionar espera adicional entre tentativas e reduzir o risco de lockout.

## Vault de Credenciais

As credenciais validas encontradas sao armazenadas em `ghost-spray.vault` com cifragem XOR + chave SHA-256 derivada da senha mestre. O vault e um arquivo local binario - sem credenciais em texto plano.

## Requisitos

- Python 3.7+
- Stdlib apenas (socket, ssl, hashlib, threading, urllib, etc.)
- SSH real requer `pip install paramiko` (opcional)

## Aviso Legal

Esta ferramenta foi desenvolvida para testes de seguranca autorizados, CTF, pesquisa e uso defensivo. Use apenas em sistemas que voce tem permissao para testar. Password spraying e credential stuffing sem autorizacao sao ilegais.

---

*Ghost-Spray v1.0.0 - Ghost Tools Arsenal*
