# Doce Encanto — Cupcakes Gourmet (PIT II)

Aplicação web responsiva para catálogo e registro de pedidos de uma loja fictícia de cupcakes gourmet, dando continuidade ao planejamento da PIT I.

## Tecnologias
- Front-end: HTML5, CSS3 e JavaScript.
- Back-end: Python 3 + Flask.
- Banco de dados: SQLite (biblioteca padrão `sqlite3` do Python).
- Organização: arquitetura em camadas inspirada no padrão MVC (models, controllers, routes e views no front-end).

A escolha de Python atende à lista de linguagens sugeridas no material da disciplina para o back-end (Java, PHP, C#, .NET ou Python).

## Funcionalidades
- Catálogo de produtos e filtros por categoria.
- Carrinho com inclusão, remoção e alteração de quantidades.
- Cálculo do total no servidor, com preços consultados no banco.
- Finalização e registro de pedidos com dados de contato, endereço de entrega e forma de pagamento escolhida (Pix, dinheiro ou cartão).
- Validação de campos, produtos e quantidades.
- Persistência de produtos, pedidos, itens, forma de pagamento e status inicial do pedido (Recebido) no SQLite.

## Como executar no Windows
1. Instale o Python 3.10 ou superior e marque a opção **Add Python to PATH** durante a instalação.
2. Extraia o ZIP para uma pasta do computador.
3. Entre na pasta `cupcake_gourmet_pit2`.
4. Dê dois cliques em `INICIAR_NO_WINDOWS.bat`. Ele instalará o Flask e iniciará o servidor.
5. Abra `http://localhost:3000` no navegador.

Alternativa pelo Prompt de Comando, aberto dentro da pasta do projeto:
```bash
py -m pip install -r requirements.txt
py app.py
```
Para encerrar o servidor, volte à janela do terminal e pressione `Ctrl + C`.

O banco `data/cupcakes.db` é criado automaticamente na primeira execução e recebe produtos de demonstração.

## Endpoints da API
- `GET /api/health` — estado da aplicação.
- `GET /api/products` — lista produtos ativos.
- `GET /api/products/<id>` — consulta um produto.
- `POST /api/orders` — registra um pedido (utilizado pelo formulário de checkout).

## Testes manuais
1. Abrir a página e verificar se os produtos aparecem.
2. Filtrar as categorias.
3. Adicionar produtos ao carrinho e alterar quantidades.
4. Verificar se o total é atualizado.
5. Tentar finalizar com carrinho vazio.
6. Tentar enviar o formulário sem preencher os campos obrigatórios.
7. Enviar um pedido válido com dados fictícios, selecionar uma forma de pagamento e verificar a confirmação.
8. Conferir no banco de dados se `payment_method` foi salvo e se o pedido recebeu status `Recebido`.
8. Abrir `http://localhost:3000/api/health` e conferir o JSON com `status: ok`.
9. Abrir `http://localhost:3000/api/products` e conferir a lista de produtos em JSON.

Registre os resultados reais, a data, o nome de cada colega que testar e as evidências. Não declare testes como aprovados sem executá-los.

## Estrutura principal
```text
app.py
app/
  config/database.py
  controllers/
  models/
  routes/
public/
  index.html
  styles.css
  app.js
requirements.txt
INICIAR_NO_WINDOWS.bat
data/ (banco criado automaticamente)
docs/
```

## Limitações conhecidas
Protótipo acadêmico funcional. Não possui autenticação de administrador, painel de gestão, integração real com gateway de pagamento, cálculo de frete ou serviço de entrega. O pedido fica registrado no banco para atendimento posterior, incluindo a forma de pagamento escolhida e o status inicial 'Recebido'. A seleção de Pix, dinheiro ou cartão é apenas informativa: não há cobrança, confirmação bancária, cálculo de frete nem rastreamento de entrega. Não inserir dados pessoais reais em demonstrações públicas.

## GitHub e entrega
Mantenha documentação e código no repositório Git solicitado pela disciplina. Não publique arquivos de banco (`*.db`), ambientes virtuais ou dados pessoais. Inclua as evidências dos testes, o formulário/relatórios dos cinco avaliadores e o vídeo de demonstração de até cinco minutos conforme as orientações da atividade.
