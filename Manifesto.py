# ---------- exemplo ----------
# piloto = 85 kg
# Passageiro = 75 kg
# Bagagem 1 = 10 kg max
# Bagagem 2 = 0 kg max
# Combustível = 26 galoes
# -----------------------------
#Rodolfo Milhomem
#https://github.com/rodolfo-space-force/

import matplotlib.pyplot as plt

# ---------- Conversão ----------
def mm(inch): 
    return inch * 25.4

def gal_to_kg(gal):
    return gal * 2.72   # 1 US gal = 2.72 kg (Avgas)

# ---------- Envelope: vértices iguais ao desenho ----------
ENV_IN_INCH = [31.00, 31.00, 32.65, 36.70, 36.70]
ENV_IN_MM   = [mm(x) for x in ENV_IN_INCH]
ENV_KG      = [475,   610,   757,   757,   475]

# ---------- Braços (dados do quadro fornecido) ----------
ARM_FRONT = mm(39.0)   # assentos dianteiros
ARM_BAG1  = mm(64.0)   # bagagem área 1
ARM_BAG2  = mm(84.0)   # bagagem área 2
ARM_FUEL  = mm(42.0)   # tanques

# Peso vazio (exemplo: 500 kg e braço ~820 mm; substitua pelo real do seu avião)
ARM_EMPTY = 820  
WEIGHT_EMPTY = 500     

def calcular_plotar():
    # Entradas
    piloto      = float(input("Peso do piloto (kg): "))
    passageiro  = float(input("Peso do passageiro (kg): "))
    bag1        = float(input("Peso da bagagem área 1 (kg): "))
    bag2        = float(input("Peso da bagagem área 2 (kg): "))

    # Combustível: escolha galões ou kg
    tipo = input("Você deseja inserir combustível em [g]alões ou [k]g? ").strip().lower()
    if tipo == "g":
        combustivel_gal = float(input("Combustível (US gal): "))
        combustivel = gal_to_kg(combustivel_gal)
    else:
        combustivel = float(input("Combustível (kg): "))

    # Itens: (peso, braço)
    items = {
        "Peso Vazio": (WEIGHT_EMPTY, ARM_EMPTY),
        "Piloto": (piloto, ARM_FRONT),
        "Passageiro": (passageiro, ARM_FRONT),
        "Bagagem 1": (bag1, ARM_BAG1),
        "Bagagem 2": (bag2, ARM_BAG2),
        "Combustível": (combustivel, ARM_FUEL),
    }

    # Tabela e somatórios
    print(f"\n{'Item':<15}{'Peso (kg)':<12}{'Braço (mm)':<12}{'Momento (kg·mm)':<20}")
    print("-"*60)
    peso_total = 0
    momento_total = 0
    for item, (peso, braco) in items.items():
        momento = peso * braco
        peso_total += peso
        momento_total += momento
        print(f"{item:<15}{peso:<12.1f}{braco:<12.0f}{momento:<20.0f}")
    cg = momento_total / peso_total
    print("-"*60)
    print(f"TOTAL: {peso_total:.1f} kg | Momento total: {momento_total:.0f} kg·mm")
    print(f"CG: {cg:.1f} mm aft of datum ({cg/25.4:.2f} in)\n")

    # Plot
    plt.figure(figsize=(9,6))
    plt.fill(ENV_IN_MM, ENV_KG, alpha=0.25, label="Envelope (POH)")
    plt.plot(ENV_IN_MM + [ENV_IN_MM[0]], ENV_KG + [ENV_KG[0]], linewidth=2)
    plt.scatter([cg], [peso_total], s=80, label="Configuração calculada")

    plt.title("Envelope de Peso e Balanceamento - Cessna 152")
    plt.xlabel("Centro de Gravidade (mm aft of datum)")
    plt.ylabel("Peso Total (kg)")
    plt.xlim(mm(30.8), mm(37.0))
    plt.ylim(470, 800)
    plt.grid(True, linestyle=":", alpha=0.6)
    plt.legend(loc="lower right")

    ax = plt.gca()
    ax_top = ax.secondary_xaxis('top', functions=(lambda x: x/25.4, lambda x: x*25.4))
    ax_top.set_xlabel("AIRPLANE C.G. LOCATION – INCHES AFT OF DATUM (STA. 0.0)")
    ax_right = ax.secondary_yaxis('right', functions=(lambda kg: kg*2.20462, lambda lb: lb/2.20462))
    ax_right.set_ylabel("LOADED AIRPLANE WEIGHT (POUNDS)")

    plt.show()

# --------- Executar ----------
calcular_plotar()

# Licença
#Este projeto está licenciado sob a **Licença MIT**.  
#Você pode usar, modificar e redistribuir este código livremente, **desde que mencione o autor original**.
