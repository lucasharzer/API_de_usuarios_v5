def normalize_path_params(cidade = None,
                        idade_min = 8,
                        idade_max = 80,
                        limit = 50,
                        offset = 0, **dados):
    if cidade:
        return {
            'idade_min': idade_min,
            'idade_max': idade_max,
            'cidade': cidade,
            'limit': limit,
            'offset': offset}
    return {
            'idade_min': idade_min,
            'idade_max': idade_max,
            'limit': limit,
            'offset': offset}

consulta_sem_cidade = "SELECT * FROM usuarios \
WHERE (idade > ? and idade < ?) \
LIMIT ? OFFSET ?"

consulta_com_cidade = "SELECT * FROM usuarios \
WHERE (idade > ? and idade < ?) \
and cidade = ? LIMIT ? OFFSET ?"