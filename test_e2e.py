import pytest

try:
    from playwright.sync_api import Page, expect
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False
    Page = None

pytestmark = pytest.mark.skipif(
    not PLAYWRIGHT_AVAILABLE,
    reason="Playwright nicht installiert"
)


class TestTodoAppE2E:
    
    BASE_URL = "http://localhost:8501" # Streamlit Standardport
    
    @pytest.fixture(scope="class")
    def setup_app(self):
        import urllib.request
        try:
            urllib.request.urlopen(self.BASE_URL, timeout=2)
        except:
            pytest.skip("Streamlit-Server nicht erreichbar")
        yield
    
    # 1. Grundlegender Seitenlade-Test
    def test_1_page_loads(self, page: Page, setup_app):
        page.goto(self.BASE_URL)
        page.wait_for_load_state("networkidle")
        assert page.url == self.BASE_URL + "/"
    
    # 2. Titelprüfung
    def test_3_has_input_field(self, page: Page, setup_app):
        page.goto(self.BASE_URL)
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(1000)
        inputs = page.locator('input[type="text"]')
        assert inputs.count() > 0
    
    # 3. Task-Erstellungs-Test
    def test_5_page_responsive(self, page: Page, setup_app):
        page.goto(self.BASE_URL)
        page.wait_for_load_state("networkidle")
        page.set_viewport_size({"width": 375, "height": 667})
        page.wait_for_timeout(500)
        assert page.url == self.BASE_URL + "/"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
