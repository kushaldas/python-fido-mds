# -*- coding: utf-8 -*-

import pytest
from fido2.utils import websafe_decode

from fido_mds.exceptions import MetadataValidationError
from fido_mds.metadata_store import FidoMetadataStore
from fido_mds.models.webauthn import Attestation
from fido_mds.tests.data import YUBIKEY_4, YUBIKEY_5_NFC, IPHONE_12, MICROSOFT_SURFACE_1796, NEXUS_5

__author__ = 'lundberg'


mds = FidoMetadataStore()


@pytest.mark.parametrize('attestation_obj,client_data', [YUBIKEY_4, YUBIKEY_5_NFC, MICROSOFT_SURFACE_1796, NEXUS_5])
def test_verify(attestation_obj, client_data):
    att = Attestation.from_base64(attestation_obj)
    cd = websafe_decode(client_data)
    assert mds.verify_attestation(attestation=att, client_data=cd) is True


# test attestations with short-lived certs so metadata can't be validated
@pytest.mark.parametrize('attestation_obj,client_data', [IPHONE_12])
def test_verify_no_validate(attestation_obj, client_data):
    att = Attestation.from_base64(attestation_obj)
    cd = websafe_decode(client_data)
    with pytest.raises(MetadataValidationError):
        mds.verify_attestation(attestation=att, client_data=cd)
