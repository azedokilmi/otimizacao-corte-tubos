import datetime
from fpdf import FPDF

# Dados de matéria-prima e peso (kg) por mm
materia_prima_pesos = {
'0306011207': 0.000990,
'0306011209': 0.001550,
'0306011214': 0.003970,
'0306011217': 0.006210,
'0306011223': 0.015900,
'0306015316': 0.000340,
'0306016514': 0.001630,
'0306021168': 0.001990,
'0306021270': 0.003265,
'0331484701': 0.010470,  
'0331484721': 0.011600,
'0331484752': 0.008010,
'0331489701': 0.008013,
'0331489703': 0.008013,
'0331499801': 0.001572,
'0331500103': 0.008409,
'0331500112': 0.005462,
'0331500113': 0.005462,
'0331500121': 0.006129,
'0331504511': 0.006129,
'0331504901': 0.002271,
}

# 1. Funções de Utilidade
def validar_entrada_inteira(mensagem):
    """Valida e retorna uma entrada numérica inteira positiva."""
    while True:
        try:
            valor = int(input(mensagem))
            if valor > 0:
                return valor
        except ValueError:
            print("❌ Entrada inválida. Digite um número inteiro positivo.")

def agrupar_cortes(cortes):
    """Agrupa os cortes por tamanho e matéria-prima."""
    cortes_agrupados = {}
    for corte in cortes:
        cortes_agrupados[corte] = cortes_agrupados.get(corte, 0) + 1
    return cortes_agrupados

# 2. Funções de Entrada de Dados
def capturar_cortes(comprimentos_tubos):
    """Captura os cortes desejados do usuário e adiciona matéria-prima."""
    cortes = []
    print("\n🔹 **Cortes Desejados**")
    print("-----------------------------------------------\n")
    print("❗️ Códigos de matéria-prima disponíveis:")
    # Mostrar os códigos de matéria-prima com um número para o usuário selecionar
    materia_prima_lista = list(materia_prima_pesos.items())
    for i, (codigo, peso) in enumerate(materia_prima_lista, start=1):
        print(f"{i}. Código: {codigo}, Peso por mm: {peso:.5f} kg")
    print("\n")

    while True:
        entrada = input("Digite o comprimento de um corte (ou 'ENTER' para finalizar): ")
        if not entrada:  # Finaliza a entrada
            break
        try:
            corte = int(entrada)
            if corte <= 0 or corte > max(comprimentos_tubos):
                print("❌ Comprimento inválido. Tente novamente.")
                continue
            quantidade = validar_entrada_inteira("Digite a quantidade desse corte: ")
            while True:
                # Permitir que o usuário escolha a matéria-prima pelo número
                materia_prima_numero = input(
                    f"Digite o número da matéria-prima para o corte de {corte} mm (pressione 'ENTER' para ignorar): "
                )
                if not materia_prima_numero:  # Usuário pressionou ENTER
                    print(f"📦 Matéria-prima ignorada. Peso atribuído como 0 kg por mm para o corte de {corte} mm.")
                    peso = 0
                    break
                try:
                    materia_prima_numero = int(materia_prima_numero)
                    if 1 <= materia_prima_numero <= len(materia_prima_lista):
                        # Pega o código e o peso da matéria-prima selecionada
                        codigo, peso = materia_prima_lista[materia_prima_numero - 1]
                        print(f"📦 Matéria-prima {codigo} com peso de {peso:.5f} kg por mm.")
                        break
                    else:
                        print(f"❌ Número de matéria-prima inválido. Tente novamente.")
                except ValueError:
                    print("❌ Entrada inválida. Tente novamente.")
            for _ in range(quantidade):
                cortes.append((corte, peso))  # Agora adiciona o peso como parte do corte
        except ValueError:
            print("❌ Entrada inválida. Tente novamente.")
    return cortes

