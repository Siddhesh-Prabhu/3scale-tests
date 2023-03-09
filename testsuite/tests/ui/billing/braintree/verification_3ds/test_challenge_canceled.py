"""
Successful Challenge Authentication:
Cardholder enrolled, authentication successful, and signature verification successful.
"""
import pytest
from threescale_api.errors import ApiClientError


def test_cancel_challenge(setup_card, create_api_invoice):
    """
    Test scenario: Cardholder enrolled, authentication successful, and signature verification successful:
        - Add CC details for an account
        - Cancel 3DS challenge
        - Verify that CC was not added
    """
    cc_view = setup_card("4000000000001091")
    cc_view.challenge_form.cancel()
    assert cc_view.alert() == "An error occurred, please review your CC details or try later."

    invoice = create_api_invoice()
    with pytest.raises(ApiClientError) as exc_info:
        invoice.charge()

    assert exc_info.type is ApiClientError
    assert "422 Unprocessable Entity" in exc_info.value.args[0]
    assert "Failed to charge the credit card" in exc_info.value.args[0]
