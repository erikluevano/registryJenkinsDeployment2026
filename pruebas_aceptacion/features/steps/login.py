from time import sleep
from behave import when, given, then
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


@given(u'que ingreso a la url: "{url}"')
def step_impl(context, url):
    # context.driver = webdriver.Chrome()
    context.driver.get(url)

@given(u'capturo el usuario: "{username}" y la contraseña "{password}"')
def step_impl(context, username, password):
    context.driver.find_element(By.NAME, 'username').send_keys(username)
    context.driver.find_element(By.NAME, 'password').send_keys(password)


@when(u'presiono el botón Identificarse')
def step_impl(context):
    context.driver.find_element(By.ID, 'btnIngresar').click()

@then(u'puedo ver el mensaje "{mensaje}"')
def step_impl(context, mensaje):
    sleep(1)
    div_mensaje = context.driver.find_element(By.ID, 'bienvenida')
    assert mensaje in div_mensaje.text, \
        f"El mensaje {mensaje} no se encuentra en {div_mensaje.text}"


@then(u'puedo ver el mensaje de error "{mensaje}"')
def step_impl(context, mensaje):
    sleep(1)
    div_mensaje = context.driver.find_element(By.ID, 'divError')
    assert mensaje in div_mensaje.text, \
        f"El mensaje {mensaje} no se encuentra en {div_mensaje.text}"

