import io
import csv


def to_csv(rows):

    buffer = io.StringIO()

    writer = csv.writer(buffer, delimiter=';', quotechar='|')
    writer.writerows(rows)

    return buffer.getvalue()
