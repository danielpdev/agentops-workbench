# Pregătire pentru interviu — AgentOps Workbench

Roluri țintă: AI Platform / Agent Evaluation.

## Prezentare de 90 de secunde

1. Explică problema concretă și cine folosește rezultatul.
2. Rulează `make demo` sau fluxul din UI.
3. Arată testul pentru un caz de eșec, apoi explică mecanismul din cod.
4. Spune ce limite are demonstrația și ce ai construi pentru producție.

Decizia de explicat: Every imported trace is schema-validated and immutable by ID. Comparison requires matching case sets and matching ground truth. Latency and token summaries remain separate from correctness.

## Cinci întrebări

1. De ce compari aceleași cazuri?
2. Ce ascunde o medie de latență?
3. Cum detectezi regresii individuale?
4. Cum gestionezi ground truth schimbat?
5. Cum ai integra OpenTelemetry?

## Exercițiu înainte de a aplica

Add OpenTelemetry ingestion, run identifiers and confidence intervals across repeated evaluations.

Alege o parte mică a acestei modificări, implementeaz-o personal, adaugă un test care verifică comportamentul și descrie rezultatul într-un commit real. Nu declara că ai înțeles sau construit singur o parte pe care nu o poți explica.

## Checklist personal

- [ ] Pot porni proiectul dintr-un checkout curat.
- [ ] Pot urmări cererea până la rezultatul salvat.
- [ ] Pot explica diferența dintre fixture și model local.
- [ ] Pot demonstra un eșec și recuperarea lui.
- [ ] Am făcut o modificare proprie și o pot explica în engleză.

Aceste puncte necesită review-ul tău; nu au fost bifate automat.
