from __future__ import annotations

import re
import unicodedata

from langchain_core.tools import tool


DEPARTMENT_CATALOG = {
    "cap cuu": {
        "name": "Cấp cứu",
        "description": "Tiếp nhận các trường hợp có dấu hiệu nguy hiểm cần xử lý ngay.",
        "common_symptoms": [
            "đau ngực dữ dội",
            "khó thở đột ngột",
            "liệt hoặc méo miệng",
            "co giật",
            "bất tỉnh",
            "chảy máu nhiều",
        ],
        "keywords": [
            "đau ngực dữ dội",
            "khó thở đột ngột",
            "bất tỉnh",
            "co giật",
            "liệt nửa người",
        ],
        "follow_up_questions": [],
    },
    "noi tong quat": {
        "name": "Nội tổng quát",
        "description": "Điểm bắt đầu an toàn khi triệu chứng còn mơ hồ hoặc chưa đủ dữ kiện để chốt chuyên khoa hẹp.",
        "common_symptoms": [
            "mệt mỏi kéo dài",
            "sốt chưa rõ nguyên nhân",
            "chóng mặt",
            "khó chịu toàn thân",
        ],
        "keywords": [
            "mệt",
            "mệt mỏi",
            "uể oải",
            "chóng mặt",
            "sốt",
            "khó chịu",
        ],
        "follow_up_questions": [
            "Triệu chứng chính là gì và xuất hiện từ khi nào?",
            "Ngoài triệu chứng này còn kèm sốt, đau, nôn hay khó thở không?",
        ],
    },
    "tim mach": {
        "name": "Tim mạch",
        "description": "Phù hợp với các vấn đề tim, huyết áp và tuần hoàn.",
        "common_symptoms": [
            "đau ngực",
            "hồi hộp",
            "tim đập nhanh",
            "tăng huyết áp",
            "phù chân",
        ],
        "keywords": [
            "đau ngực",
            "tức ngực",
            "hồi hộp",
            "tim đập nhanh",
            "đánh trống ngực",
            "cao huyết áp",
            "phù chân",
        ],
        "follow_up_questions": [
            "Cơn đau ngực xuất hiện khi nghỉ hay khi gắng sức?",
            "Có kèm khó thở, vã mồ hôi hoặc chóng mặt không?",
        ],
    },
    "ho hap": {
        "name": "Hô hấp",
        "description": "Phù hợp với triệu chứng liên quan đường thở và phổi.",
        "common_symptoms": [
            "ho kéo dài",
            "khò khè",
            "khó thở",
            "đau họng",
            "nghẹt mũi",
        ],
        "keywords": [
            "ho",
            "ho kéo dài",
            "khó thở",
            "khò khè",
            "thở rít",
            "đau họng",
            "nghẹt mũi",
            "sổ mũi",
        ],
        "follow_up_questions": [
            "Ho đã kéo dài bao lâu và có đờm hay sốt không?",
            "Khó thở xảy ra liên tục hay chỉ khi vận động?",
        ],
    },
    "tieu hoa": {
        "name": "Tiêu hóa",
        "description": "Phù hợp với vấn đề dạ dày, ruột, gan mật và tiêu hóa.",
        "common_symptoms": [
            "đau bụng",
            "buồn nôn",
            "nôn",
            "tiêu chảy",
            "táo bón",
            "ợ nóng",
        ],
        "keywords": [
            "đau bụng",
            "buồn nôn",
            "nôn",
            "tiêu chảy",
            "táo bón",
            "ợ nóng",
            "đầy hơi",
            "trào ngược",
        ],
        "follow_up_questions": [
            "Đau bụng ở vùng nào và mức độ ra sao?",
            "Có kèm nôn, tiêu chảy, sốt hoặc đi ngoài ra máu không?",
        ],
    },
    "than kinh": {
        "name": "Thần kinh",
        "description": "Phù hợp với đau đầu, tê yếu, run, co giật và các vấn đề thần kinh.",
        "common_symptoms": [
            "đau đầu kéo dài",
            "tê tay chân",
            "yếu cơ",
            "run",
            "co giật",
        ],
        "keywords": [
            "đau đầu",
            "tê tay",
            "tê chân",
            "yếu cơ",
            "run tay",
            "run chân",
            "co giật",
            "mất ngủ",
        ],
        "follow_up_questions": [
            "Triệu chứng tê/yếu xuất hiện một bên hay hai bên?",
            "Có nói khó, méo miệng hoặc nhìn mờ không?",
        ],
    },
    "co xuong khop": {
        "name": "Cơ xương khớp",
        "description": "Phù hợp với đau lưng, đau khớp, sưng khớp và hạn chế vận động.",
        "common_symptoms": [
            "đau lưng",
            "đau gối",
            "sưng khớp",
            "cứng khớp",
        ],
        "keywords": [
            "đau lưng",
            "đau gối",
            "đau khớp",
            "sưng khớp",
            "cứng khớp",
            "đau vai",
            "hạn chế vận động",
        ],
        "follow_up_questions": [
            "Đau tăng khi vận động hay cả khi nghỉ?",
            "Có sưng, đỏ, nóng tại khớp hoặc tê lan xuống tay chân không?",
        ],
    },
    "tai mui hong": {
        "name": "Tai mũi họng",
        "description": "Phù hợp với đau họng, viêm mũi xoang, đau tai, ù tai và khàn tiếng.",
        "common_symptoms": [
            "đau họng",
            "sổ mũi",
            "nghẹt mũi",
            "đau tai",
            "ù tai",
            "khàn tiếng",
        ],
        "keywords": [
            "đau họng",
            "sổ mũi",
            "nghẹt mũi",
            "đau tai",
            "ù tai",
            "khàn tiếng",
            "viêm xoang",
        ],
        "follow_up_questions": [
            "Triệu chứng kéo dài bao lâu và có sốt không?",
            "Có đau tai, ù tai hoặc khó nuốt kèm theo không?",
        ],
    },
    "da lieu": {
        "name": "Da liễu",
        "description": "Phù hợp với phát ban, ngứa, nổi mẩn, mụn hoặc các vấn đề về da.",
        "common_symptoms": [
            "ngứa",
            "phát ban",
            "nổi mẩn",
            "mụn viêm",
            "nấm da",
        ],
        "keywords": [
            "ngứa",
            "phát ban",
            "nổi mẩn",
            "mề đay",
            "mụn",
            "nấm da",
            "dị ứng da",
        ],
        "follow_up_questions": [
            "Tổn thương da xuất hiện ở vùng nào và có lan nhanh không?",
            "Có sốt, sưng môi hoặc khó thở kèm theo không?",
        ],
    },
    "noi tiet": {
        "name": "Nội tiết",
        "description": "Phù hợp với các vấn đề đường huyết, tuyến giáp và rối loạn nội tiết.",
        "common_symptoms": [
            "khát nhiều",
            "tiểu nhiều",
            "sụt cân không rõ nguyên nhân",
            "cổ to bất thường",
        ],
        "keywords": [
            "khát nhiều",
            "tiểu nhiều",
            "sụt cân",
            "đường huyết",
            "tiểu đường",
            "tuyến giáp",
            "cổ to",
        ],
        "follow_up_questions": [
            "Triệu chứng này kéo dài bao lâu rồi?",
            "Bạn có đang theo dõi tiểu đường hoặc tuyến giáp trước đó không?",
        ],
    },
    "san phu khoa": {
        "name": "Sản phụ khoa",
        "description": "Phù hợp với các vấn đề phụ khoa, thai kỳ và sức khỏe sinh sản nữ.",
        "common_symptoms": [
            "đau bụng dưới",
            "rối loạn kinh nguyệt",
            "ra huyết bất thường",
            "triệu chứng khi mang thai",
        ],
        "keywords": [
            "mang thai",
            "chậm kinh",
            "rong kinh",
            "đau bụng dưới",
            "ra huyết",
            "huyết trắng",
            "huyết bất thường",
        ],
        "follow_up_questions": [
            "Bạn có đang mang thai hoặc trễ kinh không?",
            "Có ra huyết bất thường, đau bụng tăng dần hoặc choáng không?",
        ],
    },
    "nhi": {
        "name": "Nhi",
        "description": "Phù hợp khi người bệnh là trẻ em, đặc biệt trẻ nhỏ hoặc sơ sinh.",
        "common_symptoms": [
            "sốt ở trẻ",
            "ho ở trẻ",
            "biếng ăn",
            "quấy khóc",
        ],
        "keywords": [
            "trẻ em",
            "em bé",
            "bé nhà",
            "sơ sinh",
            "bé sốt",
            "bé ho",
            "quấy khóc",
        ],
        "follow_up_questions": [
            "Bé bao nhiêu tuổi và sốt/ho từ khi nào?",
            "Bé có bỏ bú, lừ đừ, thở nhanh hoặc co giật không?",
        ],
    },
}

