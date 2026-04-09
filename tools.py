from __future__ import annotations

from langchain_core.tools import tool


FLIGHTS_DB = {
    ("Hà Nội", "Đà Nẵng"): [
        {
            "airline": "Vietnam Airlines",
            "departure": "06:00",
            "arrival": "07:20",
            "price": 1_450_000,
            "class": "economy",
        },
        {
            "airline": "Vietnam Airlines",
            "departure": "14:00",
            "arrival": "15:20",
            "price": 2_800_000,
            "class": "business",
        },
        {
            "airline": "VietJet Air",
            "departure": "08:30",
            "arrival": "09:50",
            "price": 890_000,
            "class": "economy",
        },
        {
            "airline": "Bamboo Airways",
            "departure": "11:00",
            "arrival": "12:20",
            "price": 1_200_000,
            "class": "economy",
        },
    ],
    ("Hà Nội", "Phú Quốc"): [
        {
            "airline": "Vietnam Airlines",
            "departure": "07:00",
            "arrival": "09:15",
            "price": 2_100_000,
            "class": "economy",
        },
        {
            "airline": "VietJet Air",
            "departure": "10:00",
            "arrival": "12:15",
            "price": 1_350_000,
            "class": "economy",
        },
        {
            "airline": "VietJet Air",
            "departure": "16:00",
            "arrival": "18:15",
            "price": 1_100_000,
            "class": "economy",
        },
    ],
    ("Hà Nội", "Hồ Chí Minh"): [
        {
            "airline": "Vietnam Airlines",
            "departure": "06:00",
            "arrival": "08:10",
            "price": 1_600_000,
            "class": "economy",
        },
        {
            "airline": "VietJet Air",
            "departure": "07:30",
            "arrival": "09:40",
            "price": 950_000,
            "class": "economy",
        },
        {
            "airline": "Bamboo Airways",
            "departure": "12:00",
            "arrival": "14:10",
            "price": 1_300_000,
            "class": "economy",
        },
        {
            "airline": "Vietnam Airlines",
            "departure": "18:00",
            "arrival": "20:10",
            "price": 3_200_000,
            "class": "business",
        },
    ],
    ("Hồ Chí Minh", "Đà Nẵng"): [
        {
            "airline": "Vietnam Airlines",
            "departure": "09:00",
            "arrival": "10:20",
            "price": 1_300_000,
            "class": "economy",
        },
        {
            "airline": "VietJet Air",
            "departure": "13:00",
            "arrival": "14:20",
            "price": 780_000,
            "class": "economy",
        },
    ],
    ("Hồ Chí Minh", "Phú Quốc"): [
        {
            "airline": "Vietnam Airlines",
            "departure": "08:00",
            "arrival": "09:00",
            "price": 1_100_000,
            "class": "economy",
        },
        {
            "airline": "VietJet Air",
            "departure": "15:00",
            "arrival": "16:00",
            "price": 650_000,
            "class": "economy",
        },
    ],
}


HOTELS_DB = {
    "Đà Nẵng": [
        {
            "name": "Mường Thanh Luxury",
            "stars": 5,
            "price_per_night": 1_800_000,
            "area": "Mỹ Khê",
            "rating": 4.5,
        },
        {
            "name": "Sala Danang Beach",
            "stars": 4,
            "price_per_night": 1_200_000,
            "area": "Mỹ Khê",
            "rating": 4.3,
        },
        {
            "name": "IVY Hotel Danang",
            "stars": 3,
            "price_per_night": 650_000,
            "area": "Sơn Trà",
            "rating": 4.1,
        },
        {
            "name": "Memory Hostel",
            "stars": 2,
            "price_per_night": 250_000,
            "area": "Hải Châu",
            "rating": 4.6,
        },
        {
            "name": "Christina's Homestay",
            "stars": 2,
            "price_per_night": 350_000,
            "area": "An Thượng",
            "rating": 4.7,
        },
    ],
    "Phú Quốc": [
        {
            "name": "Vinpearl Resort",
            "stars": 5,
            "price_per_night": 3_500_000,
            "area": "Bãi Dài",
            "rating": 4.4,
        },
        {
            "name": "Sol by Meliá",
            "stars": 4,
            "price_per_night": 1_500_000,
            "area": "Bãi Trường",
            "rating": 4.2,
        },
        {
            "name": "Lahana Resort",
            "stars": 3,
            "price_per_night": 800_000,
            "area": "Dương Đông",
            "rating": 4.0,
        },
        {
            "name": "Station Hostel",
            "stars": 2,
            "price_per_night": 200_000,
            "area": "Dương Đông",
            "rating": 4.5,
        },
    ],
    "Hồ Chí Minh": [
        {
            "name": "Rex Hotel",
            "stars": 5,
            "price_per_night": 2_800_000,
            "area": "Quận 1",
            "rating": 4.3,
        },
        {
            "name": "Liberty Central",
            "stars": 4,
            "price_per_night": 1_400_000,
            "area": "Quận 1",
            "rating": 4.1,
        },
        {
            "name": "A25 Zen Hotel",
            "stars": 3,
            "price_per_night": 550_000,
            "area": "Quận 3",
            "rating": 4.4,
        },
        {
            "name": "The Common Room",
            "stars": 2,
            "price_per_night": 180_000,
            "area": "Quận 1",
            "rating": 4.6,
        },
    ],
}


