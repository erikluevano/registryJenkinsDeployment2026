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
    xpath = '//*[@id="login-form"]/div[3]/input'
    context.driver.find_element(By.XPATH, xpath).click()


@then(u'puedo ver el mensaje "{mensaje}"')
def step_impl(context, mensaje):
    div_mensaje = context.driver.find_element(By.ID, 'user-tools')
    assert mensaje in div_mensaje.text, \
        f"El mensaje {mensaje} no se encuentra en {div_mensaje.text}"


@then(u'puedo ver el mensaje de error "{mensaje}"')
def step_impl(context, mensaje):
    div_mensaje = context.driver.find_element(By.CLASS_NAME, 'errornote')
    assert mensaje in div_mensaje.text, \
        f"El mensaje {mensaje} no se encuentra en {div_mensaje.text}"