EMERGENCY_RULES = [
    {
        "label": "đau ngực dữ dội hoặc tức ngực kéo dài",
        "keywords": ["đau ngực dữ dội", "tức ngực", "ép ngực", "đau thắt ngực"],
    },
    {
        "label": "khó thở đột ngột hoặc thở rít nặng",
        "keywords": ["khó thở đột ngột", "khó thở", "thở rít", "ngộp thở"],
    },
    {
        "label": "dấu hiệu đột quỵ",
        "keywords": ["méo miệng", "nói khó", "liệt nửa người", "yếu liệt", "tê nửa người"],
    },
    {
        "label": "co giật hoặc bất tỉnh",
        "keywords": ["co giật", "bất tỉnh", "ngất xỉu", "mất ý thức"],
    },
    {
        "label": "chảy máu nhiều hoặc chấn thương nặng",
        "keywords": ["chảy máu nhiều", "xuất huyết", "chấn thương nặng"],
    },
]

HOME_CONTEXT_KEYWORDS = ["ở nhà", "tại nhà", "ở nhà tự theo dõi"]
HOSPITAL_CONTEXT_KEYWORDS = [
    "ở bệnh viện",
    "đang ở viện",
    "đang ở bệnh viện",
    "tại viện",
    "tại bệnh viện",
    "quầy",
    "sảnh",
]
CORRECTION_KEYWORDS = [
    "không đúng",
    "khong dung",
    "không phải",
    "khong phai",
    "không liên quan",
    "khong lien quan",
    "chưa đúng",
    "chua dung",
]
VAGUE_PHRASES = {
    "mệt",
    "mệt mỏi",
    "đau",
    "khó chịu",
    "không khỏe",
    "uể oải",
}


