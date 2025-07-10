from selenium.webdriver.common.by import By

# ========================================
# Función principal para probar numéricos
# ========================================
def run_input_number_tests(driver): # Recibe un driver Selenium ya inicializado
    results = [] # Lista para almacenar los resultados
    inputs = driver.find_elements(By.CSS_SELECTOR, 'input[type="number"]') # Seleccionamos todos los inputs tipo number

    # ========================
    # Identificación del campo
    # ========================
    def describir_input(el, index): # Generamos una descripción legible del input
        ph = el.get_attribute("placeholder")
        name = el.get_attribute("name")
        id_attr = el.get_attribute("id")
        if ph: return f'Input con placeholder "{ph}"'
        elif name: return f'Input con name="{name}"'
        elif id_attr: return f'Input con id="{id_attr}"'
        else: return f'Input[{index}] sin identificador'

    # ======================
    # Pruebas por cada campo
    # ======================
    def probar_input(input_number, identificador):

        def test(nombre, funcion): # Ejecutamos una prueba y almacenamos el resultado
            try:
                mensaje, estado = funcion()
                results.append(f"[{estado}] {identificador} - {nombre}: {mensaje}")
            except Exception as e:
                results.append(f"[\u274c] {identificador} - {nombre}: Error durante la prueba: {str(e)}")

        def numero_valido():
            input_number.clear()
            input_number.send_keys("50")
            valor = input_number.get_attribute("value")
            return ("Acepta número dentro del rango." if valor == "50" else f"Rechaza valor válido: '{valor}'", "✔")

        def limite_inferior():
            input_number.clear()
            input_number.send_keys("0")
            valor = input_number.get_attribute("value")
            return ("Acepta límite inferior." if valor == "0" else f"Rechaza 0: '{valor}'", "✔")

        def limite_superior():
            input_number.clear()
            input_number.send_keys("100")
            valor = input_number.get_attribute("value")
            return ("Acepta límite superior." if valor == "100" else f"Rechaza 100: '{valor}'", "✔")

        def debajo_del_minimo():
            input_number.clear()
            input_number.send_keys("-1")
            valor = input_number.get_attribute("value")
            return ("Permite número menor al mínimo." if valor == "-1" else "Restringe correctamente valores menores", "⚠")

        def encima_del_maximo():
            input_number.clear()
            input_number.send_keys("101")
            valor = input_number.get_attribute("value")
            return ("Permite sobrepasar el máximo." if valor == "101" else "Restringe valores mayores a 100", "⚠")

        def decimal():
            input_number.clear()
            input_number.send_keys("50.5")
            valor = input_number.get_attribute("value")
            return ("Acepta decimal: '50.5'" if valor == "50.5" else f"Decimal modificado: '{valor}'", "✔")

        def letras():
            input_number.clear()
            input_number.send_keys("abc")
            valor = input_number.get_attribute("value")
            return ("Campo ignora letras.", "✔") if valor == "" else (f"Letras aceptadas: '{valor}'", "⚠")

        def especiales():
            input_number.clear()
            input_number.send_keys("@#%$")
            valor = input_number.get_attribute("value")
            return ("Campo ignora caracteres especiales.", "✔") if valor == "" else (f"Acepta especiales: '{valor}'", "⚠")

        def espacios():
            input_number.clear()
            input_number.send_keys("   ")
            valor = input_number.get_attribute("value")
            return ("Campo ignora espacios.", "✔") if valor == "" else (f"Acepta espacios: '{valor}'", "⚠")

        def xss():
            input_number.clear()
            input_number.send_keys("<script>alert(1)</script>")
            valor = input_number.get_attribute("value")
            return ("XSS no inyectado." if "<script" not in valor else "XSS detectado.", "✔")

        def sql():
            input_number.clear()
            input_number.send_keys("1 OR 1=1")
            valor = input_number.get_attribute("value")
            return ("SQL bloqueado correctamente." if "OR" not in valor else "Potencial SQL Injection.", "✔")

        def largo():
            input_number.clear()
            input_number.send_keys("9" * 50)
            valor = input_number.get_attribute("value")
            return ("Acepta número largo." if len(valor) >= 50 else f"Truncado. Largo: {len(valor)}", "⚠")

        test("Número válido", numero_valido)
        test("Límite inferior", limite_inferior)
        test("Límite superior", limite_superior)
        test("Debajo del mínimo", debajo_del_minimo)
        test("Encima del máximo", encima_del_maximo)
        test("Decimal", decimal)
        test("Letras", letras)
        test("Caracteres especiales", especiales)
        test("Espacios en blanco", espacios)
        test("Inyección XSS", xss)
        test("Inyección SQL", sql)
        test("Número largo", largo)

    # ======================
    # Ejecutamos por input
    # ======================
    for idx, input_el in enumerate(inputs):
        identificador = describir_input(input_el, idx + 1)
        probar_input(input_el, identificador)

    return results
