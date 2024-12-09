Building a Domain-Specific Chatbot Application

This project focuses on creating a chatbot capable of handling queries across four domains: Healthcare, Insurance, Finance, and Retail. Below is a step-by-step breakdown of the approach:

1. Data Preparation
Datasets: I utilized publicly available datasets for each domain:
Healthcare: Ram20307/HealthCareChatbot
Insurance: deccan-ai/insuranceQA-v2
Finance: poornima9348/finance-alpaca-1k-test
Retail: qgyd2021/e_commerce_customer_service
Cleaning and Formatting: Each dataset was cleaned and standardized by renaming columns to "question" and "answer" and adding a "domain" column. The datasets were then combined into a single multi-domain dataset.

2. Data Splitting
The combined dataset was split into training and testing sets using an 80-20 ratio to ensure proper evaluation of the model.

3. Model Selection and Tokenization
Base Model: I used the meta-llama/Llama-3.2-1B model as the foundation for training.
Tokenizer: The tokenizer was customized to include a padding token, ensuring compatibility with the model.
Preprocessing: Input data was tokenized by combining the "domain" and "question" fields, while the "answer" field was used as the target. Padding and truncation were applied to maintain consistency.

4. Fine-Tuning with LoRA
To optimize the model for domain-specific tasks, I applied Low-Rank Adaptation (LoRA). This technique allowed efficient fine-tuning by focusing on specific layers of the model, reducing computational overhead.
Training Configuration: The model was trained for three epochs with a small batch size and gradient accumulation to handle resource constraints.

5. Application Development
Framework: I built the chatbot interface using Streamlit for a user-friendly web application.
LLM Integration: The fine-tuned model was deployed using Hugging Face's API, ensuring seamless interaction with the chatbot.
Domain Classification: A simple keyword-based classifier was implemented to identify the domain of user queries (e.g., Healthcare, Insurance, etc.). Out-of-domain queries receive a standard response.

6. Chatbot Features
Interactive Interface: Users can input queries, and the chatbot responds based on the identified domain.
Session Management: Chat history is maintained for a better user experience.
Analytics: The application tracks the total number of queries and allows users to download chat logs for reference.
