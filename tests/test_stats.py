from core.stats import compute_stats


def test_empty_logs():
    assert compute_stats([]) == {"empty": True}


def test_splits_technologies_csv():
    """Regresión: el CSV de tecnologías debe separarse antes de agregar."""
    logs = [
        {"fecha_creacion": "2025-08-21T10:00:00Z", "horas": "2", "tecnologias_utilizadas": "Django, React"},
        {"fecha_creacion": "2025-08-21T15:00:00Z", "horas": "3", "tecnologias_utilizadas": "Django"},
    ]
    res = compute_stats(logs)
    tec = {d["tecnologia"]: d["horas"] for d in res["top_tecnologias"]}
    assert tec == {"Django": 5.0, "React": 2.0}


def test_franjas_del_dia():
    logs = [
        {"fecha_creacion": "2025-08-21T10:00:00Z", "horas": "2", "tecnologias_utilizadas": ""},
        {"fecha_creacion": "2025-08-21T20:00:00Z", "horas": "1", "tecnologias_utilizadas": ""},
    ]
    partes = {d["parte"]: d["horas"] for d in compute_stats(logs)["por_franja"]}
    assert partes == {"mañana": 2.0, "noche": 1.0}


def test_ignores_invalid_hours():
    logs = [{"fecha_creacion": "2025-08-21T10:00:00Z", "horas": "x", "tecnologias_utilizadas": "Go"}]
    assert compute_stats(logs) == {"empty": True}


def test_top_limited_to_10():
    logs = [
        {"fecha_creacion": "2025-08-21T10:00:00Z", "horas": "1", "tecnologias_utilizadas": f"tec{i}"}
        for i in range(15)
    ]
    assert len(compute_stats(logs)["top_tecnologias"]) == 10
