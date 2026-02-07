
#!/usr/bin/env python3
"""
WhatsApp Ban Tool v3.0 - Ultimate Pro Edition
Author: LORD SHAZAM 
Features: Real number verification, mass reporting, email rotation, proxy support
"""

import os
import sys
import time
import random
import json
import smtplib
import ssl
import threading
import hashlib
import re
import itertools
import requests
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from concurrent.futures import ThreadPoolExecutor, as_completed
from colorama import Fore, Style, init

init(autoreset=True)

# ===== Crypto Lord Password =====

TOOL_USERNAME = "Meta"
TOOL_PASSWORD = "admin"

# ===== GMAIL ACCOUNTS =====
GMAIL_ACCOUNTS = [
    {"email": "managerhimself032@gmail.com", "password": "inagtgypnpyweleu"},
    {"email": "arsheeqarsheeqq@gmail.com", "password": "pkkqfactxwkpvzgc"},
    {"email": "rebornlegend67@gmail.com", "password": "gcenolfafabgcnko"},
    {"email": "cryptolord25ss@gmail.com", "password": "lczszqjxovvbuxco"},
   {"email": "abayomishade96@gmail.com", "password": "qhosqqkvhmcoyrqd"},
   {"email": "shazamsolos001@gmail.com", "password": "gonlbvnhxdospiic"},
   {"email": "jackiechanski55@gmail", "password": "epzezxtxvrkaaged"},
   {"email": "calebaboagye509@gmail.com", "password": "wwtaxbgecnvfomzd"},
   {"email": "basitgaming190k@gmail.com", "password": "myeghlgusewjzgul"},
   {"email": "ferryxmartins@gmail.com", "password": "rvcrntktvmwqmxgi"},
   {"email": "kingshazam001@gmail.com", "password": "hrlggyjflzuyqdvf"},
]

# ===== PROXY CONFIGURATION =====
PROXY_LIST = []
try:
    with open('proxies.txt', 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                if '://' not in line:
                    line = f"http://{line}"
                PROXY_LIST.append(line)
    print(Fore.GREEN + f"✅ 𝗟𝗼𝗮𝗱𝗲𝗱 {len(PROXY_LIST)} 𝗽𝗿𝗼𝘅𝗶𝗲𝘀")
except FileNotFoundError:
    print(Fore.YELLOW + "⚠️ proxies.txt 𝗻𝗼𝘁 𝗳𝗼𝘂𝗻𝗱")

# ===== WHATSAPP SUPPORT EMAILS =====
WHATSAPP_EMAILS = [
    "support@support.whatsapp.com",
    "support@support.whatsapp.com",
    "support@whatsapp.com",
    "support@whatsapp.com",
    "support@whatsapp.com",
    "support@whatsapp.com", 
    "android@support.whatsapp.com",
    "support@support.whatsapp.com",
    "support@support.whatsapp.com", 
    "support@support.whatsapp.com"
]

# ===== WHATSAPP API CREDENTIALS =====
ACCESS_TOKEN = "EAAJgi17vyDYBPTGf8m4LNp0xFdUozhBKS6PTnrElQdSZCIRZCnuLFmBigzRvB4ZCUI8EBNuNZCFZBfG5e11ehZBujToi9S6zYQ3HSmDZBPNQHZBFFrd3ntSZAl6lRZAOa86mOZCp60VaaCMhgUN6s68EEvYSEJXlaIk9iiB7xe1rlZBKbEVf7YiIADUZA0kHuO9nr0QZDZD"
PHONE_NUMBER_ID = "669101662914614"

# ===== SMTP CONFIGURATION =====
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_SSL_PORT = 465

# ===== GLOBAL VARIABLES =====
sent_counter = 0
failed_counter = 0
current_account_index = 0
current_proxy_index = 0
lock = threading.Lock()

# ===== UTILITY FUNCTIONS =====
def clear():
    os.system("cls" if os.name == "nt" else "clear")

def typewriter(text, delay=0.05):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)

