import time
import random
import datetime
import schedule
import starkbank

from faker import Faker

DEBUG = False


def get_private_key() -> str:
    """
    Retorna uma chave privada ECDSA no formato PEM a partir de um arquivo
    """
    
    pkey: str = ''
    with open("keys/private-key.pem") as key:
        pkey = key.read()
    return pkey


def init() -> None:
    """
    Inicializa projeto com dados do sandbox
    """

    project = starkbank.Project(
        environment="sandbox",
        id="6283733208399872",
        private_key=get_private_key()
    )
    starkbank.user = project
    starkbank.language = "en-US"


def generate_cpf() -> str:
    """
    Cria um CPF randomico
    """

    cpf: list[int] = [random.randint(0, 9) for x in range(9)]
                                                                                
    for _ in range(2):
        val: int = sum([(len(cpf) + 1 - i) * v for i, v in enumerate(cpf)]) % 11
        cpf.append(11 - val if val > 1 else 0)

    cpf_s: list[str] = [str(i) for i in cpf]
    return f'{"".join(cpf_s[:3])}.{"".join(cpf_s[3:6])}.{"".join(cpf_s[6:9])}-{"".join(cpf_s[9:])}'


def create_invoce() -> starkbank.Invoice:
    """
    Cria um invoce com dados randomicos
    """
    invoce =  starkbank.Invoice(
        amount= random.randint(100, 1000),
        name=Faker().name(),
        tax_id=generate_cpf()
    )

    return invoce


def send_invoces() -> None:
    """
    Envia lista de invoces
    """
    invoce_list = [create_invoce() for i in range(random.randint(1, 3))] # acertar numero invoces (8, 12)
    invoices = starkbank.invoice.create(invoce_list)

    # for invoice in invoices:
    #     print(invoice)


def p_debug() -> None:
    """
    Imprime informacoes usadas para debug
    """

    print(starkbank.balance.get())

    webhooks = starkbank.webhook.query()
    for webhook in webhooks:
        print(webhook)


def job():
    print('Boo')

if __name__ == '__main__':
    fake = Faker()
    init()
    schedule.every(1).minutes.do(job)
    # schedule.every(3).hour.do(send_invoces)
    # TODO: schefuler do webhook/transfer

    end = datetime.datetime.now() + datetime.timedelta(minutes=5)
    #end = datetime.datetime.now() + datetime.timedelta(days=1)

    logs = starkbank.invoice.log.query(limit=150)

    for log in logs:
        print(log)

    #while end > datetime.datetime.now():
    #    schedule.run_pending()
    #    time.sleep(1)

    if DEBUG:
        p_debug()
