# 📰 News-to-Twitter Automation with AI 🦾  

This project automates the process of fetching the latest **technology news**, generating AI-powered summaries, and sharing the news on **Twitter** with a beautifully designed image! 🌟  

The workflow ensures that **unique articles** are shared each time to keep your audience engaged and updated. 🚀  

---

## 🎯 Features  
- **Fetches Tech News** from trusted sources using the News API. 📰  
- Generates **summaries** using Google’s Generative AI. 🤖  
- Creates **aesthetic images** with titles and summaries using Python. 🎨  
- Publishes **tweets with images** automatically to your Twitter account. 🐦  
- Ensures **no duplicate articles** are posted, thanks to a JSON-based tracking system. ✅  

---

## 📁 Repository Structure  

- **`engine.py`**: The main script that handles fetching news, generating summaries, creating images, and tweeting.  
- **`requirements.txt`**: Python dependencies for the project.  
- **`fetched_articles.json`**: Tracks already posted articles to avoid duplication.  
- **`base.jpg`**: The base template for the image used in tweets.  

---

## 🚀 Getting Started  

### Prerequisites  
1. **Python 3.10+** installed.  
2. API keys for:  
   - News API 📰  
   - Google Generative AI 🤖  
   - Twitter API 🐦  

### Setup Instructions  
1. Clone the repository:  
   ```bash  
   git clone https://github.com/<your-username>/news-twitter-automation.git  
   cd news-twitter-automation  
   ```  

2. Install dependencies:  
   ```bash  
   pip install -r requirements.txt  
   ```  

3. Add your API keys:  
   - Create a `.env` file (or configure environment variables in your CI/CD setup).  
   - Add the following keys:  
     ```env  
     NEWS_API_KEY=your_news_api_key  
     GENAI_API_KEY=your_genai_api_key  
     TWITTER_CONSUMER_KEY=your_twitter_consumer_key  
     TWITTER_CONSUMER_SECRET=your_twitter_consumer_secret  
     TWITTER_ACCESS_TOKEN=your_twitter_access_token  
     TWITTER_ACCESS_TOKEN_SECRET=your_twitter_access_token_secret  
     ```  

4. Run the script locally:  
   ```bash  
   python engine.py  
   ```  

---

## 🌐 GitHub Actions Workflow  

This project includes a GitHub Actions workflow for automation. The script runs **hourly** and ensures your Twitter account is consistently updated with fresh content.  

### Setting Up the Workflow  
1. Add the API keys as **secrets** in your GitHub repository:  
   - `NEWS_API_KEY`  
   - `GENAI_API_KEY`  
   - `TWITTER_CONSUMER_KEY`  
   - `TWITTER_CONSUMER_SECRET`  
   - `TWITTER_ACCESS_TOKEN`  
   - `TWITTER_ACCESS_TOKEN_SECRET`  

2. The workflow file (`.github/workflows/main.yml`) is already included. It:  
   - Runs the script every hour.  
   - Saves and fetches `fetched_articles.json` to prevent duplicates.  

---

## 📸 Example Output  

Here’s what a typical tweet looks like:  

**Tweet Text**:  
```  
Breaking News! 🌟  
[AI-Generated Title]  
#Tech #Technology #News #AI #Trending  

Check out more: [Article Link]  
```  

**Attached Image**:  
An elegant card featuring the news title and AI-generated summary.  

---

## 🤝 Contributions  

Feel free to fork this repository and open pull requests for improvements! Suggestions and contributions are always welcome. ❤️  

---

## 📜 License  

This project is licensed under the **MIT License**.  

---

## 🧠 Learn More  

- [News API Documentation](https://newsapi.org/docs)  
- [Google Generative AI](https://ai.google/tools/)  
- [Tweepy Documentation](https://docs.tweepy.org/)  

---

### ⭐️ If you find this project helpful, give it a star!  
Your support keeps the innovation alive! 🌟  