def _format_money(amount: int) -> str:
    return f"{amount:,}".replace(",", ".") + "đ"


def _format_budget_hint(expense_name: str, amount: int) -> str:
    return f"{expense_name}={amount}"


def _normalize_expense_name(raw_name: str) -> str:
    normalized = " ".join(raw_name.strip().replace("_", " ").lower().split())
    alias_map = {
        "vé bay": "vé máy bay",
        "vé máy bay": "vé máy bay",
        "khách sạn": "khách sạn",
        "khach san": "khách sạn",
        "hotel": "khách sạn",
        "phòng": "khách sạn",
    }
    return alias_map.get(normalized, raw_name.strip().replace("_", " "))


def _split_expense_entry(entry: str) -> tuple[str, str]:
    for separator in ("=", ":"):
        if separator in entry:
            return entry.split(separator, 1)
    raise ValueError("Mỗi khoản chi phải theo mẫu tên=số_tiền hoặc tên:số_tiền.")


def _format_flights(origin: str, destination: str, flights: list[dict]) -> str:
    lines = [f"Các chuyến bay từ {origin} đến {destination}:"]
    for flight in flights:
        lines.append(
            "- "
            f"{flight['airline']} | "
            f"{flight['departure']} - {flight['arrival']} | "
            f"{flight['class']} | "
            f"{_format_money(flight['price'])}"
        )

    cheapest_flight = min(flights, key=lambda flight: flight["price"])
    lines.append("---")
    lines.append(
        "Gợi ý để nối sang calculate_budget: "
        + _format_budget_hint("vé máy bay", cheapest_flight["price"])
    )
    return "\n".join(lines)


def _parse_amount(raw_amount: str) -> int:
    normalized = raw_amount.strip().replace(".", "")
    if not normalized.isdigit():
        raise ValueError("Số tiền phải là số nguyên hợp lệ.")
    return int(normalized)


@tool
def search_flights(origin: str, destination: str) -> str:
    """
    Tìm kiếm các chuyến bay giữa hai thành phố trong dữ liệu mock của hệ thống du lịch.

    Dùng tool này khi người dùng đã cung cấp đủ điểm khởi hành và điểm đến, và cần biết
    danh sách chuyến bay, hãng bay, giờ đi, giờ đến, hạng vé, hoặc giá vé.

    Args:
        origin: Thành phố khởi hành, ví dụ "Hà Nội" hoặc "Hồ Chí Minh".
        destination: Thành phố đến, ví dụ "Đà Nẵng" hoặc "Phú Quốc".

    Returns:
        Chuỗi tiếng Việt mô tả danh sách chuyến bay theo chiều yêu cầu.
        Nếu không có dữ liệu chiều thuận nhưng có dữ liệu chiều ngược, trả về thông báo
        tham khảo chiều ngược. Nếu không tìm thấy cả hai chiều, trả về thông báo không có kết quả.
    """
    try:
        flights = FLIGHTS_DB.get((origin, destination))
        if flights:
            return _format_flights(origin, destination, flights)

        reverse_flights = FLIGHTS_DB.get((destination, origin))
        if reverse_flights:
            return (
                f"Không tìm thấy chuyến bay từ {origin} đến {destination}.\n"
                f"Tuy nhiên, hệ thống có dữ liệu chiều ngược để bạn tham khảo:\n"
                f"{_format_flights(destination, origin, reverse_flights)}"
            )

        return f"Không tìm thấy chuyến bay từ {origin} đến {destination}."
    except Exception:
        return (
            "Hệ thống tra cứu chuyến bay đang gặp sự cố tạm thời. "
            "Vui lòng thử lại sau."
        )


