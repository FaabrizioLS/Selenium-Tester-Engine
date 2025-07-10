from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ============================================
# Función principal para probar campos de fecha y hora
# ============================================
def run_input_datetime_tests(driver, timeout=10):
    results = []
    wait = WebDriverWait(driver, timeout)

    # Tipos conocidos (HTML nativos)
    selectors = {
        "date": 'input[type="date"]',
        "time": 'input[type="time"]',
        "month": 'input[type="month"]',
        "week": 'input[type="week"]',
        "datetime-local": 'input[type="datetime-local"]',
        # Posibles inputs simulados
        "text-date": 'input[type="text"][placeholder*="fecha"], input[type="text"][placeholder*="date"], input[name*="date"], input[name*="fecha"]',
    }

    def describir_input(el, index, tipo):
        ph = el.get_attribute("placeholder")
        name = el.get_attribute("name")
        id_attr = el.get_attribute("id")
        if ph: return f'Input {tipo} con placeholder "{ph}"'
        elif name: return f'Input {tipo} con name="{name}"'
        elif id_attr: return f'Input {tipo} con id="{id_attr}"'
        else: return f'Input {tipo}[{index}] sin identificador'

    def probar_input(input_el, identificador, tipo, valor_correcto):
        def test(nombre, funcion):
            try:
                mensaje, estado = funcion()
                results.append(f"[{estado}] {identificador} - {nombre}: {mensaje}")
            except Exception as e:
                results.append(f"[❌] {identificador} - {nombre}: Error durante la prueba: {str(e)}")

        def valor_valido():
            input_el.clear()
            input_el.send_keys(valor_correcto)
            valor = input_el.get_attribute("value")
            return ("Valor aceptado correctamente." if valor == valor_correcto else f"No aceptado: '{valor}'", "✔")

        def formato_invalido():
            input_el.clear()
            input_el.send_keys("invalido")
            valor = input_el.get_attribute("value")
            return ("Formato no aceptado." if valor == "" else f"Aceptó formato inválido: '{valor}'", "⚠")

        def vacio():
            input_el.clear()
            valor = input_el.get_attribute("value")
            return ("Campo vacío permitido." if valor == "" else f"No se vació: '{valor}'", "⚠")

        def especiales():
            input_el.clear()
            input_el.send_keys("@#!")
            valor = input_el.get_attribute("value")
            return ("Caracteres especiales rechazados." if valor == "" else f"Valor actual: '{valor}'", "⚠")

        def xss():
            input_el.clear()
            input_el.send_keys("<script>alert(1)</script>")
            valor = input_el.get_attribute("value")
            return ("XSS sin sanitizar." if '<' in valor else "XSS bloqueado.", "❗" if '<' in valor else "✔")

        def sql():
            input_el.clear()
            input_el.send_keys("' OR '1'='1")
            valor = input_el.get_attribute("value")
            return ("SQL Injection posible." if '1' in valor else "SQL bloqueado.", "❗" if '1' in valor else "✔")

        test("Valor válido", valor_valido)
        test("Formato incorrecto", formato_invalido)
        test("Campo vacío", vacio)
        test("Caracteres especiales", especiales)
        test("Inyección XSS", xss)
        test("Inyección SQL", sql)

    # ============================
    # Ejecutamos pruebas por tipo
    # ============================
    for tipo, selector in selectors.items():
        try:
            elementos = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, selector)))
            for idx, el in enumerate(elementos):
                valor_correcto = {
                    "date": "2025-06-28",
                    "time": "13:30",
                    "month": "2025-06",
                    "week": "2025-W26",
                    "datetime-local": "2025-06-28T13:30",
                    "text-date": "2025-06-28"
                }.get(tipo, "2025-06-28")
                probar_input(el, describir_input(el, idx + 1, tipo), tipo, valor_correcto)
        except Exception:
            results.append(f"[❌] No se encontraron inputs para tipo: {tipo}")

    return results
