import json
from flask import Blueprint, jsonify, request
from core.models.assignments import Assignment
from core.apis.responses import APIResponse
from core.apis import decorators
from core import db

from .schema import AssignmentSchema, AssignmentGradeSchema

principal_assignments_resources = Blueprint('principal_assignments', __name__)

@principal_assignments_resources.route('/assignments', methods=['GET'])
@decorators.authenticate_principal
def get_principal_assignments(p):
    # Fetch assignments from the database (implement this function)
    assignments = Assignment.get_assignments_for_principal()
    assignments_dump = AssignmentSchema().dump(assignments, many=True)
    return APIResponse.respond(data=assignments_dump)


@principal_assignments_resources.route('/assignments/grade', methods=['POST'], strict_slashes=False)
@decorators.accept_payload
@decorators.authenticate_principal
def get_grade_assignments(p, incoming_payload):
    """Grade an assignment"""
    grade_assignment_payload = AssignmentGradeSchema().load(incoming_payload)

    graded_assignment = Assignment.mark_grade(
        _id=grade_assignment_payload.id,
        grade=grade_assignment_payload.grade,
        auth_principal=p
    )
    db.session.commit()
    graded_assignment_dump = AssignmentSchema().dump(graded_assignment)
    return APIResponse.respond(data=graded_assignment_dump)

