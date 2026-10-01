"""
TRUSTSCAN URL Crawler & Web-Safety Inspection Service
Safely fetches and inspects web page structure, visible text, forms, and redirects
WITHOUT executing JavaScript, submitting forms, or authenticating.
Enforces strict 4.5s timeouts and 500KB inspection caps for analyst safety.
"""

import re
import urllib.parse
from html.parser import HTMLParser
from typing import Dict, Any, List, Optional
import httpx


class SafeDOMExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.title = ""
        self.in_title = False
        self.text_chunks = []
        self.in_ignored_tag = False
        self.inputs = []
        self.forms = []
        self.links = []
        self.meta_desc = ""

    def handle_starttag(self, tag: str, attrs: List[tuple]):
        attrs_dict = {k.lower(): v for k, v in attrs if v is not None}
        if tag in ["script", "style", "noscript", "svg", "canvas"]:
            self.in_ignored_tag = True
        elif tag == "title":
            self.in_title = True
        elif tag == "meta":
            if attrs_dict.get("name") in ["description", "og:description"]:
                self.meta_desc = attrs_dict.get("content", "")
        elif tag == "input":
            self.inputs.append({
                "type": attrs_dict.get("type", "text").lower(),
                "name": attrs_dict.get("name", "").lower(),
                "placeholder": attrs_dict.get("placeholder", "").lower(),
                "id": attrs_dict.get("id", "").lower()
            })
        elif tag == "form":
            self.forms.append({
                "action": attrs_dict.get("action", ""),
                "method": attrs_dict.get("method", "get").lower()
            })
        elif tag == "a":
            href = attrs_dict.get("href", "")
            if href and not href.startswith("#") and not href.startswith("javascript:"):
                self.links.append(href)

    def handle_endtag(self, tag: str):
        if tag in ["script", "style", "noscript", "svg", "canvas"]:
            self.in_ignored_tag = False
        elif tag == "title":
            self.in_title = False

    def handle_data(self, data: str):
        if self.in_title:
            self.title += data
        elif not self.in_ignored_tag:
            txt = data.strip()
            if txt:
                self.text_chunks.append(txt)


