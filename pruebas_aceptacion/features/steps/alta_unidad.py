from behave import when, given, then
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from time import sleep


@given(u'ingreso a la plataforma en la url "{url}"')
def step_impl(context, url):
    context.driver = webdriver.Chrome()
    context.driver.get(url)


@given(u'doy click al menú Unidades, luego click en el submenú Nueva')
def step_impl(context):
    context.driver.find_element(By.PARTIAL_LINK_TEXT, 'Unidades').click()
    sleep(0.5)
    context.driver.find_element(By.PARTIAL_LINK_TEXT, 'Nueva').click()
    sleep(0.5)


@given(u'registró la unidad "{nombre}" y su abreviación "{abreviacion}"')
def step_impl(context, nombre, abreviacion):
    context.driver.find_element(By.NAME, 'nombre').send_keys(nombre)
    context.driver.find_element(By.NAME, 'abreviacion').send_keys(abreviacion)


@when(u'presiono el botón Agregar')
def step_impl(context):
    context.driver.find_element(By.ID, 'btnAgregar').click()


@then(u'puedo ver la unidad "{unidad}" en la lista de unidades.')
def step_impl(context, unidad):
    tbody = context.driver.find_element(By.TAG_NAME, 'tbody')
    unidades = []
    for tr in tbody.find_elements(By.TAG_NAME, 'tr'):
        td = tr.find_elements(By.TAG_NAME, 'td')
        unidades.append(td[0].text)
    assert unidad in unidades, \
        f"La unidad {unidad} no se encuentra en las unidades {str(unidades)}"
