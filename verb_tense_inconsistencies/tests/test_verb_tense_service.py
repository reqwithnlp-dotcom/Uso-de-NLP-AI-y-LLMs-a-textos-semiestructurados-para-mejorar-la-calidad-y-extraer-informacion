from service import VerbTenseService
from models.error_code import ErrorCode


def test_service_should_accept_consistent_requirement():
    service = VerbTenseService()

    text = (
        "When a registered user submits a new purchase request, "
        "the system validates the required information, verifies the available stock "
        "and stores the request in the database. "
        "After the validation process, the system sends a confirmation notification "
        "to the user and records the operation for auditing purposes."
    )

    response = service.analyze(text)

    connector_issues = [
        issue
        for issue in response.issues
        if issue.error_code == ErrorCode.CONNECTOR_MISMATCH
    ]

    assert connector_issues == []


def test_service_should_detect_inconsistent_tense_in_requirement():
    service = VerbTenseService()

    text = (
        "When a registered user submits a new purchase request, "
        "the system validates the required information and verified the available stock. "
        "The system then stores the request in the database and sends a confirmation "
        "notification to the user."
    )

    response = service.analyze(text)

    connector_issues = [
        issue
        for issue in response.issues
        if issue.error_code == ErrorCode.CONNECTOR_MISMATCH
    ]

    assert len(connector_issues) == 1

    issue = connector_issues[0]

    assert "validates" in issue.fragment
    assert "verified" in issue.fragment


def test_service_should_detect_inconsistency_between_multiple_actions():
    service = VerbTenseService()

    text = (
        "The payment processing service receives the transaction request, "
        "validates the customer information, checked the payment method "
        "and sends the transaction to the external payment provider. "
        "If the provider accepts the transaction, the system stores the result "
        "and notifies the customer."
    )

    response = service.analyze(text)

    connector_issues = [
        issue
        for issue in response.issues
        if issue.error_code == ErrorCode.CONNECTOR_MISMATCH
    ]

    assert len(connector_issues) >= 1


def test_service_should_accept_multiple_actions_in_same_tense():
    service = VerbTenseService()

    text = (
        "The order management system receives the order from the client application, "
        "validates the requested products, calculates the total amount "
        "and stores the order information. "
        "The system also generates an order identifier and returns the result "
        "to the client application."
    )

    response = service.analyze(text)

    connector_issues = [
        issue
        for issue in response.issues
        if issue.error_code == ErrorCode.CONNECTOR_MISMATCH
    ]

    assert connector_issues == []


def test_service_should_accept_different_aspects_of_same_tense():
    service = VerbTenseService()

    text = (
        "The document management system validates the uploaded file "
        "and has stored the document metadata in the repository. "
        "The system then generates a reference identifier that allows "
        "other services to retrieve the document."
    )

    response = service.analyze(text)

    connector_issues = [
        issue
        for issue in response.issues
        if issue.error_code == ErrorCode.CONNECTOR_MISMATCH
    ]

    assert connector_issues == []


def test_service_should_detect_issue_only_in_affected_requirement_sentence():
    service = VerbTenseService()

    text = (
        "The authentication service receives the user's credentials "
        "and validates them against the identity provider. "
        "If the credentials are valid, the system generates an access token "
        "and returned it to the client application. "
        "The client application stores the token and uses it for subsequent requests."
    )

    response = service.analyze(text)

    assert len(response.fragments) == 3

    connector_issues = [
        issue
        for issue in response.issues
        if issue.error_code == ErrorCode.CONNECTOR_MISMATCH
    ]

    assert len(connector_issues) == 1

    assert "generates" in connector_issues[0].fragment
    assert "returned" in connector_issues[0].fragment


def test_service_should_handle_long_requirement_with_or_connector():
    service = VerbTenseService()

    text = (
        "When the inventory level reaches the configured minimum threshold, "
        "the system creates a replenishment request or notified the warehouse manager "
        "according to the configured replenishment strategy. "
        "The system records the selected action and stores the corresponding timestamp "
        "for future auditing."
    )

    response = service.analyze(text)

    connector_issues = [
        issue
        for issue in response.issues
        if issue.error_code == ErrorCode.CONNECTOR_MISMATCH
    ]

    assert len(connector_issues) == 1

    assert "creates" in connector_issues[0].fragment
    assert "notified" in connector_issues[0].fragment


