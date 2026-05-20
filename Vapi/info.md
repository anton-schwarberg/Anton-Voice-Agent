# Vapi Assistant — Konfiguration (Struktur)

> Diese Datei beschreibt den **Aufbau** des Voice-Agent-Prompts auf hoher Ebene.
> Der vollständige Production-Prompt ist absichtlich nicht im Repo enthalten,
> um Prompt-Injection-Angriffe nicht unnötig zu erleichtern.

## First Message (Beispiel)

```
Hi {{Name}}, hier spricht Antonio, der Stimmklon von Anton.
Freut mich, dich kennenzulernen!
```

`{{Name}}` wird zur Laufzeit von Make.com aus dem Webhook-Payload eingesetzt,
bevor der Vapi-Assistant per `PUT /assistant/:id` aktualisiert wird.

## System-Prompt — Outline

Der Prompt ist in fünf Blöcke gegliedert. Jeder adressiert einen
konkreten Aspekt des gewünschten Verhaltens:

### 1. Identität & Zweck
Definiert Rolle (Stimmklon „Antonio"), Sprechweise (Ich-Form) und
inhaltlichen Scope (Lebenslauf, Ambitionen, Hobbies/Interessen).

### 2. Tonfall & Persona
- **Persönlichkeit**: freundlich, kompetent, gefasst.
- **Sprachstil**: prägnant, natürliche Verkürzungen, ruhiges Tempo.

### 3. Gesprächsverlauf
- **Einstieg**: ermittelt aktiv das Interesse des Anrufers durch Rückfragen.
- **Gesprächsführung**: Antworten zuerst kurz (1–2 Sätze), Tiefe erst bei
  Nachfragen; Themen außerhalb des Scopes werden höflich abgelehnt.
- **Off-Topic / Wissenslücken**: explizite Anweisung, keine Halluzinationen
  zu produzieren und auf den echten Anton zu verweisen.
- **Abschluss**: positives Schluss-Statement, lädt zum Kontakt mit dem echten
  Anton ein.

### 4. Antwort-Richtlinien
Verweis auf die Knowledge-Base-Dateien als alleinige Faktenquelle,
Aufforderung zu Gegenfragen, klare „Don't hallucinate"-Regel.

### 5. Ziel
Anrufer soll sich informiert fühlen und einen guten Eindruck von Anton bekommen.

## Knowledge Base

Zwei PDFs im Google Drive sind als Vapi-Knowledge-Base verbunden:

| Datei              | Inhalt                          |
|--------------------|---------------------------------|
| `Lebenslauf_CV.pdf`| CV-Daten                        |
| `Interessen.pdf`   | Hobbies, Interessen, Ambitionen |

Die IDs werden in der Make-Blueprint als `<CV_FILE_ID>` und
`<INTERESTS_FILE_ID>` referenziert.

## Modell-Stack

| Layer        | Provider / Modell                            |
|--------------|----------------------------------------------|
| LLM          | OpenAI — `chatgpt-4o-latest`                 |
| TTS / Voice  | ElevenLabs — `eleven_turbo_v2_5`, geklonte Stimme |
| STT          | Deepgram — `nova-2` (de)                     |
| Voicemail    | Vapi built-in detection                      |
