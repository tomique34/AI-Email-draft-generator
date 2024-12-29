import os
import openai
import streamlit as st
from dotenv import load_dotenv
from anthropic import Anthropic

# Load environment variables
load_dotenv()

# Available models and providers
PROVIDERS = {
    "Sambanova API": {
        "models": [
            "Meta-Llama-3.1-405B-Instruct",
            "Meta-Llama-3.1-70B-Instruct",
            "Meta-Llama-3.1-8B-Instruct",
            "Meta-Llama-3.2-1B-Instruct",
            "Meta-Llama-3.2-3B-Instruct",
            "Meta-Llama-3.3-70B-Instruct",
            "Meta-Llama-Guard-3-8B",
            "Qwen2.5-72B-Instruct",
            "Qwen2.5-Coder-32B-Instruct",
            "QwQ-32B-Preview",
            "Meta-Llama-3.1-34B-Instruct",
            "Mixtral-8x7B-Instruct"
        ],
        "base_url": "https://api.sambanova.ai/v1"
    },
    "OpenAI": {
        "models": ["gpt-4o","gpt-4o-mini", "gpt-4", "gpt-4-turbo", "gpt-3.5-turbo"],
        "base_url": "https://api.openai.com/v1"
    },
    "Anthropic": {
        "models": ["claude-3-sonnet-20240229", "claude-3-opus-20240229"],
        "base_url": "https://api.anthropic.com/v1"
    }
}

@st.cache_resource
def get_client(provider, api_key):
    if not api_key:
        st.error(f"Please provide an API key for {provider}")
        return None
        
    if provider == "Sambanova API":
        return openai.OpenAI(
            api_key=api_key,
            base_url=PROVIDERS[provider]["base_url"]
        )
    elif provider == "OpenAI":
        return openai.OpenAI(api_key=api_key)
    elif provider == "Anthropic":
        return Anthropic(api_key=api_key)
    return None

def generate_email(client, provider, model, system_prompt, user_prompt, temperature, top_p):
    if not client:
        return "Error: No valid client. Please check your API key."
        
    try:
        if provider in ["Sambanova API", "OpenAI"]:
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": user_prompt})
            
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                top_p=top_p
            )
            return response.choices[0].message.content
        elif provider == "Anthropic":
            messages = f"{system_prompt}\n\n{user_prompt}" if system_prompt else user_prompt
            response = client.messages.create(
                model=model,
                max_tokens=1000,
                temperature=temperature,
                messages=[{"role": "user", "content": messages}]
            )
            return response.content[0].text
    except Exception as e:
        return f"Error generating email: {str(e)}"

def main():
    st.title("📧 Email Draft Generator with Multiple LLM Providers")
    
    # Initialize session state for authentication
    if 'sambanova_authenticated' not in st.session_state:
        st.session_state.sambanova_authenticated = False

    # Sidebar for provider, model and parameter settings
    st.sidebar.header("Model Settings")
    
    selected_provider = st.sidebar.selectbox(
        "Select Provider",
        list(PROVIDERS.keys()),
        index=0
    )
    
    # API Key input with different handling for Sambanova
    if selected_provider == "Sambanova API":
        # Password protection for Sambanova
        if not st.session_state.sambanova_authenticated:
            st.sidebar.warning("🔒 Access to preloaded Sambanova API key requires authentication")
            password = st.sidebar.text_input("Enter password to use Sambanova", type="password")
            if st.sidebar.button("Authenticate"):
                correct_password = os.getenv("SAMBANOVA_ACCESS_PASSWORD")
                if not correct_password:
                    st.sidebar.error("❌ Authentication not configured. Contact administrator.")
                elif password == correct_password:
                    st.session_state.sambanova_authenticated = True
                    st.rerun()
                else:
                    st.sidebar.error("❌ Incorrect password")
            api_key = ""  # No API key until authenticated
        else:
            # Show logout option
            if st.sidebar.button("Logout from using Sambanova API"):
                st.session_state.sambanova_authenticated = False
                st.rerun()
            
            # For authenticated users, use environment variable without showing in UI
            api_key = os.getenv("SAMBANOVA_API_KEY", "")
            if not api_key:
                st.sidebar.error("Sambanova API key not found in environment variables")
            else:
                st.sidebar.success("✅ Authenticated and SambanovaAPI key is loaded")
    else:
        # For other providers, allow UI input with visibility toggle
        api_key = st.sidebar.text_input(
            f"{selected_provider} API Key",
            type="password",
            value=os.getenv(f"{selected_provider.upper()}_API_KEY", ""),
            help=f"Enter your {selected_provider} API key"
        )
    
    selected_model = st.sidebar.selectbox(
        "Select Model",
        PROVIDERS[selected_provider]["models"],
        index=0
    )
    
    temperature = st.sidebar.slider(
        "Temperature",
        min_value=0.0,
        max_value=1.0,
        value=0.1,
        step=0.1,
        help="Higher values make the output more random, lower values make it more focused and deterministic."
    )
    
    top_p = st.sidebar.slider(
        "Top P",
        min_value=0.0,
        max_value=1.0,
        value=0.1,
        step=0.1,
        help="Controls diversity via nucleus sampling."
    )
    
    # Initialize the client
    client = get_client(selected_provider, api_key)
    
    # Main content area
    st.header("Email Configuration")
    
    system_prompt = st.text_area(
        "System Prompt (Optional)",
        help="Set the behavior and context for the AI. Leave empty to use default behavior.",
        height=100
    )
    
    user_prompt = st.text_area(
        "Email Request",
        placeholder="Example: Draft a follow-up email for a customer who hasn't responded in 2 weeks regarding their product inquiry",
        height=100,
        key="user_prompt"
    )
    
    if st.button("Generate Email"):
        if user_prompt:
            with st.spinner("Generating email..."):
                generated_email = generate_email(
                    client,
                    selected_provider,
                    selected_model,
                    system_prompt,
                    user_prompt,
                    temperature,
                    top_p
                )
                st.markdown("### Generated Email:")
                st.markdown(generated_email)
        else:
            st.error("Please provide an email request.")
    
    # Display some example prompts
    with st.expander("Example Prompts"):
        st.markdown("""
        - Draft a follow-up email for a customer who hasn't responded in 2 weeks
        - Write a thank you email to a client after a successful meeting
        - Create an email to announce a new product launch to existing customers
        - Draft an email following up on a job application
        """)

if __name__ == "__main__":
    main()