def test_service_should_handle_long_requirement_with_but_connector():
    service = VerbTenseService()

    text = (
        "The notification service receives the event generated by the order system "
        "and validates the destination address, but sent the notification only "
        "when the configured delivery conditions are satisfied. "
        "The service records the delivery attempt and stores the provider response."
    )

    response = service.analyze(text)

    connector_issues = [
        issue
        for issue in response.issues
        if issue.error_code == ErrorCode.CONNECTOR_MISMATCH
    ]

    assert len(connector_issues) == 1


def test_service_should_detect_invalid_present_perfect_structure():
    service = VerbTenseService()

    text = (
        "When the user submits a new support request, "
        "the system has validate the mandatory fields before processing the ticket. "
        "If the information is complete, the system assigns the request "
        "to the corresponding support queue."
    )

    response = service.analyze(text)

    auxiliary_issues = [
        issue
        for issue in response.issues
        if issue.error_code == ErrorCode.AUXILIARY_MISMATCH
    ]

    assert len(auxiliary_issues) == 1

    assert "has validate" in auxiliary_issues[0].fragment


def test_service_should_detect_invalid_past_perfect_structure():
    service = VerbTenseService()

    text = (
        "Before the batch process started, "
        "the system had process all pending transactions from the previous execution. "
        "After completing the validation stage, the application stores "
        "the execution summary for auditing purposes."
    )

    response = service.analyze(text)

    auxiliary_issues = [
        issue
        for issue in response.issues
        if issue.error_code == ErrorCode.AUXILIARY_MISMATCH
    ]

    assert len(auxiliary_issues) == 1

    assert "had process" in auxiliary_issues[0].fragment


def test_service_should_detect_invalid_present_continuous_structure():
    service = VerbTenseService()

    text = (
        "While the administrator reviews the configuration, "
        "the monitoring service is generate diagnostic information "
        "for each active component. "
        "The system stores the generated information "
        "and makes it available through the administration interface."
    )

    response = service.analyze(text)

    auxiliary_issues = [
        issue
        for issue in response.issues
        if issue.error_code == ErrorCode.AUXILIARY_MISMATCH
    ]

    assert len(auxiliary_issues) == 1

    assert "is generate" in auxiliary_issues[0].fragment


def test_service_should_detect_invalid_future_structure():
    service = VerbTenseService()

    text = (
        "When the nightly synchronization process begins, "
        "the system will validates every record received from the external provider. "
        "Records that pass validation are stored in the local repository "
        "and become available to the reporting service."
    )

    response = service.analyze(text)

    auxiliary_issues = [
        issue
        for issue in response.issues
        if issue.error_code == ErrorCode.AUXILIARY_MISMATCH
    ]

    assert len(auxiliary_issues) == 1

    assert "will validates" in auxiliary_issues[0].fragment


def test_service_should_detect_invalid_future_perfect_structure():
    service = VerbTenseService()

    text = (
        "By the time the reporting process starts, "
        "the system will have generate all required aggregation records. "
        "The reporting module reads those records "
        "and generates the final operational report."
    )

    response = service.analyze(text)

    auxiliary_issues = [
        issue
        for issue in response.issues
        if issue.error_code == ErrorCode.AUXILIARY_MISMATCH
    ]

    assert len(auxiliary_issues) == 1

    assert "will have generate" in auxiliary_issues[0].fragment

def test_service_should_report_multiple_invalid_verb_structures():
    service = VerbTenseService()

    text = (
        "When the operator starts the reconciliation process, "
        "the system has load all pending transactions from the repository. "
        "The validation module is compare each transaction with the external source. "
        "After the comparison finishes, the reporting service will generates "
        "a summary containing every detected discrepancy."
    )

    response = service.analyze(text)

    auxiliary_issues = [
        issue
        for issue in response.issues
        if issue.error_code == ErrorCode.AUXILIARY_MISMATCH
    ]

    assert len(auxiliary_issues) == 3

    fragments = [
        issue.fragment
        for issue in auxiliary_issues
    ]

    assert "has load" in fragments
    assert "is compare" in fragments
    assert "will generates" in fragments