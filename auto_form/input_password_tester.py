from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def run_input_password_tests(driver, timeout=10):
    results = []
    wait = WebDriverWait(driver, timeout)

    # Selectores para inputs de contraseña (también inputs text disfrazados)
    selectors = [
        'input[type="password"]',
        'input[type="text"][placeholder*="contraseña" i]',
        'input[type="text"][name*="contraseña" i]',
        'input[type="text"][id*="contraseña" i]'
    ]

    encontrados = set()
    index = 1

    def describir_input(el, idx):
        ph = el.get_attribute("placeholder")
        name = el.get_attribute("name")
        id_attr = el.get_attribute("id")
        if ph: return f'Input con placeholder "{ph}"'
        elif name: return f'Input con name="{name}"'
        elif id_attr: return f'Input con id="{id_attr}"'
        else: return f'Input[{idx}] sin identificador'

    def probar_input(input_password, identificador):
        def test(nombre, funcion):
            try:
                mensaje, estado = funcion()
                results.append(f"[{estado}] {identificador} - {nombre}: {mensaje}")
            except Exception as e:
                results.append(f"[❌] {identificador} - {nombre}: Error: {str(e)}")

        def contrasena_valida():
            input_password.clear()
            input_password.send_keys("Segura123!")
            valor = input_password.get_attribute("value")
            return ("Contraseña aceptada." if valor == "Segura123!" else f"Rechazada: '{valor}'", "✔")

        def vacio():
            input_password.clear()
            valor = input_password.get_attribute("value")
            return ("Campo vacío permitido." if valor == "" else f"No se vació: '{valor}'", "⚠")

        def solo_espacios():
            input_password.clear()
            input_password.send_keys("     ")
            valor = input_password.get_attribute("value")
            return ("Campo acepta solo espacios." if valor.strip() == "" else f"Valor con espacios: '{valor}'", "⚠")

        def caracteres_especiales():
            input_password.clear()
            input_password.send_keys("@#$%^&*()_+=")
            valor = input_password.get_attribute("value")
            return (f"Acepta caracteres especiales: '{valor}'", "✔")

        def xss():
            input_password.clear()
            payload = "<script>alert(1)</script>"
            input_password.send_keys(payload)
            valor = input_password.get_attribute("value")
            return ("XSS sin sanitizar." if payload in valor else "XSS bloqueado.", "❗" if payload in valor else "✔")

        def sql():
            input_password.clear()
            payload = "' OR '1'='1"
            input_password.send_keys(payload)
            valor = input_password.get_attribute("value")
            return ("SQL Injection posible." if payload in valor else "SQL bloqueado.", "❗" if payload in valor else "✔")

        def longitud_larga():
            input_password.clear()
            texto = "Aa1!" * 300  # 1200 caracteres
            input_password.send_keys(texto)
            valor = input_password.get_attribute("value")
            if len(valor) >= 1000:
                return "Campo acepta contraseña muy larga.", "✔"
            elif 0 < len(valor) < 1000:
                return f"Texto recortado. Largo final: {len(valor)}", "⚠"
            else:
                return "Texto largo rechazado.", "❌"

        test("Contraseña válida", contrasena_valida)
        test("Campo vacío", vacio)
        test("Solo espacios", solo_espacios)
        test("Caracteres especiales", caracteres_especiales)
        test("Inyección XSS", xss)
        test("Inyección SQL", sql)
        test("Texto largo", longitud_larga)

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
            results.append(f"[⚠] No se encontraron inputs con selector: {selector}")

    return results
