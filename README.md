# Event Planner

Este projeto distribui palestras em diferentes sessões de tracks durante uma conferência, obedecendo regras de horário e duração.

## Como usar

### Executar agendamento

```bash
python scheduler.py
```

### Rodar testes

```bash
python -m unittest discover tests
```

## Lógica

A alocação das palestras é feita por blocos de tempo: manhã (até 12h), tarde (até 17h), com almoço e networking automaticamente inseridos.

O código evita a repetição da mesma lógica e busca variedade nas palestras alocadas por track.
