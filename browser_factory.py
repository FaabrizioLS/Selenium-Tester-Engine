from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.firefox.service import Service as FirefoxService

def crear_driver(navegador: str):
    navegador = navegador.lower()
    driver = None

    if navegador == "chrome":
        options = ChromeOptions()
        options.add_argument("--headless")
        service = ChromeService(executable_path="C:/WebDriver/chromedriver.exe")
        driver = webdriver.Chrome(service=service, options=options)

    elif navegador == "edge":
        options = EdgeOptions()
        options.add_argument("--headless")
        service = EdgeService(executable_path="C:/WebDriver/msedgedriver.exe")
        driver = webdriver.Edge(service=service, options=options)

    elif navegador == "brave":
        options = ChromeOptions()
        options.binary_location = "C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe"
        options.add_argument("--headless")
        service = ChromeService(executable_path="C:/WebDriver/chromedriver.exe")
        driver = webdriver.Chrome(service=service, options=options)

    elif navegador == "vivaldi":
        options = ChromeOptions()
        options.binary_location = "C:/Program Files/Vivaldi/Application/vivaldi.exe"
        options.add_argument("--headless")
        service = ChromeService(executable_path="C:/WebDriver/chromedriver.exe")
        driver = webdriver.Chrome(service=service, options=options)

    else:  
        options = FirefoxOptions()
        options.add_argument("--headless")
        service = FirefoxService(executable_path="C:/WebDriver/geckodriver.exe")
        driver = webdriver.Firefox(service=service, options=options)

    return driver
