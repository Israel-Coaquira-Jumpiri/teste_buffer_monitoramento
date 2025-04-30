import redis
import psutil
import json
import time
import socket

redis_client = redis.Redis(host="13.217.158.61", port=6379, decode_responses=True)

maquina = socket.gethostname()

while True:
    dados = {
        "tempo": time.strftime("%H:%M:%S"),
        "porcentagemCPU": psutil.cpu_percent(interval=1),
        "porcentagemRAM": psutil.virtual_memory().percent,
        "porcentagemDISCO": psutil.disk_usage('C:\\').percent,
        "hostname": maquina
    }

    chave_redis = f"monitoramento:{maquina}"

    redis_client.rpush(chave_redis, json.dumps(dados))
    redis_client.ltrim(chave_redis, -6, -1)

    print(f"[{maquina}] Dados enviados:", dados)
    time.sleep(1)