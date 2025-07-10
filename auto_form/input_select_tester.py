from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

# =============================================
# Función principal para probar campos <select>
# =============================================
def run_input_select_tests(driver):
    results = []
    selects = driver.find_elements(By.TAG_NAME, "select")

    def describir_select(el, index):
        name = el.get_attribute("name")
        id_attr = el.get_attribute("id")
        if name:
            return f'Select con name="{name}"'
        elif id_attr:
            return f'Select con id="{id_attr}"'
        else:
            return f'Select[{index}] sin identificador'

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
            return ("XSS sin sanitizar.", "❗") if "<script>" in valor else ("XSS bloqueado.", "✔")

        def visibilidad_y_estado():
            visible = el.is_displayed()
            enabled = el.is_enabled()
            return f"Visible: {visible}, Enabled: {enabled}", "✔" if visible and enabled else "⚠"

        def atributos_extra():
            datos = {
                "autocomplete": el.get_attribute("autocomplete"),
                "required": el.get_attribute("required"),
                "multiple": el.get_attribute("multiple"),
                "aria-label": el.get_attribute("aria-label"),
                "aria-required": el.get_attribute("aria-required"),
            }
            return f"Atributos detectados: {datos}", "✔"

        test("Opción por defecto", opcion_por_defecto)
        test("Seleccionar cada opción válida", seleccionar_todas)
        test("Valor inválido por manipulación", valor_invalido)
        test("Inyección XSS", xss)
        test("Visibilidad y estado", visibilidad_y_estado)
        test("Atributos comunes", atributos_extra)

    for idx, sel in enumerate(selects):
        identificador = describir_select(sel, idx + 1)
        probar_select(sel, identificador)

    print("\n=== RESULTADOS DE PRUEBA DE CAMPOS <SELECT> ===\n")
    for r in results:
        print(r)

    return results
