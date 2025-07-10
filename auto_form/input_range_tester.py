from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

def run_input_text_tests(driver):
    results = []
    inputs = driver.find_elements(By.CSS_SELECTOR, 'input[type="text"]')

    def describir_input(el, index):
        ph = el.get_attribute("placeholder")
        name = el.get_attribute("name")
        id_attr = el.get_attribute("id")
        if ph: return f'Input text con placeholder "{ph}"'
        elif name: return f'Input text con name="{name}"'
        elif id_attr: return f'Input text con id="{id_attr}"'
        else: return f'Input text[{index}] sin identificador'

    def probar_input(input_el, identificador):

        def test(nombre, funcion):
            try:
                mensaje, estado = funcion()
                results.append(f"[{estado}] {identificador} - {nombre}: {mensaje}")
            except Exception as e:
                results.append(f"[❌] {identificador} - {nombre}: Error durante la prueba: {str(e)}")

        def valor_valido():
            input_el.clear()
            input_el.send_keys("Texto de prueba")
            return ("Texto aceptado correctamente." if input_el.get_attribute("value") == "Texto de prueba" else "Texto no aceptado.", "✔")

        def caracteres_especiales():
            input_el.clear()
            input_el.send_keys("@#$%^&*()")
            return ("Especiales aceptados." if input_el.get_attribute("value") == "@#$%^&*()" else "Especiales rechazados.", "✔")

        def texto_largo():
            largo = "x" * 1000
            input_el.clear()
            input_el.send_keys(largo)
            val = input_el.get_attribute("value")
            if len(val) == len(largo): return "Texto largo aceptado.", "✔"
            elif len(val) > 0: return f"Texto recortado: {len(val)}", "⚠"
            return "Texto largo rechazado.", "❌"

        def xss():
            input_el.clear()
            payload = "<script>alert(1)</script>"
            input_el.send_keys(payload)
            val = input_el.get_attribute("value")
            return ("XSS no bloqueado." if "<" in val else "XSS bloqueado.", "❗" if "<" in val else "✔")

        def sql():
            input_el.clear()
            payload = "' OR '1'='1"
            input_el.send_keys(payload)
            val = input_el.get_attribute("value")
            return ("SQL Injection posible." if "1" in val else "Bloqueado.", "❗" if "1" in val else "✔")

        def solo_espacios():
            input_el.clear()
            input_el.send_keys("   ")
            val = input_el.get_attribute("value")
            return ("Espacios vacíos aceptados." if val.strip() == "" else "Espacios procesados.", "⚠")

        def eventos_dom():
            input_el.clear()
            driver.execute_script("arguments[0].addEventListener('input', () => arguments[0].setAttribute('data-test', 'ok'))", input_el)
            input_el.send_keys("trigger")
            val = input_el.get_attribute("data-test")
            return ("Evento DOM ejecutado." if val == "ok" else "Evento no disparado.", "✔" if val == "ok" else "❌")

        def teclado_tab():
            input_el.clear()
            input_el.send_keys(Keys.TAB)
            return ("Tecla TAB enviada sin error.", "✔")

        def interaccion_movil():
            ActionChains(driver).move_to_element(input_el).click().perform()
            input_el.send_keys("tap_test")
            val = input_el.get_attribute("value")
            return ("Tap móvil simulado con éxito." if "tap_test" in val else "No se simuló el tap.", "✔" if "tap_test" in val else "❌")

        test("Texto válido", valor_valido)
        test("Caracteres especiales", caracteres_especiales)
        test("Texto largo", texto_largo)
        test("Inyección XSS", xss)
        test("Inyección SQL", sql)
        test("Solo espacios", solo_espacios)
        test("Evento input DOM", eventos_dom)
        test("Simulación teclado (TAB)", teclado_tab)
        test("Simulación táctil móvil", interaccion_movil)

    for idx, input_el in enumerate(inputs):
        identificador = describir_input(input_el, idx + 1)
        probar_input(input_el, identificador)

    return results