def get_next_account():
    """Rotate through Gmail accounts"""
    global current_account_index
    with lock:
        account = GMAIL_ACCOUNTS[current_account_index]
        current_account_index = (current_account_index + 1) % len(GMAIL_ACCOUNTS)
        return account

def get_next_proxy():
    """Rotate through proxy list"""
    global current_proxy_index
    if not PROXY_LIST:
        return None
    with lock:
        proxy = PROXY_LIST[current_proxy_index]
        current_proxy_index = (current_proxy_index + 1) % len(PROXY_LIST)
        return proxy

def validate_phone_number(phone):
    """Validate phone number format"""
    pattern = r'^\+[1-9]\d{1,14}$'
    return bool(re.match(pattern, phone))

def test_proxy(proxy_url):
    """Test if a proxy is working"""
    try:
        proxies = {
            "http": proxy_url,
            "https": proxy_url
        }
        response = requests.get("http://httpbin.org/ip", proxies=proxies, timeout=10)
        if response.status_code == 200:
            return True, response.json().get("origin", "Unknown")
        return False, "Failed"
    except Exception as e:
        return False, str(e)

# ===== REAL WHATSAPP NUMBER CHECKING =====
def check_whatsapp_number(phone):
    """Real WhatsApp number checking using Facebook Graph API"""
    url = f"https://graph.facebook.com/v19.0/{PHONE_NUMBER_ID}/contacts"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    payload = {
        "blocking": "wait",
        "contacts": [phone],
        "force_check": True
    }

    proxy = get_next_proxy()
    
    try:
        print(Fore.CYAN + f"\n🔍 Checking WhatsApp status for {phone}")
        
        if proxy:
            print(Fore.CYAN + f"   Using proxy: {proxy}")
            proxies = {"http": proxy, "https": proxy}
            response = requests.post(url, headers=headers, json=payload, timeout=15, proxies=proxies)
        else:
            response = requests.post(url, headers=headers, json=payload, timeout=15)
            
    except Exception as e:
        print(Fore.RED + f"\n⚠️ Request failed: {e}")
        if proxy:
            print(Fore.YELLOW + f"   Proxy: {proxy} may be dead")
        return

    if response.status_code == 200:
        data = response.json()
        contacts = data.get("contacts", [])
        
        if contacts:
            for contact in contacts:
                status = contact.get("status", "unknown")
                wa_id = contact.get("wa_id", "N/A")
                
                if status == "valid":
                    print(Fore.GREEN + f"\n✅ 𝗡𝘂𝗺𝗯𝗲𝗿: {wa_id} is 𝗥𝗘𝗚𝗜𝗦𝗧𝗘𝗥𝗘𝗗 𝗼𝗻 𝗪𝗵𝗮𝘁𝘀𝗔𝗽𝗽.")
                    print(Fore.CYAN + f"   𝗦𝘁𝗮𝘁𝘂𝘀: 𝗔𝗰𝘁𝗶𝘃𝗲 𝗮𝗻𝗱 𝘃𝗮𝗹𝗶𝗱")
                elif status == "invalid":
                    print(Fore.RED + f"\n❌ 𝗡𝘂𝗺𝗯𝗲𝗿: {wa_id} 𝗶𝘀 𝗡𝗢𝗧 𝗥𝗘𝗚𝗜𝗦𝗧𝗘𝗥𝗘𝗗 𝗼𝗻 𝗪𝗵𝗮𝘁𝘀𝗔𝗽𝗽.")
                else:
                    print(Fore.YELLOW + f"\n⚠️ 𝗡𝘂𝗺𝗯𝗲𝗿: {wa_id} - 𝗦𝘁𝗮𝘁𝘂𝘀: {status}")
                
                # Additional info
                info = {
                    "Input": phone,
                    "WhatsApp ID": wa_id,
                    "Status": status.upper(),
                    "Checked At": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "Via Proxy": proxy if proxy else "Direct"
                }
                
                for key, value in info.items():
                    print(Fore.WHITE + f"   {key}: {value}")
        else:
            print(Fore.RED + f"\n❌ 𝗡𝘂𝗺𝗯𝗲𝗿 {phone} 𝗶𝘀 𝗻𝗼𝘁 𝗿𝗲𝗴𝗶𝘀𝘁𝗲𝗿𝗲𝗱 𝗼𝗻 𝗪𝗵𝗮𝘁𝘀𝗔𝗽𝗽.")
            
    else:
        print(Fore.RED + f"\n⚠️ 𝗔𝗣𝗜 𝗘𝗿𝗿𝗼𝗿: 𝗦𝘁𝗮𝘁𝘂𝘀 {response.status_code}")
        try:
            error_data = response.json()
            print(Fore.YELLOW + f"   Error: {error_data.get('error', {}).get('message', 'Unknown error')}")
        except:
            print(Fore.YELLOW + f"   𝗥𝗲𝘀𝗽𝗼𝗻𝘀𝗲: {response.text[:200]}")

