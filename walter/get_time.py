def get_time(segundos):
    minutos = segundos // 60
    segundos_restantes = segundos % 60
    return f"{minutos}m:{segundos_restantes:02d}s"
