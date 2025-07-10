from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def run_input_email_tests(driver, timeout=10):
    results = []
    wait = WebDriverWait(driver, timeout)

    # Soportamos tanto email como inputs de texto con nombres sospechosos
    selectors = [
        'input[type="email"]',
        'input[type="text"][placeholder*="email" i]',
        'input[type="text"][name*="email" i]',
        'input[type="text"][id*="email" i]'
    ]

    def describir_input(el, index):
        ph = el.get_attribute("placeholder")
        name = el.get_attribute("name")
        id_attr = el.get_attribute("id")
        if ph: return f'Input con placeholder "{ph}"'
        elif name: return f'Input con name="{name}"'
        elif id_attr: return f'Input con id="{id_attr}"'
        else: return f'Input[{index}] sin identificador'

    def probar_input(input_email, identificador):
        def test(nombre, funcion):
            try:
                mensaje, estado = funcion()
                results.append(f"[{estado}] {identificador} - {nombre}: {mensaje}")
            except Exception as e:
                results.append(f"[❌] {identificador} - {nombre}: Error: {str(e)}")

        def correo_valido():
            input_email.clear()
            input_email.send_keys("usuario@correo.com")
            valor = input_email.get_attribute("value")
            return ("Correo aceptado correctamente." if valor == "usuario@correo.com"
                    else f"No aceptado. Valor: '{valor}'", "✔" if valor == "usuario@correo.com" else "❌")

        def sin_arroba():
            input_email.clear()
            input_email.send_keys("usuariocorreo.com")
            valor = input_email.get_attribute("value")
            return ("Falta arroba. Formato inválido.", "❌") if "@" not in valor else ("Aceptó valor sin @", "❗")

        def dominio_invalido():
            input_email.clear()
            input_email.send_keys("usuario@")
            valor = input_email.get_attribute("value")
            return ("Dominio incompleto detectado.", "❌") if valor.endswith("@") else ("Dominio incompleto modificado.", "⚠")

        def doble_arroba():
            input_email.clear()
            input_email.send_keys("user@@dominio.com")
            valor = input_email.get_attribute("value")
            return ("Doble @ detectado.", "❌") if valor.count("@") > 1 else ("Aceptó doble @", "⚠")

        def vacio():
            input_email.clear()
            valor = input_email.get_attribute("value")
            return ("Campo vacío permitido." if valor == "" else f"No se vació correctamente: '{valor}'", "⚠")

        def espacios():
            input_email.clear()
            input_email.send_keys("     ")
            valor = input_email.get_attribute("value")
            return ("Campo acepta solo espacios.", "⚠") if valor.strip() == "" else (f"Valor tras limpiar: '{valor}'", "⚠")

        def xss():
            input_email.clear()
            payload = '<script>alert(1)</script>'
            input_email.send_keys(payload)
            valor = input_email.get_attribute("value")
            return ("XSS sin sanitizar." if payload in valor else "XSS bloqueado o sanitizado.",
                    "❗" if payload in valor else "✔")

        def sql():
            input_email.clear()
            payload = "' OR '1'='1"
            input_email.send_keys(payload)
            valor = input_email.get_attribute("value")
            return ("SQL Injection posible." if payload in valor else "SQL Injection bloqueado.",
                    "❗" if payload in valor else "✔")

        def largo():
            input_email.clear()
            texto = "a" * 200 + "@gmail.com"
            input_email.send_keys(texto)
            valor = input_email.get_attribute("value")
            if len(valor) >= len(texto): return "Correo largo aceptado.", "✔"
            elif 0 < len(valor) < len(texto): return f"Texto recortado. Largo final: {len(valor)}", "⚠"
            else: return "Texto largo rechazado.", "❌"

        test("Correo válido", correo_valido)
        test("Sin @", sin_arroba)
        test("Dominio incompleto", dominio_invalido)
        test("Doble @", doble_arroba)
        test("Campo vacío", vacio)
        test("Solo espacios", espacios)
        test("Inyección XSS", xss)
        test("Inyección SQL", sql)
        test("Texto largo", largo)

    # Buscar y testear cada input encontrado por selector
    index = 1
    encontrados = set()
    for selector in selectors:
        try:
            elementos = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, selector)))
            for el in elementos:
                if el in encontrados:
                    continue
                encontrados.add(el)
                identificador = describir_input(el, index)
                probar_input(el, identificador)
                index += 1
        except:
            results.append(f"[⚠] No se encontraron elementos con selector: {selector}")

    return results
