from instagrapi import Client
import time
import random

# 🔑 Ler credenciais do arquivo
with open("you.txt", "r") as arquivo:
    dados = arquivo.read().splitlines()
    usuario = dados[0]
    senha = dados[1]

# 🔗 Link da postagem
url_postagem = "your link"

# 💛 Configurações de comentário
emoji = "💛"
quantidade = 1000  # Total de comentários
corações_iniciais = 1  # Começa com 1 coração
aumenta_cada = 10  # A cada 10 comentários, aumenta a quantidade de corações
tempo_min = 50  # Tempo mínimo (segundos)
tempo_max = 70  # Tempo máximo (segundos)

# 🚀 Login no Instagram com autenticação de 2 fatores
cl = Client()

try:
    cl.load_settings("sessao.json")
    cl.login(usuario, senha)
    cl.dump_settings("sessao.json")
    print("✅ Login bem-sucedido usando sessão salva!")

except Exception as e:
    print("⚠️ Login via sessão falhou. Tentando login manual...")

    try:
        # 🔐 Pedir código do 2FA
        codigo_2fa = input("🔐 Digite o código do 2FA (Google Authenticator): ")
        cl.login(usuario, senha, verification_code=codigo_2fa)
        cl.dump_settings("sessao.json")
        print("✅ Login manual bem-sucedido e sessão salva!")

    except Exception as erro:
        print(f"❌ Erro no login: {erro}")
        exit()

# 🎯 Obter ID da postagem
try:
    media_id = cl.media_id(cl.media_pk_from_url(url_postagem))
    print("🔗 Postagem localizada com sucesso!")
except Exception as erro:
    print(f"❌ Erro ao localizar a postagem: {erro}")
    exit()

# 🔄 Loop dos comentários
for i in range(1, quantidade + 1):
    try:
        # 💛 Monta o comentário com quantidade de corações proporcional
        coracoes = corações_iniciais + (i // aumenta_cada)
        comentario = emoji * coracoes

        cl.media_comment(media_id, comentario)
        print(f"[{i}/{quantidade}] ✅ Comentário enviado: {comentario}")

        # ⏳ Tempo aleatório entre tempo_min e tempo_max
        tempo_espera = random.randint(tempo_min, tempo_max)
        print(f"⏳ Aguardando {tempo_espera} segundos antes do próximo...")

        time.sleep(tempo_espera)

    except Exception as e:
        print(f"⚠️ Erro ao comentar: {e}")
        print("⏸️ Aguardando 5 minutos antes de tentar novamente...")
        time.sleep(300)

print("🎉 ✅ Todos os comentários foram enviados com sucesso!")
