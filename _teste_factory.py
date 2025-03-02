import factory
import random
from faker import Faker

fake = Faker()

# Pedido (Order) Factory
class PedidoFactory(factory.Factory):
    class Meta:
        model = dict  # Can be replaced with a Django/SQLAlchemy model

    PedidoID = factory.Sequence(lambda n: n + 1000)
    NumeroPedido = factory.LazyAttribute(lambda _: fake.unique.random_int(100000, 999999))
    ClienteID = factory.Sequence(lambda n: n + 500)
    DataPedido = factory.Faker("date_this_year")
    DataEntregaPrevista = factory.Faker("date_between", start_date="+2d", end_date="+30d")
    StatusPedido = factory.Iterator(["Pendente", "Aprovado", "Cancelado", "Entregue"])
    CanalVenda = factory.Iterator(["Site", "Telefone", "Vendedor"])
    VendedorID = factory.Sequence(lambda n: n + 10)
    TotalBruto = factory.LazyAttribute(lambda _: round(random.uniform(100, 5000), 2))
    TotalDesconto = factory.LazyAttribute(lambda _: round(random.uniform(0, 500), 2))
    TotalImpostos = factory.LazyAttribute(lambda _: round(random.uniform(10, 500), 2))
    TotalLiquido = factory.LazyAttribute(lambda obj: obj.TotalBruto - obj.TotalDesconto - obj.TotalImpostos)
    FormaPagamento = factory.Iterator(["Boleto", "Cartão", "PIX", "Transferência"])
    CampanhaID = factory.Sequence(lambda n: n + 100)  
    DataAprovacao = factory.Faker("date_this_year")
    UsuarioAprovacao = factory.Faker("first_name")
    PrioridadeEntrega = factory.Iterator(["Normal", "Alta", "Urgente"])
    EntregaID = factory.Sequence(lambda n: n + 200)

# PedidoLinha (Order Line) Factory
class PedidoLinhaFactory(factory.Factory):
    class Meta:
        model = dict  

    PedidoLinhaID = factory.Sequence(lambda n: n + 10000)
    PedidoID = factory.SubFactory(PedidoFactory)
    ProdutoID = factory.Sequence(lambda n: n + 200)
    Quantidade = factory.LazyAttribute(lambda _: random.randint(1, 10))
    PrecoUnitario = factory.LazyAttribute(lambda _: round(random.uniform(10, 200), 2))
    ValorBruto = factory.LazyAttribute(lambda obj: obj.PrecoUnitario * obj.Quantidade)
    ValorImpostos = factory.LazyAttribute(lambda obj: round(obj.ValorBruto * 0.1, 2))
    ValorLiquido = factory.LazyAttribute(lambda obj: obj.ValorBruto - obj.ValorImpostos)
    ValorFrete = factory.LazyAttribute(lambda _: round(random.uniform(0, 50), 2))
    ValorComissao = factory.LazyAttribute(lambda _: round(random.uniform(0, 20), 2))
    ValorCusto = factory.LazyAttribute(lambda _: round(random.uniform(5, 50), 2))
    ValorDesconto = factory.LazyAttribute(lambda _: round(random.uniform(0, 10), 2))
    StatusItemPedido = factory.Iterator(["Pendente", "Faturado", "Cancelado"])
    DataEntregaPrevista = factory.Faker("date_between", start_date="+2d", end_date="+30d")
    TabelaPrecoID = factory.Sequence(lambda n: n + 300)
    PercentualComissaoVendedor = factory.LazyAttribute(lambda _: round(random.uniform(1, 10), 2))

# Cliente (Customer) Factory
class ClienteFactory(factory.Factory):
    class Meta:
        model = dict  

    ClienteID = factory.Sequence(lambda n: n + 500)
    CodigoCliente = factory.LazyAttribute(lambda _: fake.unique.random_int(10000, 99999))
    RazaoSocial = factory.Faker("company")
    NomeFantasia = factory.Faker("company_suffix")
    CNPJ = factory.Faker("ean13")
    Latitude = factory.LazyAttribute(lambda _: round(random.uniform(-30, -15), 6))
    Longitude = factory.LazyAttribute(lambda _: round(random.uniform(-60, -35), 6))
    InscricaoEstadual = factory.Faker("ean8")
    TipoCliente = factory.Iterator(["PJ", "PF"])
    SegmentoCliente = factory.Iterator(["Varejo", "Atacado", "Distribuidor"])
    Cidade = factory.Faker("city")
    Estado = factory.Faker("state_abbr")
    DataCadastro = factory.Faker("date_this_decade")
    LimiteCredito = factory.LazyAttribute(lambda _: round(random.uniform(500, 50000), 2))
    StatusCredito = factory.Iterator(["Aprovado", "Negado", "Em análise"])
    CondicaoPagamentoPadrao = factory.Iterator(["30 dias", "À vista", "Parcelado"])
    VendedorID = factory.Sequence(lambda n: n + 10)

# Produto (Product) Factory
class ProdutoFactory(factory.Factory):
    class Meta:
        model = dict  

    ProdutoID = factory.Sequence(lambda n: n + 200)
    CodigoProduto = factory.LazyAttribute(lambda _: fake.unique.random_int(1000, 9999))
    DescricaoCurta = factory.Faker("word")
    DescricaoCompleta = factory.Faker("sentence")
    Marca = factory.Faker("company")
    Categoria = factory.Iterator(["Vinhos", "Cervejas", "Destilados"])
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


pedido = PedidoFactory()
print(pedido)

# Generate 10 customers
clientes = ClienteFactory.create_batch(10)
for cliente in clientes:
    print(cliente)

# Generate 5 products
produtos = ProdutoFactory.create_batch(5)
for produto in produtos:
    print(produto)

# Generate an order with multiple order lines
pedido = PedidoFactory()
pedido_linhas = PedidoLinhaFactory.create_batch(3, PedidoID=pedido["PedidoID"])

print(pedido)
for linha in pedido_linhas:
    print(linha)