def _strip_accents(text: str) -> str:
    text = text.replace("đ", "d").replace("Đ", "D")
    normalized = unicodedata.normalize("NFD", text)
    return "".join(char for char in normalized if unicodedata.category(char) != "Mn")


def _normalize(text: str) -> str:
    lowered = _strip_accents(text).lower()
    lowered = re.sub(r"[^a-z0-9\s]", " ", lowered)
    return " ".join(lowered.split())


def _has_phrase(normalized_text: str, phrase: str) -> bool:
    normalized_phrase = _normalize(phrase)
    if not normalized_phrase:
        return False

    pattern = re.compile(rf"\b{re.escape(normalized_phrase)}\b")
    if not pattern.search(normalized_text):
        return False

    for negative_prefix in ("khong", "chua", "ko"):
        negative_pattern = re.compile(
            rf"\b{negative_prefix}\s+{re.escape(normalized_phrase)}\b"
        )
        if negative_pattern.search(normalized_text):
            return False

    return True


def _dedupe_keep_order(items: list[str]) -> list[str]:
    seen: set[str] = set()
    deduped: list[str] = []
    for item in items:
        if item not in seen:
            deduped.append(item)
            seen.add(item)
    return deduped


def _confidence_label(top_score: int, second_score: int = 0) -> str:
    if top_score >= 6 and top_score >= second_score + 2:
        return "cao"
    if top_score >= 3:
        return "vừa"
    return "thấp"


