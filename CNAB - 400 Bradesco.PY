import tkinter as tk
from tkinter import messagebox

# Função para separar os campos da linha CNAB 400
def separar_campos_cnab_400(linha):
    campos = {
        'identificacao_titulo': linha[70:82],  # Posição 71-82
        'identificacao_ocorrencia': linha[108:110],  # Posição 109-110
        'data_vencimento': linha[146:152],  # Posição 147-152
        'valor_titulo': linha[152:165],  # Posição 153-165
        'valor_pago': linha[253:266],  # Posição 254-266
        'data_pagamento': linha[295:301],  # Posição 296-301
        'coluna_medicao': linha[395:401]  # Posição 396-401
    }
    return campos

# Função para gerar a linha CNAB 400 corrigida
def gerar_linha_cnab_400():
    linha_usuario = campo_linha_usuario.get("1.0", tk.END).strip()
    
    # Verificar se a linha tem exatamente 400 caracteres
    if len(linha_usuario) != 400:
        messagebox.showerror("Erro", "A linha CNAB 400 deve ter exatamente 400 caracteres!")
        return

    # Separar os campos da linha CNAB 400
    campos = separar_campos_cnab_400(linha_usuario)

    # Garantindo que os campos não ultrapassem os limites de caracteres e ajustando os tamanhos
    campos['identificacao_titulo'] = campo_identificacao_titulo.get().ljust(12)[:12]
    campos['identificacao_ocorrencia'] = campo_identificacao_ocorrencia.get().ljust(2)[:2]
    campos['data_vencimento'] = campo_data_vencimento.get().ljust(6)[:6]
    campos['valor_titulo'] = campo_valor_titulo.get().ljust(13)[:13]
    campos['valor_pago'] = campo_valor_pago.get().ljust(13)[:13]
    campos['data_pagamento'] = campo_data_pagamento.get().ljust(6)[:6]
    campos['coluna_medicao'] = campo_coluna_medicao.get().ljust(6)[:6]
    
    # Gerando a linha corrigida
    linha_corrigida = (
        linha_usuario[:70] + campos['identificacao_titulo'] +
        linha_usuario[82:108] + campos['identificacao_ocorrencia'] +
        linha_usuario[110:146] + campos['data_vencimento'] +
        campos['valor_titulo'] + linha_usuario[165:253] +
        campos['valor_pago'] + linha_usuario[266:295] +
        campos['data_pagamento'] + linha_usuario[301:395] +
        campos['coluna_medicao']
    )

    # Exibe a linha corrigida na área de texto
    text_area.delete(1.0, tk.END)
    text_area.insert(tk.END, linha_corrigida)

# Função para carregar a linha CNAB 400
def carregar_linha():
    linha_usuario = campo_linha_usuario.get("1.0", tk.END).strip()
    
    # Verifica se a linha tem exatamente 400 caracteres
    if len(linha_usuario) != 400:
        messagebox.showerror("Erro", "A linha CNAB 400 deve ter exatamente 400 caracteres!")
        return

    campos = separar_campos_cnab_400(linha_usuario)

    # Preenche os campos com os valores extraídos da linha CNAB
    campo_identificacao_titulo.delete(0, tk.END)
    campo_identificacao_titulo.insert(tk.END, campos['identificacao_titulo'])
    
    campo_identificacao_ocorrencia.delete(0, tk.END)
    campo_identificacao_ocorrencia.insert(tk.END, campos['identificacao_ocorrencia'])
    
    campo_data_vencimento.delete(0, tk.END)
    campo_data_vencimento.insert(tk.END, campos['data_vencimento'])
    
    campo_valor_titulo.delete(0, tk.END)
    campo_valor_titulo.insert(tk.END, campos['valor_titulo'])
    
    campo_valor_pago.delete(0, tk.END)
    campo_valor_pago.insert(tk.END, campos['valor_pago'])
    
    campo_data_pagamento.delete(0, tk.END)
    campo_data_pagamento.insert(tk.END, campos['data_pagamento'])

    campo_coluna_medicao.delete(0, tk.END)
    campo_coluna_medicao.insert(tk.END, campos['coluna_medicao'])

# Função de validação para garantir os limites de caracteres
def validar_input(valor, max_len):
    if len(valor) > max_len:
        return False  # Impede a digitação de mais do que o limite
    return True

# Funções de validação específicas para cada campo (tamanho máximo)
def validar_input_identificacao_titulo(valor):
    return len(valor) <= 12

def validar_input_identificacao_ocorrencia(valor):
    return len(valor) <= 2

def validar_input_data_vencimento(valor):
    return len(valor) <= 6

def validar_input_valor_titulo(valor):
    return len(valor) <= 13

def validar_input_valor_pago(valor):
    return len(valor) <= 13

def validar_input_data_pagamento(valor):
    return len(valor) <= 6

