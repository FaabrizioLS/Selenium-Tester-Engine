from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time

def run_input_search_tests(driver):
    results = []
    inputs = driver.find_elements(By.CSS_SELECTOR, 'input[type="search"]')

    def describir_input(el, index):
        ph = el.get_attribute("placeholder")
        name = el.get_attribute("name")
        id_attr = el.get_attribute("id")
        if ph:
            return f'Input con placeholder "{ph}"'
        elif name:
            return f'Input con name="{name}"'
        elif id_attr:
            return f'Input con id="{id_attr}"'
        else:
            return f'Input[{index}] sin identificador'

    def probar_input(input_search, identificador):
        def test(nombre, funcion):
            try:
                mensaje, estado = funcion()
                results.append(f"[{estado}] {identificador} - {nombre}: {mensaje}")
            except Exception as e:
                results.append(f"[❌] {identificador} - {nombre}: Error durante la prueba: {str(e)}")

        def texto_valido():
            input_search.clear()
            input_search.send_keys("zapatos nike")
            valor = input_search.get_attribute("value")
            return ("Texto aceptado correctamente." if valor == "zapatos nike" else f"Texto no aceptado: '{valor}'", "✔" if valor == "zapatos nike" else "✘")

        def vacio():
            input_search.clear()
            valor = input_search.get_attribute("value")
            return ("Campo vacío permitido." if valor == "" else f"No se vació correctamente: '{valor}'", "⚠" if valor == "" else "✘")

        def solo_espacios():
            input_search.clear()
            input_search.send_keys("     ")
            valor = input_search.get_attribute("value")
            return ("Campo acepta solo espacios. Validamos limpieza.", "⚠") if valor.strip() == "" else (f"Contiene caracteres tras limpiar: '{valor}'", "⚠")

        def comillas():
            input_search.clear()
            input_search.send_keys('"zapatos"')
            valor = input_search.get_attribute("value")
            return f"Comillas aceptadas: '{valor}'", "✔"

        def largo():
            input_search.clear()
            texto = "producto" * 200
            input_search.send_keys(texto)
            valor = input_search.get_attribute("value")
            if len(valor) >= len(texto):
                return "Campo aceptó búsqueda larga.", "✔"
            elif 0 < len(valor) < len(texto):
                return f"Texto recortado. Largo final: {len(valor)}", "⚠"
            return "Texto largo rechazado.", "✘"

        def xss():
            input_search.clear()
            payload = '<script>alert(1)</script>'
            input_search.send_keys(payload)
            valor = input_search.get_attribute("value")
            return ("XSS sin sanitizar.", "❗") if payload in valor else ("XSS bloqueado o modificado.", "✔")

        def sql():
            input_search.clear()
            payload = "' OR '1'='1"
            input_search.send_keys(payload)
            valor = input_search.get_attribute("value")
            return ("SQL Injection posible.", "❗") if payload in valor else ("SQL Injection bloqueado.", "✔")

        def especiales():
            input_search.clear()
            input_search.send_keys("!@#$%^&*()")
            valor = input_search.get_attribute("value")
            return f"Especiales aceptados: '{valor}'", "✔"

        def emojis():
            input_search.clear()
            input_search.send_keys("🍕 búsqueda ❤️")
            valor = input_search.get_attribute("value")
            return f"Unicode/emojis aceptados: '{valor}'", "✔"

        def focus_visibilidad():
            visible = input_search.is_displayed()
            enabled = input_search.is_enabled()
            input_search.click()
            focused = driver.switch_to.active_element == input_search
            return f"Visible: {visible}, Enabled: {enabled}, Focused: {focused}", "✔" if visible and enabled and focused else "⚠"

        def atributos_extra():
            datos = {
                "autocomplete": input_search.get_attribute("autocomplete"),
                "maxlength": input_search.get_attribute("maxlength"),
                "spellcheck": input_search.get_attribute("spellcheck"),
                "inputmode": input_search.get_attribute("inputmode"),
            }
            aria_attrs = {k: input_search.get_attribute(k) for k in input_search.get_property("attributes") if "aria" in k}
            datos.update(aria_attrs)
            return f"Atributos detectados: {datos}", "✔"

        def shadow_dom():
            try:
                shadow = driver.execute_script("return arguments[0].shadowRoot", input_search)
                return ("Presente" if shadow else "No está en Shadow DOM", "⚠" if shadow else "✔")
            except:
                return "No accesible como Shadow DOM", "✔"

        def datalist():
            list_attr = input_search.get_attribute("list")
            if list_attr:
                try:
                    options = driver.find_elements(By.CSS_SELECTOR, f'datalist#{list_attr} option')
                    return f"Datalist detectado con {len(options)} opciones.", "✔"
                except:
                    return "Datalist declarado pero no accesible.", "⚠"
            return "Sin datalist asociado.", "✔"

        def eventos_input_change():
            input_search.clear()
            input_search.send_keys("evento prueba")
            driver.execute_script("arguments[0].dispatchEvent(new Event('input', { bubbles: true }));", input_search)
            driver.execute_script("arguments[0].dispatchEvent(new Event('change', { bubbles: true }));", input_search)
            return "Eventos input y change disparados.", "✔"


        test("Texto válido", texto_valido)
        test("Campo vacío", vacio)
        test("Solo espacios", solo_espacios)
        test("Uso de comillas", comillas)
        test("Texto largo", largo)
        test("Inyección XSS", xss)
        test("Inyección SQL", sql)
        test("Caracteres especiales", especiales)
        test("Emojis y Unicode", emojis)
        test("Focus y visibilidad", focus_visibilidad)
        test("Atributos comunes y aria", atributos_extra)
        test("Shadow DOM", shadow_dom)
        test("Datalist asociado", datalist)
        test("Eventos input/change", eventos_input_change)

    for idx, input_el in enumerate(inputs):
        identificador = describir_input(input_el, idx + 1)
        probar_input(input_el, identificador)

    print("\n=== RESULTADOS DE PRUEBA DE INPUT TYPE=SEARCH ===\n")
    for r in results:
        print(r)

    return results