def _detect_care_context(symptoms: str, care_context: str = "unknown") -> str:
    normalized_text = _normalize(f"{care_context} {symptoms}")
    if any(_has_phrase(normalized_text, phrase) for phrase in HOSPITAL_CONTEXT_KEYWORDS):
        return "hospital"
    if any(_has_phrase(normalized_text, phrase) for phrase in HOME_CONTEXT_KEYWORDS):
        return "home"

    normalized_context = _normalize(care_context)
    if normalized_context in {"hospital", "benh vien"}:
        return "hospital"
    if normalized_context in {"home", "nha"}:
        return "home"
    return "unknown"


def _detect_profile_flags(normalized_text: str) -> dict[str, bool]:
    return {
        "child": any(
            _has_phrase(normalized_text, phrase)
            for phrase in ["trẻ em", "em bé", "bé nhà", "sơ sinh", "bé"]
        ),
        "pregnant": any(
            _has_phrase(normalized_text, phrase)
            for phrase in ["mang thai", "trễ kinh", "chậm kinh", "thai kỳ"]
        ),
        "elderly": any(
            _has_phrase(normalized_text, phrase)
            for phrase in ["người già", "cao tuổi", "lớn tuổi", "người lớn tuổi"]
        ),
    }


def detect_emergency_signals(text: str) -> list[str]:
    normalized_text = _normalize(text)
    signals: list[str] = []

    for rule in EMERGENCY_RULES:
        if any(_has_phrase(normalized_text, keyword) for keyword in rule["keywords"]):
            signals.append(rule["label"])

    return signals


def format_emergency_response(
    signals: list[str], care_context: str = "unknown"
) -> str:
    resolved_context = _detect_care_context("", care_context)
    lines = [
        "Mình thấy đây là trường hợp có red flag và nên ưu tiên đi Cấp cứu ngay.",
        "Dấu hiệu đáng chú ý:",
    ]
    lines.extend(f"- {signal}" for signal in signals)

    lines.append("Bước tiếp theo:")
    if resolved_context == "hospital":
        lines.append("- Nếu bạn đang ở bệnh viện, hãy đến quầy/khoa Cấp cứu ngay hoặc nhờ nhân viên hỗ trợ lập tức.")
    elif resolved_context == "home":
        lines.append("- Nếu bạn đang ở nhà, hãy đi Cấp cứu hoặc đến bệnh viện gần nhất ngay.")
    else:
        lines.append("- Hãy đến quầy/khoa Cấp cứu ngay hoặc tới bệnh viện gần nhất càng sớm càng tốt.")
    lines.append("- Không nên tiếp tục chờ tư vấn online thông thường với các dấu hiệu này.")
    lines.append("Lưu ý: đây là cảnh báo an toàn ban đầu, không phải chẩn đoán.")
    return "\n".join(lines)


def _score_departments(symptoms: str) -> list[dict]:
    normalized_text = _normalize(symptoms)
    profile_flags = _detect_profile_flags(normalized_text)
    ranked: list[dict] = []

    for key, department in DEPARTMENT_CATALOG.items():
        if key == "cap cuu":
            continue

        matches: list[str] = []
        score = 0
        for keyword in department.get("keywords", []):
            if _has_phrase(normalized_text, keyword):
                matches.append(keyword)
                score += 2 if len(_normalize(keyword).split()) > 1 else 1

        if key == "nhi" and profile_flags["child"]:
            score += 3
            matches.append("người bệnh là trẻ em")
        if key == "san phu khoa" and profile_flags["pregnant"]:
            score += 3
            matches.append("có dấu hiệu liên quan thai kỳ/phụ khoa")
        if key == "noi tong quat" and score == 0 and len(normalized_text.split()) <= 6:
            score += 1
            matches.append("triệu chứng còn khá mơ hồ")

        if score > 0:
            ranked.append(
                {
                    "key": key,
                    "name": department["name"],
                    "score": score,
                    "matches": _dedupe_keep_order(matches),
                    "description": department["description"],
                    "follow_up_questions": department["follow_up_questions"],
                }
            )

    ranked.sort(key=lambda item: item["score"], reverse=True)
    return ranked


