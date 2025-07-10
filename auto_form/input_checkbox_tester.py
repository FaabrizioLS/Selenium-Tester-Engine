from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

def run_input_checkbox_tests(driver):
    results = []

    def get_checkbox(index):
        return driver.find_elements(By.CSS_SELECTOR, 'input[type="checkbox"]')[index]

    def describir_input(index):
        try:
            el = get_checkbox(index)  
            label = driver.execute_script("return arguments[0].nextSibling?.textContent", el)
            name = el.get_attribute("name")
            id_attr = el.get_attribute("id")
            if label and label.strip():
                return f'Checkbox con texto "{label.strip()}"'
            elif name:
                return f'Checkbox con name="{name}"'
            elif id_attr:
                return f'Checkbox con id="{id_attr}"'
            else:
                return f'Checkbox[{index + 1}] sin identificador'
        except Exception as e:
            return f'Checkbox[{index + 1}] (descripción no disponible): {str(e)}'

    def probar_checkbox(index):
        def test(nombre, funcion):
            try:
                mensaje, estado = funcion()
                identificador = describir_input(index)  # <- MOVER AQUÍ, SEGURO Y ACTUAL
                results.append(f"[{estado}] {identificador} - {nombre}: {mensaje}")
            except Exception as e:
                identificador = f'Checkbox[{index + 1}]'
                results.append(f"[❌] {identificador} - {nombre}: Error: {str(e)}")

        def estado_por_defecto():
            el = get_checkbox(index)
            return ("No está marcado por defecto.", "✔") if not el.is_selected() else ("Marcado por defecto.", "⚠")

        def marcar_y_verificar():
            el = get_checkbox(index)
            if not el.is_selected():
                try:
                    el.click()
                    time.sleep(0.2)
                except:
                    driver.execute_script("arguments[0].click();", el)
            el = get_checkbox(index)
            return ("Marcado correctamente.", "✔") if el.is_selected() else ("No se pudo marcar.", "❌")

        def desmarcar_y_verificar():
            el = get_checkbox(index)
            if el.is_selected():
                try:
                    el.click()
                    time.sleep(0.2)
                except:
                    driver.execute_script("arguments[0].click();", el)
            el = get_checkbox(index)
            return ("Desmarcado correctamente.", "✔") if not el.is_selected() else ("No se pudo desmarcar.", "❌")

        def accesibilidad_tab():
            el = get_checkbox(index)
            el.send_keys(Keys.TAB)
            return ("Accesible por TAB.", "✔")

        def manipulacion_js():
            el = get_checkbox(index)
            driver.execute_script("arguments[0].checked = true;", el)
            time.sleep(0.2)
            el = get_checkbox(index)
            return ("Fue manipulado por JS.", "⚠") if el.is_selected() else ("Resiste JS.", "✔")

        # Ejecutar cada test
        test("Estado por defecto", estado_por_defecto)
        test("Marcar checkbox", marcar_y_verificar)
        test("Desmarcar checkbox", desmarcar_y_verificar)
        test("Accesibilidad (TAB)", accesibilidad_tab)
        test("Manipulación por JavaScript", manipulacion_js)

    total = len(driver.find_elements(By.CSS_SELECTOR, 'input[type="checkbox"]'))
    for idx in range(total):
        probar_checkbox(idx)
        time.sleep(0.3)

    return results
