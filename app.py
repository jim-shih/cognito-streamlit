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
# if you want to use session to connect to cognito instead of client then use below code
# session = boto3.Session(
#     aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
#     aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
#     aws_session_token=os.getenv("AWS_SESSION_TOKEN"),
# )
# client = session.client("cognito-idp", region_name=REGION_NAME)

client = boto3.client("cognito-idp", region_name=REGION_NAME)


def _initiate_auth(username, password):
    try:
        response = client.initiate_auth(
            ClientId=CLIENT_ID,
            AuthFlow="USER_PASSWORD_AUTH",
            AuthParameters={
                "USERNAME": username,
                "PASSWORD": password
            },
        )
        return response
    except client.exceptions.NotAuthorizedException:
        st.error("Incorrect username or password")
    except client.exceptions.UserNotFoundException:
        st.error("User does not exist")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
    return None


def _check_user_exists(username):
    try:
        response = client.admin_get_user(UserPoolId=USER_POOL_ID,
                                         Username=username)
        return response
    except client.exceptions.UserNotFoundException:
        st.error("User does not exist")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
    return None


def _delete_user(username):
    try:
        response = client.admin_delete_user(UserPoolId=USER_POOL_ID,
                                            Username=username)
        return response
    except client.exceptions.UserNotFoundException:
        st.error("User does not exist")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
    return None


def _sign_up(username, password):
    try:
        response = client.sign_up(
            ClientId=CLIENT_ID,
            Username=username,
            Password=password,
            UserAttributes=[{
                "Name": "email",
                "Value": username
            }],
        )
        st.success(
            "Sign-up successful. Please check your email for the verification code."
        )
        st.session_state["show_verification"] = True
        st.session_state["username"] = username
        return response
    except client.exceptions.UsernameExistsException:
        st.error("Username already exists")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")


def _confirm_sign_up(username, verification_code):

    try:
        response = client.confirm_sign_up(ClientId=CLIENT_ID,
                                          Username=username,
                                          ConfirmationCode=verification_code)
        st.success("Account verification successful. You can now login.")
        st.session_state["user_created"] = True
        st.session_state["email_verified"] = True
        return response
    except client.exceptions.CodeMismatchException:
        st.error("Incorrect verification code")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")


def _resent_verification_code(username):
    try:
        response = client.resend_confirmation_code(ClientId=CLIENT_ID,
                                                   Username=username)

        st.success("Verification code resent successfully")
        st.session_state["user_created"] = True
        return response
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")


def user_login_page():
    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):

        response = _initiate_auth(username, password)
        if response:
            st.balloons()
            st.success("Login successful")
            st.session_state["access_token"] = response[
                "AuthenticationResult"]["AccessToken"]
            st.session_state["refresh_token"] = response[
                "AuthenticationResult"]["RefreshToken"]
            st.session_state["id_token"] = response["AuthenticationResult"][
                "IdToken"]
            st.session_state["username"] = username
            st.session_state["authenticated"] = True


def user_signup_page():
    st.title("Sign Up")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    st.session_state["user_created"] = False
    st.session_state["email_verified"] = False
    if st.button("Sign Up"):
        _sign_up(username, password)

    if st.session_state.get("show_verification"):
        verification_code = st.text_input("Verification Code")
        if st.button("Verify"):
            _confirm_sign_up(st.session_state["username"], verification_code)
        if st.button("Resend Verification Code"):
            _resent_verification_code(st.session_state["username"])


def main():
    st.title("Cognito Authentication")
    st.sidebar.title("Menu")
    menu = ["Login", "Sign Up"]
    choice = st.sidebar.selectbox("Select Option", menu)

    if choice == "Login":
        user_login_page()
    elif choice == "Sign Up":
        user_signup_page()


if __name__ == "__main__":
    main()
