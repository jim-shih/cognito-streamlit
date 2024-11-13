import os

import boto3
import botocore.exceptions
import streamlit as st
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# AWS Cognito configuration
USER_POOL_ID = os.getenv("USER_POOL_ID")
CLIENT_ID = os.getenv("USER_POOL_CLIENT_ID")
REGION_NAME = os.getenv("USER_POOL_REGION_NAME")

# Initialize Cognito Identity Provider Client
session = boto3.Session(
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    aws_session_token=os.getenv("AWS_SESSION_TOKEN"),
)
client = session.client("cognito-idp", region_name=REGION_NAME)


def initiate_auth(username, password):
    try:
        response = client.initiate_auth(
            ClientId=CLIENT_ID,
            AuthFlow="USER_PASSWORD_AUTH",
            AuthParameters={"USERNAME": username, "PASSWORD": password},
        )
        return response
    except client.exceptions.NotAuthorizedException:
        st.error("Incorrect username or password")
    except client.exceptions.UserNotFoundException:
        st.error("User does not exist")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
    return None


def main():
    st.title("AWS Cognito Authentication")

    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if not st.session_state.authenticated:
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            response = initiate_auth(username, password)
            if response and "AuthenticationResult" in response:
                st.session_state.authenticated = True
                st.session_state.access_token = response["AuthenticationResult"][
                    "AccessToken"
                ]
                st.session_state.id_token = response["AuthenticationResult"]["IdToken"]
                st.session_state.refresh_token = response["AuthenticationResult"][
                    "RefreshToken"
                ]
                st.rerun()
    else:
        st.write("You are logged in!")
        if st.button("Logout"):
            for key in ["authenticated", "access_token", "id_token", "refresh_token"]:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()

        # Protected content
        st.write("This is protected content only visible to authenticated users.")


if __name__ == "__main__":
    main()