def _build_generic_questions(normalized_text: str) -> list[str]:
    questions: list[str] = []

    if any(word in normalized_text.split() for word in {"dau", "te", "sung"}):
        questions.append("Triệu chứng nằm ở vị trí nào trên cơ thể?")
    if not any(
        token in normalized_text
        for token in ["ngay", "tuan", "thang", "hom nay", "bao lau"]
    ):
        questions.append("Triệu chứng xuất hiện bao lâu rồi?")
    if not any(
        token in normalized_text
        for token in ["nang", "du doi", "nhe", "vua"]
    ):
        questions.append("Mức độ hiện tại là nhẹ, vừa hay nặng?")
    if not any(
        token in normalized_text
        for token in ["tre", "be", "mang thai", "thai", "nguoi lon"]
    ):
        questions.append("Người bệnh là người lớn, trẻ em hay phụ nữ đang mang thai?")

    return questions


def _build_follow_up_questions(
    normalized_text: str, ranked: list[dict], previous_feedback: str
) -> list[str]:
    questions = _build_generic_questions(normalized_text)

    if ranked:
        questions.extend(ranked[0]["follow_up_questions"])

    normalized_feedback = _normalize(previous_feedback)
    if any(_has_phrase(normalized_feedback, keyword) for keyword in CORRECTION_KEYWORDS):
        questions.append("Bạn có thể nói rõ triệu chứng nào khiến bạn thấy gợi ý trước đó chưa phù hợp?")
        questions.append("Triệu chứng hiện tại khác gì so với lần khám hoặc lần tư vấn trước?")

    return _dedupe_keep_order(questions)[:3]


def _needs_handoff(
    ranked: list[dict],
    normalized_text: str,
    previous_feedback: str,
    turn_index: int,
) -> bool:
    if turn_index < 3:
        return False

    if not ranked:
        return True

    top_score = ranked[0]["score"]
    second_score = ranked[1]["score"] if len(ranked) > 1 else 0
    too_close = second_score >= top_score - 1
    too_vague = len(normalized_text.split()) <= 4 or normalized_text in {
        _normalize(phrase) for phrase in VAGUE_PHRASES
    }
    correction = any(
        _has_phrase(_normalize(previous_feedback), keyword)
        for keyword in CORRECTION_KEYWORDS
    )
    return top_score < 3 or too_close or too_vague or correction


def _context_next_steps(
    care_context: str, requires_handoff: bool = False
) -> list[str]:
    if requires_handoff:
        if care_context == "hospital":
            return [
                "Bạn nên nhờ nhân viên điều phối/quầy tiếp nhận hỗ trợ trực tiếp để tránh đi nhầm khoa.",
                "Có thể đưa luôn phần tóm tắt triệu chứng hiện tại để nhân viên tiếp nhận nhanh hơn.",
            ]
        if care_context == "home":
            return [
                "Bạn nên kết nối với tổng đài hoặc nhân viên hỗ trợ đặt lịch để được điều phối chính xác hơn.",
                "Nếu triệu chứng nặng lên trong lúc chờ, hãy đi khám trực tiếp thay vì tiếp tục chờ tư vấn online.",
            ]
        return [
            "Mình khuyên nên kết nối với nhân viên hỗ trợ/điều phối để được hướng dẫn chính xác hơn.",
            "Nếu triệu chứng tăng nhanh hoặc có thêm red flag, hãy đi khám trực tiếp ngay.",
        ]

    if care_context == "hospital":
        return [
            "Nếu bạn đang ở bệnh viện, có thể đến quầy đăng ký hoặc khu điều phối và nói rõ nhóm triệu chứng này.",
            "Nếu triệu chứng thay đổi hoặc nặng lên trong lúc chờ, hãy báo ngay cho nhân viên y tế.",
        ]
    if care_context == "home":
        return [
            "Bạn có thể dùng gợi ý chuyên khoa này để đặt lịch khám phù hợp.",
            "Nếu triệu chứng nặng thêm hoặc xuất hiện red flag, hãy đi khám trực tiếp ngay.",
        ]
    return [
        "Bạn có thể dùng gợi ý chuyên khoa này như điểm bắt đầu để đăng ký khám.",
        "Nếu triệu chứng còn mơ hồ, hãy trả lời thêm các câu hỏi làm rõ trước khi chốt khoa khám.",
    ]


