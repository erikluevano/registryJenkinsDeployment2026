from behave import given, when, then
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from time import sleep


@given(u'doy click al menu Programas, lugo click en el sub menu Nuevo')
def step_impl(context):
    sleep(2)
    context.driver.find_element(By.PARTIAL_LINK_TEXT, 'Programas').click()
    sleep(0.5)
    context.driver.find_element(By.PARTIAL_LINK_TEXT, 'Nuevo').click()


@given(u'registro el programa "{nombre}" y su abreviacion "{abreviacion}" y su unidad "{unidad}"')
def step_impl(context, nombre, abreviacion, unidad):
    sleep(1)
    context.driver.find_element(By.NAME, 'nombre').send_keys(nombre)
    context.driver.find_element(By.NAME, 'abreviacion').send_keys(abreviacion)
    context.driver.find_element(By.NAME, 'unidad_academica').send_keys(unidad)


@when(u'presione el boton Agregar del formulario')
def step_impl(context):
    sleep(1)
    context.driver.find_element(
        By.XPATH, '/html/body/div[1]/div[2]/section/div/div/div[2]/form/button').click()


@then(u'puedo ver el programa "{programa}" en la lista de Programas.')
def step_impl(context, programa):
    sleep(2)
    tbody = context.driver.find_element(By.ID, "tbodyResultados")
    programas = []
    for tr in tbody.find_elements(By.TAG_NAME, 'tr'):
        td = tr.find_elements(By.TAG_NAME, 'td')
        programas.append(td[0].text)

    assert programa in programas, \
        f"El programa '{programa}' no se encuentra en los programas {programas}"
