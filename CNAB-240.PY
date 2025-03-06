import tkinter as tk
from tkinter import messagebox
import datetime

# Função para gerar o header do arquivo
def gerar_header(codigo_banco, cnpj_empresa, nome_empresa, data_geracao, hora_geracao, numero_remessa):
    header = f"0{codigo_banco:03d}2{cnpj_empresa:014d}{nome_empresa:<40}{data_geracao}{hora_geracao}{numero_remessa:06d}"
    return header

# Função para gerar o registro detalhe (um boleto)
def gerar_registro_detalhe(codigo_banco, tipo_inscricao, numero_inscricao, nome_pagador, endereco_pagador, numero_boleto, nosso_numero, data_vencimento, valor_boleto):
    detalhe = f"1{codigo_banco:03d}{tipo_inscricao:01d}{numero_inscricao:014d}{nome_pagador:<40}{endereco_pagador:<40}{numero_boleto:012d}{nosso_numero:012d}{data_vencimento}{valor_boleto:013.2f}"
    return detalhe

# Função para gerar o trailer do arquivo
def gerar_trailer(qtd_registros, valor_total):
    trailer = f"9{qtd_registros:06d}{valor_total:013.2f}"
    return trailer

# Função para gerar o arquivo CNAB 240 a partir dos dados fornecidos pela interface
def gerar_arquivo_cnab_240():
    try:
        # Dados do header
        codigo_banco = int(entry_codigo_banco.get())  # Código do banco
        cnpj_empresa = int(entry_cnpj_empresa.get())  # CNPJ da empresa
        nome_empresa = entry_nome_empresa.get()  # Nome da empresa
        data_geracao = datetime.datetime.now().strftime("%d%m%Y")  # Data de geração (ddmmaaaa)
        hora_geracao = datetime.datetime.now().strftime("%H%M")  # Hora de geração (hhmm)
        numero_remessa = int(entry_numero_remessa.get())  # Número da remessa

        # Gerar header
        header = gerar_header(codigo_banco, cnpj_empresa, nome_empresa, data_geracao, hora_geracao, numero_remessa)

        # Criar registros de detalhe a partir dos dados fornecidos
        registros_detalhe = []
        for i in range(len(entries_registros)):
            tipo_inscricao = int(entries_registros[i][0].get())
            numero_inscricao = int(entries_registros[i][1].get())
            nome_pagador = entries_registros[i][2].get()
            endereco_pagador = entries_registros[i][3].get()
            numero_boleto = int(entries_registros[i][4].get())
            nosso_numero = int(entries_registros[i][5].get())
            data_vencimento = entries_registros[i][6].get()
            valor_boleto = float(entries_registros[i][7].get())
            
            registro = gerar_registro_detalhe(codigo_banco, tipo_inscricao, numero_inscricao, nome_pagador, endereco_pagador, numero_boleto, nosso_numero, data_vencimento, valor_boleto)
            registros_detalhe.append(registro)

        # Dados do trailer
        qtd_registros = len(registros_detalhe) + 1  # 1 para o header
        valor_total = sum([float(entries_registros[i][7].get()) for i in range(len(entries_registros))])  # Soma dos valores dos boletos

        trailer = gerar_trailer(qtd_registros, valor_total)

        # Gerar o arquivo CNAB 240 completo
        arquivo_cnab = header + "\n" + "\n".join(registros_detalhe) + "\n" + trailer

        # Salvar o arquivo
        with open("cnab_240.txt", "w") as f:
            f.write(arquivo_cnab)
        messagebox.showinfo("Sucesso", "Arquivo CNAB 240 gerado com sucesso!")

    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro: {e}")

# Configuração da interface gráfica
root = tk.Tk()
root.title("Gerador CNAB 240")

# Layout dos campos de entrada para o usuário
frame_entrada = tk.Frame(root)
frame_entrada.pack(pady=10)

