from selenium.webdriver.common.by import By # Para seleccionar elementos del DOM por tipo
from selenium.webdriver.common.keys import Keys # Para simular pulsaciones de teclado

# ===================================
# Función principal para probar texto
# ===================================
def run_input_text_tests(driver): # Recibimos un driver Selenium ya inicializado
    results = [] # Creamos una lista para almacenar los resultados
    inputs = driver.find_elements(By.CSS_SELECTOR, 'input[type="text"]') # Obtenemos todos los campos tipo texto

    # =========================================
    # Función auxiliar para describir un input
    # =========================================
    def describir_input(el, index): # Intentamos identificar el input con algún atributo
        ph = el.get_attribute("placeholder") # Obtenemos el atributo placeholder
        name = el.get_attribute("name") # Obtenemos el atributo name
        id_attr = el.get_attribute("id") # Obtenemos el atributo id
        if ph: return f'Input con placeholder "{ph}"'
        elif name: return f'Input con name="{name}"'
        elif id_attr: return f'Input con id="{id_attr}"'
        else: return f'Input[{index}] sin identificador' # Si no tiene ningún atributo útil

    # ================================
    # Probamos un solo input de texto
    # ================================
    def probar_input(input_text, identificador): # Ejecutamos todas las pruebas sobre un input

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
            input_text.clear() # Limpiamos el campo
            input_text.send_keys("Texto válido") # Ingresamos un texto simple
            valor = input_text.get_attribute("value") # Obtenemos el valor actual
            if valor == "Texto válido": return "Texto aceptado correctamente.", "✔"
            else: return f"Texto no aceptado. Valor: '{valor}'", "✘"

        def vacio():
            input_text.clear() # Limpiamos el campo
            valor = input_text.get_attribute("value") # Verificamos si quedó vacío
            requerido = input_text.get_attribute("required") # Revisamos si el campo es obligatorio
            if valor == "" and requerido: return "Campo requerido pero se permitió vacío.", "✘"
            elif valor == "": return "Campo vacío permitido.", "⚠"
            else: return f"No se vació correctamente: '{valor}'", "✘"

        def espacios():
            input_text.clear() # Limpiamos el campo
            input_text.send_keys("     ") # Ingresamos solo espacios
            valor = input_text.get_attribute("value") # Obtenemos el valor ingresado
            if valor.strip() == "": return "Campo acepta solo espacios. Validamos limpieza.", "⚠"
            return f"Contiene caracteres tras limpiar espacios: '{valor}'", "⚠"

        def especiales():
            input_text.clear() # Limpiamos el campo
            input_text.send_keys("@#$%^&*()") # Ingresamos caracteres especiales
            valor = input_text.get_attribute("value") # Obtenemos el valor ingresado
            return f"Especiales aceptados: '{valor}'", "✔"

        def xss():
            input_text.clear() # Limpiamos el campo
            payload = '<script>alert(1)</script>' # Preparamos un payload XSS
            input_text.send_keys(payload) # Ingresamos el payload
            valor = input_text.get_attribute("value") # Obtenemos el valor ingresado
            if payload in valor: return "XSS sin sanitizar.", "❗"
            else: return "XSS bloqueado o modificado.", "✔"

        def sql():
            input_text.clear() # Limpiamos el campo
            payload = "' OR '1'='1" # Preparamos una inyección SQL
            input_text.send_keys(payload) # Ingresamos el payload
            valor = input_text.get_attribute("value") # Obtenemos el valor ingresado
            if payload in valor: return "SQL Injection posible.", "❗"
            else: return "SQL Injection bloqueado.", "✔"

        def largo():
            input_text.clear() # Limpiamos el campo
            texto = "A" * 1000 # Preparamos un texto largo
            input_text.send_keys(texto) # Ingresamos el texto largo
            valor = input_text.get_attribute("value") # Obtenemos el valor ingresado
            maxlength = input_text.get_attribute("maxlength") # Revisamos si hay límite de longitud
            if maxlength and len(valor) > int(maxlength): return f"Texto excede maxlength ({maxlength}).", "✘"
            if len(valor) >= 1000: return "Campo aceptó texto largo.", "✔"
            elif 0 < len(valor) < 1000: return f"Texto recortado. Largo final: {len(valor)}", "⚠"
            else: return "Texto largo rechazado.", "✘"

        # ==========================
        # Ejecutamos todas las pruebas
        # ==========================
        test("Texto válido", texto_valido)
        test("Campo vacío", vacio)
        test("Solo espacios", espacios)
        test("Caracteres especiales", especiales)
        test("Inyección XSS", xss)
        test("Inyección SQL", sql)
        test("Texto largo", largo)

    # ===============================
    # Aplicamos pruebas a cada input
    # ===============================
    for idx, input_el in enumerate(inputs): # Recorremos todos los inputs encontrados
        identificador = describir_input(input_el, idx + 1) # Generamos una descripción
        probar_input(input_el, identificador) # Ejecutamos las pruebas

    return results # Devolvemos los resultados finales
