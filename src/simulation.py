import threading
import time
from queue import Queue
from config import BUFFER_CAPACITY, PRODUCERS, CONSUMERS, TIMESTEPS
from utils import log_status

class ProductionLine:
    def __init__(self, buffer_capacity, producers, consumers, timesteps):
        self.buffer = Queue(maxsize=buffer_capacity)
        self.buffer_capacity = buffer_capacity
        self.producers = producers
        self.consumers = consumers
        self.timesteps = timesteps
        self.produced_items = 0
        self.consumed_items = 0
        self.buffer_log = []
        self.lock = threading.Lock()
        self.sem_items = threading.Semaphore(0)
        self.sem_space = threading.Semaphore(buffer_capacity)

    def producer(self, producer_id):
        for timestep in range(1, self.timesteps + 1):
            self.sem_space.acquire()
            with self.lock:
                self.buffer.put(1)
                self.produced_items += 1
                self.buffer_log.append(len(self.buffer.queue))
            print(f"TS: {timestep} | Produtor {producer_id} produziu 1 item.")
            self.sem_items.release()
            time.sleep(0.1)  # Simulação de produção
        print(f"Produtor {producer_id} finalizado.")

    def consumer(self, consumer_id):
        while True:
            self.sem_items.acquire()
            with self.lock:
                item = self.buffer.get()
                if item is None:  # Pílula venenosa detectada
                    print(f"Consumidor {consumer_id} recebeu sinal de término.")
                    break
                self.consumed_items += 1
                self.buffer_log.append(len(self.buffer.queue))
                print(f"Consumidor {consumer_id} consumiu 1 item.")
            self.sem_space.release()
            time.sleep(0.1)  # Simulação de consumo
        print(f"Consumidor {consumer_id} finalizado.")

    def run_simulation(self):
        threads = []

        # Criando threads para produtores
        for i in range(self.producers):
            t = threading.Thread(target=self.producer, args=(i,), name=f"Producer-{i}")
            threads.append(t)
            print(f"Produtor {i} iniciado.")

        # Criando threads para consumidores
        for i in range(self.consumers):
            t = threading.Thread(target=self.consumer, args=(i,), name=f"Consumer-{i}")
            threads.append(t)
            print(f"Consumidor {i} iniciado.")

        # Iniciando as threads
        for t in threads:
            t.start()

        # Aguardando os produtores terminarem
        for t in threads[:self.producers]:
            t.join()
            print(f"Thread {t.name} finalizada.")

        # Inserindo pílulas venenosas no buffer
        print("Inserindo pílulas venenosas para finalizar os consumidores.")
        for _ in range(self.consumers):
            self.sem_space.acquire()
            with self.lock:
                self.buffer.put(None)  # 'None' representa a pílula venenosa
            self.sem_items.release()

        # Aguardando os consumidores terminarem
        for t in threads[self.producers:]:
            t.join()
            print(f"Thread {t.name} finalizada.")

        print("Todas as threads foram concluídas.")
        return self.produced_items, self.consumed_items, self.buffer_log

