#!/usr/bin/env python3
"""
Teste simples do sistema sem numpy
"""
import tkinter as tk
from tkinter import ttk

def test_window():
    """Criar janela de teste"""
    root = tk.Tk()
    root.title("Teste - Sistema Lanchonete")
    root.geometry("800x600")
    
    # Centralizar janela
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    pos_x = (root.winfo_screenwidth() // 2) - (width // 2)
    pos_y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f"{width}x{height}+{pos_x}+{pos_y}")
    
    # Criar interface
    main_frame = ttk.Frame(root, padding="20")
    main_frame.pack(fill=tk.BOTH, expand=True)
    
    title = ttk.Label(main_frame, text="🍔 Sistema de Lanchonete", font=("Arial", 16, "bold"))
    title.pack(pady=20)
    
    # Botões principais
    btn_frame = ttk.Frame(main_frame)
    btn_frame.pack(pady=20)
    
    ttk.Button(btn_frame, text="📦 Gerenciar Estoque", width=20).pack(pady=5)
    ttk.Button(btn_frame, text="💰 Registrar Venda", width=20).pack(pady=5)
    ttk.Button(btn_frame, text="📊 Dashboard", width=20, command=lambda: test_dashboard(root)).pack(pady=5)
    ttk.Button(btn_frame, text="❌ Sair", width=20, command=root.quit).pack(pady=5)
    
    root.mainloop()

def test_dashboard(parent):
    """Teste do dashboard simplificado"""
    dashboard = tk.Toplevel(parent)
    dashboard.title("📊 Dashboard Financeiro")
    dashboard.geometry("1300x850")
    dashboard.transient(parent)
    dashboard.grab_set()
    
    # Centralizar
    dashboard.update_idletasks()
    width = dashboard.winfo_width()
    height = dashboard.winfo_height()
    pos_x = (dashboard.winfo_screenwidth() // 2) - (width // 2)
    pos_y = (dashboard.winfo_screenheight() // 2) - (height // 2)
    dashboard.geometry(f"{width}x{height}+{pos_x}+{pos_y}")
    
    # Interface do dashboard
    main_frame = ttk.Frame(dashboard, padding="15")
    main_frame.pack(fill=tk.BOTH, expand=True)
    
    # Título
    title = ttk.Label(main_frame, text="📊 Dashboard Executivo", font=("Arial", 18, "bold"))
    title.pack(pady=(0, 20))
    
    # Métricas
    metrics_frame = ttk.LabelFrame(main_frame, text="💰 Métricas Principais", padding="12")
    metrics_frame.pack(fill=tk.X, pady=(0, 15))
    
    for i, metric in enumerate(["Vendas Hoje", "Receita Total", "Produtos Vendidos", "Margem Lucro"]):
        frame = ttk.Frame(metrics_frame)
        frame.grid(row=0, column=i, padx=10, pady=5, sticky="ew")
        metrics_frame.columnconfigure(i, weight=1)
        
        ttk.Label(frame, text=metric, font=("Arial", 10)).pack()
        ttk.Label(frame, text="R$ 1.234,56", font=("Arial", 14, "bold"), foreground="green").pack()
    
    # Área de gráficos
    charts_frame = ttk.LabelFrame(main_frame, text="📈 Análises Visuais", padding="10")
    charts_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
    
    ttk.Label(charts_frame, text="Dashboard carregado com novo tamanho: 1300x850 pixels", 
             font=("Arial", 12), foreground="blue").pack(expand=True)
    
    # Botões
    btn_frame = ttk.Frame(main_frame)
    btn_frame.pack(fill=tk.X, pady=10)
    
    ttk.Button(btn_frame, text="🔄 Atualizar", width=15).pack(side=tk.LEFT, padx=(0, 10))
    ttk.Button(btn_frame, text="❌ Fechar", width=15, command=dashboard.destroy).pack(side=tk.RIGHT)

if __name__ == "__main__":
    test_window()