# 🌊 **DeepClaude**

This project implements an API that integrates with Anthropic's Claude model, allowing requests and receiving responses in streaming format.

## 🚀 Features

- Integration with Claude API (Anthropic)
- Real-time streaming responses
- Support for claude-3-opus-20240229 model

## 🔧 Installation

1. Clone the repository:
git clone https://github.com/ingridytakada/deepclaude.git
cd deepclaude


2. Install dependencies:
pip install -r requirements.txt



3. Set up environment variables:
- Copy `.env.example` to `.env`
- Add your API keys to the `.env` file


## 💻 How to Use

1. Start the server:
python server.py


2. In another terminal, run the client:
python test_api.py


## 📝 Usage Example

The project comes configured with a basic example. To ask different questions, modify the "content" field in the `test_api.py` file:

python
"messages": [
{
"role": "user",
"content": "Your question here"
}
]


## 🛠️ Technologies Used

- FastAPI
- HTTPX
- Python-dotenv
- Uvicorn






