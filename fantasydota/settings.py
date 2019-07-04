SOCIAL_AUTH_USER_MODEL = 'fantasydota.models.User'
SOCIAL_AUTH_LOGIN_FUNCTION = 'fantasydota.auth.login_user'
SOCIAL_AUTH_LOGGEDIN_FUNCTION = 'fantasydota.auth.login_required'

SOCIAL_AUTH_LOGIN_URL = '/done'
SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/done'

SOCIAL_AUTH_AUTHENTICATION_BACKENDS = (
    'social_core.backends.facebook.FacebookOAuth2',
    'social_core.backends.open_id.OpenIdAuth',  # for Google authentication
    'social_core.backends.google.GoogleOpenId',  # for Google authentication
    'social_core.backends.google.GoogleOAuth2',
    'social_core.backends.steam.SteamOpenId'
)

# Google OAuth2 (google-oauth2)
SOCIAL_AUTH_GOOGLE_OAUTH2_IGNORE_DEFAULT_SCOPE = True
SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = [
'https://www.googleapis.com/auth/userinfo.email',
'https://www.googleapis.com/auth/userinfo.profile'
]

# Google+ SignIn (google-plus)
SOCIAL_AUTH_GOOGLE_PLUS_IGNORE_DEFAULT_SCOPE = True
SOCIAL_AUTH_GOOGLE_PLUS_SCOPE = [
'https://www.googleapis.com/auth/plus.login',
'https://www.googleapis.com/auth/userinfo.email',
'https://www.googleapis.com/auth/userinfo.profile'
]

SOCIAL_AUTH_GOOGLE_OAUTH2_USE_DEPRECATED_API = True
SOCIAL_AUTH_GOOGLE_PLUS_USE_DEPRECATED_API = True

# # Specified key was too long mysql social auth bug
# SOCIAL_AUTH_UID_LENGTH = 128
# SOCIAL_AUTH_NONCE_SERVER_URL_LENGTH = 128
# SOCIAL_AUTH_ASSOCIATION_SERVER_URL_LENGTH = 128
# SOCIAL_AUTH_ASSOCIATION_HANDLE_LENGTH = 128

SOCIAL_AUTH_TRAILING_SLASH = True

SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.auth_allowed',
    'social_core.pipeline.social_auth.social_user',
    'fantasydota.lib.account.get_non_unique_username',
    #'social_core.pipeline.user.get_username',
    'fantasydota.lib.account.create_user',
    #'social_core.pipeline.user.create_user',
    'social_core.pipeline.social_auth.associate_user',
    #'social_core.pipeline.debug.debug',
    'social_core.pipeline.social_auth.load_extra_data',
    #'social_core.pipeline.user.user_details',
)
    #'social_core.pipeline.debug.debug')