def _triage_case_impl(
    symptoms: str,
    care_context: str = "unknown",
    previous_feedback: str = "",
    turn_index: int = 1,
) -> str:
    if not symptoms.strip():
        return "Mình cần bạn mô tả ít nhất một vài triệu chứng để có thể định hướng chuyên khoa."

    resolved_context = _detect_care_context(symptoms, care_context)
    emergency_signals = detect_emergency_signals(symptoms)
    if emergency_signals:
        return format_emergency_response(emergency_signals, resolved_context)

    normalized_text = _normalize(symptoms)
    ranked = _score_departments(symptoms)
    follow_up_questions = _build_follow_up_questions(
        normalized_text, ranked, previous_feedback
    )
    requires_handoff = _needs_handoff(
        ranked, normalized_text, previous_feedback, turn_index
    )

    normalized_feedback = _normalize(previous_feedback)
    correction = any(
        _has_phrase(normalized_feedback, keyword) for keyword in CORRECTION_KEYWORDS
    )

    if correction:
        intro_line = (
            "Mình ghi nhận là gợi ý trước đó chưa phù hợp, nên sẽ định hướng lại dựa trên thông tin mới."
        )
    else:
        intro_line = "Đây là hướng triage sơ bộ dựa trên mô tả hiện tại của bạn."

    if not ranked or ranked[0]["score"] < 2:
        lines = [
            intro_line,
            "Mình chưa đủ chắc chắn để chốt một chuyên khoa hẹp ngay lúc này.",
            "Điểm bắt đầu an toàn: Nội tổng quát.",
        ]
        if requires_handoff:
            lines.append(
                "Vì đã qua nhiều vòng mà thông tin vẫn chưa đủ rõ, mình khuyên nên kết nối với nhân viên hỗ trợ/điều phối."
            )
        lines.append("Nên hỏi thêm:")
        lines.extend(f"- {question}" for question in follow_up_questions)
        lines.append("Bước tiếp theo:")
        lines.extend(
            f"- {step}" for step in _context_next_steps(resolved_context, requires_handoff)
        )
        lines.append("Lưu ý: đây là gợi ý phân luồng ban đầu, không phải chẩn đoán bệnh.")
        return "\n".join(lines)

    top_score = ranked[0]["score"]
    second_score = ranked[1]["score"] if len(ranked) > 1 else 0
    confidence = _confidence_label(top_score, second_score)
    top_candidates = [
        item for item in ranked[:3] if item["score"] >= max(2, top_score - 2)
    ]

    lines = [intro_line]
    if requires_handoff:
        lines.append(
            "Ca này vẫn còn khá khó chốt chắc chắn sau nhiều vòng, nên mình sẽ giữ gợi ý ở mức tham khảo và khuyên có người hỗ trợ trực tiếp."
        )
    else:
        lines.append(
            f"Chuyên khoa phù hợp nhất trước mắt có mức tự tin {confidence}."
        )

    lines.append("Gợi ý chuyên khoa:")
    for index, item in enumerate(top_candidates, start=1):
        reason_text = ", ".join(item["matches"][:4])
        lines.append(
            f"- Gợi ý {index}: {item['name']} (độ phù hợp: {_confidence_label(item['score'], second_score if index == 1 else 0)})"
        )
        lines.append(f"  Lý do: khớp với các tín hiệu như {reason_text}.")
        lines.append(f"  Mô tả ngắn: {item['description']}")

    if follow_up_questions:
        if requires_handoff:
            lines.append("Nếu tiếp tục làm rõ trước khi gặp nhân viên, nên hỏi/nghĩ thêm:")
        else:
            lines.append("Để chắc hơn, nên làm rõ thêm:")
        lines.extend(f"- {question}" for question in follow_up_questions)

    lines.append("Bước tiếp theo:")
    lines.extend(
        f"- {step}" for step in _context_next_steps(resolved_context, requires_handoff)
    )
    lines.append("Lưu ý: đây là gợi ý phân luồng ban đầu, không phải chẩn đoán bệnh.")
    return "\n".join(lines)


