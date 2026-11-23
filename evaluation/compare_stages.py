"""Compare stage outputs using reviewer annotations; no auto-claimed accuracy."""
from evaluation.coverage import calculate_coverage

def stage_summary(stages,reviewed):
    return {'stages':list(stages),'reviewed_coverage':calculate_coverage(reviewed),
            'note':'Accuracy/hallucination require human review of each claim and source.'}
