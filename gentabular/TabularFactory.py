import factory
import random
from faker import Faker
import json

fake = Faker()

with open("data/vemma/schema_processado.json", "r", encoding="utf-8") as file:
    schema = json.load(file)["SchemaCompleto"]["Produto"]

def pick_weighted_random_element(dynamic_list, fixed_weights=None):
    # If fixed_weights is provided, it must match the list length.
    # Otherwise, generate random weights for each element.
    weights = fixed_weights if fixed_weights else [random.random() for _ in dynamic_list]
    return random.choices(dynamic_list, weights=weights, k=1)[0]

# Produto (Product) Factory
class ProdutoFactory(factory.Factory):

    class Meta:
        model = dict  

    ProdutoID = factory.Sequence(lambda n: n + 1)
    NomeProdutoCurto = factory.Iterator(schema["NomeProdutoCurto"]["Exemplos"])

    Marca = factory.Iterator(schema["Marca"]["Exemplos"])
    NomeProdutoCompleto = factory.LazyAttribute(lambda o: o.Marca + " " + o.NomeProdutoCurto)

    DescricaoCompleta = factory.Faker("sentence")
    
    #arrumar aqui, o pick weighted tem que ser em conjunto, nao da pra selecionar categoria refrigerante e gerar subcategoria IPA
    Categoria = factory.LazyFunction(lambda: pick_weighted_random_element(schema["Categoria"]["Exemplos"]))


    Subcategoria = factory.Iterator(["Tinto", "Branco", "IPA", "Pilsen"])
    TipoBebida = factory.Iterator(["Alcoólica", "Não Alcoólica"])
    TeorAlcoolico = factory.LazyAttribute(lambda _: round(random.uniform(0, 15), 2))
    VolumeMl = factory.LazyAttribute(lambda _: random.randint(330, 750))
    PesoLiquido = factory.LazyAttribute(lambda _: round(random.uniform(0.3, 2.0), 2))
    PesoBruto = factory.LazyAttribute(lambda _: round(random.uniform(0.5, 2.5), 2))
    Altura = factory.LazyAttribute(lambda _: round(random.uniform(10, 40), 2))
    Largura = factory.LazyAttribute(lambda _: round(random.uniform(5, 15), 2))
    Comprimento = factory.LazyAttribute(lambda _: round(random.uniform(5, 15), 2))
    StatusProduto = factory.Iterator(["Ativo", "Inativo"])
    DataCadastro = factory.Faker("date_this_decade")


# Generate 5 products
produtos = ProdutoFactory.create_batch(5)
for produto in produtos:
    print(produto)


