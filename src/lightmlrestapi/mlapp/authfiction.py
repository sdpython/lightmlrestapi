"""
@file
@brief Authentification part.
"""
import falcon
from ..args import encrypt_password, load_passwords


class AuthMiddleware:
    """
    Authentification. The name and secret comes from
    a file. The file must store encrypted password.
    """

    help_url = "http://www.xavierdupre.fr/app/lightmlrestapi/helpsphinx/tutorial/first_rest_api.html"

    def __init__(self, source, algo="sha224"):
        """
        @param      source      filename or dataframe for encrypted password
        @param      algo        algorithm used to hash the passwords
        """
        if source is None:
            raise ValueError("source cannot be empty")
        self.allowed = load_passwords(source)
        self.algo = algo

    def process_request(self, req, resp):
        """
        Processes an authentification request.

        @param  req     request
        @param  resp    unused
        """
        if req.protocol.lower() != 'https':
            raise falcon.HTTPBadRequest(title='HTTPS Required',
                                        description=('All requests must be performed via the HTTPS protocol. '
                                                     'Please switch to HTTPS and try again.'))

        token = req.get_header('token')
        account_id = req.get_header('uid')

        challenges = ['Token type="Fernet"']

        if token is None:
            description = (
                'Please provide an auth token as part of the request.')
            raise falcon.HTTPUnauthorized('Authentification token required',
                                          description, challenges,
                                          href=AuthMiddleware.help_url)

        if not self._token_is_valid(token, account_id):
            description = (
                'The provided auth token is not valid. Please request a new token and try again.')
            raise falcon.HTTPUnauthorized('Authentication required',
                                          description, challenges,
                                          href=AuthMiddleware.help_url)

    def _token_is_valid(self, token, account_id):
        """
        Decides if it is valid or not.
        """
        if account_id not in self.allowed:
            return False
        enc = encrypt_password(token, algo=self.algo)
        return self.allowed[account_id] == enc
