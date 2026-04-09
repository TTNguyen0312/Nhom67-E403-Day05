# 🏥 Medical Triage Agent — Unified Monorepo Structure
project/
│
├── frontend/                          # UI layer
│   ├── components/                    # chat UI, result cards
│   ├── pages/                         # main screens
│   ├── services/                      # API calls (triage, image, booking)
│   ├── hooks/                         # state management (chat, fetch)
│   ├── types/                         # frontend types (sync từ shared)
│   ├── styles/                        # CSS / Tailwind
│   └── utils/
│
├── backend/                           # API layer
│   ├── api/
│   │   ├── routes/
│   │   │   ├── triage.py              # main endpoint
│   │   │   ├── image.py               # future: image upload
│   │   │   └── booking.py             # future: booking
│   │   │
│   │   └── schemas/
│   │       ├── request.py             # request models
│   │       └── response.py            # response models
│   │
│   ├── services/
│   │   ├── agent_service/             # call agent system
│   │   ├── booking_service/           # future
│   │   └── image_service/             # future
│   │
│   ├── middleware/
│   │   ├── logging.py
│   │   └── error_handler.py
│   │
│   ├── config/
│   │   ├── settings.py
│   │   └── env.py
│   │
│   └── main.py                        # entry point
│
├── agent/                             # LangGraph AI system
│   ├── graph/
│   │   ├── builder.py                 # build graph
│   │   ├── edges.py                   # transitions
│   │   └── runner.py                  # execute graph
│   │
│   ├── nodes/                         # processing steps
│   │   ├── extract/                   # extract symptoms
│   │   ├── triage/                    # classify specialty
│   │   ├── recommend/                 # generate response
│   │   ├── router/                    # routing logic
│   │   ├── error_handler/             # fallback
│   │   ├── risk_detection/            # future: emergency detection
│   │   ├── image_analysis/            # future
│   │   └── booking/                   # future
│   │
│   ├── state/
│   │   └── agent_state.py             # shared state schema
│   │
│   ├── prompts/
│   │   ├── extract_prompt.txt
│   │   └── triage_prompt.txt
│   │
│   ├── tools/
│   │   ├── medical_search.py          # future (RAG)
│   │   └── hospital_api.py            # future
│   │
│   ├── pipelines/
│   │   ├── triage_pipeline.py         # main flow
│   │   └── multimodal_pipeline.py     # future
│   │
│   ├── evaluation/
│   │   ├── test_runner.py
│   │   └── metrics.py
│   │
│   └── utils/
│
├── data/                              # data layer
│   ├── raw/                           # raw datasets (optional)
│   ├── processed/                     # cleaned data
│   │
│   ├── mappings/
│   │   └── symptom_to_specialty.json  # core mapping
│   │
│   ├── schemas/
│   │   └── symptom_schema.json
│   │
│   ├── eval/
│   │   ├── test_cases.json            # input cases
│   │   └── expected_outputs.json      # expected results
│   │
│   └── examples/
│       └── sample_inputs.json
│
├── shared/                            # shared FE-BE layer
│   ├── types/
│   │   ├── triage.ts                  # shared response type
│   │   └── common.ts
│   │
│   ├── constants/
│   │   ├── specialties.ts
│   │   └── config.ts
│   │
│   └── utils/
│
├── infra/                             # deployment & config
│   ├── docker/
│   │   ├── Dockerfile.backend
│   │   └── Dockerfile.frontend
│   │
│   ├── docker-compose.yml
│   │
│   └── env/
│       └── .env.example
│
├── tests/                             # testing
│   ├── backend/
│   ├── agent/
│   └── e2e/
│
└── README.md
