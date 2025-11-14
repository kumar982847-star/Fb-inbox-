import streamlit as st
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

st.title("Facebook Auto Message Tool")

chat_id = st.text_input("Chat/Conversation ID")
hatersname = st.text_input("Hatersname")
delay = st.number_input("Delay (seconds)", min_value=5, max_value=600, value=30)
cookies = st.text_area("Facebook Cookies (optional)")
messages_text = st.text_area("Messages (one per line)")

if st.button("Start Automation"):
    if chat_id and messages_text:
        driver = webdriver.Chrome()  # ChromeDriver path सेट करें अगर ज़रूरी हो
        driver.get("https://www.facebook.com/messages/t/" + chat_id)
        
        # Facebook में लॉगिन क्रियेटिवली करना होगा या पहले लॉगिन रहना चाहिए
        if cookies:
            # Optional: Cookies डालने का कोड यहाँ लगाएं (Advanced)
            pass
        
        st.write("Automation started...")
        messages = messages_text.strip().split("\n")
        
        for msg in messages:
            try:
                # Message input बॉक्स में मैसेज डालें (XPath वगैरह चेंज हो सकता है)
                time.sleep(5)
                message_box = driver.find_element(By.XPATH, "//div[@aria-label='Message']")
                message_box.click()
                message_box.send_keys(msg)
                message_box.send_keys(Keys.RETURN)
                st.write(f"Sent: {msg}")
                time.sleep(delay)
            except Exception as e:
                st.write(f"Error sending message: {e}")
        driver.quit()
        st.write("Automation completed!")
    else:
        st.write("Chat ID और Messages दोनों भरें।")