# ===== ENHANCED EMAIL SENDING WITH ROTATION =====
def send_whatsapp_report(subject, body, target_email, report_type="ban"):
    """Send report to WhatsApp with rotation and tracking"""
    global sent_counter, failed_counter
    
    account = get_next_account()
    sender_email = account["email"]
    sender_password = account["password"]
    
    try:
        # Create message with proper headers
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = f"WhatsApp User <{sender_email}>"
        msg['To'] = target_email
        msg['X-Priority'] = '1'
        msg['Importance'] = 'high'
        msg['X-Mailer'] = 'Microsoft Outlook 16.0'
        
        # Generate unique message ID
        msg_id = f"{int(time.time())}.{random.randint(1000, 9999)}@gmail.com"
        msg['Message-ID'] = f"<{msg_id}>"
        
        # Create both text and HTML versions
        text_part = MIMEText(body, 'plain')
        
        # Enhanced HTML version
        html_part = MIMEText(f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; background: #f5f5f5; }}
                .container {{ background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); margin: 20px auto; }}
                .header {{ background: linear-gradient(135deg, #25D366, #128C7E); padding: 20px; border-radius: 10px 10px 0 0; color: white; text-align: center; }}
                .content {{ padding: 25px; }}
                .footer {{ font-size: 12px; color: #666; text-align: center; margin-top: 20px; padding-top: 10px; border-top: 1px solid #ddd; }}
                .urgent {{ color: #d32f2f; font-weight: bold; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h2>WhatsApp Support Request</h2>
                </div>
                <div class="content">
                    {body.replace(chr(10), '<br>')}
                    <div class="footer">
                        <p>Request ID: {random.randint(100000, 999999)}</p>
                        <p>Type: {report_type.upper()} | Sender: {sender_email}</p>
                        <p>Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                    </div>
                </div>
            </div>
        </body>
        </html>
        """, 'html')
        
        msg.attach(text_part)
        msg.attach(html_part)
        
        # Send email with fallback mechanism
        try:
            # Try STARTTLS first
            server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout=30)
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)
            server.quit()
            
            with lock:
                sent_counter += 1
            
            return True, "Success", sender_email
            
        except Exception as e:
            # Fallback to SSL
            try:
                context = ssl.create_default_context()
                server = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_SSL_PORT, context=context, timeout=30)
                server.login(sender_email, sender_password)
                server.send_message(msg)
                server.quit()
                
                with lock:
                    sent_counter += 1
                
                return True, "Success (SSL)", sender_email
            except Exception as ssl_error:
                raise ssl_error
        
    except Exception as e:
        error_msg = str(e)
        with lock:
            failed_counter += 1
        
        return False, error_msg, sender_email

def mass_report_attack(target_number, report_type, report_count=50):
    """Execute mass reporting attack with complete rotation"""
    global sent_counter, failed_counter
    sent_counter = 0
    failed_counter = 0
    
    # Validate count (10-50)
    report_count = max(10, min(50, report_count))
    
    # Calculate optimal distribution
    senders = len(GMAIL_ACCOUNTS)
    targets = len(WHATSAPP_EMAILS)
    total_pairs = senders * targets
    
    # Generate all possible sender-target combinations
    all_pairs = []
    for sender in GMAIL_ACCOUNTS:
        for target in WHATSAPP_EMAILS:
            all_pairs.append((sender, target))
    
    # Randomize the pairs and take required number
    random.shuffle(all_pairs)
    selected_pairs = all_pairs[:report_count]
    
    print(Fore.CYAN + f"\n🚀 𝗜𝗻𝗶𝘁𝗶𝗮𝗹𝗶𝘇𝗶𝗻𝗴 {report_type.upper()} 𝗮𝘁𝘁𝗮𝗰𝗸 𝗼𝗻 {target_number}")
    print(Fore.CYAN + f"📊 𝗥𝗲𝗽𝗼𝗿𝘁𝘀 𝘁𝗼 𝘀𝗲𝗻𝗱: {report_count}")
    print(Fore.CYAN + f"📧 𝗨𝘀𝗶𝗻𝗴 {senders} 𝘀𝗲𝗻𝗱𝗲𝗿 𝗮𝗰𝗰𝗼𝘂𝗻𝘁𝘀")
    print(Fore.CYAN + f"🎯 𝗧𝗮𝗿𝗴𝗲𝘁𝗶𝗻𝗴 {targets} 𝗪𝗵𝗮𝘁𝘀𝗔𝗽𝗽 𝘀𝘂𝗽𝗽𝗼𝗿𝘁 𝗲𝗺𝗮𝗶𝗹𝘀")
    print(Fore.YELLOW + "="*60)
    
    # Generate report content based on type
    if report_type == "ban":
        subject = f"URGENT BAN REQUEST: {target_number} - HARASSMENT & SPAM"
        body = f"""
To the WhatsApp Trust and Safety / Cybercrime Review Team,

I am submitting this report as a formal child porn Dealer complaint concerning a WhatsApp account involved in coordinated and repeated criminal activity, including fraud, phishing, sexual spam distribution, and attempted account compromise.
Reported WhatsApp Number:
{target_number}
Nature of Complaint:
The reported account is actively engaging in behavior consistent with organized children porn activities operations. The activities observed are intentional, repeated, and designed to deceive, exploit, and harm users of the WhatsApp platform.
Details of Criminal Activity:
The account has sent unsolicited messages containing fraudulent content, phishing links, and malicious URLs intended to steal personal data, login credentials, verification codes, and financial information from victims. These links are structured to impersonate legitimate services and mislead users into providing sensitive information.
In addition, the account distributes explicit sexual video links as spam without user consent. This content is used as a lure to manipulate recipients into clicking malicious links or engaging further, which is a known tactic in online exploitation and account hijacking attempts.
The sender has also attempted to pressure and manipulate recipients into actions that could lead to unauthorized access to their WhatsApp accounts, including social engineering techniques commonly associated with hacking attempts.
Pattern of Abuse:
The behavior is persistent and continues even after users ignore or disengage, indicating deliberate malicious intent rather than accidental or isolated misuse. This pattern strongly suggests systematic abuse of the platform.
Risk Assessment:
This activity poses a serious risk to user safety, privacy, and financial security. It also represents a potential threat to minors and vulnerable users due to the distribution of explicit content and deceptive messaging tactics.
Request for Immediate Action:
I respectfully request an urgent manual investigation into this account by the WhatsApp Trust and Safety and Cybercrime Review teams. Given the severity, repetition, and criminal nature of these actions, I request appropriate enforcement measures, including account suspension or permanent removal, to prevent further harm.
Thank you for your attention to this serious matter.
Sincerely,
A Concerned WhatsApp User
"""
    elif report_type == "fraud":
        subject = f"FRAUD ALERT: {target_number} - FINANCIAL SCAM"
        body = f"""
To the WhatsApp Trust and Safety / Cybercrime Review Team,

I am submitting this report as a formal cybercrime complaint concerning a WhatsApp account involved in coordinated and repeated criminal activity, including fraud, phishing, sexual spam distribution, and attempted account compromise.
Reported WhatsApp Number:
{target_number}
Nature of Complaint:
The reported account is actively engaging in behavior consistent with organized cybercrime operations. The activities observed are intentional, repeated, and designed to deceive, exploit, and harm users of the WhatsApp platform.
Details of Criminal Activity:
The account has sent unsolicited messages containing fraudulent content, phishing links, and malicious URLs intended to steal personal data, login credentials, verification codes, and financial information from victims. These links are structured to impersonate legitimate services and mislead users into providing sensitive information.
In addition, the account distributes explicit sexual video links as spam without user consent. This content is used as a lure to manipulate recipients into clicking malicious links or engaging further, which is a known tactic in online exploitation and account hijacking attempts.
The sender has also attempted to pressure and manipulate recipients into actions that could lead to unauthorized access to their WhatsApp accounts, including social engineering techniques commonly associated with hacking attempts.
Pattern of Abuse:
The behavior is persistent and continues even after users ignore or disengage, indicating deliberate malicious intent rather than accidental or isolated misuse. This pattern strongly suggests systematic abuse of the platform.
Risk Assessment:
This activity poses a serious risk to user safety, privacy, and financial security. It also represents a potential threat to minors and vulnerable users due to the distribution of explicit content and deceptive messaging tactics.
Request for Immediate Action:
I respectfully request an urgent manual investigation into this account by the WhatsApp Trust and Safety and Cybercrime Review teams. Given the severity, repetition, and criminal nature of these actions, I request appropriate enforcement measures, including account suspension or permanent removal, to prevent further harm.
Thank you for your attention to this serious matter.
Sincerely,
A Concerned WhatsApp User
"""
    elif report_type == "unban":
        subject = f"APPEAL: Wrongful Ban - {target_number}"
        body = f"""Request for Review and Reinstatement of My WhatsApp Account

Dear WhatsApp Support Team,

I am writing to respectfully request a thorough review of my WhatsApp account associated with the phone number {target_number}, which has recently been banned. I understand that WhatsApp enforces strict policies to maintain a safe and trusted platform, and I fully support these efforts.
However, I strongly believe that my account was banned in error, as I have never knowingly violated WhatsApp's Terms of Service or Community Guidelines. I use WhatsApp primarily for personal communication with family, friends, and professional contacts, and I have always acted responsibly on the platform.
If any of my recent activity was flagged unintentionally or misunderstood, I sincerely apologize. It was never my intention to misuse WhatsApp in any way. I am more than willing to cooperate fully and adjust my usage to comply strictly with all policies going forward.
I kindly request that you review my account again and consider reinstating it. Losing access has significantly affected my daily communication, and I assure you that this situation will not be repeated.
I truly regret any action—intentional or unintentional—that may have led to this situation.
If any of my behavior violated WhatsApp's policies, I take full responsibility and sincerely apologize. I now understand the importance of strictly following all guidelines to protect the integrity of the platform and the safety of its users.
WhatsApp plays a critical role in my daily life, including communication with family members, work-related coordination, and important personal matters. The loss of access has been extremely difficult for me.
I respectfully request one opportunity to correct my mistake. I assure you that I will be extremely careful moving forward and will fully comply with all WhatsApp rules without exception.
"""
    elif report_type == "nuclear":
        subject = f"EMERGENCY SECURITY THREAT: {target_number} - TERRORIST ACTIVITIES"
        body = f"""
To the WhatsApp Trust and Safety / Cybercrime Review Team,

I am submitting this report as a formal cybercrime complaint concerning a WhatsApp account involved in coordinated and repeated criminal activity, including fraud, phishing, sexual spam distribution, and attempted account compromise.
Reported WhatsApp Number:
{target_number}
Nature of Complaint:
The reported ac
"""