def validar_input_coluna_medicao(valor):
    return len(valor) <= 6

# Função para criar validadores para cada campo
def criar_validador(funcao_validacao):
    return root.register(funcao_validacao)

# Função para obter o banco escolhido pelo usuário
def obter_banco_selecionado():
    return banco_var.get()

# Configuração da interface gráfica
root = tk.Tk()
root.title("Correção de Linha CNAB 400")

# Layout dos campos de entrada para o usuário
frame_entrada = tk.Frame(root)
frame_entrada.pack(pady=10)

# Campo para o usuário inserir a linha CNAB 400
tk.Label(frame_entrada, text="Cole a linha CNAB 400 (400 caracteres):").grid(row=0, column=0, padx=5, pady=5)
campo_linha_usuario = tk.Text(frame_entrada, height=3, width=60)
campo_linha_usuario.grid(row=0, column=1, padx=5, pady=5)

# Adicionando o seletor de banco
tk.Label(frame_entrada, text="Escolha o Banco:").grid(row=1, column=0, padx=5, pady=5)
banco_var = tk.StringVar()
banco_var.set("Bradesco")  # Valor inicial
seletor_banco = tk.OptionMenu(frame_entrada, banco_var, "Bradesco", "Itaú")
seletor_banco.grid(row=1, column=1, padx=5, pady=5)

# Botão para carregar os valores dos campos a partir da linha CNAB 400
botao_carregar = tk.Button(root, text="Carregar Linha CNAB 400", command=carregar_linha)
botao_carregar.pack(pady=10)

# Identificação do Título
tk.Label(frame_entrada, text="Identificação do Título (Posição 71-82):").grid(row=2, column=0, padx=5, pady=5)
campo_identificacao_titulo = tk.Entry(frame_entrada, width=30, validate="key", validatecommand=(criar_validador(validar_input_identificacao_titulo), '%P'))
campo_identificacao_titulo.grid(row=2, column=1, padx=5, pady=5)

# Identificação da Ocorrência
tk.Label(frame_entrada, text="Identificação da Ocorrência (Posição 109-110):").grid(row=3, column=0, padx=5, pady=5)
campo_identificacao_ocorrencia = tk.Entry(frame_entrada, width=30, validate="key", validatecommand=(criar_validador(validar_input_identificacao_ocorrencia), '%P'))
campo_identificacao_ocorrencia.grid(row=3, column=1, padx=5, pady=5)

# Data de Vencimento
tk.Label(frame_entrada, text="Data de Vencimento (Posição 147-152):").grid(row=4, column=0, padx=5, pady=5)
campo_data_vencimento = tk.Entry(frame_entrada, width=30, validate="key", validatecommand=(criar_validador(validar_input_data_vencimento), '%P'))
campo_data_vencimento.grid(row=4, column=1, padx=5, pady=5)

# Valor do Título
tk.Label(frame_entrada, text="Valor do Título (Posição 153-165):").grid(row=5, column=0, padx=5, pady=5)
campo_valor_titulo = tk.Entry(frame_entrada, width=30, validate="key", validatecommand=(criar_validador(validar_input_valor_titulo), '%P'))
campo_valor_titulo.grid(row=5, column=1, padx=5, pady=5)

# Valor Pago
tk.Label(frame_entrada, text="Valor Pago (Posição 254-266):").grid(row=6, column=0, padx=5, pady=5)
campo_valor_pago = tk.Entry(frame_entrada, width=30, validate="key", validatecommand=(criar_validador(validar_input_valor_pago), '%P'))
campo_valor_pago.grid(row=6, column=1, padx=5, pady=5)

# Data do Pagamento
tk.Label(frame_entrada, text="Data do Pagamento (Posição 296-301):").grid(row=7, column=0, padx=5, pady=5)
campo_data_pagamento = tk.Entry(frame_entrada, width=30, validate="key", validatecommand=(criar_validador(validar_input_data_pagamento), '%P'))
campo_data_pagamento.grid(row=7, column=1, padx=5, pady=5)

# Coluna de Medição
tk.Label(frame_entrada, text="Coluna de Medição (Posição 396-401):").grid(row=8, column=0, padx=5, pady=5)
campo_coluna_medicao = tk.Entry(frame_entrada, width=30, validate="key", validatecommand=(criar_validador(validar_input_coluna_medicao), '%P'))
campo_coluna_medicao.grid(row=8, column=1, padx=5, pady=5)

# Botão para gerar a linha CNAB 400 corrigida
botao_gerar = tk.Button(root, text="Gerar Linha CNAB 400 Corrigida", command=gerar_linha_cnab_400)
botao_gerar.pack(pady=10)

# Área de texto para exibir a linha corrigida
text_area = tk.Text(root, height=5, width=80)
text_area.pack(pady=10)

# Executa a interface
root.mainloop()
