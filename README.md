# AI Email Draft Generator with Multiple LLM Providers

#### Author: **Tomas Vince**  
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue.svg?style=flat-square&logo=linkedin)](https://www.linkedin.com/in/tomasvince/)

A Streamlit-based web application that leverages multiple LLM providers (Sambanova AI, OpenAI, and Anthropic) to generate professional email drafts. This application allows users to customize their email generation using different AI models and parameters, making it flexible for various email writing needs.

## Features

- 🤖 Multiple LLM Provider Support:
  - **Sambanova Models**:
    - Meta-Llama-3.1-405B-Instruct
    - Meta-Llama-3.1-70B-Instruct
    - Meta-Llama-3.1-8B-Instruct
    - Meta-Llama-3.2-1B-Instruct
    - Meta-Llama-3.2-3B-Instruct
    - Meta-Llama-3.3-70B-Instruct
    - Meta-Llama-Guard-3-8B
    - Qwen2.5-72B-Instruct
    - Qwen2.5-Coder-32B-Instruct
    - QwQ-32B-Preview
    - Meta-Llama-3.1-34B-Instruct
    - Mixtral-8x7B-Instruct
  - **OpenAI Models**:
    - GPT-4
    - GPT-4 Turbo Preview
    - GPT-3.5 Turbo
  - **Anthropic Models**:
    - Claude-3 Sonnet
    - Claude-3 Opus
- 🔑 Secure API Key Management
- 🎛️ Adjustable AI Parameters:
  - Temperature control
  - Top P sampling
- 📝 Customizable Prompts:
  - System prompt for context setting
  - User prompt for specific email requirements
- 💡 Example Prompts Included
- 🚀 Real-time Email Generation

## Prerequisites

- Python 3.8 or higher
- API keys for your chosen providers:
  - Sambanova API key
  - OpenAI API key (optional)
  - Anthropic API key (optional)
- Virtual environment (recommended)

## Installation

1. Clone the repository or download the source files.

2. Create and activate a virtual environment (recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. Install required packages:
   ```bash
   pip install openai streamlit python-dotenv anthropic
   ```

4. Create a `.env` file in the project root directory with your API keys:
   ```bash
   SAMBANOVA_API_KEY=your_sambanova_key_here
   OPENAI_API_KEY=your_openai_key_here
   ANTHROPIC_API_KEY=your_anthropic_key_here
   ```

## Environment Variables and API Key Management

The application uses environment variables for configuration. Copy `env.example` to `.env` and update the Sambanova API key:

```bash
cp env.example .env
```

Required variable:
- `SAMBANOVA_API_KEY`: Your Sambanova AI API key (required in .env file)

For OpenAI and Anthropic API keys, we recommend using the Streamlit UI input field instead of environment variables for several reasons:

### Security Benefits
- API keys are not stored in configuration files
- Keys are only held in memory during the session
- Keys are not exposed in logs or container inspection
- No risk of accidentally committing API keys to version control

### Flexibility Advantages
- Switch between different API keys without restarting the application
- Use different API keys for different providers in the same session
- Test various configurations on the fly
- Easy key rotation and management

### Development/Production Consistency
- Same code works across all environments (local, container, production)
- No need to manage multiple .env files
- Simplified deployment process
- Consistent behavior across different setups

## Usage

1. Start the Streamlit application:
   ```bash
   streamlit run streamlit_sambanova_emaildraft.py
   ```

2. The application will open in your default web browser.

3. In the sidebar:
   - Select your preferred LLM provider
   - Enter your API key (if not set in environment variables)
   - Select an AI model from the chosen provider
   - Adjust temperature (0.0-1.0)
   - Adjust top P value (0.0-1.0)

4. In the main area:
   - (Optional) Enter a system prompt to set context
   - Enter your email request in the user prompt field
   - Click "Generate Email" to create your draft

## Example Use Cases

- Follow-up emails for customer inquiries
- Thank you emails after meetings
- Product launch announcements
- Job application follow-ups
- Customer service responses
- Meeting scheduling emails

## Tips for Best Results

- Be specific in your prompts
- Use the system prompt to set the tone and style
- Choose the appropriate provider and model for your use case:
  - Sambanova models for high-performance local inference
  - GPT-4 for complex reasoning and professional writing
  - Claude-3 for detailed analysis and creative writing
- Adjust temperature:
  - Lower (0.1-0.3) for more focused, professional emails
  - Higher (0.7-0.9) for more creative variations

## Docker Deployment

### Prerequisites
- Docker and Docker Compose installed
- Traefik reverse proxy running with `traefik-net` network
- Valid SSL certificate configured in Traefik for `your-domain.com`

### Local Build and Run
```bash
# Build the Docker image
docker build -t email-draft-generator .

# Run with Docker Compose
docker-compose up -d
```

### Docker Configuration
The application is containerized and configured to run behind a Traefik reverse proxy with the following features:

- **Base URL**: `https://your-domain.com/email-draft-generator`
- **Container Port**: 8501 (Streamlit default)
- **Network**: Uses external `traefik-net` network
- **Environment Variables**: 
  - `SAMBANOVA_API_KEY` (for Sambanova AI)
  - `OPENAI_API_KEY` (for OpenAI)
  - `ANTHROPIC_API_KEY` (for Anthropic)

### Traefik Integration
The service is configured with Traefik labels for:
- Automatic HTTPS routing
- Path-based routing with prefix stripping
- Secure TLS configuration
- Load balancing

### Deployment Steps
1. Ensure Traefik is running and `traefik-net` network exists:
   ```bash
   docker network ls | grep traefik-net
   ```

2. Create `.env` file with your API keys:
   ```bash
   SAMBANOVA_API_KEY=your_sambanova_key_here
   OPENAI_API_KEY=your_openai_key_here
   ANTHROPIC_API_KEY=your_anthropic_key_here
   ```

3. Deploy the service:
   ```bash
   docker-compose up -d
   ```

4. Verify deployment:
   ```bash
   docker-compose ps
   ```

5. Access the application at `https://your-domain.com/email-draft-generator`

## Troubleshooting

- If you get API errors:
  - Verify your API keys in the `.env` file or sidebar input
  - Check that you have access to the selected model
  - Ensure you have sufficient API credits
- Ensure all dependencies are installed in your virtual environment
- Check that you're running the latest version of Python and required packages

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Built with Streamlit
- Powered by:
  - Sambanova AI
  - OpenAI
  - Anthropic
- Special thanks to all the AI providers for their powerful language models