class URLCrawlerService:
    FREE_HOSTING_DOMAINS = [
        "vercel.app", "netlify.app", "github.io", "pages.dev", "weebly.com",
        "blogspot.com", "firebaseapp.com", "web.app", "glitch.me", "onrender.com",
        "render.com", "ngrok-free.app", "surge.sh", "000webhostapp.com", "wixsite.com",
        "site123.me", "carrd.co", "mystrikingly.com", "godaddysites.com"
    ]

    ODD_SUSPICIOUS_TLDS = [
        ".xyz", ".top", ".cc", ".tk", ".ml", ".ga", ".cf", ".gq",
        ".buzz", ".work", ".live", ".shop", ".icu", ".vip", ".fit",
        ".rest", ".online", ".site", ".casa", ".click", ".surf"
    ]

    KNOWN_BRANDS = [
        ("Netflix", ["netflix", "stream"]),
        ("State Bank of India (SBI)", ["state bank", "sbi", "onlinesbi", "yono"]),
        ("MetaMask", ["metamask", "crypto wallet", "seed phrase"]),
        ("Microsoft", ["microsoft", "office365", "outlook", "azure", "windows"]),
        ("Google", ["google", "gmail", "workspace", "drive"]),
        ("Amazon", ["amazon", "prime", "aws"]),
        ("PayPal", ["paypal", "send money"]),
        ("Apple", ["apple", "icloud", "apple id"]),
        ("WhatsApp", ["whatsapp", "meta messaging"]),
        ("Instagram", ["instagram", "meta"]),
        ("Facebook", ["facebook", "meta"]),
        ("HDFC Bank", ["hdfc", "hdfcbank"]),
        ("ICICI Bank", ["icici", "icicibank"]),
        ("Chase Bank", ["chase", "jpmorgan"]),
        ("Bank of America", ["bank of america", "bofa"]),
        ("Wells Fargo", ["wells fargo"]),
        ("Binance", ["binance"]),
        ("Coinbase", ["coinbase"]),
        ("DHL Express", ["dhl", "tracking parcel"]),
        ("FedEx", ["fedex"]),
        ("India Post / Speed Post", ["india post", "indiapost", "speedpost"]),
        ("Income Tax Department", ["income tax", "incometax", "itr refund"])
    ]

    OFFICIAL_SOUNDING_WORDS = [
        "admin", "support", "secure", "verify", "verification", "center",
        "headquarters", "helpdesk", "portal", "security-desk", "account-service",
        "security", "login-portal", "update-account", "auth", "validation",
        "billing-center", "recovery", "reactivate"
    ]

    URGENCY_KEYWORDS = [
        "account suspended", "urgent", "24 hours", "immediate", "blocked",
        "penalty", "action required", "congratulations", "winner", "prize",
        "security alert", "warning", "locked", "expire in", "immediate action",
        "failure to update", "permanent closure", "terminate", "unauthorized access"
    ]

    @classmethod
    async def fetch_and_inspect_page(cls, raw_url: str) -> Dict[str, Any]:
        """
        Safely fetches the URL with httpx and extracts structural web-safety indicators.
        Does NOT execute JavaScript or submit data.
        """
        url = raw_url.strip()
        if not url.startswith("http://") and not url.startswith("https://"):
            url = f"https://{url}"

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9"
        }

        initial_url = url
        final_url = url
        status_code = None
        html_content = ""
        fetch_error = None
        redirect_chain = []

        try:
            async with httpx.AsyncClient(timeout=4.5, follow_redirects=True, verify=False) as client:
                resp = await client.get(url, headers=headers)
                final_url = str(resp.url)
                status_code = resp.status_code
                if resp.history:
                    redirect_chain = [str(r.url) for r in resp.history] + [final_url]
                # Read at most 500KB
                html_content = resp.text[:500000]
        except Exception as e:
            fetch_error = str(e)
            # If https failed, fallback check domain
            final_url = url

        # Parse DOM safely
        parser = SafeDOMExtractor()
        if html_content:
            try:
                parser.feed(html_content)
            except Exception:
                pass

        page_title = parser.title.strip() if parser.title else ""
        meta_desc = parser.meta_desc.strip()
        all_text = " ".join(parser.text_chunks)
        visible_snippet = all_text[:2500]

        # Domain breakdown
        parsed_domain = urllib.parse.urlparse(final_url).netloc.lower()
        if ":" in parsed_domain:
            parsed_domain = parsed_domain.split(":")[0]

        # 1. Free hosting check
        is_free_host = any(parsed_domain.endswith(fh) or fh in parsed_domain for fh in cls.FREE_HOSTING_DOMAINS)
        flagged_free_host = next((fh for fh in cls.FREE_HOSTING_DOMAINS if parsed_domain.endswith(fh) or fh in parsed_domain), None)

        # 2. Odd TLD check
        is_odd_tld = any(parsed_domain.endswith(tld) for tld in cls.ODD_SUSPICIOUS_TLDS)

        # 3. Form input audit
        flagged_sensitive_inputs = []
        for inp in parser.inputs:
            itype = inp.get("type", "")
            iname = inp.get("name", "")
            iplc = inp.get("placeholder", "")
            combined = f"{itype} {iname} {iplc}".lower()

            if itype == "password" or any(w in combined for w in ["password", "passcode", "pwd"]):
                flagged_sensitive_inputs.append("Password / Master Passcode")
            elif any(w in combined for w in ["card", "cvv", "credit", "debit", "expiry", "cvc"]):
                flagged_sensitive_inputs.append("Credit / Debit Card Number or CVV")
            elif any(w in combined for w in ["otp", "one time password", "2fa", "code", "sms pin"]):
                flagged_sensitive_inputs.append("One-Time Password (OTP) / 2FA Token")
            elif any(w in combined for w in ["seed", "recovery phrase", "private key", "mnemonic", "secret phrase"]):
                flagged_sensitive_inputs.append("Cryptocurrency Seed Phrase / Private Key")
            elif any(w in combined for w in ["ssn", "aadhaar", "pan", "social security", "national id"]):
                flagged_sensitive_inputs.append("National Identity Number (SSN / Aadhaar / PAN)")
            elif any(w in combined for w in ["pin", "mpin", "atm pin", "upi pin"]):
                flagged_sensitive_inputs.append("Banking ATM / UPI PIN")

        flagged_sensitive_inputs = list(dict.fromkeys(flagged_sensitive_inputs))

        # 4. Brand recognition check
        combined_search_corpus = f"{page_title} {meta_desc} {visible_snippet}".lower()
        claimed_brand = None
        for brand_name, brand_keywords in cls.KNOWN_BRANDS:
            if any(k in combined_search_corpus for k in brand_keywords):
                # Verify if domain matches official brand
                claimed_brand = brand_name
                break

        # Check copyright regex
        cr_match = re.search(r'(?:copyright|©)\s*(?:20\d\d)?\s*([a-zA-Z0-9\s,.-]{3,35})', combined_search_corpus)
        if cr_match and not claimed_brand:
            claimed_brand = cr_match.group(1).strip().title()

        # Check if domain belongs to claimed brand
        belongs_to_claimed_entity = True
        domain_mismatch_warning = None
        if claimed_brand:
            brand_slug = claimed_brand.lower().split()[0]
            if brand_slug not in parsed_domain:
                belongs_to_claimed_entity = False
                domain_mismatch_warning = f"Page visually claims to be '{claimed_brand}', but the website lives on unaffiliated domain '{parsed_domain}'."

        # 5. Generic official-sounding words
        detected_official_words = [w for w in cls.OFFICIAL_SOUNDING_WORDS if w in parsed_domain or w in final_url.lower()]

        # 6. Urgency and pressure tactics
        detected_urgency = [w for w in cls.URGENCY_KEYWORDS if w in combined_search_corpus]

        # 7. Educational / Institutional whitelist
        is_edu_or_gov = any(tld in parsed_domain for tld in [".edu", ".edu.in", ".ac.in", ".gov", ".gov.in", ".org", "nitte.edu.in"])

        return {
            "initial_url": initial_url,
            "final_url": final_url,
            "redirected": initial_url.rstrip("/") != final_url.rstrip("/"),
            "redirect_chain": redirect_chain,
            "status_code": status_code,
            "fetch_error": fetch_error,
            "title": page_title or ("(Page title unavailable)" if not fetch_error else f"(Connection Error: {fetch_error})"),
            "domain": parsed_domain,
            "visible_text_snippet": visible_snippet,
            "total_inputs_found": len(parser.inputs),
            "flagged_sensitive_inputs": flagged_sensitive_inputs,
            "forms_count": len(parser.forms),
            "is_free_host": is_free_host,
            "flagged_free_host": flagged_free_host,
            "is_odd_tld": is_odd_tld,
            "claimed_brand": claimed_brand,
            "belongs_to_claimed_entity": belongs_to_claimed_entity,
            "domain_mismatch_warning": domain_mismatch_warning,
            "official_sounding_words": detected_official_words,
            "urgency_phrases_found": detected_urgency,
            "is_edu_or_gov": is_edu_or_gov
        }
