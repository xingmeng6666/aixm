from langchain_core.tools import tool
from tools.crawler import WebCrawlerTool
from tools.email_tool import EmailTool

@tool
def search_web(url: str) -> str:
    """Fetch and extract text content from a web page URL."""
    crawler = WebCrawlerTool()
    content = crawler.fetch_page(url)
    return crawler.extract_text(content)

@tool
def send_email(to_address: str, subject: str, body: str) -> str:
    """Send an email to a specific address with a subject and body."""
    email_tool = EmailTool()
    success = email_tool.send_email(to_address, subject, body)
    return "Email sent successfully" if success else "Failed to send email"

@tool
def post_tweet(content: str) -> str:
    """Post a tweet to Twitter."""
    # Mock implementation of Twitter posting
    print(f"[TwitterTool] Posting tweet: {content}")
    return f"Tweet posted successfully: {content}"
