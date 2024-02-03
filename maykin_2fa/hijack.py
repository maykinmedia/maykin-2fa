from hijack.permissions import superusers_only  # the library default

from .typing import VerifiableUser


def superusers_only_and_is_verified(
    *, hijacker: VerifiableUser, hijacked: VerifiableUser
):
    return hijacker.is_verified() and superusers_only(
        hijacker=hijacker, hijacked=hijacked
    )
