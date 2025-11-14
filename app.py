import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

st.title("Facebook Auto Message Tool (Fully Fixed Version)")

chat_id = st.text_input("Chat / Conversation ID")
delay = st.number_input("Delay (seconds)", min_value=5, max_value=600, value=30)
cookies_text = st.text_area("Facebook Cookies (optional)")
messages_text = st.text_area("Messages (one per line)")


def add_cookies(driver, cookies_raw):
    try:
        cookies_list = cookies_raw.split(";")
        for c in cookies_list:
            if "=" in c:
                name, value = c.split("=", 1)
                driver.add_cookie({"name": name.strip(), "value": value.strip()})
        return True
    except:
        return False


if st.button("Start Automation"):
    if not chat_id or not messages_text:
        st.error("Chat ID aur Messages dono enter karo.")
        st.stop()

    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")       # IMPORTANT FIX
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")

    driver = webdriver.Chrome(options=chrome_options)

    # Step 1: Open FB Home
    driver.get("https://www.facebook.com")

    # Step 2: Add cookies if user provided
    if cookies_text.strip():
        add_cookies(driver, cookies_text)
        driver.get("https://www.facebook.com/messages/t/" + chat_id)
    else:
        st.warning("Cookies nahi diye → login page open hoga. Message nahi jaayega.")

    st.write("Automation started...")

    messages = messages_text.strip().split("\n")

    # ALL POSSIBLE XPATH SELECTORS
    possible_xpaths = [
        "//p[@data-lexical-text='true']",
        "//div[@role='textbox']",
        "//*[@contenteditable='true']",
        "//div[contains(@aria-label,'Message')]"
    ]

    for msg in messages:
        try:
            msg_box = None

            # TRY ALL XPATHS
            for xp in possible_xpaths:
                try:
                    msg_box = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, xp))
                    )
                    break
                except:
                    pass

            if not msg_box:
                st.error("Message box nahi mil raha. Cookies ya chat ID galat ho sakti hai.")
                continue

            msg_box.click()
            time.sleep(1)
            msg_box.send_keys(msg)
            msg_box.send_keys(Keys.RETURN)

            st.write(f"Sent: {msg}")
            time.sleep(delay)

        except Exception as e:
            st.error(f"Error sending message: {e}")

    driver.quit()
    st.success("Automation completed!")
