"""
@file
@brief Helper about encryption.
"""
import jwt


def encrypt_password(pwd, secret):
    """
    Encrypts one password.

    @param      pwd     string
    @param      secret  secret
    @return             encrypted password
    """
    return jwt.encode({'token': pwd}, secret, algorithm='HS256').decode('ascii')


def encrypt_passwords(users, secret):
    """
    Encrypts users passwords.

    @param      users   dataframe or...
    @param      secret  secret
    @return             password are replaced by the encrypted passwords
    """
    if isinstance(users, list):
        res = []
        for login, pwd in users:
            pwd = encrypt_password(pwd, secret)
            res.append((login, pwd))
        return res
    elif hasattr(users, "values"):
        df = users.copy()
        col = df.columns[1]
        df[col] = df[col].apply(lambda pwd: encrypt_password(pwd, secret))
        return df
    else:
        raise TypeError("Unexpected type '{0}'".format(type(users)))
