import random
import time

# ----------------------------------------------------
#   ALGORITMO GENÉTICO - PROBLEMA DO TIME POKÉMON
# ----------------------------------------------------
#  Objetivo: montar um time Pokémon com o maior poder
#  possível, sem ultrapassar o limite máximo de peso.
# ----------------------------------------------------

# ---------------- CONFIGURAÇÃO DO PROBLEMA ----------------
POKEMONS = [
    {"nome": "Pikachu", "peso": 6, "poder": 55},
    {"nome": "Bulbasaur", "peso": 6.9, "poder": 49},
    {"nome": "Charmander", "peso": 8.5, "poder": 52},
    {"nome": "Squirtle", "peso": 9, "poder": 48},
    {"nome": "Snorlax", "peso": 460, "poder": 110},
    {"nome": "Cosmoem", "peso": 999.9, "poder": 45},
    {"nome": "Eevee", "peso": 6.5, "poder": 50},
    {"nome": "Machop", "peso": 19.5, "poder": 80},
    {"nome": "Pidgeotto", "peso": 30, "poder": 60},
    {"nome": "Onix", "peso": 210, "poder": 45},
]

CAPACIDADE = 60  # limite máximo de peso (capacidade da mochila)
NUM_POKEMONS = len(POKEMONS)

# ---------------- PARÂMETROS DO ALGORITMO ----------------
TAMANHO_POPULACAO = 10
TAXA_SOBREVIVENCIA = 0.5
TAXA_MUTACAO = 0.1
GERACOES = 100
random.seed(42)  # para resultados reproduzíveis

# ---------------- FUNÇÕES GENÉTICAS ----------------
def criar_treinador():
    """
    Cria um indivíduo representando um treinador com um time.
    Cada posição é 1 (Pokémon escolhido) ou 0 (não escolhido).
    """
    return [random.randint(0, 1) for _ in range(NUM_POKEMONS)]


def calcular_fitness(individuo):
    """
    Calcula o 'poder total' do time.
    Se o peso total ultrapassar o limite, o fitness é 0 (penalização).
    """
    peso_total = sum(POKEMONS[i]["peso"] * individuo[i] for i in range(NUM_POKEMONS))
    poder_total = sum(POKEMONS[i]["poder"] * individuo[i] for i in range(NUM_POKEMONS))
    if peso_total > CAPACIDADE:
        return 0
    return poder_total


def selecionar_individuo(populacao, fitness):
    """
    Seleciona um indivíduo da população usando o método da roleta.
    Quanto maior o fitness, maior a chance de ser escolhido.
    """
    total_fitness = sum(fitness)
    if total_fitness == 0:
        return random.choice(populacao)
    ponto = random.uniform(0, total_fitness)
    soma = 0
    for i, ind in enumerate(populacao):
        soma += fitness[i]
        if soma > ponto:
            return ind
    return populacao[-1]


def selecionar_populacao(populacao, fitness, taxa_sobrevivencia):
    """
    Seleciona uma porcentagem dos indivíduos mais aptos
    (baseado na taxa de sobrevivência).
    """
    sobreviventes = []
    numero_sobreviventes = int(taxa_sobrevivencia * len(populacao))
    for _ in range(numero_sobreviventes):
        sobreviventes.append(selecionar_individuo(populacao, fitness))
    return sobreviventes


def cruzar(pai1, pai2):
    """Realiza o cruzamento entre dois indivíduos."""
    ponto = random.randint(1, NUM_POKEMONS - 1)
    filho = pai1[:ponto] + pai2[ponto:]
    return filho


def mutar(individuo, taxa_mutacao):
    """Aplica mutação em genes aleatórios do indivíduo."""
    for i in range(NUM_POKEMONS):
        if random.random() < taxa_mutacao:
            individuo[i] = 1 - individuo[i]
    return individuo

# ---------------- EXECUÇÃO DO ALGORITMO ----------------
inicio = time.time()

populacao = [criar_treinador() for _ in range(TAMANHO_POPULACAO)]

for geracao in range(GERACOES):
    fitness = [calcular_fitness(ind) for ind in populacao]

    # Seleciona os melhores (sobreviventes)
    nova_populacao = selecionar_populacao(populacao, fitness, TAXA_SOBREVIVENCIA)

    # Gera filhos até completar a população novamente
    while len(nova_populacao) < TAMANHO_POPULACAO:
        pai1 = random.choice(nova_populacao)
        pai2 = random.choice(nova_populacao)
        filho = cruzar(pai1, pai2)
        filho = mutar(filho, TAXA_MUTACAO)
        nova_populacao.append(filho)

    populacao = nova_populacao

fim = time.time()

# ---------------- RESULTADOS ----------------
melhor_individuo = max(populacao, key=calcular_fitness)
melhor_fitness = calcular_fitness(melhor_individuo)
peso_total = sum(POKEMONS[i]["peso"] * melhor_individuo[i] for i in range(NUM_POKEMONS))
time_final = [POKEMONS[i]["nome"] for i in range(NUM_POKEMONS) if melhor_individuo[i] == 1]

print("\n=== MELHOR TIME POKÉMON ENCONTRADO ===")
print("Pokémons escolhidos:", ", ".join(time_final))
print(f"Poder total: {melhor_fitness}")
print(f"Peso total: {peso_total:.1f} / {CAPACIDADE}")
print(f"Tempo de execução: {fim - inicio:.4f} segundos")
