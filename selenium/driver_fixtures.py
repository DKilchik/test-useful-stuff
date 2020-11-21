import pytest, allure
from selenium import webdriver


"""
    Example of attaching screenshot to allure report after test failed

"""


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    # This function helps to detect that some test failed
    # and pass this information to teardown:

    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)
    return rep


@pytest.fixture
def browser(request):
    browser = webdriver.Chrome()
    yield browser
    if request.node.rep_call.failed:
        try:
            # Attach screenshot to Allure report:
            allure.attach(browser.get_screenshot_as_png(),
                          name=request.function.__name__,
                          attachment_type=allure.attachment_type.PNG)
        finally:
            browser.quit()
    browser.quit()


####################################################################################################################