@tool
def check_emergency(symptoms: str, care_context: str = "unknown") -> str:
    """
    Kiểm tra nhanh red flag/cấp cứu từ mô tả triệu chứng.

    Dùng khi người dùng hỏi có cần đi cấp cứu không hoặc khi cần safety check riêng.
    """
    signals = detect_emergency_signals(symptoms)
    if not signals:
        return (
            "Chưa phát hiện red flag rõ ràng từ mô tả hiện tại. "
            "Nếu triệu chứng tăng nhanh, đau dữ dội, khó thở, lơ mơ hoặc xuất hiện dấu hiệu mới nguy hiểm, "
            "vẫn nên đi Cấp cứu ngay."
        )
    return format_emergency_response(signals, care_context)


@tool
def triage_case(
    symptoms: str,
    care_context: str = "unknown",
    previous_feedback: str = "",
    turn_index: int = 1,
) -> str:
    """
    Tool chính cho bài toán triage: đọc triệu chứng, phát hiện red flag, gợi ý chuyên khoa,
    sinh câu hỏi làm rõ và đề xuất handoff khi ca vẫn mơ hồ sau nhiều vòng.
    """
    return _triage_case_impl(
        symptoms=symptoms,
        care_context=care_context,
        previous_feedback=previous_feedback,
        turn_index=turn_index,
    )


@tool
def suggest_specialties(
    symptoms: str,
    care_context: str = "unknown",
    previous_feedback: str = "",
    turn_index: int = 1,
) -> str:
    """
    Tool tương thích ngược để gợi ý chuyên khoa; nội bộ dùng chung logic với triage_case.
    """
    return _triage_case_impl(
        symptoms=symptoms,
        care_context=care_context,
        previous_feedback=previous_feedback,
        turn_index=turn_index,
    )


def _resolve_department_key(raw_specialty: str) -> str | None:
    normalized_input = _normalize(raw_specialty)
    if normalized_input in DEPARTMENT_CATALOG:
        return normalized_input

    for key, department in DEPARTMENT_CATALOG.items():
        if normalized_input == _normalize(department["name"]):
            return key
    return None


@tool
def lookup_specialty_info(specialty: str) -> str:
    """
    Tra cứu phạm vi cơ bản của một chuyên khoa để giải thích cho bệnh nhân vì sao khoa đó phù hợp.
    """
    department_key = _resolve_department_key(specialty)
    if department_key is None:
        return (
            f"Chưa có thông tin chuẩn hóa cho chuyên khoa '{specialty}'. "
            "Bạn có thể hỏi các nhóm như Nội tổng quát, Tim mạch, Hô hấp, Tiêu hóa, "
            "Thần kinh, Cơ xương khớp, Tai mũi họng, Da liễu, Nội tiết, Sản phụ khoa hoặc Nhi."
        )

    department = DEPARTMENT_CATALOG[department_key]
    lines = [
        f"Chuyên khoa: {department['name']}",
        f"Mô tả: {department['description']}",
        "Triệu chứng thường gặp:",
    ]
    lines.extend(f"- {symptom}" for symptom in department["common_symptoms"])
    follow_up_questions = department.get("follow_up_questions", [])
    if follow_up_questions:
        lines.append("Thông tin thường cần làm rõ thêm:")
        lines.extend(f"- {question}" for question in follow_up_questions[:2])
    lines.append(
        "Lưu ý: thông tin này dùng để định hướng khoa khám ban đầu, không thay thế chẩn đoán của bác sĩ."
    )
    return "\n".join(lines)
