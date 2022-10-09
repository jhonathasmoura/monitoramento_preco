import urllib.request
import yagmail
import os
from time import sleep


os.system("cls" if os.name == "nt" else "clear")


def consulta_preco(url):
    pagina = urllib.request.urlopen(url)
    texto = pagina.read().decode("utf-8")
    inicio = texto.find(">$") + 2
    fim = texto.find("</", inicio)
    preco = texto[inicio:fim]
    return float(preco)


def envia_email(email_remetente, senha, email_destinatario, assunto, preco, url, mensagem):
    server = yagmail.SMTP(email_remetente, senha)
    server.send(email_destinatario, assunto, mensagem)

    print(f"Email com link de compra enviado para: ")
    for email in email_destinatario:
        print(f"<{email}>")


if __name__ == "__main__":
    if os.path.isfile("dados.txt"):
        arquivo = open("dados.txt", "r", encoding="utf-8")
    else:
        arquivo = open("dados.txt", "w", encoding="utf-8")
        arquivo.write(input("Digite o seu email: ") + " ")
        senha = input("Digite a senha: ")
        arquivo.write(f"{senha}\n")
        qtd_destinatarios = int(input("Deseja enviar a oferta para quantos destinatários? "))
        for i in range(qtd_destinatarios):
            arquivo.write(input(f"Digite o email do destinatário{'' if qtd_destinatarios == 1 else f' {i + 1}'}: ") + " ")
        print("Arquivo com informações de login e destinatários criado!")
        arquivo.close()

        arquivo = open("dados.txt", "r", encoding="utf-8")

    dados = [dado.strip().split(' ') for dado in arquivo.readlines()]
    email_remetente = dados[0][0]
    senha = dados[0][1]
    email_destinatario = dados[1]
    assunto = "Alerta de Preço!"
    arquivo.close()

    while True:
        urls = [
            "http://beans.itcarlow.ie/prices.html",
            "http://beans.itcarlow.ie/prices-loyalty.html",
        ]
        preco_normal = consulta_preco(urls[0])
        preco_promocional = consulta_preco(urls[1])
        print(f"Preço Normal: US${preco_normal:.2f}")
        print(f"Preço Promocional: US${preco_promocional:.2f}")
        print("-" * 45)

        if preco_normal < 4.70 or preco_promocional < 4.70:
            if min(preco_normal, preco_promocional) == preco_normal:
                print(f"Preço baixo encontrado.")
                mensagem = [
                        f"O preço do café baixou para US${preco_normal:.2f}", 
                        f"Compre agora em: {urls[0]}"
                ]
                envia_email(email_remetente, senha, email_destinatario, assunto, preco_normal, urls[0], mensagem)
                break
            elif min(preco_normal, preco_promocional) == preco_promocional:
                print(f"Preço baixo encontrado.")
                mensagem = [
                        f"O preço do café baixou para US${preco_promocional:.2f}",
                        f"Compre agora em: {urls[1]}"
                ]
                envia_email(email_remetente, senha, email_destinatario, assunto, preco_promocional, urls[1], mensagem)
                break
        else:
            print("Preço alto! Aguarde um pouco para comprar.")
            print("Consultando novo preço...")

        sleep(2)
