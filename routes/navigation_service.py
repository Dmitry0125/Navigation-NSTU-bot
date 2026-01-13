from routes.routes_data import ROOMS_DATABASE, OUTDOOR_ROUTES, INDOOR_ROUTES
import re

class NavigationService:
    
    @staticmethod
    def normalize_room_number(room_input: str) -> str:
        """Нормализует номер аудитории: приводит к верхнему регистру и убирает пробелы"""
        return room_input.strip().upper()
    
    @staticmethod
    def is_valid_room_format(room_input: str) -> tuple[bool, str]:
        """
        Проверяет формат номера аудитории
        
        Возвращает: (is_valid, error_message)
        Допустимые форматы:
        - 101 (3 цифры)
        - 101А (3 цифры + русская буква)
        - 108Б (3 цифры + русская буква)
        - 1001 (4 цифры)
        - 1001А (4 цифры + русская буква)
        """
        normalized = NavigationService.normalize_room_number(room_input)
        
        if not normalized:
            return False, "❌ Введен пустой номер"
        
        # Паттерн: 2-4 цифры, необязательно одна русская буква в конце
        pattern = r'^(\d{2,4})([А-Я])?$'
        match = re.match(pattern, normalized)
        
        if not match:
            return False, (
                "❌ Неверный формат номера аудитории.\n\n"
                "**Допустимые форматы:**\n"
                "• 101 (3 цифры)\n"
                "• 101А (3 цифры + буква А или Б)\n"
            )
        
        return True, ""
    
    @staticmethod
    def extract_room_parts(room_input: str) -> tuple[str, str]:
        """
        Разделяет номер аудитории на числовую часть и букву
        
        Примеры:
        - "203" → ("203", "")
        - "203Б" → ("203", "Б")
        - "101А" → ("101", "А")
        """
        normalized = NavigationService.normalize_room_number(room_input)
        match = re.match(r'^(\d{2,4})([А-Я])?$', normalized)
        
        if match:
            numeric_part = match.group(1)
            letter_part = match.group(2) or ""
            return numeric_part, letter_part
        
        return room_input, ""
    
    @staticmethod
    def find_room_in_database(room_input: str):
        """
        Ищет аудиторию в базе данных
        
        Возвращает: (room_info, found_exact, suggestion)
        - room_info: информация об аудитории или None
        - found_exact: True если найдено точное совпадение
        - suggestion: предложение если нет точного совпадения
        """
        normalized = NavigationService.normalize_room_number(room_input)
        numeric_part, letter_part = NavigationService.extract_room_parts(normalized)
        
        # 1. Проверяем точное совпадение
        if normalized in ROOMS_DATABASE:
            return ROOMS_DATABASE[normalized], True, None
        
        # 2. Если есть буква в конце, проверяем есть ли просто числовая часть
        if letter_part:
            if numeric_part in ROOMS_DATABASE:
                # Есть только числовая часть, без буквы
                suggestion = (
                    f"⚠ Аудитории '{normalized}' нет в базе, но есть аудитория '{numeric_part}'.\n"
                    f"Возможно, буква '{letter_part}' означает дополнительный кабинет рядом с '{numeric_part}'."
                )
                return ROOMS_DATABASE[numeric_part], False, suggestion
        
        # 3. Ищем ближайшие варианты
        suggestions = []
        for room_in_db in ROOMS_DATABASE.keys():
            db_numeric, db_letter = NavigationService.extract_room_parts(room_in_db)
            
            if db_numeric == numeric_part:
                # Та же числовая часть, но другая буква
                suggestions.append(room_in_db)
            elif db_numeric.startswith(numeric_part[:2]):  # Первые 2 цифры совпадают
                suggestions.append(room_in_db)
        
        if suggestions:
            suggestion_text = f"Ближайшие аудитории: {', '.join(sorted(suggestions)[:5])}"
            return None, False, suggestion_text
        
        return None, False, "Аудитория не найдена"
    
    @staticmethod
    def get_route_to_room(target_corpus: str, room_input: str) -> tuple[str, bool]:
        """
        Получить маршрут ОТ 1 КОРПУСА до аудитории
        
        Возвращает: (message, is_success)
        """
        # Проверяем формат
        is_valid, error_msg = NavigationService.is_valid_room_format(room_input)
        if not is_valid:
            return error_msg, False
        
        normalized = NavigationService.normalize_room_number(room_input)
        numeric_part, letter_part = NavigationService.extract_room_parts(normalized)
        
        # Ищем в базе
        room_info, found_exact, suggestion = NavigationService.find_room_in_database(room_input)
        
        # Если аудитория не найдена
        if not room_info:
            if suggestion:
                return f"❌ Аудитория '{normalized}' не найдена.", False
            return f"❌ Аудитория '{normalized}' не найдена в базе данных.", False
        
        # Проверяем корпус
        if room_info["corpus"] != target_corpus:
            suggestion_text = f"⚠ Аудитория '{normalized}' находится в {room_info['corpus']} корпусе."
            
            # Предлагаем аудитории в целевом корпусе
            rooms_in_target = [
                room for room, info in ROOMS_DATABASE.items() 
                if info["corpus"] == target_corpus
            ]
            if rooms_in_target:
                suggestion_text += f"\n\nВ {target_corpus} корпусе есть аудитории: {', '.join(sorted(rooms_in_target)[:8])}"
            
            return suggestion_text, False
        
        # Если найдено не точное совпадение, а только числовая часть
        if not found_exact and letter_part:
            suggestion_msg = (
                f"ℹ️ Аудитории '{normalized}' нет в базе, но есть '{numeric_part}'.\n"
                f"Показываю маршрут до аудитории '{numeric_part}':\n\n"
            )
        else:
            suggestion_msg = ""
        
        # Собираем маршрут
        parts = []
        
        # Заголовок
        if found_exact:
            parts.append(f"🧭 **Маршрут до аудитории {normalized}**")
        else:
            parts.append(f"🧭 **Маршрут до аудитории {numeric_part}**")
        
        parts.append(f"📍 **Корпус:** {target_corpus}")
        parts.append("")  # Пустая строка
        
        # Уличный маршрут
        if target_corpus in OUTDOOR_ROUTES:
            parts.append("**🚶 Как дойти от 1 корпуса:**")
            for i, step in enumerate(OUTDOOR_ROUTES[target_corpus], 1):
                parts.append(f"{i}. {step}")
            parts.append("")  # Пустая строка
        
        # Внутри корпуса
        if target_corpus in INDOOR_ROUTES:
            floor = str(room_info["floor"])
            
            parts.append(f"**🏢 Внутри {target_corpus} корпуса:**")
            
            if "entrance" in INDOOR_ROUTES[target_corpus]:
                parts.append(f"• {INDOOR_ROUTES[target_corpus]['entrance']}")
            
            # Ищем маршрут для аудитории
            room_to_search = normalized if found_exact else numeric_part
            
            if floor in INDOOR_ROUTES[target_corpus]:
                if room_to_search in INDOOR_ROUTES[target_corpus][floor]:
                    route = INDOOR_ROUTES[target_corpus][floor][room_to_search]
                    parts.append(f"**📍 На {floor} этаже:**")
                    
                    if isinstance(route, list):
                        for step in route:
                            parts.append(f"• {step}" if not step.startswith("•") else step)
                    else:
                        parts.append(f"• {route}")
                elif numeric_part in INDOOR_ROUTES[target_corpus][floor]:
                    # Показываем маршрут до числовой части
                    route = INDOOR_ROUTES[target_corpus][floor][numeric_part]
                    parts.append(f"**📍 На {floor} этаже:**")
                    
                    if isinstance(route, list):
                        for step in route:
                            parts.append(f"• {step}" if not step.startswith("•") else step)
                    else:
                        parts.append(f"• {route}")
                    
                    if letter_part:
                        parts.append(f"\n🔍 **Примечание:** Аудитория с буквой '{letter_part}' "
                                    f"обычно находится рядом с аудиторией '{numeric_part}'")
                else:
                    parts.append(f"**📍 На {floor} этаже:**")
                    parts.append(f"• Аудитория {numeric_part} находится на этом этаже")
        
        # Финальное сообщение
        parts.append("")
        if found_exact:
            parts.append("✅ **Маршрут построен!**")
        else:
            parts.append("✅ **Показан маршрут до ближайшей аудитории**")
        
        # Добавляем примечание в начало если нужно
        full_message = (suggestion_msg + "\n".join(parts)) if suggestion_msg else "\n".join(parts)
        
        return full_message, True
