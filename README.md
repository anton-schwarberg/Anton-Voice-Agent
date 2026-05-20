# Anton-Voice-Agent

This interactive voice agent (using my voice) will call you through the phone and answer questions about my CV.

Link: [https://www.antonschwarberg.de](https://www.antonschwarberg.de)

This page is password-protected for security reasons (otherwise I might end up with a high phone bill).
If you'd like to use the feature, just send me a quick message or check my CV for the password.

## Architecture

```mermaid
flowchart LR
    User([Caller<br/>Browser])

    subgraph AWS["AWS"]
        S3[S3 Static Website<br/>index.html<br/>call_redirect_page.html]
        APIGW[API Gateway<br/>/checkpw · /checktoken]
        L1[Lambda<br/>passwordtest.py]
        L2[Lambda<br/>checktoken.py]
        DDB[(DynamoDB<br/>TokenDB)]
    end

    subgraph Make["Make.com"]
        WH[Custom Webhook]
        VAR[Set Variables<br/>Caller + Call Config]
        VAPI_UPD[Vapi API<br/>PUT /assistant/:id]
        VAPI_CALL[Vapi API<br/>createOutboundPhoneCall]
        GS[Google Sheets<br/>addRow]
    end

    subgraph Vapi["Vapi"]
        ASSIST[Assistant<br/>Antonio]
        SIP[SIP Trunk]
    end

    User -->|1. Password| S3
    S3 -->|2. POST password| APIGW --> L1 --> DDB
    L1 -->|3. token + TTL| S3
    S3 -->|4. POST token| APIGW --> L2 --> DDB
    L2 -->|5. webhook URL| S3
    S3 -->|6. POST name + phone| WH
    WH --> VAR --> VAPI_UPD --> VAPI_CALL
    VAPI_CALL --> ASSIST --> SIP
    SIP -->|7. outbound call| User
    VAPI_CALL --> GS
```

| Layer        | Tooling                              |
|--------------|--------------------------------------|
| Hosting      | AWS S3 (static)                      |
| API          | AWS API Gateway (HTTP)               |
| Compute      | AWS Lambda (Python)                  |
| Storage      | AWS DynamoDB                         |
| Orchestration | Make.com                            |
| Voice / LLM  | Vapi + OpenAI GPT-4o + ElevenLabs (cloned voice) + Deepgram |
| Telephony    | Vapi-managed SIP Trunk → PSTN        |
| Logging      | Google Sheets                        |

For the full architecture (sequence diagrams, API contracts, sanitized code excerpts, security design) see **[ARCHITECTURE.md](ARCHITECTURE.md)**.

## Repo Structure

```
.
├── ARCHITECTURE.md             # Detailed architecture documentation
├── Lambda/                     # AWS Lambda functions (Python)
│   ├── passwordtest.py         # Password check → token generation
│   └── checktoken.py           # Token validation → webhook delivery
├── Make.com/
│   └── voice-agent.blueprint.json   # Make scenario export (sanitized)
├── Vapi/
│   └── info.md                 # Vapi assistant configuration outline
├── website/
│   ├── index.html              # Password login page
│   └── call_redirect_page.html # Name + phone form
├── .env.example                # Required environment variables
└── .gitignore
```
