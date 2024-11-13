Certainly! I'll modify the README to include information about using Poetry for package management and the boto3 session manager. Here's the updated version:

# Streamlit AWS Cognito Authentication

This project demonstrates how to implement AWS Cognito user authentication in a Streamlit application. It provides a secure way to manage user access to your Streamlit app using AWS Cognito's robust identity management services, with Poetry for dependency management and boto3 session manager for AWS interactions.

## Features

- User authentication using AWS Cognito
- Secure storage of AWS credentials using environment variables
- Simple Streamlit interface for login and logout
- Protected content visible only to authenticated users
- Poetry for dependency management
- boto3 session manager for AWS resource management

## Prerequisites

- Python 3.x
- AWS account with Cognito User Pool set up
- Basic understanding of Streamlit, AWS Cognito, and Poetry
- Poetry installed on your system

## Installation

1. Clone this repository:

   ```
   git clone https://github.com/jim-shih/streamlit-cognito-auth.git
   cd streamlit-cognito-auth
   ```

2. Install dependencies using Poetry:

   ```
   poetry install
   ```

3. Activate the Poetry virtual environment:
   ```
   poetry shell
   ```

## Configuration

1. Create a `.env` file in the project root directory with your AWS Cognito credentials:

   ```
   USER_POOL_ID=your-user-pool-id
   USER_POOL_CLIENT_ID=your-client-id
   USER_POOL_REGION_NAME=your-region

   AWS_ACCESS_KEY_ID=your-access-key-id
   AWS_SECRET_ACCESS_KEY=your-secret-access-key
   AWS_SESSION_TOKEN=your-session-token
   ```

2. Ensure your `.env` file is added to `.gitignore` to keep your credentials secure.

## Usage

1. Run the Streamlit app:

   ```
   poetry run streamlit run app.py
   ```

2. Open your web browser and navigate to `http://localhost:8501`.

3. Use the login form to authenticate with your AWS Cognito credentials.

4. Once logged in, you'll see the protected content.

5. Use the logout button to end your session.

## Code Structure

The main application file `app.py` includes:

- AWS Session management using boto3
- Cognito client initialization
- Authentication logic using Cognito User Pool
- Streamlit UI components for login/logout

Example of boto3 session manager usage:

```python
import boto3
from botocore.exceptions import ClientError

session = boto3.Session(
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    aws_session_token=os.getenv('AWS_SESSION_TOKEN')
)

cognito_client = session.client('cognito-idp', region_name=os.getenv('USER_POOL_REGION_NAME'))
```

## Customization

- Modify the `app.py` file to add your own Streamlit components and logic.
- Adjust the authentication flow in the `initiate_auth` function if needed.
- Update `pyproject.toml` to manage dependencies with Poetry.

## Security Notes

- Always use environment variables or secure secrets management for storing sensitive information.
- Implement proper error handling and logging in a production environment.
- Regularly update dependencies to ensure you have the latest security patches.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Streamlit for the amazing framework
- AWS for providing Cognito services
- Poetry for simplified dependency management
- All contributors and maintainers of the used libraries
