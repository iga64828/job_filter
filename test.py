import requests
from bs4 import BeautifulSoup
import time
import json

def scrape_job_detail(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    try:
        print(f"\nProcessing URL: {url}")
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        print("Page Title:", soup.title.string.strip() if soup.title else "No Title")

        print("--- Address ---")

        location_blocks = soup.select("div.basic-info__icon--location")

        if len(location_blocks) >= 2:
            address_tag = location_blocks[1].select_one("p.basic-info__address a")
            if address_tag:
                print("地址：", address_tag.text.strip())
                print("Google Maps：", address_tag["href"])
            else:
                print("第二個 location 沒有地址")
        else:
            print("找不到第二個 location")

        update_date = soup.select("div.basic-info__icon--last_updated_at")[0].select_one("p.basic-info__last_updated_at").get_text()[6:].strip()
        if update_date:
            print("最近更新日期：", update_date)

        # Define the sections we are looking for
        sections = {
            "Job Description": "工作內容",
            "Requirements": "條件要求",
            "Bonus Requirements":"加分條件",
            "Salary": "薪資範圍",
            "Remote Type":"遠端型態"
        }
        
        for name, keyword in sections.items():
            print(f"--- Searching for {name} ({keyword}) ---")
            # Look for headers containing the keyword
            # Note: Renamed variable from 'headers' to 'header_tags' to avoid conflict with request headers
            header_tags = soup.find_all(lambda tag: tag.name in ['h1', 'h2', 'h3', 'h4', 'div', 'span'] and keyword in tag.get_text())
            
            if not header_tags:
                print(f"No element found containing text '{keyword}'")
                continue
                
            for h in header_tags:
                # Filter out obvious navigation or unrelated elements if needed
                if len(h.get_text(strip=True)) > 20: # Skip long paragraphs that just happen to contain the word
                    continue
                    
                # Try to find the content following this header
                
                # Check next sibling
                next_sibling = h.find_next_sibling()
                if next_sibling:
                    if (keyword == "薪資範圍") or (keyword == "遠端型態"):
                        print(next_sibling.get_text(strip=True))
                    else: 
                        print(next_sibling.get_text())
                else:
                    print("  No next sibling.")
                    
    except Exception as e:
        print(f"Error scraping {url}: {e}")

def main():
    keywords = ['資料工程師','數據工程師', 'Data Engineer']
    base_url = "https://www.yourator.co"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/512"
    }

    for k in keywords:
        print(f"\n=== Fetching job list for keyword: {k} ===")
        # Using term[]={k} as per original logic
        api_url = f"https://www.yourator.co/api/v4/jobs?sort=most_related&term[]={k}"
        
        try:
            response = requests.get(api_url, headers=headers)
            response.raise_for_status()
            data = response.json()
            
            # The structure based on original code: response.json()['payload']['jobs']
            jobs = data.get('payload', {}).get('jobs', [])
            print(f"Found {len(jobs)} jobs.")
            
            for job in jobs:
                path = job.get('path')
                if path:
                    full_url = base_url + path
                    scrape_job_detail(full_url)
                    time.sleep(1) # Be polite
                else:
                    print(f"Skipping job id {job.get('id', 'unknown')} - No path found")
                    
        except Exception as e:
            print(f"Error fetching API for {k}: {e}")

if __name__ == "__main__":
    main()
