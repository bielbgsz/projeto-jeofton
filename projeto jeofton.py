import tkinter as tk
from tkinter import ttk, messagebox, filedialog

class CurrencyConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Conversor de Moedas (Offline com Histórico)")
        self.root.geometry("500x550")
        self.root.resizable(False, False)

        self.bg_color = "#e6f2e6"
        self.fg_color = "#2e7d32"
        self.button_bg = "#388e3c"
        self.button_fg = "#ffffff"
        self.entry_bg = "#ffffff"
        self.history_bg = "#dcedc8"

        self.root.configure(bg=self.bg_color)

        self.exchange_rates = {
            'USD': {'BRL': 5.10, 'EUR': 0.93, 'JPY': 156.5},
            'BRL': {'USD': 0.196, 'EUR': 0.18, 'JPY': 30.6},
            'EUR': {'USD': 1.08, 'BRL': 5.6, 'JPY': 168.2},
            'JPY': {'USD': 0.0064, 'BRL': 0.033, 'EUR': 0.0059},
        }

        self.history = []
        self.currencies = list(self.exchange_rates.keys())

        self.create_widgets()

    def create_widgets(self):
        style = ttk.Style()
        style.theme_use('clam')

        style.configure("TLabel", background=self.bg_color, foreground=self.fg_color, font=("Helvetica", 12))
        style.configure("Header.TLabel", font=("Helvetica", 16, "bold"), foreground=self.fg_color, background=self.bg_color)
        style.configure("TButton", background=self.button_bg, foreground=self.button_fg, font=("Helvetica", 11, "bold"))
        style.map("TButton",
                  background=[('active', '#2e7d32')],
                  foreground=[('active', self.button_fg)])
        style.configure("TCombobox", fieldbackground=self.entry_bg, background=self.entry_bg, foreground=self.fg_color, font=("Helvetica", 11))

        ttk.Label(self.root, text="Conversor de Moedas", style="Header.TLabel").pack(pady=10)

        frame = ttk.Frame(self.root)
        frame.pack(pady=10)

        ttk.Label(frame, text="Valor:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.entry_amount = ttk.Entry(frame, font=("Helvetica", 11))
        self.entry_amount.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(frame, text="De:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.combo_from = ttk.Combobox(frame, values=self.currencies, state="readonly")
        self.combo_from.set("USD")
        self.combo_from.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(frame, text="Para:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.combo_to = ttk.Combobox(frame, values=self.currencies, state="readonly")
        self.combo_to.set("BRL")
        self.combo_to.grid(row=2, column=1, padx=5, pady=5)

        btn_invert = ttk.Button(frame, text="↔ Inverter", command=self.invert_currencies)
        btn_invert.grid(row=3, column=1, pady=10, sticky="e")

        ttk.Button(self.root, text="Converter", command=self.convert_currency).pack(pady=10)

        self.label_result = ttk.Label(self.root, text="", font=("Helvetica", 14, "bold"), background=self.bg_color, foreground=self.fg_color)
        self.label_result.pack(pady=5)

        ttk.Label(self.root, text="Histórico de conversões:", font=("Helvetica", 12, "bold"), background=self.bg_color, foreground=self.fg_color).pack(pady=5)

        self.history_box = tk.Text(self.root, height=10, width=50, state="disabled", wrap="word",
                                   bg=self.history_bg, fg=self.fg_color, font=("Courier New", 10), relief="solid", bd=1)
        self.history_box.pack(pady=5)

        ttk.Button(self.root, text="Salvar Histórico", command=self.save_history).pack(pady=(0, 10))

    def convert_currency(self):
        try:
            amount = float(self.entry_amount.get())
            from_currency = self.combo_from.get()
            to_currency = self.combo_to.get()

            if from_currency == to_currency:
                result = amount
            else:
                rate = self.exchange_rates[from_currency][to_currency]
                result = amount * rate

            result_str = f"{amount:.2f} {from_currency} = {result:.2f} {to_currency}"
            self.label_result.config(text=result_str)
            self.add_to_history(result_str)

        except ValueError:
            messagebox.showerror("Erro", "Digite um valor numérico válido.")
        except KeyError:
            messagebox.showerror("Erro", "Conversão não suportada.")

    def add_to_history(self, entry):
        self.history.append(entry)
        self.history_box.config(state="normal")
        self.history_box.delete(1.0, tk.END)
        for item in reversed(self.history[-10:]):
            self.history_box.insert(tk.END, item + "\n")
        self.history_box.config(state="disabled")

    def invert_currencies(self):
        from_curr = self.combo_from.get()
        to_curr = self.combo_to.get()
        self.combo_from.set(to_curr)
        self.combo_to.set(from_curr)

    def save_history(self):
        if not self.history:
            messagebox.showinfo("Histórico vazio", "Não há histórico para salvar.")
            return

        filepath = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Arquivo de texto", "*.txt"), ("Todos os arquivos", "*.*")],
            title="Salvar histórico de conversões"
        )
        if filepath:
            try:
                with open(filepath, 'w', encoding='utf-8') as f:
                    for line in self.history:
                        f.write(line + "\n")
                messagebox.showinfo("Sucesso", f"Histórico salvo em:\n{filepath}")
            except Exception as e:
                messagebox.showerror("Erro", f"Falha ao salvar o arquivo:\n{e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = CurrencyConverterApp(root)
    root.mainloop()
