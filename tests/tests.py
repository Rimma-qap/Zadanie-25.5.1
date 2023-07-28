import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


@pytest.mark.usefixtures('testing_auth_and_my_pets')
class TestMyPetsPage:
    def get_my_pets_info(self):
        WebDriverWait(pytest.driver, 10).until(
            EC.visibility_of_all_elements_located((By.XPATH, '//tbody/tr'))
        )
        my_pets = pytest.driver.find_elements(By.XPATH, '//tbody/tr')
        my_pets_count = len(my_pets)

        WebDriverWait(pytest.driver, 10).until(
            EC.visibility_of_all_elements_located(
                (By.XPATH, '//tbody/tr/td[1]')
            )
        )
        WebDriverWait(pytest.driver, 10).until(
            EC.visibility_of_all_elements_located(
                (By.XPATH, '//tbody/tr/td[2]')
            )
        )
        WebDriverWait(pytest.driver, 10).until(
            EC.visibility_of_all_elements_located(
                (By.XPATH, '//tbody/tr/td[3]')
            )
        )
        # Имена
        names_my_pets = pytest.driver.find_elements(
            By.XPATH, '//tbody/tr/td[1]'
        )
        # Породы
        species_my_pets = pytest.driver.find_elements(
            By.XPATH, '//tbody/tr/td[2]'
        )
        # Возрасты
        ages_my_pets = pytest.driver.find_elements(
            By.XPATH, '//tbody/tr/td[3]'
        )
        return names_my_pets, species_my_pets, ages_my_pets, my_pets_count

    def test_pets_count(self):
        """Проверяем, что в таблице есть все питомцы пользователя"""

        WebDriverWait(pytest.driver, 10).until(
            EC.visibility_of_element_located(
                (By.XPATH, '//div[@class=".col-sm-4 left"]')
            )
        )
        user_statistics_str = pytest.driver.find_element(
            By.XPATH, '//div[@class=".col-sm-4 left"]'
        ).text
        user_statistics_list = user_statistics_str.split('\n')
        my_pets_count_statistics = None

        for i in user_statistics_list:
            if 'Питомцев' in i:
                my_pets_count_statistics = int(i.split(': ')[1])

        WebDriverWait(pytest.driver, 10).until(
            EC.visibility_of_all_elements_located((By.XPATH, '//tbody/tr'))
        )
        my_pets = pytest.driver.find_elements(By.XPATH, '//tbody/tr')
        my_pets_count_table = len(my_pets)
        assert my_pets_count_statistics == my_pets_count_table

    def test_images(self):
        """Проверяем, что хотя бы у половины питомцев есть фото"""

        WebDriverWait(pytest.driver, 10).until(
            EC.visibility_of_all_elements_located((By.XPATH, '//tbody/tr'))
        )
        my_pets = pytest.driver.find_elements(By.XPATH, '//tbody/tr')
        my_pets_count_table = len(my_pets)

        WebDriverWait(pytest.driver, 10).until(
            EC.presence_of_all_elements_located(
                (By.XPATH, '//tbody/tr/th/img')
            )
        )
        images_my_pets = pytest.driver.find_elements(
            By.XPATH, '//tbody/tr/th/img'
        )
        images_my_pets_count = 0

        for i in range(my_pets_count_table):
            if images_my_pets[i].get_attribute('src') != '':
                images_my_pets_count += 1

        assert images_my_pets_count >= my_pets_count_table / 2

    def test_names_species_ages(self):
        """Проверяем, что у всех питомцев есть имя, возраст и порода"""

        (
            names_my_pets,
            species_my_pets,
            ages_my_pets,
            my_pets_count,
        ) = self.get_my_pets_info()

        for i in range(my_pets_count):
            assert names_my_pets[i].text != ''
            assert species_my_pets[i].text != ''
            assert ages_my_pets[i].text != ''

    def test_names_difference(self):
        """Проверяем, что у всех питомцев разные имена"""

        WebDriverWait(pytest.driver, 10).until(
            EC.visibility_of_all_elements_located(
                (By.XPATH, '//tbody/tr/td[1]')
            )
        )
        # Имена
        names_my_pets = pytest.driver.find_elements(
            By.XPATH, '//tbody/tr/td[1]'
        )
        names_my_pets_list = [name.text for name in names_my_pets]
        names_my_pets_set = set(names_my_pets_list)
        assert len(names_my_pets_list) == len(names_my_pets_set)

    def test_pets_difference(self):
        """Проверяем, что в списке нет повторяющихся питомцев -
        это питомцы, у которых одинаковое имя, порода и возраст"""

        (
            names_my_pets,
            species_my_pets,
            ages_my_pets,
            my_pets_count,
        ) = self.get_my_pets_info()

        my_pets_info_list = []

        for i in range(my_pets_count):
            my_pets_info_list.append(
                {
                    'name': names_my_pets[i].text,
                    'species': species_my_pets[i].text,
                    'age': ages_my_pets[i].text,
                }
            )

        unique_pets_list = [
            dict(t)
            for t in {tuple(info.items()) for info in my_pets_info_list}
        ]
        assert len(unique_pets_list) == my_pets_count
