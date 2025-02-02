import time
import random
import datetime
import schedule
import starkbank

from faker import Faker


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


def create_invoice() -> starkbank.Invoice:
    """
    Cria um invoice com dados randomicos
    """
    invoice =  starkbank.Invoice(
        amount= random.randint(100, 1000),
        name=Faker().name(),
        tax_id=generate_cpf()
    )

    return invoice


def send_invoices() -> None:
    """
    Envia lista de invoices
    """
    n_invoices = random.randint(1, 2)
    invoice_list = [create_invoice() for i in range(n_invoices)] # acertar numero invoices (8, 12)
    invoices = starkbank.invoice.create(invoice_list)

    print(f'{datetime.datetime.now().strftime("%d/%m, %H:%M")} | Enviando {str(n_invoices).zfill(2)} invoices:')
    for invoice in invoices:
        print(f'  - Nome: {invoice.name}, Doc: {invoice.tax_id}, Valor:{float(invoice.amount)/100}')
    print('\n')


if __name__ == '__main__':
    init()
    schedule.every(3).hours.do(send_invoices)
    end = datetime.datetime.now() + datetime.timedelta(days=1)

    print('\nIniciando envio de invoices:')
    send_invoices()
    #while end > datetime.datetime.now():
    #    schedule.run_pending()
    #    time.sleep(1)
    print('Finalizando envio de invoices\n')
