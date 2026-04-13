from playwright.sync_api import sync_playwright



def analyze_competitors(query):
    parm = query.replace(" ", "%20")
    url = f"https://cse.google.com/cse?cx=50b4bd2ad493b4b0f#gsc.tab=0&gsc.q={parm}&gsc.sort="

    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.goto(url)
        page.wait_for_selector('.gsc-webResult', timeout=15000)

        # Evaluate JavaScript directly in the browser context
        results = page.evaluate("""
        () => {
            const data = [];
            document.querySelectorAll('.gsc-webResult').forEach(r => {
                const titleEl = r.querySelector('.gs-title');
                const descEl = r.querySelector('.gs-snippet');
                const title = titleEl ? titleEl.innerText.trim() : "No title";
                const link = titleEl && titleEl.querySelector('a') ? titleEl.querySelector('a').href : null;
                const desc = descEl ? descEl.innerText.trim() : "No description";
                data.push({title, link, desc});
            });
            return data;
        }
        """)

        res = {
            "compatiotors":
            [
                {
                    "title": r["title"],
                    "link": r["link"],
                    "desc": r["desc"]
                }
                for r in results
            ]
        }


        

        browser.close()

    return res
