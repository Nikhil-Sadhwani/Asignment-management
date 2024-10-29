from flask import Blueprint
from core.models.teachers import Teacher
from core.apis.responses import APIResponse
from core.apis import decorators

from .schema import TeacherSchema

principal_teachers_resources = Blueprint('principal_teachers', __name__)

@principal_teachers_resources.route('/teachers', methods=['GET'])
@decorators.authenticate_principal
def get_all_teachers_list(p):
    # Fetch teachers list from the database (implement this function)
    teachers_list = Teacher.get_all_teacher()
    teachers_list_dump = TeacherSchema().dump(teachers_list, many=True)
    return APIResponse.respond(data=teachers_list_dump)

