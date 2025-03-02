from faker import Faker
import random
from gentabular import utils
from datetime import datetime, timedelta

fake = Faker('pt_BR')

def vendedores(NUM_VENDEDORES):
    vendedores = []
    regioes = ["Norte", "Sul", "Leste", "Oeste", "Centro", "Nordeste", "Sudeste", "Centro-Oeste", "Sul-Sudeste", "Norte-Nordeste"]
    
    for i in range(1, NUM_VENDEDORES + 1):
        vendedor = {
            'VendedorID': i,
            'Nome': fake.name(),
            'Email': fake.email(),
            'Telefone': fake.phone_number(),
            'RegiaoPrincipal': random.choice(regioes),
            'DataContratacao': utils.random_date(datetime(2010, 1, 1), datetime(2023, 1, 1)).strftime('%Y-%m-%d'),
            'Status': random.choices(['Ativo', 'Inativo', 'Férias', 'Licença'], weights=[0.8, 0.1, 0.05, 0.05])[0],
            'MetaMensal': round(random.uniform(50000, 300000), 2),
            'PercentualComissaoPadrao': round(random.uniform(1.5, 5.0), 2)
        }
        vendedores.append(vendedor)
    
    return vendedores