# 3. Funções de Alocação
def alocar_cortes_em_pacotes(agrupamento_cortes, comprimentos_tubos):
    """Aloca cortes nos tubos disponíveis, separando por matéria-prima."""
    resultado = []
    cortes_restantes = agrupamento_cortes.copy()

    while cortes_restantes:
        for comprimento_tubo in comprimentos_tubos:
            tubo = {'comprimento': comprimento_tubo, 'cortes': [], 'restante': comprimento_tubo, 'materia_prima': None}
            materia_prima_usada = None  # Matéria-prima associada ao tubo atual
            alocado = False

            for (corte, materia_prima), quantidade in list(cortes_restantes.items()):
                if materia_prima_usada is None:
                    materia_prima_usada = materia_prima  # Define a matéria-prima usada neste tubo

                if materia_prima == materia_prima_usada:  # Alocar apenas cortes da mesma matéria-prima
                    for _ in range(quantidade):
                        if tubo['restante'] >= corte:
                            tubo['cortes'].append((corte, materia_prima))
                            tubo['restante'] -= corte
                            cortes_restantes[(corte, materia_prima)] -= 1
                            alocado = True
                            if cortes_restantes[(corte, materia_prima)] == 0:
                                del cortes_restantes[(corte, materia_prima)]
                        else:
                            break
            if alocado:
                # Garantir que a matéria-prima seja atribuída ao tubo alocado
                tubo['materia_prima'] = materia_prima_usada
                resultado.append(tubo)
    return resultado

def associar_materia_prima_aos_tubos(tubos, materia_prima_por_corte):
    for tubo in tubos:
        if tubo['cortes']:
            # Supondo que todos os cortes em um tubo compartilhem a mesma matéria-prima
            materia_prima = materia_prima_por_corte.get(tubo['cortes'][0][1], 'Não especificado')
            tubo['materia_prima'] = materia_prima
        else:
            tubo['materia_prima'] = 'Não especificado'

def obter_codigo_materia_prima_por_peso(peso, mapa):
    """
    Retorna o código alfanumérico correspondente ao peso específico.
    :param peso: Peso específico (float)
    :param mapa: Dicionário de mapeamento (codigo -> peso)
    :return: Código alfanumérico ou "Código não encontrado" se não existir
    """
    for codigo, peso_mapeado in mapa.items():
        if peso_mapeado == peso:
            return codigo
    return "Código não encontrado"

# Calculando os dados necessários para o desperdício total
def calcular_desperdicio_total(resultado, materia_prima_pesos):
    """
    Calcula o desperdício total de matéria-prima e o peso correspondente por tipo de tubo.
    :param resultado: Lista de tubos com cortes e matéria-prima associada.
    :param materia_prima_pesos: Dicionário com peso por mm por código de matéria-prima.
    :return: Dicionários com o desperdício total e peso por matéria-prima.
    """
    desperdicio_por_materia_prima = {}
    peso_desperdicio_por_materia = {}

    # Calcula o desperdício por matéria-prima
    for tubo in resultado:
        comprimento_tubo = tubo['comprimento']
        materia_prima = tubo['materia_prima']
        sobra_tubo = tubo['restante']

        if materia_prima not in desperdicio_por_materia_prima:
            desperdicio_por_materia_prima[materia_prima] = 0

        desperdicio_por_materia_prima[materia_prima] += sobra_tubo

    # Cálculo do peso do desperdício por matéria-prima
    for codigo, desperdicio in desperdicio_por_materia_prima.items():
        peso = materia_prima_pesos.get(codigo, 0)  # Obtemos o peso por mm para a matéria-prima
        peso_desperdicio_por_materia[codigo] = desperdicio * peso

    return desperdicio_por_materia_prima, peso_desperdicio_por_materia