# Campos de entrada para o Header
tk.Label(frame_entrada, text="Código do Banco:").grid(row=0, column=0, padx=5, pady=5)
entry_codigo_banco = tk.Entry(frame_entrada)
entry_codigo_banco.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame_entrada, text="CNPJ da Empresa:").grid(row=1, column=0, padx=5, pady=5)
entry_cnpj_empresa = tk.Entry(frame_entrada)
entry_cnpj_empresa.grid(row=1, column=1, padx=5, pady=5)

tk.Label(frame_entrada, text="Nome da Empresa:").grid(row=2, column=0, padx=5, pady=5)
entry_nome_empresa = tk.Entry(frame_entrada)
entry_nome_empresa.grid(row=2, column=1, padx=5, pady=5)

tk.Label(frame_entrada, text="Número da Remessa:").grid(row=3, column=0, padx=5, pady=5)
entry_numero_remessa = tk.Entry(frame_entrada)
entry_numero_remessa.grid(row=3, column=1, padx=5, pady=5)

# Adicionando campos de detalhes (exemplo de 2 registros)
frame_detalhes = tk.LabelFrame(root, text="Registros Detalhe", padx=10, pady=10)
frame_detalhes.pack(padx=10, pady=10)

entries_registros = []

for i in range(2):  # Exemplo com 2 registros de boleto
    tk.Label(frame_detalhes, text=f"Registro {i+1}").grid(row=i*8, column=0, columnspan=2, padx=5, pady=5)
    
    tk.Label(frame_detalhes, text="Tipo de Inscrição:").grid(row=i*8+1, column=0, padx=5, pady=5)
    tipo_inscricao = tk.Entry(frame_detalhes)
    tipo_inscricao.grid(row=i*8+1, column=1, padx=5, pady=5)
    
    tk.Label(frame_detalhes, text="Número de Inscrição:").grid(row=i*8+2, column=0, padx=5, pady=5)
    numero_inscricao = tk.Entry(frame_detalhes)
    numero_inscricao.grid(row=i*8+2, column=1, padx=5, pady=5)
    
    tk.Label(frame_detalhes, text="Nome do Pagador:").grid(row=i*8+3, column=0, padx=5, pady=5)
    nome_pagador = tk.Entry(frame_detalhes)
    nome_pagador.grid(row=i*8+3, column=1, padx=5, pady=5)
    
    tk.Label(frame_detalhes, text="Endereço do Pagador:").grid(row=i*8+4, column=0, padx=5, pady=5)
    endereco_pagador = tk.Entry(frame_detalhes)
    endereco_pagador.grid(row=i*8+4, column=1, padx=5, pady=5)
    
    tk.Label(frame_detalhes, text="Número do Boleto:").grid(row=i*8+5, column=0, padx=5, pady=5)
    numero_boleto = tk.Entry(frame_detalhes)
    numero_boleto.grid(row=i*8+5, column=1, padx=5, pady=5)
    
    tk.Label(frame_detalhes, text="Nosso Número:").grid(row=i*8+6, column=0, padx=5, pady=5)
    nosso_numero = tk.Entry(frame_detalhes)
    nosso_numero.grid(row=i*8+6, column=1, padx=5, pady=5)
    
    tk.Label(frame_detalhes, text="Data de Vencimento:").grid(row=i*8+7, column=0, padx=5, pady=5)
    data_vencimento = tk.Entry(frame_detalhes)
    data_vencimento.grid(row=i*8+7, column=1, padx=5, pady=5)
    
    tk.Label(frame_detalhes, text="Valor do Boleto:").grid(row=i*8+8, column=0, padx=5, pady=5)
    valor_boleto = tk.Entry(frame_detalhes)
    valor_boleto.grid(row=i*8+8, column=1, padx=5, pady=5)
    
    # Armazenar as entradas para esse registro
    entries_registros.append([tipo_inscricao, numero_inscricao, nome_pagador, endereco_pagador, numero_boleto, nosso_numero, data_vencimento, valor_boleto])

# Botão para gerar o arquivo CNAB 240
botao_gerar = tk.Button(root, text="Gerar Arquivo CNAB 240", command=gerar_arquivo_cnab_240)
botao_gerar.pack(pady=10)

# Executa a interface
root.mainloop()
