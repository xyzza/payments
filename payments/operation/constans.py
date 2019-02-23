class OperationStatusEnum:

    DRAFT = 'DRAFT'
    PROCESSING = 'PROCESSING'
    ACCEPTED = 'ACCEPTED'
    FAILED = 'FAILED'

    COUNT = {
        DRAFT: 1,
        PROCESSING: 2,
        ACCEPTED: 3,
        FAILED: 3
    }


class OperationTypeEnum:

    CREDIT = 1
    TRANSFER = 2
