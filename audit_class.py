import requests
from bs4 import BeautifulSoup
import re, json, os
from urllib.parse import urljoin
from collections import Counter
from datetime import datetime
from nltk.corpus import stopwords
import nltk
from dotenv import load_dotenv

load_dotenv()
nltk.download('stopwords', quiet=True)

from dachecker import get_domain_metrics
from googlesearch import analyze_competitors


class Audit:
    def __init__(self, url):
        self.url = url
        self.report = {}

    def scrape_basic(self):
        try:
            response = requests.get(self.url, timeout=15)
            soup = BeautifulSoup(response.text, "lxml")

            title = soup.title.string.strip() if soup.title else None
            desc = soup.find("meta", attrs={"name": "description"})
            desc = desc["content"].strip() if desc else None

            keywords = soup.find("meta", attrs={"name": "keywords"})
            keywords = keywords["content"].split(",") if keywords else []

            headings = {
                "h1": [h.get_text(strip=True) for h in soup.find_all("h1")],
                "h2": [h.get_text(strip=True) for h in soup.find_all("h2")]
            }

            links = [a.get("href") for a in soup.find_all("a", href=True)]
            broken_links = [l for l in links if not l or l.startswith("#")]
            total_links = len(links)

            imgs = soup.find_all("img")
            missing_alt = [img.get("src") for img in imgs if not img.get("alt")]
            total_imgs = len(imgs)

            text = soup.get_text(separator=" ").strip()
            word_count = len(text.split())
            https = self.url.startswith("https")

            self.report["basic"] = {
                "url": self.url,
                "title": title,
                "description": desc,
                "keywords": keywords,
                "headings": headings,
                "links": {"total": total_links, "broken": broken_links},
                "images": {"total": total_imgs, "missing_alt": missing_alt[:10]},
                "content": {"word_count": word_count},
                "performance": {"https": https}
            }
        except Exception as e:
            self.report["basic"] = {"error": str(e)}

    def check_robots_sitemap(self):
        result = {}
        try:
            r = requests.get(urljoin(self.url, "/robots.txt"), timeout=10)
            result["robots_txt"] = "Found" if r.status_code == 200 else "Missing"
        except:
            result["robots_txt"] = "Error"

        try:
            s = requests.get(urljoin(self.url, "/sitemap.xml"), timeout=10)
            result["sitemap"] = "Found" if s.status_code == 200 else "Missing"
        except:
            result["sitemap"] = "Error"

        try:
            soup = BeautifulSoup(requests.get(self.url, timeout=10).text, "lxml")
            canonical = soup.find("link", {"rel": "canonical"})
            result["canonical"] = canonical["href"] if canonical else "Missing"
        except:
            result["canonical"] = "Error"

        self.report["robots_sitemap"] = result

    def extract_schema(self):
        try:
            import extruct
            from w3lib.html import get_base_url

            html = requests.get(self.url, timeout=10).text
            base_url = get_base_url(html, self.url)
            data = extruct.extract(html, base_url=base_url)
            schemas = data.get("json-ld", [])
            self.report["schema"] = {"schema_count": len(schemas), "schemas": schemas[:3]}
        except Exception as e:
            self.report["schema"] = {"schema_count": 0, "error": str(e)}

    def mobile_test(self):
        api_key =  os.getenv("GOOGLE_API_KEY")
        if not api_key:
            self.report["mobile"] = {"mobile_friendly": "API Key Missing"}
            return
        try:
            endpoint = f"https://searchconsole.googleapis.com/v1/urlTestingTools/mobileFriendlyTest:run?key={api_key}"
            res = requests.post(endpoint, json={"url": self.url}).json()
            self.report["mobile"] = {"mobile_friendly": res.get("mobileFriendliness", res)}
        except Exception as e:
            self.report["mobile"] = {"mobile_friendly": "Error", "error": str(e)}

    def performance_audit(self):
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            self.report["core_web_vitals"] = {"performance_score": "API Key Missing"}
            return
        try:
            endpoint = f"https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url={self.url}&key={api_key}&strategy=mobile"
            res = requests.get(endpoint).json()
            lighthouse = res["lighthouseResult"]["categories"]["performance"]["score"]
            audits = res["lighthouseResult"]["audits"]
            self.report["core_web_vitals"] = {
                "performance_score": lighthouse * 100,
                "LCP": audits["largest-contentful-paint"]["displayValue"],
                "CLS": audits["cumulative-layout-shift"]["displayValue"],
                "TBT": audits["total-blocking-time"]["displayValue"]
            }
        except Exception as e:
            self.report["core_web_vitals"] = {"error": str(e)}

    def keyword_analysis(self):
        try:
            html = requests.get(self.url, timeout=10).text
            soup = BeautifulSoup(html, "lxml")
            text = re.sub(r'[^a-zA-Z\s]', '', soup.get_text().lower())
            words = [w for w in text.split() if w not in stopwords.words("english")]
            freq = Counter(words).most_common(10)
            self.report["keywords"] = {"top_keywords": freq}
        except Exception as e:
            self.report["keywords"] = {"error": str(e)}

    def seo_audit(self):
        self.scrape_basic()
        self.check_robots_sitemap()
        # self.extract_schema()
        # self.keyword_analysis()
        # self.report["authority"] = get_domain_metrics(self.url)
        self.report["competitors"] = analyze_competitors(self.url)
        # self.mobile_test()
        self.performance_audit()
        self.report["checked_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return self.report


if __name__ == "__main__":
    test_url = "https://the-digitalbridge.com/"
    audit = Audit(test_url)
    report = audit.seo_audit()
    print("\nFinal SEO Audit Report:\n")
    print(json.dumps(report, indent=2))
