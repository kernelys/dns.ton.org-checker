from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from threading import Thread
import time
import random

def presearch(driver):
    driver.get("https://dns.ton.org")

    input_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "startInputElement"))
    )
    
    input_field.send_keys("bobaboboboboaobob")
    input_field.send_keys(Keys.ENTER)
    time.sleep(1)
    
def dns_is_valid(driver, domain_name):
    url = f"https://dns.ton.org/#{domain_name}"
    driver.get(url)
    time.sleep(2)

    try:
        domain_status_span = WebDriverWait(driver, 15).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "#domainStatus span"))
        )

        span_text = domain_status_span.text.strip()

        if span_text:
            if "свободен" in span_text.lower():
                print(f"Домен '{domain_name}' свободен")
                return True
            else:
                print(f"Домен '{domain_name}' занят")
    except:
        pass

def worker(domains, free_domains):
    driver = webdriver.Chrome() 
    
    presearch(driver=driver)
    
    for domain in domains:
        if '.ton' in domain:
            domain = domain.replace('.ton', '')
            
        if dns_is_valid(driver=driver, domain_name=domain):
            free_domains.add(f"{domain}.ton")
            
    driver.quit()

def write_results(data):
    name = "result" + str(random.randint(10000, 100000)) + ".txt"  # Добавляем расширение .txt
    try:
        with open(name, 'w') as f:

            f.write("\n".join(data))
    except Exception as e:
        print(e)
   
if __name__ == "__main__":
    with open("domains.txt", "r") as f:
        domains_to_check = (f.read()).split("\n")
        
    free_domains = set()
    
    threads = []
    batch_size = 100
    
    for i in range(0, len(domains_to_check), batch_size):
        batch = domains_to_check[i:i + batch_size]
        thread = Thread(target=worker, args=(batch, free_domains))
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()
        
    write_results(data=free_domains)