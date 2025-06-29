from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

# =============================================
# Función principal para probar campos <select>
# =============================================
def run_input_select_tests(driver): # Recibimos un driver Selenium ya inicializado
    results = [] # Lista para almacenar resultados
    selects = driver.find_elements(By.TAG_NAME, "select") # Capturamos todos los select

    # ================================
    # Función para describir el select
    # ================================
    def describir_select(el, index):
        name = el.get_attribute("name")
        id_attr = el.get_attribute("id")
        if name: return f'Select con name="{name}"'
        elif id_attr: return f'Select con id="{id_attr}"'
        else: return f'Select[{index}] sin identificador'

    # ===========================
    # Probar un solo campo select
    # ===========================
    def probar_select(el, identificador):
        def test(nombre, funcion):
            try:
                mensaje, estado = funcion()
                results.append(f"[{estado}] {identificador} - {nombre}: {mensaje}")
            except Exception as e:
                results.append(f"[❌] {identificador} - {nombre}: Error durante la prueba: {str(e)}")

        sel = Select(el)

        def opcion_por_defecto():
            valor = el.get_attribute("value")
            return ("Sin opción seleccionada por defecto." if valor == "" else f"Opción inicial: '{valor}'", "✔")

        def seleccionar_todas():
            mensajes = []
            for opt in sel.options:
                val = opt.get_attribute("value")
                sel.select_by_value(val)
                actual = el.get_attribute("value")
                mensajes.append(f"{val} → OK" if actual == val else f"{val} → Falla")
            return ("; ".join(mensajes), "✔")

        def valor_invalido():
            driver.execute_script("arguments[0].value = 'invalido'", el)
            valor = el.get_attribute("value")
            if valor == "invalido":
                return "Valor inválido aceptado por manipulación.", "❗"
            else:
                return "Valor inválido rechazado.", "✔"

        def xss():
            driver.execute_script("arguments[0].innerHTML += '<option value=\"<script>alert(1)</script>\">XSS</option>'", el)
            sel.select_by_value("<script>alert(1)</script>")
            valor = el.get_attribute("value")
            if "<script>" in valor:
                return "XSS sin sanitizar.", "❗"
            return "XSS bloqueado.", "✔"

        test("Opción por defecto", opcion_por_defecto)
        test("Seleccionar cada opción válida", seleccionar_todas)
        test("Valor inválido por manipulación", valor_invalido)
        test("Inyección XSS", xss)

    # ===============================
    # Ejecutamos pruebas a cada select
    # ===============================
    for idx, sel in enumerate(selects):
        identificador = describir_select(sel, idx + 1)
        probar_select(sel, identificador)

    return results
