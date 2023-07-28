import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from settings import BASE_URL, EMAIL, PASSWORD, SITE_NAME


@pytest.fixture(scope='class')
def testing_auth_and_my_pets():
    try:
        pytest.driver = webdriver.Chrome()
        pytest.driver.implicitly_wait(10)
        pytest.driver.get(BASE_URL)

        # Кнопка "Зарегистрироваться"
        pytest.driver.find_element(By.CLASS_NAME, 'btn.btn-success').click()
        assert pytest.driver.current_url == f'{BASE_URL}/new_user'

        # Ссылка "У меня уже есть аккаунт"
        pytest.driver.find_element(By.CSS_SELECTOR, 'a[href="/login"]').click()
        assert pytest.driver.current_url == f'{BASE_URL}/login'

        # Поле "Электронная почта"
        pytest.driver.find_element(By.ID, 'email').send_keys(EMAIL)

        # Поле "Пароль"
        pytest.driver.find_element(By.ID, 'pass').send_keys(PASSWORD)

        # Кнопка "Войти"
        pytest.driver.find_element(By.CLASS_NAME, 'btn.btn-success').click()
        assert pytest.driver.current_url == f'{BASE_URL}/all_pets'
        assert pytest.driver.find_element(By.TAG_NAME, 'h1').text == SITE_NAME

        # Ссылка "Мои питомцы"
        WebDriverWait(pytest.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[href="/my_pets"]'))
        )
        pytest.driver.find_element(
            By.CSS_SELECTOR, 'a[href="/my_pets"]'
        ).click()
        assert pytest.driver.current_url == f'{BASE_URL}/my_pets'

        yield

    finally:
        pytest.driver.quit()