# 4. Função para gerar relatório PDF
def gerar_relatorio_pdf(resultado, desperdicio_total, quantidade_cortes, quantidade_tubos_utilizados, materia_prima_pesos):
    pdf = FPDF()
    pdf.set_margins(15, 15, 15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Título
    pdf.set_font("Arial", style='B', size=16)
    pdf.cell(0, 10, txt="Relatório de Cortes de Tubos", ln=True, align='C')
    pdf.ln(5)

    # Inicializar as variáveis para armazenar o grupo atual e a matéria-prima
    grupo_atual = None
    materia_prima_atual = None

    # Inicializa os dicionários para desperdício por matéria-prima e peso desperdício por matéria-prima
    desperdicio_por_materia_prima = {}
    peso_desperdicio_por_materia = {}

    for i, tubo in enumerate(resultado):
        cortes_str = ', '.join(f"{corte[0]} mm" for corte in tubo['cortes'])

        # Garantir que a matéria-prima esteja associada corretamente ao tubo
        materia_prima = tubo.get('materia_prima', 'Não especificado')

        # Se a matéria-prima for numérica (peso), busque o código alfanumérico
        if isinstance(materia_prima, float):
            materia_prima = obter_codigo_materia_prima_por_peso(materia_prima, materia_prima_pesos)

        texto = (f"Tubo {i + 1} (Comprimento: {tubo['comprimento']} mm, "
                 f"Matéria-prima: {materia_prima}): "
                 f"Cortes: [{cortes_str}] | Sobrou: {tubo['restante']} mm")

        # Calcula o desperdício do tubo e acumula no desperdício por matéria-prima
        desperdicio = tubo['restante']
        if materia_prima not in desperdicio_por_materia_prima:
            desperdicio_por_materia_prima[materia_prima] = 0
        desperdicio_por_materia_prima[materia_prima] += desperdicio

        # Acumular o desperdício de peso por matéria-prima
        if materia_prima not in peso_desperdicio_por_materia:
            peso_desperdicio_por_materia[materia_prima] = 0
        peso_desperdicio_por_materia[materia_prima] += desperdicio * materia_prima_pesos.get(materia_prima, 1)  # Supondo que materia_prima_pesos tenha os valores de peso

        # Verificar se houve alteração no grupo de cortes ou matéria-prima
        if grupo_atual != materia_prima_atual or materia_prima_atual != materia_prima:
            pdf.ln(5)  # Espaçamento
            pdf.set_draw_color(255, 0, 0)  # Cor da linha (vermelho)
            pdf.set_line_width(1)  # Espessura da linha
            pdf.line(15, pdf.get_y(), 195, pdf.get_y())  # Desenhar linha
            pdf.ln(5)

            # Mudar o grupo atual
            grupo_atual = materia_prima  # Atualiza para o novo grupo
            materia_prima_atual = materia_prima

            # Adicionar título para o novo agrupamento
            pdf.set_font("Arial", style='B', size=12)
            pdf.set_text_color(255, 0, 0)  # Cor do título (vermelho)
            pdf.cell(0, 10, txt=f"Padrão de Corte {len(desperdicio_por_materia_prima)}", ln=True, align='L')
            pdf.set_text_color(0, 0, 0)  # Voltar para a cor de texto padrão

            pdf.set_fill_color(255, 235, 235)  # Fundo suave
            pdf.multi_cell(0, 10, texto, align='L', border=1, fill=True)
            pdf.ln(5)
        else:
            pdf.set_fill_color(255, 255, 255)  # Cor de fundo (branco)
            pdf.multi_cell(0, 10, texto, align='L', border=0, fill=True)
            pdf.ln(5)

    # Quantidade de tubos utilizados por comprimento
    pdf.ln(5)
    pdf.set_font("Arial", style='B', size=12)
    pdf.cell(0, 10, txt="Quantidade de tubos utilizados por comprimento:", ln=True)
    pdf.set_font("Arial", size=12)
    for comprimento, quantidade in quantidade_tubos_utilizados.items():
        pdf.cell(0, 10, txt=f"- Tubos de {comprimento} mm: {quantidade} utilizados", ln=True)

    # Quantidade de cortes realizados por tipo
    pdf.ln(5)
    pdf.set_font("Arial", style='B', size=12)
    pdf.cell(0, 10, txt="Quantidade de cortes realizados por tipo:", ln=True)
    pdf.set_font("Arial", size=12)
    total_cortes = 0  # Inicializa o total de cortes
    # Supondo que 'quantidade_cortes' seja um dicionário no formato: 
    # { (comprimento, materia_prima): quantidade }
    for (comprimento, materia_prima), quantidade in quantidade_cortes.items():
        # Se a matéria-prima for numérica (peso), busque o código alfanumérico
        if isinstance(materia_prima, float):
            materia_prima = obter_codigo_materia_prima_por_peso(materia_prima, materia_prima_pesos)
        pdf.cell(0, 10, txt=f"- Corte de {comprimento} mm (Matéria-prima: {materia_prima}): {quantidade} realizados", ln=True)
        total_cortes += quantidade  # Soma ao total

    # Total de cortes realizados
    pdf.ln(5)
    pdf.set_font("Arial", style='B', size=12)
    pdf.cell(0, 10, txt=f"Total de cortes realizados: {total_cortes}", ln=True)

    # Desperdício total por matéria-prima
    pdf.ln(5)
    pdf.set_font("Arial", style='B', size=12)
    pdf.cell(0, 10, txt="Comprimento total desperdiçado por matéria-prima (mm):", ln=True)
    pdf.set_font("Arial", size=12)
    for materia_prima, desperdicio in desperdicio_por_materia_prima.items():
        pdf.cell(0, 10, txt=f"- {materia_prima}: {desperdicio:} mm", ln=True)

    # Comprimento total desperdiçado
    pdf.ln(5)
    pdf.set_font("Arial", style='B', size=12)
    pdf.cell(0, 10, txt=f"Comprimento total desperdiçado: {desperdicio_total} mm", ln=True)

    pdf.ln(5)
    pdf.set_font("Arial", style='B', size=12)
    pdf.cell(0, 10, txt="Peso total desperdiçado por matéria-prima (kg):", ln=True)
    pdf.set_font("Arial", size=12)
    for materia_prima, peso in peso_desperdicio_por_materia.items():
        pdf.cell(0, 10, txt=f"- {materia_prima}: {peso:.2f} kg", ln=True)

    # Peso total desperdiçado
    pdf.ln(5)
    pdf.set_font("Arial", style='B', size=12)
    peso_total_desperdicio = sum(peso_desperdicio_por_materia.values())
    pdf.cell(0, 10, txt=f"Peso total desperdiçado: {peso_total_desperdicio:.2f} kg", ln=True)

    # Salvar o arquivo
    data_atual = datetime.datetime.now().strftime("%d-%m-%Y")
    pdf_file_name = f"Relatório_Corte_Tubos_{data_atual}.pdf"
    pdf.output(pdf_file_name)
    
# 5. Processo Principal
def processar_agrupamento_e_alocacao():
    """Executa o processo principal de alocação e geração de relatório."""
    print("\n✅ Bem-vindo ao Otimizador de Corte de Tubos! ✅")
    print("-----------------------------------------------\n")

    # Entrada dos comprimentos de tubos disponíveis
    comprimentos_tubos = []
    print("🔹 **Comprimentos dos tubos disponíveis**")
    print("-----------------------------------------------\n")
    while True:
        entrada = input("Digite o comprimento de um tubo disponível para corte (ou 'ENTER' para finalizar): ")
        if not entrada:
            break
        try:
            comprimento = int(entrada)
            if comprimento > 0:
                comprimentos_tubos.append(comprimento)
        except ValueError:
            print("❌ Entrada inválida. Digite um número inteiro positivo.")
    if not comprimentos_tubos:
        print("❌ Nenhum comprimento de tubo foi informado. Saindo...")
        return

    # Entrada dos cortes
    cortes = capturar_cortes(comprimentos_tubos)
    if not cortes:
        print("❌ Nenhum corte foi informado. Saindo...")
        return

    # Agrupamento de cortes por tipo
    agrupamento_cortes = agrupar_cortes(cortes)

    # Alocação de cortes nos tubos, garantindo que a matéria-prima seja associada corretamente
    resultado = alocar_cortes_em_pacotes(agrupamento_cortes, comprimentos_tubos)

    # Calcular desperdício total em comprimento
    desperdicio_total = sum(tubo['restante'] for tubo in resultado)

    # Calcular desperdício total em peso
    desperdicio_em_peso = sum(
        tubo['restante'] * materia_prima_pesos.get(tubo.get('materia_prima', 'Desconhecido'), 0)
        for tubo in resultado if tubo.get('restante', 0) > 0
    )
    
    # Quantificar os cortes e os tubos utilizados
    quantidade_cortes = agrupar_cortes(cortes)
    quantidade_tubos_utilizados = {comprimento: sum(1 for tubo in resultado if tubo['comprimento'] == comprimento)
                                   for comprimento in comprimentos_tubos}

    # Resumo
    #print("\n🔹 **Resumo da Alocação**")
    #print(f"📦 Total de cortes realizados: {sum(quantidade_cortes.values())}")
    #print(f"📉 Desperdício total em comprimento: {desperdicio_total} mm")
    #print(f"📉 Desperdício total em peso: {desperdicio_em_peso:.2f} kg")
    #print(f"📈 Quantidade de tubos utilizados: {len(resultado)}")
    
    # Gerar relatório, passando a variável materia_prima_pesos
    gerar_relatorio_pdf(resultado, desperdicio_total, quantidade_cortes, quantidade_tubos_utilizados, materia_prima_pesos)
    print("\n ✅ Relatório gerado com sucesso!")

    input("\nPressione ENTER para sair...")

# Chama a função principal para iniciar
processar_agrupamento_e_alocacao()