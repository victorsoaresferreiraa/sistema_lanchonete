"""
Funções auxiliares para o sistema
"""

import tkinter as tk
from datetime import datetime
import re


def centralizar_janela(janela, largura=None, altura=None):
    """
    Centraliza uma janela na tela
    
    Args:
        janela: Janela tkinter a ser centralizada
        largura: Largura da janela (opcional)
        altura: Altura da janela (opcional)
    """
    # Atualizar janela para obter dimensões corretas
    janela.update_idletasks()
    
    # Obter dimensões da janela
    if largura is None or altura is None:
        geometry = janela.geometry()
        size_match = re.match(r'(\d+)x(\d+)', geometry)
        if size_match:
            largura = int(size_match.group(1))
            altura = int(size_match.group(2))
        else:
            largura = largura or 400
            altura = altura or 300
    
    # Obter dimensões da tela
    largura_tela = janela.winfo_screenwidth()
    altura_tela = janela.winfo_screenheight()
    
    # Calcular posição central
    pos_x = (largura_tela // 2) - (largura // 2)
    pos_y = (altura_tela // 2) - (altura // 2)
    
    # Garantir que a janela não saia da tela
    pos_x = max(0, pos_x)
    pos_y = max(0, pos_y)
    
    # Aplicar geometria
    janela.geometry(f"{largura}x{altura}+{pos_x}+{pos_y}")


def formatar_data(data_str, formato_origem="%d/%m/%Y %H:%M:%S", formato_destino="%d/%m/%Y"):
    """
    Formata uma string de data
    
    Args:
        data_str: String da data a ser formatada
        formato_origem: Formato original da data
        formato_destino: Formato desejado
        
    Returns:
        String da data formatada ou string original se houver erro
    """
    try:
        data_obj = datetime.strptime(data_str, formato_origem)
        return data_obj.strftime(formato_destino)
    except ValueError:
        return data_str


def validar_numero(valor, tipo=int, minimo=None, maximo=None):
    """
    Valida se um valor é um número válido
    
    Args:
        valor: Valor a ser validado
        tipo: Tipo esperado (int ou float)
        minimo: Valor mínimo permitido
        maximo: Valor máximo permitido
        
    Returns:
        Tuple (is_valid, converted_value, error_message)
    """
    try:
        # Converter para string se necessário
        if not isinstance(valor, str):
            valor = str(valor)
            
        # Remover espaços
        valor = valor.strip()
        
        if not valor:
            return False, None, "Valor não pode estar vazio"
            
        # Tentar converter
        if tipo == int:
            numero = int(valor)
        elif tipo == float:
            numero = float(valor)
        else:
            return False, None, "Tipo não suportado"
            
        # Verificar limites
        if minimo is not None and numero < minimo:
            return False, None, f"Valor deve ser maior ou igual a {minimo}"
            
        if maximo is not None and numero > maximo:
            return False, None, f"Valor deve ser menor ou igual a {maximo}"
            
        return True, numero, None
        
    except ValueError:
        tipo_nome = "número inteiro" if tipo == int else "número decimal"
        return False, None, f"Valor deve ser um {tipo_nome} válido"


def formatar_moeda(valor, simbolo="R$"):
    """
    Formata um valor numérico como moeda
    
    Args:
        valor: Valor numérico
        simbolo: Símbolo da moeda
        
    Returns:
        String formatada como moeda
    """
    try:
        return f"{simbolo} {valor:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
    except (ValueError, TypeError):
        return f"{simbolo} 0,00"


def truncar_texto(texto, tamanho_maximo=50, sufixo="..."):
    """
    Trunca um texto se ele for maior que o tamanho máximo
    
    Args:
        texto: Texto a ser truncado
        tamanho_maximo: Tamanho máximo permitido
        sufixo: Sufixo a ser adicionado quando truncado
        
    Returns:
        Texto truncado se necessário
    """
    if not texto or len(texto) <= tamanho_maximo:
        return texto
        
    return texto[:tamanho_maximo - len(sufixo)] + sufixo


def limpar_string(texto):
    """
    Remove caracteres especiais e espaços extras de uma string
    
    Args:
        texto: String a ser limpa
        
    Returns:
        String limpa
    """
    if not texto:
        return ""
        
    # Remover espaços extras
    texto = re.sub(r'\s+', ' ', texto.strip())
    
    return texto


def validar_produto_nome(nome):
    """
    Valida se o nome do produto é válido
    
    Args:
        nome: Nome do produto
        
    Returns:
        Tuple (is_valid, cleaned_name, error_message)
    """
    if not nome or not nome.strip():
        return False, "", "Nome do produto não pode estar vazio"
        
    # Limpar nome
    nome_limpo = limpar_string(nome)
    
    # Verificar tamanho
    if len(nome_limpo) < 2:
        return False, nome_limpo, "Nome do produto deve ter pelo menos 2 caracteres"
        
    if len(nome_limpo) > 100:
        return False, nome_limpo, "Nome do produto não pode ter mais de 100 caracteres"
        
    # Verificar caracteres válidos (letras, números, espaços e alguns símbolos)
    if not re.match(r'^[a-zA-ZÀ-ÿ0-9\s\-\.\/\(\)]+$', nome_limpo):
        return False, nome_limpo, "Nome do produto contém caracteres inválidos"
        
    return True, nome_limpo.title(), None


def criar_backup_nome(nome_base):
    """
    Cria um nome de arquivo de backup com timestamp
    
    Args:
        nome_base: Nome base do arquivo
        
    Returns:
        Nome do arquivo com timestamp
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    nome_sem_ext, ext = nome_base.rsplit('.', 1) if '.' in nome_base else (nome_base, '')
    
    if ext:
        return f"{nome_sem_ext}_backup_{timestamp}.{ext}"
    else:
        return f"{nome_base}_backup_{timestamp}"


def verificar_permissoes_arquivo(caminho):
    """
    Verifica se é possível ler e escrever em um arquivo
    
    Args:
        caminho: Caminho do arquivo
        
    Returns:
        Tuple (pode_ler, pode_escrever, erro)
    """
    import os
    
    try:
        # Verificar se o diretório existe
        diretorio = os.path.dirname(caminho)
        if diretorio and not os.path.exists(diretorio):
            return False, False, f"Diretório não existe: {diretorio}"
            
        # Verificar se o arquivo existe
        if os.path.exists(caminho):
            pode_ler = os.access(caminho, os.R_OK)
            pode_escrever = os.access(caminho, os.W_OK)
        else:
            # Se o arquivo não existe, verificar permissões do diretório
            pode_ler = True  # Assumir que pode ler se pode criar
            pode_escrever = os.access(diretorio or '.', os.W_OK)
            
        return pode_ler, pode_escrever, None
        
    except Exception as e:
        return False, False, str(e)
