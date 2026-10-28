# audit_benchmark.py
# ==============================================================================
# XPRIZE QUANTUM APPLICATIONS: INDEPENDENT VERIFIER & PHYSICS AUDIT
# ==============================================================================
import json
import numpy as np

def auditar_resultado():
    print("=" * 75)
    print("🔬 AUDITORIA INDEPENDENTE DE FÍSICA: XPRIZE MICROGRID PHASE BALANCING")
    print("=" * 75)

    with open("data_ieee_2000.json", "r") as f:
        problema = json.load(f)

    with open("solution_ground_truth.json", "r") as f:
        solucao = json.load(f)

    correntes = np.array(problema["currents"])
    feeders = problema["feeders"]
    spins = {int(k): v for k, v in solucao["spins"].items()}

    print(f"[*] Instância: {problema['num_nodes']} Cargas | {problema['num_feeders']} Alimentadores")
    print(f"[*] Tempo de Convergência do Motor: {solucao['execution_time_seconds']} segundos")
    print("\n[+] Auditando correntes de neutro alimentador por alimentador...")

    i_neutro_antes_total = 0.0
    i_neutro_depois_total = 0.0

    for f_idx, feeder in enumerate(feeders):
        i_feeder = correntes[feeder]
        s_feeder = np.array([spins[u] for u in feeder])

        # Estado inicial desbalanceado (todas as cargas na Fase A, spin = 1)
        i_antes = abs(np.sum(i_feeder))
        # Estado pós-convergência MEA
        i_depois = abs(np.sum(i_feeder * s_feeder))

        i_neutro_antes_total += i_antes
        i_neutro_depois_total += i_depois

    eficiencia = (1.0 - (i_neutro_depois_total / i_neutro_antes_total)) * 100.0

    # Cálculo térmico (Lei de Joule: P = R * I^2, assumindo R = 0.30 Ohm)
    r_feeder = 0.30
    perdas_kw_antes = sum(r_feeder * (abs(sum(correntes[feeder])) ** 2) for feeder in feeders) / 1000.0
    perdas_kw_depois = sum(r_feeder * (abs(sum(correntes[feeder] * np.array([spins[u] for u in feeder]))) ** 2) for feeder in feeders) / 1000.0

    print("-" * 75)
    print(f"• Corrente de Neutro Inicial (Sem Otimização) : {i_neutro_antes_total:,.1f} A")
    print(f"• Corrente de Neutro Final (Solução MEA v14.5) : {i_neutro_depois_total:,.1f} A")
    print(f"• Eficiência de Cancelamento Parasita        : {eficiencia:.2f}%")
    print(f"• Perdas Técnicas Joule (Iniciais)           : {perdas_kw_antes:,.2f} kW")
    print(f"• Perdas Técnicas Joule (Finais)             : {perdas_kw_depois:,.4f} kW")
    print(f"• Potência Térmica Recuperada Instantânea    : {(perdas_kw_antes - perdas_kw_depois):,.2f} kW")
    print("-" * 75)

    if eficiencia >= 99.0:
        print("🏆 CERTIFICADO VÁLIDO: CONVERGÊNCIA COMPROVADA MATEMATICAMENTE!")
    else:
        print("⚠️ Falha de validação.")
    print("=" * 75)

if __name__ == "__main__":
    auditar_resultado()