import re
import tkinter as tk
from tkinter import messagebox, simpledialog

class MotorInferencia:
    def __init__(self):
        self.regras = []
        self.fatos = set()
    
    def adicionar_regra(self, antecedente, consequente):
        self.regras.append((antecedente, consequente))
    
    def adicionar_fato(self, fato):
        self.fatos.add(fato)
    
    def encadeamento_para_tras(self, objetivo, caminho=None):
        if caminho is None:
            caminho = set()
        
        if objetivo in self.fatos:
            return True
        
        if objetivo in caminho:
            return False  # Evita loops
        
        caminho.add(objetivo)
        
        for antecedente, consequente in self.regras:
            if consequente == objetivo:
                if all(self.encadeamento_para_tras(p, caminho) for p in antecedente):
                    self.fatos.add(objetivo)
                    return True
        
        return False
    
    def encadeamento_para_frente(self):
        alterado = True
        while alterado:
            alterado = False
            for antecedente, consequente in self.regras:
                if consequente not in self.fatos and all(p in self.fatos for p in antecedente):
                    self.fatos.add(consequente)
                    alterado = True
    
    def encadeamento_misto(self, objetivo):
        self.encadeamento_para_frente()
        return self.encadeamento_para_tras(objetivo)
    
    def explanação(self, objetivo):
        if objetivo in self.fatos:
            return f"O fato {objetivo} já é conhecido."
        
        for antecedente, consequente in self.regras:
            if consequente == objetivo:
                explicacao = "Porque " + " e ".join(antecedente) + ", então " + objetivo
                return explicacao
        
        return f"Não há explicação para {objetivo}."

class InterfaceGUI:
    def __init__(self, motor):
        self.motor = motor
        self.root = tk.Tk()
        self.root.title("Sistema Baseado em Conhecimento")
        
        self.label = tk.Label(self.root, text="Escolha uma opção:", font=("Arial", 14))
        self.label.pack(pady=10)
        
        self.btn_adicionar_fato = tk.Button(self.root, text="Adicionar Fato", command=self.adicionar_fato)
        self.btn_adicionar_fato.pack(pady=5)
        
        self.btn_adicionar_regra = tk.Button(self.root, text="Adicionar Regra", command=self.adicionar_regra)
        self.btn_adicionar_regra.pack(pady=5)
        
        self.btn_verificar = tk.Button(self.root, text="Verificar Objetivo", command=self.verificar)
        self.btn_verificar.pack(pady=5)
        
        self.btn_explicar = tk.Button(self.root, text="Explicar", command=self.explicar)
        self.btn_explicar.pack(pady=5)
        
        self.btn_sair = tk.Button(self.root, text="Sair", command=self.root.quit)
        self.btn_sair.pack(pady=5)
    
    def adicionar_fato(self):
        fato = simpledialog.askstring("Adicionar Fato", "Digite o fato:")
        if fato:
            self.motor.adicionar_fato(fato)
            messagebox.showinfo("Sucesso", f"Fato '{fato}' adicionado.")
    
    def adicionar_regra(self):
        regra = simpledialog.askstring("Adicionar Regra", "Digite a regra no formato 'SE X E Y ENTÃO Z':")
        if regra:
            partes = re.findall(r'\w+', regra)
            if "SE" in partes and "ENTÃO" in partes:
                idx_se = partes.index("SE") + 1
                idx_entao = partes.index("ENTÃO")
                antecedente = tuple(partes[idx_se:idx_entao])
                consequente = partes[idx_entao + 1]
                self.motor.adicionar_regra(antecedente, consequente)
                messagebox.showinfo("Sucesso", f"Regra adicionada: SE {' e '.join(antecedente)} ENTÃO {consequente}")
    
    def verificar(self):
        objetivo = simpledialog.askstring("Verificar Objetivo", "Digite o objetivo a ser verificado:")
        if objetivo:
            resultado = self.motor.encadeamento_para_tras(objetivo)
            messagebox.showinfo("Resultado", f"Pode provar {objetivo} = Sim? {resultado}")
    
    def explicar(self):
        objetivo = simpledialog.askstring("Explicar", "Digite o objetivo para explicação:")
        if objetivo:
            explicacao = self.motor.explanação(objetivo)
            messagebox.showinfo("Explicação", explicacao)
    
    def executar(self):
        self.root.mainloop()

# Executando a interface
tk_motor = MotorInferencia()
tk_interface = InterfaceGUI(tk_motor)
tk_interface.executar()