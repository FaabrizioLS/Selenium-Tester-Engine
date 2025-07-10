from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def run_input_radio_tests(driver, timeout=10):
    results = []
    wait = WebDriverWait(driver, timeout)

    # Nombres únicos de grupo (agrupados por name)
    def obtener_nombres_grupos():
        radios = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'input[type="radio"]')))
        return list({r.get_attribute("name") for r in radios if r.get_attribute("name")})

    # Obtener radios actuales del grupo (fresh cada vez)
    def radios_de_grupo(name):
        return driver.find_elements(By.CSS_SELECTOR, f'input[type="radio"][name="{name}"]')

    nombres_grupos = obtener_nombres_grupos()

    for nombre in nombres_grupos:

        def test(nombre_prueba, funcion):
            try:
                mensaje, estado = funcion()
                results.append(f"[{estado}] Grupo radio '{nombre}' - {nombre_prueba}: {mensaje}")
            except Exception as e:
                results.append(f"[❌] Grupo radio '{nombre}' - {nombre_prueba}: Error en prueba: {str(e)}")

        def seleccion_unica():
            radios = radios_de_grupo(nombre)
            seleccionados = []
            for r in radios:
                driver.execute_script("arguments[0].click()", r)
                if r.is_selected():
                    seleccionados.append(r)
            return (
                "Solo una opción seleccionada." if len(seleccionados) == 1 else f"{len(seleccionados)} radios quedaron seleccionados.",
                "✔" if len(seleccionados) == 1 else "❌"
            )

        def cambio_de_seleccion():
            radios = radios_de_grupo(nombre)
            if len(radios) < 2:
                return ("No hay suficientes radios para probar cambio de selección.", "⚠")
            driver.execute_script("arguments[0].click()", radios[0])
            driver.execute_script("arguments[0].click()", radios[1])
            radios_refreshed = radios_de_grupo(nombre)
            actualizado = radios_refreshed[1].is_selected() and not radios_refreshed[0].is_selected()
            return (
                "Cambio de selección funcional." if actualizado else "No se reflejó el cambio.",
                "✔" if actualizado else "❌"
            )

        def sin_seleccion_inicial():
            radios = radios_de_grupo(nombre)
            seleccionados = [r for r in radios if r.is_selected()]
            return (
                "Ninguno está seleccionado por defecto." if not seleccionados else f"{len(seleccionados)} ya seleccionados.",
                "⚠" if seleccionados else "✔"
            )

        def value_correcto():
            radios = radios_de_grupo(nombre)
            for r in radios:
                if not r.get_attribute("value"):
                    return ("Falta atributo 'value' en un radio.", "❌")
            return ("Todos los radios tienen valor asignado.", "✔")

        def prueba_teclado():
            radios = radios_de_grupo(nombre)
            if not radios:
                return ("No hay radios disponibles.", "❌")
            try:
                radios[0].send_keys(" ")  # Simula pulsar espacio
                return ("Responde a entrada por teclado (espacio).", "✔")
            except:
                return ("No responde a navegación por teclado.", "❌")

        test("Selección única", seleccion_unica)
        test("Cambio de selección", cambio_de_seleccion)
        test("Sin selección inicial", sin_seleccion_inicial)
        test("Validación de 'value'", value_correcto)
        test("Navegación con teclado", prueba_teclado)

    return results
