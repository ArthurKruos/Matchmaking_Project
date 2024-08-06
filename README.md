# Matchmaking de Jogos

Este projeto é um algoritmo de matchmaking desenvolvido em Python, que visa encontrar pares de jogadores com base em características de preferência como idade, gênero, preferências de jogos, disponibilidade de horário e gostos pessoais.

## Funcionalidades

- Coleta de dados dos usuários (idade, preferências de jogos, disponibilidade de horário, etc.).
- Armazenamento de dados em listas e dicionários.
- Cálculo de similaridade entre usuários.
- Algoritmo Quicksort para ordenar usuários por similaridade.
- Interface de usuário via terminal para interação.

## Como Funciona

1. **Coleta de Dados**: Os usuários preenchem um formulário com suas preferências.
2. **Armazenamento**: Os dados são armazenados em uma lista de dicionários.
3. **Cálculo de Similaridade**: A similaridade entre usuários é calculada usando uma combinação de idade, preferências de jogos e disponibilidade de horário.
4. **Ordenação**: Os usuários são ordenados por similaridade usando o algoritmo Quicksort.
5. **Matchmaking**: O sistema encontra e sugere o melhor par de jogadores baseado na similaridade.

## Estrutura do Projeto

- `main.py`: Contém a lógica principal do programa.
- `quicksort.py`: Implementação do algoritmo Quicksort.
- `similarity.py`: Funções para cálculo de similaridade entre usuários.

## Executando o Projeto

1. Clone este repositório:
   ```sh
   git clone https://github.com/seu_usuario/matchmaking-jogos.git
