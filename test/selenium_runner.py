from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# Move FormBot class to module level (outside the function)
class FormBot:
    def __init__(self, driver, wait_time=10):
        self.driver = driver
        self.wait = WebDriverWait(driver, wait_time)

    def select_dropdown_by_text(self, element_id, visible_text):
        try:
            dropdown = self.wait.until(EC.presence_of_element_located((By.ID, element_id)))
            Select(dropdown).select_by_visible_text(visible_text)
        except Exception as e:
            print(f"❌ خطا در انتخاب '{element_id}': {e}")

    def wait_for_dropdown_options(self, dropdown_id, min_options=2, timeout=5):
        try:
            def options_loaded(driver):
                dropdown = driver.find_element(By.ID, dropdown_id)
                options = dropdown.find_elements(By.TAG_NAME, "option")
                return len(options) >= min_options
            WebDriverWait(self.driver, timeout).until(options_loaded)
        except Exception as e:
            print(f"❌ گزینه‌های '{dropdown_id}' بارگذاری نشدند: {e}")

    def fill_text_field(self, field_id, text):
        try:
            field = self.wait.until(EC.presence_of_element_located((By.ID, field_id)))
            field.clear()
            field.send_keys(text)
        except Exception as e:
            print(f"❌ خطا در پر کردن '{field_id}': {e}")

    def submit_form(self, submit_button_id):
        try:
            button = self.wait.until(EC.element_to_be_clickable((By.ID, submit_button_id)))
            button.click()
        except Exception as e:
            print(f"❌ خطا در ارسال فرم: {e}")

def get_driver():
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-extensions")
    return webdriver.Chrome(options=options)

def run_bot():
    try:
        driver = get_driver()
        driver.get("https://ve.cbi.ir/VC/TasRequestVC.aspx")

        bot = FormBot(driver)

        # استان و شهر محل تولد پدر
        bot.select_dropdown_by_text("ctl00_ContentPlaceHolder1_ddlPBrState", "تهران")
        bot.wait_for_dropdown_options("ctl00_ContentPlaceHolder1_ddlPBrCity")
        bot.select_dropdown_by_text("ctl00_ContentPlaceHolder1_ddlPBrCity", "تهران")

        # شماره ملی پدر
        bot.fill_text_field("ctl00_ContentPlaceHolder1_tbPIDNo", "1234567890")

        # تاریخ تولد پدر
        bot.select_dropdown_by_text("ctl00_ContentPlaceHolder1_ddlPBrDay", "10")
        bot.select_dropdown_by_text("ctl00_ContentPlaceHolder1_ddlPBrMonth", "مهر")
        bot.fill_text_field("ctl00_ContentPlaceHolder1_tbPBrYear", "1365")

        # تاریخ تولد فرزند
        bot.select_dropdown_by_text("ctl00_ContentPlaceHolder1_ddlCBrDay", "15")
        bot.select_dropdown_by_text("ctl00_ContentPlaceHolder1_ddlCBrMonth", "فروردین")
        bot.fill_text_field("ctl00_ContentPlaceHolder1_tbCBrYear", "1395")

        # استان و شهر محل تولد فرزند
        bot.select_dropdown_by_text("ctl00_ContentPlaceHolder1_ddlCBrState", "تهران")
        bot.wait_for_dropdown_options("ctl00_ContentPlaceHolder1_ddlCBrCity")
        bot.select_dropdown_by_text("ctl00_ContentPlaceHolder1_ddlCBrCity", "تهران")

        # تعداد فرزندان (مثلاً "اول")
        bot.select_dropdown_by_text("ctl00_ContentPlaceHolder1_ddlChildNo", "اول")

        # شماره موبایل پدر
        bot.fill_text_field("ctl00_ContentPlaceHolder1_tbMobileNo", "09123456789")

        # کد ملی فرزند
        bot.fill_text_field("ctl00_ContentPlaceHolder1_tbCIDNo", "0081234567")

        # کپچا دستی
        input("✅ کپچا رو داخل مرورگر وارد کن، بعدش Enter بزن تا فرم ارسال بشه...")

        # ارسال فرم اولیه
        bot.submit_form("ctl00_ContentPlaceHolder1_btnSendConfirmCode")

        # وارد کردن کد تأیید تستی (مثلاً 1234)
        bot.fill_text_field("ctl00_ContentPlaceHolder1_tbConfirmCode", "1234")
        bot.submit_form("ctl00_ContentPlaceHolder1_btnConfirmCode")

        # نگه‌داشتن مرورگر برای بررسی نتیجه
        input("✅ فرم ارسال شد. برای بستن مرورگر Enter بزن...")

    except Exception as e:
        print(f"❌ خطا در اجرای ربات: {e}")
    finally:
        if 'driver' in locals():
            driver.quit()

if __name__ == "__main__":
    run_bot()