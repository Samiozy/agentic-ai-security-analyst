"""Coverage accounting with manual adjudication, avoiding fake precision.

A retrieved candidate does not count as grounded until a human marks it valid.
"""
def calculate_coverage(adjudications):
    values=list(adjudications)
    total=len(values)
    grounded=sum(x.get('verified_grounded') is True for x in values)
    return {'total':total,'verified_grounded':grounded,'coverage_fraction':grounded/total if total else None,
            'gap_or_unverified':total-grounded}
