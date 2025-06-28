from selenium.webdriver.common.by import By

# ====================================
# Función principal para probar search
# ====================================
def run_input_search_tests(driver): # Recibimos un driver Selenium ya inicializado
    results = [] # Creamos una lista para almacenar los resultados
    inputs = driver.find_elements(By.CSS_SELECTOR, 'input[type="search"]') # Obtenemos todos los campos tipo search

    # =========================================
    # Función auxiliar para describir un input
    # =========================================
    def describir_input(el, index): # Intentamos identificar el input con algún atributo
        ph = el.get_attribute("placeholder") # Obtenemos el atributo placeholder
        name = el.get_attribute("name") # Obtenemos el atributo name
        id_attr = el.get_attribute("id") # Obtenemos el atributo id

        if ph:
            return f'Input con placeholder "{ph}"'
        elif name:
            return f'Input con name="{name}"'
        elif id_attr:
            return f'Input con id="{id_attr}"'
        else:
            return f'Input[{index}] sin identificador' # Si no tiene ningún atributo útil

    # ==================================
    # Probamos un solo input de búsqueda
    # ==================================
    def probar_input(input_search, identificador): # Ejecutamos todas las pruebas sobre un input

        def test(nombre, funcion): # Ejecutamos una prueba individual
            try:
                mensaje, estado = funcion() # Ejecutamos la función de prueba
                results.append(f"[{estado}] {identificador} - {nombre}: {mensaje}") # Guardamos el resultado
            except Exception as e:
                results.append(f"[❌] {identificador} - {nombre}: Error durante la prueba: {str(e)}") # Capturamos errores

        # =====================
        # Pruebas individuales
        # =====================
        def texto_valido():
            input_search.clear() # Limpiamos el campo
            input_search.send_keys("zapatos nike") # Ingresamos una búsqueda válida
            valor = input_search.get_attribute("value") # Obtenemos el valor actual
            if valor == "zapatos nike":
                return "Texto aceptado correctamente.", "✔"
            else:
                return f"Texto no aceptado. Valor: '{valor}'", "✘"

        def vacio():
            input_search.clear() # Limpiamos el campo
            valor = input_search.get_attribute("value") # Obtenemos el valor actual
            if valor == "":
                return "Campo vacío permitido.", "⚠"
            else:
                return f"No se vació correctamente: '{valor}'", "✘"

        def solo_espacios():
            input_search.clear() # Limpiamos el campo
            input_search.send_keys("     ") # Ingresamos espacios
            valor = input_search.get_attribute("value") # Obtenemos el valor actual
            if valor.strip() == "":
                return "Campo acepta solo espacios. Validamos limpieza.", "⚠"
            return f"Contiene caracteres tras limpiar: '{valor}'", "⚠"

        def comillas():
            input_search.clear() # Limpiamos el campo
            input_search.send_keys('"zapatos"') # Ingresamos comillas
            valor = input_search.get_attribute("value") # Obtenemos el valor actual
            return f"Comillas aceptadas: '{valor}'", "✔"

        def largo():
            input_search.clear() # Limpiamos el campo
            texto = "producto" * 200 # Generamos un texto muy largo
            input_search.send_keys(texto) # Lo enviamos al campo
            valor = input_search.get_attribute("value") # Obtenemos el valor actual
            if len(valor) >= len(texto):
                return "Campo aceptó búsqueda larga.", "✔"
            elif 0 < len(valor) < len(texto):
                return f"Texto recortado. Largo final: {len(valor)}", "⚠"
            else:
                return "Texto largo rechazado.", "✘"

        def xss():
            input_search.clear() # Limpiamos el campo
            payload = '<script>alert(1)</script>' # Payload XSS
            input_search.send_keys(payload) # Lo enviamos al campo
            valor = input_search.get_attribute("value") # Obtenemos el valor actual
            if payload in valor:
                return "XSS sin sanitizar.", "❗"
            else:
                return "XSS bloqueado o modificado.", "✔"

        def sql():
            input_search.clear() # Limpiamos el campo
            payload = "' OR '1'='1" # Payload SQL
            input_search.send_keys(payload) # Lo enviamos al campo
            valor = input_search.get_attribute("value") # Obtenemos el valor actual
            if payload in valor:
                return "SQL Injection posible.", "❗"
            else:
                return "SQL Injection bloqueado.", "✔"

        def especiales():
            input_search.clear() # Limpiamos el campo
            input_search.send_keys("!@#$%^&*()") # Ingresamos caracteres especiales
            valor = input_search.get_attribute("value") # Obtenemos el valor actual
            return f"Especiales aceptados: '{valor}'", "✔"

        def emojis():
            input_search.clear() # Limpiamos el campo
            input_search.send_keys("🍕 búsqueda ❤️") # Ingresamos emojis
            valor = input_search.get_attribute("value") # Obtenemos el valor actual
            return f"Unicode/emojis aceptados: '{valor}'", "✔"

        # ==========================
        # Ejecutamos todas las pruebas
        # ==========================
        test("Texto válido", texto_valido)
        test("Campo vacío", vacio)
        test("Solo espacios", solo_espacios)
        test("Uso de comillas", comillas)
        test("Texto largo", largo)
        test("Inyección XSS", xss)
        test("Inyección SQL", sql)
        test("Caracteres especiales", especiales)
        test("Emojis y Unicode", emojis)

    # ===============================
    # Aplicamos pruebas a cada input
    # ===============================
    for idx, input_el in enumerate(inputs): # Recorremos todos los inputs encontrados
        identificador = describir_input(input_el, idx + 1) # Generamos una descripción
        probar_input(input_el, identificador) # Ejecutamos las pruebas

    return results # Devolvemos los resultados finales
