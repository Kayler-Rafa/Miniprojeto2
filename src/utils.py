import threading

def log_status(timestep, buffer):
    """Retorna o estado atual do buffer no formato legível."""
    return f"Timestep {timestep}: {len(buffer)} item(s) no buffer."

def create_lock():
    """Cria e retorna um lock (mutex)."""
    return threading.Lock()