@tool
def search_hotels(city: str, max_price_per_night: int = 99_999_999) -> str:
    """
    Tìm kiếm khách sạn theo thành phố và ngân sách tối đa mỗi đêm trong dữ liệu mock.

    Dùng tool này khi người dùng muốn tìm nơi lưu trú tại một thành phố cụ thể, có thể
    kèm điều kiện về giá tối đa mỗi đêm. Kết quả được lọc theo ngân sách và sắp xếp
    theo rating giảm dần để ưu tiên lựa chọn tốt hơn.

    Args:
        city: Thành phố cần tìm khách sạn, ví dụ "Đà Nẵng", "Phú Quốc", "Hồ Chí Minh".
        max_price_per_night: Mức giá tối đa mỗi đêm bằng VND. Mặc định là không giới hạn.

    Returns:
        Chuỗi tiếng Việt liệt kê tên khách sạn, số sao, giá/đêm, khu vực, rating.
        Nếu không có thành phố trong dữ liệu hoặc không có khách sạn phù hợp ngân sách,
        trả về thông báo rõ ràng để agent có thể phản hồi lại người dùng.
    """
    try:
        hotels = HOTELS_DB.get(city)
        if hotels is None:
            return f"Không tìm thấy dữ liệu khách sạn tại {city}."

        filtered_hotels = [
            hotel for hotel in hotels if hotel["price_per_night"] <= max_price_per_night
        ]
        filtered_hotels.sort(key=lambda hotel: hotel["rating"], reverse=True)

        if not filtered_hotels:
            return (
                f"Không tìm thấy khách sạn tại {city} giá dưới "
                f"{_format_money(max_price_per_night)}/đêm. Hãy thử tăng ngân sách."
            )

        lines = [f"Các khách sạn tại {city} phù hợp ngân sách:"]
        for hotel in filtered_hotels:
            lines.append(
                "- "
                f"{hotel['name']} | "
                f"{hotel['stars']} sao | "
                f"{_format_money(hotel['price_per_night'])}/đêm | "
                f"Khu vực: {hotel['area']} | "
                f"Rating: {hotel['rating']}"
            )

        cheapest_hotel = min(
            filtered_hotels, key=lambda hotel: hotel["price_per_night"]
        )
        lines.append("---")
        lines.append(
            "Gợi ý để nối sang calculate_budget: "
            + _format_budget_hint("khách sạn mỗi đêm", cheapest_hotel["price_per_night"])
        )
        lines.append(
            "Khi cần tính tổng chi phí khách sạn, hãy lấy giá mỗi đêm nhân với số đêm lưu trú."
        )
        return "\n".join(lines)
    except Exception:
        return (
            "Hệ thống tra cứu khách sạn đang gặp sự cố tạm thời. "
            "Vui lòng thử lại sau."
        )


@tool
def calculate_budget(total_budget: int, expenses: str) -> str:
    """
    Tính toán ngân sách còn lại sau khi trừ các khoản chi được mô tả bằng chuỗi.

    Dùng tool này khi người dùng cần biết tổng chi, phần ngân sách còn lại, hoặc đang
    kiểm tra xem kế hoạch chuyến đi có vượt ngân sách hay không.

    Args:
        total_budget: Tổng ngân sách ban đầu bằng VND.
        expenses: Chuỗi các khoản chi theo định dạng "tên=số_tiền", ngăn cách bằng dấu phẩy.
            Ví dụ: "vé máy bay=890000,khách sạn=650000".

    Returns:
        Chuỗi tiếng Việt gồm bảng chi tiết chi phí, tổng chi, ngân sách ban đầu và số tiền
        còn lại hoặc số tiền vượt. Nếu chuỗi `expenses` sai định dạng, trả về thông báo lỗi rõ ràng.
    """
    try:
        parsed_total_budget = int(total_budget)
        expense_items: list[tuple[str, int]] = []
        raw_entries = [entry.strip() for entry in expenses.split(",") if entry.strip()]

        if not raw_entries:
            return (
                "Lỗi định dạng chi phí: vui lòng nhập ít nhất một khoản theo mẫu "
                "tên=số_tiền hoặc tên:số_tiền."
            )

        for entry in raw_entries:
            try:
                name, raw_amount = _split_expense_entry(entry)
            except ValueError:
                return (
                    "Lỗi định dạng chi phí: mỗi khoản phải theo mẫu tên=số_tiền "
                    f"hoặc tên:số_tiền, nhưng nhận được '{entry}'."
                )

            name = _normalize_expense_name(name)
            raw_amount = raw_amount.strip()

            if not name:
                return "Lỗi định dạng chi phí: tên khoản chi không được để trống."
            if not raw_amount:
                return f"Lỗi định dạng chi phí: khoản '{name}' đang thiếu số tiền."

            try:
                amount = _parse_amount(raw_amount)
            except ValueError:
                return (
                    f"Lỗi định dạng chi phí: số tiền của khoản '{name}' không hợp lệ. "
                    "Vui lòng dùng số nguyên, có thể kèm dấu chấm ngăn cách hàng nghìn."
                )

            expense_items.append((name, amount))

        total_expenses = sum(amount for _, amount in expense_items)
        remaining_budget = parsed_total_budget - total_expenses

        lines = ["Bảng ghi chi phí:"]
        for name, amount in expense_items:
            lines.append(f"- {name}: {_format_money(amount)}")

        lines.append("---")
        lines.append(f"Tổng chi: {_format_money(total_expenses)}")
        lines.append(f"Ngân sách: {_format_money(parsed_total_budget)}")

        if remaining_budget >= 0:
            lines.append(f"Còn lại: {_format_money(remaining_budget)}")
        else:
            lines.append(f"Vượt ngân sách: {_format_money(abs(remaining_budget))}")
            lines.append("Cần điều chỉnh kế hoạch chi tiêu.")

        return "\n".join(lines)
    except Exception:
        return (
            "Hệ thống tính ngân sách đang gặp sự cố tạm thời. "
            "Vui lòng kiểm tra lại dữ liệu và thử lại."
        )
