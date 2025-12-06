def calcular_custo_tempo_mao_obra(
    qtd_pedido, 
    velocidade_nominal_maquina, 
    eficiencia_operacional, 
    equipe_salarios, 
    encargos_percentual, 
    tempo_setup_minutos=15
):
    """
    Calcula custo de MO e tempo para um pedido específico.
    
    Args:
    qtd_pedido (int): Quantidade de camisetas.
    velocidade_nominal_maquina (int): Peças por hora (ex: Atlas MAX ~100-150).
    eficiencia_operacional (float): 0.0 a 1.0 (ex: 0.70 para 70%).
    equipe_salarios (dict): Dict com cargos e salários base.
    encargos_percentual (float): Taxa de encargos sobre folha (ex: 0.80 para 80%).
    tempo_setup_minutos (int): Tempo morto para preparar o job (limpeza, arquivos).
    """
    
    # 1. Calcular Custo Mensal Total da Equipe
    total_salarios = sum(equipe_salarios.values())
    custo_total_mensal = total_salarios * (1 + encargos_percentual)
    
    # 2. Calcular Custo por Hora e Minuto (Base 176h mensais - 1 turno)
    horas_mes = 176
    custo_hora_equipe = custo_total_mensal / horas_mes
    custo_minuto_equipe = custo_hora_equipe / 60
    
    # 3. Calcular Produtividade Real
    pecas_por_hora_real = velocidade_nominal_maquina * eficiencia_operacional
    pecas_por_minuto_real = pecas_por_hora_real / 60
    
    if pecas_por_minuto_real == 0:
        return "Erro: Eficiência ou Velocidade não podem ser zero."

    # 4. Calcular Tempo Necessário para o Pedido
    # Tempo de impressão + Setup inicial
    tempo_impressao_minutos = qtd_pedido / pecas_por_minuto_real
    tempo_total_job_minutos = tempo_impressao_minutos + tempo_setup_minutos
    
    # Converter para horas decimais para visualização
    tempo_total_horas = tempo_total_job_minutos / 60
    
    # 5. Calcular Custo Específico deste Pedido
    custo_mao_obra_job = tempo_total_job_minutos * custo_minuto_equipe
    custo_mao_obra_unidade = custo_mao_obra_job / qtd_pedido
    
    return {
        "Custo Hora da Equipe (R$)": round(custo_hora_equipe, 2),
        "Velocidade Real (peças/h)": round(pecas_por_hora_real, 0),
        "Tempo Total Job (Horas)": round(tempo_total_horas, 2),
        "Custo Total M.O. Job (R$)": round(custo_mao_obra_job, 2),
        "Custo M.O. por Camiseta (R$)": round(custo_mao_obra_unidade, 2)
    }

# --- SIMULAÇÃO COM DADOS DA PLANILHA (Sheet 1) ---

# Salários aproximados baseados na planilha (Sheet 1, Linhas 60-65)
equipe = {
    "Operador Maquina": 3000.00,
    "Ajudante": 2500.00,
    # "Supervisor": 4000.00 # Opcional: ratear supervisor se ele cuida de várias máquinas
}

# Dados de Entrada
pedido_camisetas = 1000  # O cliente quer 1000 camisetas
velocidade_maquina = 120 # Atlas MAX (média teórica)
eficiencia = 0.70        # 70% (padrão de indústria)
encargos_br = 0.80       # 80% de encargos trabalhistas (estimativa CLT Brasil)

resultado = calcular_custo_tempo_mao_obra(
    pedido_camisetas, 
    velocidade_maquina, 
    eficiencia, 
    equipe, 
    encargos_br
)

print(f"--- ORÇAMENTO DE MÃO DE OBRA PARA {pedido_camisetas} PEÇAS ---")
for k, v in resultado.items():
    print(f"{k}: {v}")