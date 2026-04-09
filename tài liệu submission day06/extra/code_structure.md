project/
│
├── frontend/                          # UI layer
│   ├── components/
│   ├── pages/
│   ├── services/                      # gọi API backend
│   ├── hooks/
│   ├── types/
│   ├── styles/
│   └── utils/
│
├── backend/                           # Backend = API + Agent service
│   │
│   ├── api/                           # 🌐 HTTP layer
│   │   ├── routes/
│   │   │   ├── triage.py              # POST /triage
│   │   │   ├── image.py               # future
│   │   │   └── booking.py             # future
│   │   │
│   │   └── schemas/
│   │       ├── request.py
│   │       └── response.py
│   │
│   ├── services/                      # 🧩 Business services
│   │   ├── agent_service/             # ⭐ wrapper gọi agent
│   │   │   ├── triage_service.py      # entry point chính
│   │   │   └── dto.py                 # input/output contract
│   │   │
│   │   ├── booking_service/           # future
│   │   └── image_service/             # future
│   │
│   ├── agent/                         # 🧠 AI system (LangGraph)
│   │   ├── graph/
│   │   │   ├── builder.py
│   │   │   ├── edges.py
│   │   │   └── runner.py
│   │   │
│   │   ├── nodes/
│   │   │   ├── extract/
│   │   │   ├── triage/
│   │   │   ├── recommend/
│   │   │   ├── router/
│   │   │   ├── error_handler/
│   │   │   ├── risk_detection/        # future
│   │   │   ├── image_analysis/        # future
│   │   │   └── booking/               # future
│   │   │
│   │   ├── state/
│   │   │   └── agent_state.py
│   │   │
│   │   ├── prompts/
│   │   │   ├── extract_prompt.txt
│   │   │   └── triage_prompt.txt
│   │   │
│   │   ├── tools/
│   │   │   ├── medical_search.py
│   │   │   └── hospital_api.py
│   │   │
│   │   ├── pipelines/
│   │   │   ├── triage_pipeline.py
│   │   │   └── multimodal_pipeline.py
│   │   │
│   │   ├── evaluation/
│   │   │   ├── test_runner.py
│   │   │   └── metrics.py
│   │   │
│   │   └── utils/
│   │
│   ├── middleware/
│   │   ├── logging.py
│   │   └── error_handler.py
│   │
│   ├── config/
│   │   ├── settings.py
│   │   └── env.py
│   │
│   └── main.py                        # entry point backend
│
├── data/                              # data layer
│   ├── raw/
│   ├── processed/
│   │
│   ├── mappings/
│   │   └── symptom_to_specialty.json
│   │
│   ├── schemas/
│   │   └── symptom_schema.json
│   │
│   ├── eval/
│   │   ├── test_cases.json
│   │   └── expected_outputs.json
│   │
│   └── examples/
│
├── shared/                            # shared types/constants
│   ├── types/
│   ├── constants/
│   └── utils/
│
├── infra/
│   ├── docker/
│   ├── docker-compose.yml
│   └── env/
│
├── tests/
│   ├── backend/
│   ├── agent/
│   └── e2e/
│
└── README.md