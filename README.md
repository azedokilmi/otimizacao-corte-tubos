# 🧠 Otimizador de Corte de Tubos

Este projeto em Python realiza a alocação ideal de cortes de tubos de comprimentos variados, buscando minimizar o desperdício de matéria-prima. O sistema gera um relatório completo em PDF contendo os cortes realizados, sobras de material e peso desperdiçado por tipo de tubo.

---

## ⚙️ Como Funciona?

1. 📥 **Entrada de Dados**
   - O usuário informa os **comprimentos disponíveis dos tubos** e os **cortes desejados**.
   - Para cada corte, é possível associar um tipo de **matéria-prima**, identificada por um código e seu respectivo **peso por milímetro**.
   - Exemplo de código de matéria-prima: `0306011217` com peso de `0.006210 kg/mm`.

2. 🧠 **Algoritmo de Alocação**
   - Os cortes são agrupados por comprimento e tipo de matéria-prima.
   - O algoritmo aloca os cortes nos tubos disponíveis, sempre utilizando tubos da mesma matéria-prima.
   - A alocação considera o melhor aproveitamento possível para minimizar o material desperdiçado.

3. 📊 **Relatório em PDF**
   - Detalhamento completo da alocação:
     - Comprimento do tubo
     - Matéria-prima utilizada
     - Cortes realizados
     - Sobra de material
   - Estatísticas incluídas:
     - Total de cortes realizados
     - Quantidade de tubos utilizados por comprimento
     - Desperdício total em milímetros e em quilos por matéria-prima

---

## 🚀 Passo a Passo para Execução

1. **Tenha o Python instalado**  
   Recomendado: Python 3.8+

2. **Instale a dependência necessária:**

   ```bash
   pip install fpdf
   ```

3. **Execute o programa**: no terminal (ou prompt de comando), navegue até a área de trabalho onde o arquivo `.py` (👉 [Clique aqui para visualizar o arquivo](https://github.com/azedokilmi/distribuicao-ordens-robos/blob/main/Relatorio-das-Ordens-dos-Robos.py)) deve estar localizado e execute o comando abaixo:
   
   Após a execução do script, os arquivos de saída serão gerados na mesma pasta onde o programa foi executado.
   ```bash
   python Corte-de-Tubos.py
   ```
   
4. **Siga as instruções no terminal**:
   - Informe os comprimentos dos tubos disponíveis.
   - Adicione os cortes desejados e selecione a matéria-prima correspondente.
  
5. **🖱️ Executável OneFile (.exe)**

   Para facilitar o uso diário e tornar o processo mais prático, foi gerado um executável "onefile" (.exe) que pode ser rodado diretamente com dois cliques, sem a necessidade de abrir o prompt de comando ou programas de codagem como JupyterLab ou VS Code.

   📂 O arquivo .exe está localizado na área de trabalho do Windows, e ao executá-lo, o processo funciona normalmente como se estivesse rodando o script .py.
  
## 📂 O que será Gerado

Após rodar o programa, os seguintes arquivos serão gerados:

  - 📄 **Relatório em PDF**  

    - Documento completo com:
    
    - Lista de tubos utilizados
    
    - Cortes em cada tubo
    
    - Desperdícios
    
    - Análise por tipo de matéria-prima
    
    O nome do arquivo será gerado com a data atual, por exemplo:
    
    **Relatório_Corte_Tubos_15-04-2025.pdf**
    (👉 [Clique aqui para visualizar o relatório em PDF](https://github.com/azedokilmi/distribuicao-ordens-robos/raw/main/Pecas-e-Componentes-Relatorio-Ordens-11-04-2025.pdf))
  
    ![Prévia do Relatório em PDF](https://github.com/azedokilmi/distribuicao-ordens-robos/raw/main/preview-pdf.png)

## 💡 Ideias Futuras

Exportação dos dados em Excel ou CSV.

Interface gráfica para facilitar o apontamento dos cortes.

Visualização gráfica do aproveitamento dos tubos.

Integração com ERP para automatizar entrada de dados.

Algoritmo otimizado de cutting stock problem com heurísticas mais eficientes.

## ✍️ Autor

Feito com dedicação por Pedro Cicilini de Nadai 💻
GitHub: @azedokilmi
