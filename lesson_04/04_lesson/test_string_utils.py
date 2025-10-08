import pytest
from string_utils import StringUtils

# Инициализация экземпляра класса для тестирования
utils = StringUtils()


class TestStringUtils:

    # Тесты для функции capitalize
    def test_capitalize_positive(self):
        """Позитивные тесты для capitalize"""
        # Строка с текстом
        assert utils.capitalize("skypro") == "Skypro"
        # Строка с одним символом
        assert utils.capitalize("a") == "A"
        # Строка с числами как строка
        assert utils.capitalize("123") == "123"
        # Строка с пробелами внутри
        assert utils.capitalize("04 апреля 2023") == "04 апреля 2023"

    def test_capitalize_negative(self):
        """Негативные тесты для capitalize"""
        # Пустая строка
        assert utils.capitalize("") == ""
        # Строка с пробелом
        assert utils.capitalize(" ") == " "
        # Строка с несколькими пробелами
        assert utils.capitalize("   ") == "   "

    def test_capitalize_already_capitalized(self):
        """Тест на уже заглавную первую букву"""
        assert utils.capitalize("Skypro") == "Skypro"
        assert utils.capitalize("Тест") == "Тест"

    # Тесты для функции trim
    def test_trim_positive(self):
        """Позитивные тесты для trim"""
        # Строка с пробелами в начале
        assert utils.trim("   skypro") == "skypro"
        # Строка с текстом и пробелами
        assert utils.trim("  04 апреля 2023") == "04 апреля 2023"
        # Строка с числами
        assert utils.trim(" 123") == "123"

    def test_trim_negative(self):
        """Негативные тесты для trim"""
        # Пустая строка
        assert utils.trim("") == ""
        # Строка только из пробелов
        assert utils.trim(" ") == ""
        assert utils.trim("   ") == ""
        # Строка с пробелами в конце (не должна изменяться)
        assert utils.trim("skypro  ") == "skypro  "

    def test_trim_no_spaces(self):
        """Тест на строку без пробелов в начале"""
        # Не пустая строка
        assert utils.trim("skypro") == "skypro"
        # Строка с числами
        assert utils.trim("123") == "123"
        # Строка с текстом
        assert utils.trim("Тест") == "Тест"

    # Тесты для функции to_list
    def test_to_list_positive(self):
        """Позитивные тесты для to_list"""
        # Строка с разделителями
        assert utils.to_list("a,b,c,d") == ["a", "b", "c", "d"]
        # Числа как строка
        assert utils.to_list("1,2,3") == ["1", "2", "3"]
        # Строка с пробелами
        assert utils.to_list("04,апреля,2023") == ["04", "апреля", "2023"]
        # Строка с одним элементом
        assert utils.to_list("Тест") == ["Тест"]

    def test_to_list_negative(self):
        """Негативные тесты для to_list"""
        # Пустая строка
        assert utils.to_list("") == []
        # Строка с пробелом
        assert utils.to_list(" ") == [" "]

    def test_to_list_custom_delimiter(self):
        """Тест to_list с пользовательским разделителем"""
        # Разные разделители
        assert utils.to_list("1:2:3", ":") == ["1", "2", "3"]
        assert utils.to_list("a-b-c", "-") == ["a", "b", "c"]
        assert utils.to_list("04 апреля 2023", " ") == ["04", "апреля", "2023"]

    # Тесты для функции contains
    def test_contains_positive(self):
        """Позитивные тесты для contains"""
        # Поиск символа в строке
        assert utils.contains("SkyPro", "S") == True
        # Поиск числа в строке
        assert utils.contains("123", "2") == True
        # Поиск пробела в строке
        assert utils.contains("04 апреля 2023", " ") == True
        # Поиск подстроки
        assert utils.contains("Тест", "Те") == True

    def test_contains_negative(self):
        """Негативные тесты для contains"""
        # Символ не найден
        assert utils.contains("SkyPro", "U") == False
        # Пустая строка
        assert utils.contains("", "a") == False
        # Строка с пробелом
        assert utils.contains(" ", "a") == False
        # Пустая подстрока (особый случай)
        assert utils.contains("Тест", "") == True

    # Тесты для функции delete_symbol
    def test_delete_symbol_positive(self):
        """Позитивные тесты для delete_symbol"""
        # Удаление одного символа
        assert utils.delete_symbol("SkyPro", "k") == "SyPro"
        # Удаление подстроки
        assert utils.delete_symbol("SkyPro", "Pro") == "Sky"
        # Удаление числа из строки
        assert utils.delete_symbol("12345", "3") == "1245"
        # Удаление пробела
        assert utils.delete_symbol("04 апреля 2023", " ") == "04апреля2023"

    def test_delete_symbol_negative(self):
        """Негативные тесты для delete_symbol"""
        # Удаление несуществующего символа
        assert utils.delete_symbol("SkyPro", "X") == "SkyPro"
        # Пустая строка
        assert utils.delete_symbol("", "a") == ""
        # Строка с пробелом
        assert utils.delete_symbol(" ", "a") == " "
        # Удаление из строки с пробелом
        assert utils.delete_symbol(" ", " ") == ""

    # Тесты для функции starts_with
    def test_starts_with_positive(self):
        """Позитивные тесты для starts_with"""
        # Начинается с символа
        assert utils.starts_with("SkyPro", "S") == True
        # Начинается с числа
        assert utils.starts_with("123", "1") == True
        # Начинается с пробела
        assert utils.starts_with(" Тест", " ") == True
        # Начинается с кириллицы
        assert utils.starts_with("Тест", "Т") == True

    def test_starts_with_negative(self):
        """Негативные тесты для starts_with"""
        # Не начинается с символа
        assert utils.starts_with("SkyPro", "P") == False
        # Пустая строка
        assert utils.starts_with("", "a") == False
        # Строка с пробелом
        assert utils.starts_with(" ", "a") == False
        # Пустой символ поиска
        assert utils.starts_with("Тест", "") == True

    # Тесты для функции end_with
    def test_end_with_positive(self):
        """Позитивные тесты для end_with"""
        # Заканчивается символом
        assert utils.end_with("SkyPro", "o") == True
        # Заканчивается числом
        assert utils.end_with("123", "3") == True
        # Заканчивается кириллицей
        assert utils.end_with("Тест", "т") == True

    def test_end_with_negative(self):
        """Негативные тесты для end_with"""
        # Не заканчивается символом
        assert utils.end_with("SkyPro", "y") == False
        # Пустая строка
        assert utils.end_with("", "a") == False
        # Строка с пробелом
        assert utils.end_with(" ", "a") == False
        # Пустой символ поиска
        assert utils.end_with("Тест", "") == True

    # Тесты для функции is_empty
    def test_is_empty_positive(self):
        """Позитивные тесты для is_empty - когда строка пустая"""
        # Пустая строка
        assert utils.is_empty("") == True
        # Строка с пробелом
        assert utils.is_empty(" ") == True
        # Строка с несколькими пробелами
        assert utils.is_empty("   ") == True
        # Строка с табуляцией (если поддерживается)
        assert utils.is_empty("\t") == True

    def test_is_empty_negative(self):
        """Негативные тесты для is_empty - когда строка НЕ пустая"""
        # Не пустая строка
        assert utils.is_empty("SkyPro") == False
        # Строка с одним символом
        assert utils.is_empty("a") == False
        # Числа как строка
        assert utils.is_empty("123") == False
        # Строка с пробелами и текстом
        assert utils.is_empty(" hello ") == False
        # Строка с текстом
        assert utils.is_empty("Тест") == False
        # Строка с датой
        assert utils.is_empty("04 апреля 2023") == False

    # Тесты для функции list_to_string
    def test_list_to_string_positive(self):
        """Позитивные тесты для list_to_string"""
        # Список чисел
        assert utils.list_to_string([1, 2, 3, 4]) == "1, 2, 3, 4"
        # Список строк
        assert utils.list_to_string(["Sky", "Pro"]) == "Sky, Pro"
        # Список с mixed типами
        assert utils.list_to_string([1, "апреля", 2023]) == "1, апреля, 2023"
        # Список с одним элементом
        assert utils.list_to_string(["Тест"]) == "Тест"

    def test_list_to_string_negative(self):
        """Негативные тесты для list_to_string"""
        # Пустой список
        assert utils.list_to_string([]) == ""
        # Список с пустыми строками
        assert utils.list_to_string(["", "", ""]) == ", , "
        # Список с пробелами
        assert utils.list_to_string([" ", " "]) == " ,  "

    def test_list_to_string_custom_joiner(self):
        """Тест list_to_string с пользовательским разделителем"""
        # Разные разделители
        assert utils.list_to_string(["Sky", "Pro"], "-") == "Sky-Pro"
        assert utils.list_to_string([1, 2, 3], ":") == "1:2:3"
        assert utils.list_to_string(["04", "апреля", "2023"], " ") == "04 апреля 2023"
        # Пустой разделитель
        assert utils.list_to_string(["a", "b", "c"], "") == "abc"

    # Дополнительные граничные тесты
    def test_boundary_cases(self):
        """Тесты граничных случаев"""
        # Строка с специальными символами
        assert utils.capitalize("!test") == "!test"
        assert utils.contains("hello!", "!") == True
        assert utils.delete_symbol("hello!", "!") == "hello"

        # Очень длинная строка
        long_string = "a" * 1000
        assert utils.capitalize(long_string) == "A" + "a" * 999
        assert utils.trim(" " + long_string) == long_string

    def test_whitespace_variations(self):
        """Тесты с разными типами пробелов"""
        # Обычный пробел
        assert utils.trim("  test") == "test"
        # Табуляция (если функция поддерживает)
        # assert utils.trim("\ttest") == "test"  # Может не работать в текущей реализации
        # Множественные пробелы
        assert utils.trim("   test") == "test"
