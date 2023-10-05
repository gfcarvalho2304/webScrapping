from selenium import webdriver
from bs4 import BeautifulSoup
import os
import smtplib
from email.message import EmailMessage



def retorna_rodada(url):
    navegador = webdriver.Chrome()
    navegador.get(url)

    tagRodada = navegador.find_element_by_class_name("lista-jogos__navegacao--rodada")
    htmlRodada = tagRodada.get_attribute("outerHTML")
    rodadaSoup = BeautifulSoup(htmlRodada, 'html.parser')

    rodadaText = rodadaSoup.text
    rodadaAux = ""

    for i in rodadaText:
        if i.isdigit():
            rodadaAux += i
    rodadaNum = int(rodadaAux)
    return rodadaNum
    navegador.quit()


def enviar_email(subj, text):
    email_adress = os.getenv('EMAIL_ADRESS')
    email_password = os.getenv('EMAIL_PASSWORD')
    email_to = os.getenv('EMAIL_TO')


    msg = EmailMessage()
    msg['Subject'] = subj
    msg['From'] = email_adress
    msg['To'] = email_to
    msg.set_content(text)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(email_adress, email_password)
        smtp.send_message(msg)

