from main import parse_propostas, alocar_palestras

def test_parse_propostas():
    palestras = parse_propostas("propostas.txt")
    assert len(palestras) == 19
    assert any(p.titulo == "Rails para usuários de Django" and p.duracao == 5 for p in palestras)

def test_alocacao_tempos():
    palestras = parse_propostas("propostas.txt")
    tracks, restantes = alocar_palestras(palestras)
    for manha, tarde in tracks:
        assert sum(p.duracao for p in manha) <= 180
        assert 180 <= sum(p.duracao for p in tarde) <= 240
