import urllib.request
import smtplib
import getpass
import os
from email.mime.text import MIMEText
from time import sleep


def consulta_preco(url):
    pagina = urllib.request.urlopen(url)
    texto = pagina.read().decode("utf-8")
    inicio = texto.find(">$") + 2
    fim = texto.find("</", inicio)
    preco = texto[inicio:fim]
    return float(preco)


def envia_email(email_remetente, senha, email_destinatario, assunto, mensagem):
    msg = MIMEText(mensagem)
    msg["FROM"] = email_remetente
    msg["TO"] = ", ".join(email_destinatario)
    msg["SUBJECT"] = assunto

    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.login(email_remetente, senha)
    server.sendmail(email_remetente, email_destinatario, msg.as_string())
    server.quit()

    print(f"Email enviado para <{email_destinatario[0]}> com link de compra!")


if __name__ == "__main__":
    if os.path.isfile("login.txt"):
        arquivo = open("login.txt", "r", encoding="utf-8")
    else:
        arquivo = open("login.txt", "w", encoding="utf-8")
        arquivo.write(input("Digite o seu email: ") + "\n")
        senha = getpass.getpass("Digite a senha: ")
        arquivo.write(f"{senha}\n")
        arquivo.write(input("Digite o email do destinatário: "))
        print("Arquivo de login criado!")
        arquivo.close()

        arquivo = open("login.txt", "r", encoding="utf-8")

    login = [dado.strip() for dado in arquivo.readlines()]
    email_remetente = login[0]
    senha = login[1]
    email_destinatario = [login[2]]
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
                mensagem = f"O preço do café baixou para US${preco_normal:.2f}\nCompre agora em: {urls[0]}"
                envia_email(
                    email_remetente, senha, email_destinatario, assunto, mensagem
                )
                break
            elif min(preco_normal, preco_promocional) == preco_promocional:
                print(f"Preço baixo encontrado.")
                mensagem = f"O preço do café baixou para US${preco_promocional:.2f}\nCompre agora em: {urls[1]}"
                envia_email(
                    email_remetente, senha, email_destinatario, assunto, mensagem
                )
                break
        else:
            print("Preço alto! Aguarde um pouco para comprar.")
            print("Consultando novo preço...")

        sleep(2)
