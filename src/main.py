import csv
import matplotlib.pyplot as plt
from simulation import ProductionLine
from config import BUFFER_CAPACITY, PRODUCERS, CONSUMERS, TIMESTEPS

def save_csv(data, filename):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Timestep", "Buffer Items"])
        for timestep, buffer_items in enumerate(data, 1):
            writer.writerow([timestep, buffer_items])

def save_plot(data, filename):
    plt.figure(figsize=(10, 6))
    plt.plot(range(1, len(data) + 1), data, label="Buffer Status")
    plt.axhline(BUFFER_CAPACITY, color='r', linestyle='--', label="Buffer Capacity")
    plt.xlabel("Timesteps")
    plt.ylabel("Items in Buffer")
    plt.title("Buffer Status Over Time")
    plt.legend()
    plt.grid()
    plt.savefig(filename)
    plt.close()

def save_report(total_produced, total_consumed, max_items, filename):
    with open(filename, 'w') as file:
        file.write("# Relatório da Linha de Produção\n")
        file.write(f"- Total de Itens Produzidos: {total_produced}\n")
        file.write(f"- Total de Itens Consumidos: {total_consumed}\n")
        file.write(f"- Máximo de Itens no Buffer: {max_items}\n")

def main():
    print("Iniciando a simulação da linha de produção...")
    production_line = ProductionLine(BUFFER_CAPACITY, PRODUCERS, CONSUMERS, TIMESTEPS)

    # Executa a simulação
    total_produced, total_consumed, buffer_log = production_line.run_simulation()

    # Logs finais antes de salvar
    print(f"\nSimulação concluída!")
    print(f"Total produzido: {total_produced}")
    print(f"Total consumido: {total_consumed}")
    print(f"Máximo de itens no buffer: {max(buffer_log)}")

    # Salvando os resultados
    print("Gerando relatórios e gráficos...")
    save_csv(buffer_log, "output/buffer_data.csv")
    save_plot(buffer_log, "output/buffer_plot.png")
    save_report(total_produced, total_consumed, max(buffer_log), "output/relatorio.md")

    print("\nRelatórios gerados com sucesso:")
    print(" - output/buffer_data.csv")
    print(" - output/buffer_plot.png")
    print(" - output/relatorio.md")

if __name__ == "__main__":
    main()
