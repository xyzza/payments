from payments.transfer import OperationStatusEnum


def process_credit_operation(operation_id: int) -> OperationStatusEnum:
    raise NotImplementedError()
    return 'operation status / ACCEPTED / FAILED'


def process_transfer_operation(operation_id: int) -> OperationStatusEnum:
    raise NotImplementedError()
    return 'operatino status / ACCEPTED / FAILED'


