import base64
import datetime
import os
import time

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.core.mail import EmailMultiAlternatives
from django.http import JsonResponse, HttpResponse
from django.views.generic.base import View
from django_redis import get_redis_connection
from items.courses.models import Course
from items.groups.models import GroupOrg
from items.operations.models import UserCourse, UserGroup, Tag, UserTag, UserLikeTag, Authority, \
    Key, ProjectFile, ProjectComment
from items.projects.models import Project
from items.users.models import UserProfile
from django.core.cache import cache
import logging

logger = logging.getLogger(__name__)

r = get_redis_connection()
EXPIRE_TIME = 600


def get_from_request(request, arg):
    """
    A encapsulation of decoding request.
    :param request: The request from frontend.
    :param arg: The key.
    :return: The value of the key in request.
    """
    return eval(request.body.decode()).get(arg)


def delete_token(token):
    """
    Delete token from redis.
    :param token:
    :return:
    """
    cache.delete_pattern(token)


def check_token(token) -> bool:
    """
    Check if the token exists and is not expired. If the result is true, then
    the token is updated automatically.
    :param token: The token from frontend.
    :return: token exists and is not expired (user is online)
    """
    record = r.get(token)
    logger.debug('check_token(token) token: %s, record: %s', token, record)
    if record is None:
        return False
    update_token(token)
    return True


def update_token(token) -> None:
    r.expire(token, EXPIRE_TIME)


def create_token(sid, password):
    try:
        string = sid + ',' + password + ',' + str(time.time())
        token = base64.b64encode(string.encode("utf-8")).decode("utf-8")
        r.set(token, sid, EXPIRE_TIME)
        return token
    except Exception as e:
        logger.exception('create_token(sid, password) %s', e)
        return None


def get_sid(token):
    """
    Get corresponding sid from token. It is assumed that the token exists and is not expired.
    :param token: The token from frontend.
    :return: The sid.
    """
    try:
        stored_sid = r.get(token)
        if stored_sid is None:
            return None
        else:
            r.expire(token, EXPIRE_TIME)
            return stored_sid.decode()
    except Exception as e:
        logger.exception('get_sid(token) %s', e)
        return None


class GetIdentity(View):
    def post(self, request):
        """
        # TODO: Update doc.
        POST /get_identity/
        Get identity from token.
        :param request: The request from frontend.
        :return: {success, identity}/offline/failure
        """
        try:
            token = get_from_request(request, 'token')
            if check_token(token):
                sid = get_sid(token)
                users = UserProfile.objects.filter(student_id=sid)
                assert len(users) == 1
                user = users[0]
                if user.is_staff == 1:
                    response_data = {'attempt': 'success', 'identity': 'teacher'}
                else:
                    response_data = {'attempt': 'success', 'identity': 'student'}
            else:
                response_data = {'attempt': 'offline'}
            return JsonResponse(response_data)
        except Exception as e:
            logger.exception('%s %s', self, e)
            response_data = {'attempt': 'failure', 'identity': 'student'}
            return JsonResponse(response_data)



class Logout(View):
    def post(self, request):
        """
        TODO: Update doc.
        POST /logout/
        Delete redis token and logout.
        :param request: The request from frontend.
        :return: success/offline/failure
        """
        try:
            token = get_from_request(request, 'token')
            if check_token(token):
                delete_token(token)
                response_data = {'attempt': 'success'}
            else:
                response_data = {'attempt': 'offline'}
            logger.debug('%s logout %s', self, token)
            return JsonResponse(response_data)
        except Exception as e:
            logger.exception('%s %s', self, e)
            response_data = {'attempt': 'failure'}
            return JsonResponse(response_data)


class Login(View):
    """
        @method_decorator(ensure_csrf_cookie)
        # def get(self, request, *args, **kwargs):
        #     return render(request, "login.html")
    """

    def post(self, request):
        try:
            logger.debug('%s request.body %s', self, request.body)
            token = get_from_request(request, 'token')
            logger.debug('%s token %s', self, token)

            if token is not None and check_token(token):
                logger.debug('%s token login success', self)
                sid = get_sid(token)
                users = UserProfile.objects.filter(student_id=sid)
                for user in users:
                    if user.is_staff == 1:
                        logger.debug('%s staff login', self)
                        return JsonResponse({'loginCheck': 'teacher', 'token': token})
                    else:
                        logger.debug('%s student login', self)
                        return JsonResponse({'loginCheck': 'student', 'token': token})

            student_id = eval(request.body.decode()).get("sid")
            password = eval(request.body.decode()).get("pswd")

            # 通过用户名和密码确认数据库中是否有和user对应的记录
            user = UserProfile.objects.filter(student_id=student_id, password=password)
            # 如果能查询到相应记录
            if user.count() == 0:
                return JsonResponse({"LoginCheck": "failed"})
            # 如果未能查询到用户
            else:
                token = create_token(sid=student_id, password=password)
                logger.debug('%s new token %s', self, token)
                for i in user:
                    if i.is_staff == 1:
                        logger.debug('%s staff login', self)
                        return JsonResponse({'loginCheck': 'teacher', 'token': token})
                    else:
                        logger.debug('%s student login', self)
                        return JsonResponse({'loginCheck': 'student', 'token': token})
        except Exception as e:
            logger.debug('%s %s', self, e)
            return JsonResponse({"loginCheck": "failed"})


class ShowOtherPersonalData(View):
    # 当用户按下登录按键时
    def post(self, request):
        try:
            token = eval(request.body.decode()).get("token")
            t_id = eval(request.body.decode()).get("sid_target")

            # 通过用户名和密码确认数据库中是否有和user对应的记录

            x = UserProfile.objects.get(student_id=t_id)

            return JsonResponse({"ShowOtherPersonalDataCheck": "ShowPersonalData success!",
                                 "sid": t_id,
                                 "realname": x.real_name,
                                 "student_id": x.student_id,
                                 "gender": x.gender,
                                 "address": x.address,
                                 "email": x.email,
                                 "mobile": x.mobile,
                                 "image": None
                                 })

            # return JsonResponse({"ShowPersonalData": "success"})

        except Exception as e:
            logger.debug('%s %s', self, e)
            return JsonResponse({"ShowOtherPersonalDataCheck": "failed"})


class ChangePassword(View):
    # 当用户按下登录按键时
    def post(self, request):
        try:
            print(request.body)

            student_id = eval(request.body.decode()).get("sid")
            old_password = eval(request.body.decode()).get("old")
            new_password = eval(request.body.decode()).get("new")

            # 通过用户名和密码确认数据库中是否有和user对应的记录
            user = UserProfile.objects.filter(student_id=student_id, password=old_password)
            # 如果能查询到相应记录
            if user.count() == 0:
                return JsonResponse({"ChangePasswordCheck": "failed"})
            # 如果未能查询到用户
            else:
                user.update(password=new_password)
                return JsonResponse({"ChangePasswordCheck": "success"})

        except Exception as e:
            return JsonResponse({"ChangePasswordCheck": "failed"})


class ShowPersonalData(View):
    def post(self, request):
        """
        # TODO: Update doc.
        POST /show_personal_data/
        :param request: The request from frontend.
        :return: Personal profile of a user.
        """
        try:
            logger.debug('%s request.body: %s', self, request.body)
            token = get_from_request(request, 'token')
            logger.debug('%s token %s', self, token)

            if check_token(token):
                sid = get_sid(token)
                profile = UserProfile.objects.get(student_id=sid)
                response_data = {'attempt': 'success',
                                 'realName': profile.real_name,
                                 'sid': profile.student_id,
                                 'gender': profile.gender,
                                 'address': profile.address,
                                 'email': profile.email,
                                 'mobile': profile.mobile,
                                 'imageUrl': 'Not Implemented Feature',
                                 }
                return JsonResponse(response_data)

            # TODO: Implement avatar feature.
            arr = request.FILES.keys()
            file_name = ''

            for k in arr:
                file_name = k

            if file_name != '':
                file = request.FILES.get(file_name)
                path = default_storage.save('tmp/' + file_name + ".jpg",
                                            ContentFile(file.read()))  # 根据名字存图(无类型)

        except Exception as e:
            logger.debug('%s %s', self, e)
            response_data = {'attempt': 'failure'}
            return JsonResponse(response_data)


class ChangePersonalData(View):
    # {student_id:string, password:string, email: string, gender: string, mobile: string, address: string}
    def post(self, request):
        """
        POST /change_personal_data/
        :param request: The request from frontend.
        :return: success/failure/offline
        """
        try:
            token = get_from_request(request, 'token')
            if check_token(token):
                sid = get_sid(token)
                email = get_from_request(request, 'email')
                gender = get_from_request(request, 'gender')
                mobile = get_from_request(request, 'mobile')
                address = get_from_request(request, 'address')
                query_set = UserProfile.objects.filter(student_id=sid)
                if query_set.count == 0:
                    logger.debug('%s No such user.', self)
                    response_data = {'attempt': 'failure'}
                    return JsonResponse(response_data)
                query_set.update(email=email, gender=gender, mobile=mobile, address=address)
                logger.debug('%s Personal profile of %s is changed', self, sid)
                response_data = {'attempt': 'success'}
                return JsonResponse(response_data)
            else:
                response_data = {'attempt': 'offline'}
                return JsonResponse(response_data)

        except Exception as e:
            logger.debug('%s %s', self, e)
            response_data = {'attempt': 'failure'}
            return JsonResponse(response_data)


class UploadFile(View):

    def post(self, request):
        try:
            print(request.body)

            file_obj = request.FILES.get('file', None)

            if not file_obj:
                return JsonResponse({"UploadFileCheck": "failed"})
            else:
                print("file_obj", file_obj.name)

                file_path = os.path.join('static', 'files_uploaded', file_obj.name)

                print("file_path", file_path)

                with open(file_path, 'wb+') as f:
                    for chunk in file_obj.chunks():
                        f.write(chunk)

                return JsonResponse({"UploadFileCheck": "success"})

        except Exception as e:
            return JsonResponse({"UploadFileCheck": "failed"})


class DownloadFile(View):
    def post(self, request):
        try:
            print(request.body)

            path = eval(request.body.decode()).get("path")
            file_name = eval(request.body.decode()).get("file_name")

            file_obj = open(path, 'rb')

            response = HttpResponse(file_obj)
            response['Content-Type'] = 'application/octet-stream'
            response['Content-Disposition'] = "attachment;filename=" + file_name
            return response
        except Exception as e:
            return JsonResponse({"DownloadFile": "failed"})


class Test(View):
    def get(self, request):
        logger.debug('%s request %s', self, request)
        logger.debug('%s request.body %s', self, request.body)
        logger.debug('%s request.GET %s', self, request.GET)
        try:
            token = request.GET['token']
            sid = get_sid(token)
            logger.debug('%s sid %s', self, sid)
            with open('head_images/11811001/2020_11_23_07_49_55/file.jpg', 'rb') as f:
                return HttpResponse(f.read(), content_type='image/jpeg')
        except Exception as e:
            logger.debug('%s %s', self, e)
            student_id = "11811002"
            password = "123"
            # get file

            file = open('LinuxLogo.jpg', 'wb+')
            print(file)
            path = default_storage.save('static\head_images' + 'LinuxLogo' + '.jpg',
                                        file)  # 根据名字存图(无类型)

            response = HttpResponse(content_type='image/jpeg')
            return response

    def post(self, request):
        try:
            logger.debug('%s %s', self, request.body)
            arr = request.FILES.keys()
            print(arr)
            file_name = ''
            for k in arr:
                file_name = k

            sid = ''
            pswd = ''
            for k in request.POST:
                if str(k) == 'sid':
                    sid = str(request.POST[k])
                else:
                    pswd = str(request.POST[k])

            print(sid, pswd)

            if file_name != '':
                file = request.FILES.get(file_name)
                path = default_storage.save('tmp/' + file_name + ".jpg",
                                            ContentFile(file.read()))  # 根据名字存图(无类型)
                print(path)

            # 通过用户名和密码确认数据库中是否有和user对应的记录
            user = UserProfile.objects.filter(student_id=sid, password=pswd)
            # 如果能查询到相应记录
            if user.count() == 0:
                print('avatar fail')
                return JsonResponse({"ShowPersonalDataCheck": "ShowPersonalData failed!"})
            # 如果未能查询到用户
            else:
                print('avatar success')
                x = UserProfile.objects.get(student_id=sid, password=pswd)

                return JsonResponse({"ShowPersonalDataCheck": "ShowPersonalData success!",
                                     # "realname": x.real_name,
                                     # "student_id": x.student_id,
                                     # "gender": x.gender,
                                     # "address": x.address,
                                     # "email": x.email,
                                     # "mobile": x.mobile,
                                     "image": None
                                     })

            # return JsonResponse({"ShowPersonalData": "success"})

        except Exception as e:
            logger.exception('%s %s', self, e)
            return JsonResponse({"ShowPersonalData": "failed"})


class StudentGetsAllProjects(View):
    def post(self, request):
        """
        POST /student_gets_all_projects/
        :param request: The request from frontend.
        :return: {success, projects}/offline/failure
        """
        try:
            token = get_from_request(request, 'token')
            if check_token(token):
                projects = []
                student_id = get_sid(token)
                user = UserProfile.objects.filter(student_id=student_id)
                assert len(user) == 1
                user = user[0]
                courses = UserCourse.objects.filter(user_name_id=user.id)

                # Iterate over all courses one is visible to.
                for course in courses:
                    course_object = Course.objects.filter(id=course.course_name_id)
                    assert len(course_object) == 1
                    course_object = course_object[0]
                    name = course_object.name

                    # Get all projects one course has.
                    new_projects = Project.objects.filter(course_id=course_object.id)
                    for project in new_projects:
                        projects.append((project.id, name, project.name))

                response_data = {'attempt': 'success', 'projects': projects, 'sid': student_id}
                return JsonResponse(response_data)
            else:
                response_data = {'attempt': 'offline'}
                return JsonResponse(response_data)

        except Exception as e:
            logger.debug('%s %s', self, e)
            return JsonResponse({"StudentGetsAllProjectsCheck": "failure"})


class StudentGetsSingleProjectInformation(View):
    def post(self, request):
        """
        TODO: Update doc.
        POST /student_gets_single_project_information/
        :param request: The request from frontend.
        :return:{success,projectName,projectIntroduction,courseName}/offline/failure
        """
        try:
            token = get_from_request(request, 'token')
            if check_token(token):
                project_id = get_from_request(request, 'projectId')
                projects = Project.objects.filter(id=project_id)
                assert len(projects) == 1
                project = projects[0]
                courses = Course.objects.filter(id=project.course_id)
                assert len(courses) == 1
                course = courses[0]
                response_data = {'attempt': 'success',
                                 'projectName': project.name,
                                 'projectIntroduction': project.introduction,
                                 'courseName': course.name,
                                 'project_id': project_id}
            else:
                response_data = {'attempt': 'offline'}
            return JsonResponse(response_data)

        except Exception as e:
            logger.debug('%s %s', self, e)
            response_data = {'attempt': 'failure'}
            return JsonResponse(response_data)


class StudentGetsAllGroups(View):
    def post(self, request):
        try:
            token = eval(request.body.decode()).get("token")
            student_id = get_sid(token)
            user = UserProfile.objects.filter(student_id=student_id)
            group_id = ""
            for i in user:
                # 获得学生参加的所有队伍
                group_id = UserGroup.objects.filter(user_name_id=i.id)

            groups = {}
            for i in group_id:
                group_obj = GroupOrg.objects.filter(id=i.group_name_id)
                for j in group_obj:
                    group_name = j.group_name
                    groups[group_name] = {}
                    groups[group_name]["group_id"] = j.id

                    project_id = j.project_id
                    groups[group_name]["project_id"] = project_id
                    project = Project.objects.filter(id=project_id)
                    for k in project:
                        project_name = k.name
                        groups[group_name]["project_name"] = project_name
                        course_id = k.course_id
                        groups[group_name]["course_id"] = course_id
                        course = Course.objects.filter(id=course_id)
                        for l in course:
                            course_name = l.name
                            groups[group_name]["course_name"] = course_name
            return JsonResponse({"Data": groups})
        except Exception as e:
            return JsonResponse({"StudentGetsAllGroups": "failed"})

    # 返回{队伍名:{队伍id,项目id,项目名,课程id,课程名},}


class StudentGetsSingleGroupInformation(View):
    def post(self, request):
        try:
            group_id = eval(request.body.decode()).get("group_id")
            token = eval(request.body.decode()).get("token")
            student_id = get_sid(token)
            query_set = GroupOrg.objects.filter(id=group_id)

            group_name = ""
            group_detail = ""
            project_name = ""
            course_name = ""
            captain_name = ""
            captain_id = 0
            project_id = 0
            course_id = 0
            members = []

            for i in query_set:
                group_name = i.group_name
                group_detail = i.detail
                captain_id = i.captain_name_idS
                project_id = i.project_id

                query_set3 = Project.objects.filter(id=project_id)
                for j in query_set3:
                    project_name = j.name
                    course_id = j.course_id
                    query_set1 = Course.objects.filter(id=project_id)
                    for k in query_set1:
                        course_name = k.name

                query_set3 = UserProfile.objects.filter(id=captain_id)
                for j in query_set3:
                    captain_name = j.student_id

                query_set3 = UserGroup.objects.filter(id=group_id)
                for j in query_set3:
                    user_id = j.user_name_id
                    query_set1 = UserProfile.objects.filter(id=user_id)
                    for k in query_set1:
                        members.append(k.student_id)

            return JsonResponse({"group_name": group_name,
                                 "group_introduction": group_detail,
                                 "project_id": project_id,
                                 "project_name": project_name,
                                 "course_id": course_id,
                                 "course_name": course_name,
                                 "captain_name": captain_name,
                                 "members": members,
                                 })
        except Exception as e:
            logger.exception('%s %s', self, e)
            return JsonResponse({"StudentGetsSingleGroupInformation": "failed"})
        # 返回{队伍名，队伍简介,项目id,项目名,课程id,课程名,队长学号,[队伍成员1学号,队伍成员2学号,...]}


class StudentGetsGroupInformationInProject(View):
    def post(self, request):
        """
        TODO: Please avoid this kind of variable reuse. Extremely error-prone.
        TODO: Backend finishes it himself.
        :param request:
        :return:
        """
        try:
            project_id = eval(request.body.decode()).get("project_id")
            token = eval(request.body.decode()).get("token")
            student_id = get_sid(token)

            user = UserProfile.objects.filter(student_id=student_id)

            if user.count() == 0:
                return JsonResponse({"StudentGetsGroupInformationInProject": "failed"})

            for i in user:
                student_id = i.id

            group_id = 0

            group = UserGroup.objects.filter(user_name_id=student_id)

            if group.count() == 0:
                print('count', group)
                return JsonResponse({"StudentGetsGroupInformationInProject": "no group"})
            for i in group:
                project = GroupOrg.objects.filter(id=i.group_name_id)
                for j in project:
                    if j.project_id == int(project_id):
                        group_id = j.id
            if group_id == 0:
                return JsonResponse({"StudentGetsGroupInformationInProject": "no group"})
            query_set = GroupOrg.objects.filter(id=group_id)
            group_name = ""
            group_detail = ""
            project_name = ""
            course_name = ""
            captain_name = ""
            captain_id = 0
            project_id = 0
            course_id = 0
            members = []

            for i in query_set:
                group_name = i.group_name
                group_detail = i.detail
                captain_id = i.captain_name_id
                project_id = i.project_id

                query_set3 = Project.objects.filter(id=project_id)
                for j in query_set3:
                    project_name = j.name
                    course_id = j.course_id
                    query_set1 = Course.objects.filter(id=project_id)
                    for k in query_set1:
                        course_name = k.name

                query_set3 = UserProfile.objects.filter(id=captain_id)
                for j in query_set3:
                    captain_name = j.student_id

                query_set3 = UserGroup.objects.filter(id=group_id)
                for j in query_set3:
                    user_id = j.user_name_id
                    query_set1 = UserProfile.objects.filter(id=user_id)
                    for k in query_set1:
                        members.append(k.student_id)

            return JsonResponse({"group_name": group_name,
                                 "group_introduction": group_detail,
                                 "project_id": project_id,
                                 "project_name": project_name,
                                 "course_id": course_id,
                                 "course_name": course_name,
                                 "captain_name": captain_name,
                                 "members": members,
                                 "group_id": group_id,
                                 })
        except Exception as e:
            logger.exception('%s %s', self, e)
            return JsonResponse({"StudentGetsGroupInformationInProject": "failed"})
        # 返回{队伍名，队伍简介,项目id,项目名,课程id,课程名,队长学号,[队伍成员1学号,队伍成员2学号,...]}


class StudentCreatesGroup(View):
    def post(self, request):
        try:
            token = eval(request.body.decode()).get("token")
            student_id = get_sid(token)
            group_name = eval(request.body.decode()).get("group_name")
            introduction = eval(request.body.decode()).get("introduction")
            project_id = eval(request.body.decode()).get("project_id")

            query_set = UserProfile.objects.filter(student_id=student_id)
            captain_id = 0
            members = 1

            for i in query_set:
                captain_id = i.id

            # create group
            GroupOrg.objects.create(group_name=group_name,
                                    members=members,
                                    detail=introduction,
                                    captain_name_id=captain_id,
                                    project_id=project_id
                                    )

            # update user_group
            query_set = GroupOrg.objects.filter(group_name=group_name, captain_name_id=captain_id,
                                                project_id=project_id)
            for i in query_set:
                UserGroup.objects.create(group_name_id=i.id, user_name_id=captain_id)

            return JsonResponse({"CreatesGroupCheck": "success"})

        except Exception as e:
            return JsonResponse({"CreatesGroupCheck": "failed"})


class EditsGroupIntroduction(View):
    def post(self, request):
        try:
            token = eval(request.body.decode()).get("token")
            student_id = get_sid(token)
            group_id = eval(request.body.decode()).get("group_id")
            group_introduction = eval(request.body.decode()).get("group_introduction")

            GroupOrg.objects.filter(id=group_id).update(detail=group_introduction)

            # 后面可能要做站内信功能，记录谁修改了简介，所以先留着学号和密码

            return JsonResponse({"EditsGroupIntroductionCheck": "success"})

        except Exception as e:
            return JsonResponse({"EditsGroupIntroductionCheck": "failed"})


class EditsGroupName(View):
    def post(self, request):
        try:
            token = eval(request.body.decode()).get("token")
            student_id = get_sid(token)
            group_id = eval(request.body.decode()).get("group_id")
            group_name = eval(request.body.decode()).get("group_name")

            GroupOrg.objects.filter(id=group_id).update(group_name=group_name)

            return JsonResponse({"EditsGroupNameCheck": "success"})

        except Exception as e:
            return JsonResponse({"EditsGroupNameCheck": "failed"})


class GroupMemberValidation(View):
    def post(self, request):
        try:
            token = eval(request.body.decode()).get("token")
            student_id = get_sid(token)
            group_id = eval(request.body.decode()).get("group_id")

            user_id = 0

            query_set = UserProfile.objects.filter(student_id=student_id)
            for i in query_set:
                user_id = i.id

            query_set = UserGroup.objects.filter(user_name_id=user_id, group_name_id=group_id)
            if query_set.count() == 0:
                return JsonResponse({"GroupMemberValidation": "guest"})

            query_set = GroupOrg.objects.filter(id=group_id, captain_name_id=user_id)
            if query_set.count() == 0:
                return JsonResponse({"GroupMemberValidation": "member"})
            else:
                return JsonResponse({"GroupMemberValidation": "captain"})

        except Exception as e:
            return JsonResponse({"GroupMemberValidation": "failed"})


class StudentQuitsGroup(View):
    def post(self, request):
        try:
            group_id = eval(request.body.decode()).get("group_id")
            token = eval(request.body.decode()).get("token")
            student_id = get_sid(token)

            user = UserProfile.objects.filter(student_id=student_id)
            user_id = 0
            for i in user:
                user_id = i.id
            group = GroupOrg.objects.filter(group_name_id=group_id)
            mem = 0
            for i in group:
                mem = i.member - 1
            GroupOrg.objects.filter(group_name_id=group_id).update(member=mem)
            UserGroup.objects.delete(group_name_id=group_id, user_name_id=user_id)
            return JsonResponse({"StudentQuitGroupCheck": "success"})
        except Exception as e:
            return JsonResponse({"StudentQuitGroupCheck": "failed"})


class CaptainKickMember(View):
    def post(self, request):
        try:
            group_id = eval(request.body.decode()).get("group_id")
            token = eval(request.body.decode()).get("token")
            student_id = get_sid(token)
            target_id = eval(request.body.decode()).get("t_sid")
            group = GroupOrg.objects.filter(group_name_id=group_id)
            mem = 0
            for i in group:
                mem = i.member - 1
            GroupOrg.objects.filter(group_name_id=group_id).update(member=mem)
            UserGroup.objects.delete(group_name_id=group_id, user_name_id=target_id)
            return JsonResponse({"CaptainKickMemberCheck": "success"})
        except Exception as e:
            return JsonResponse({"CaptainKickMemberCheck": "failed"})


class CaptainDismissGroup(View):
    def post(self, request):
        try:
            group_id = eval(request.body.decode()).get("group_id")
            token = eval(request.body.decode()).get("token")
            student_id = get_sid(token)

            GroupOrg.objects.filter(group_name_id=group_id).delete()
            UserGroup.objects.filter(group_name_id=group_id).delete()
            return JsonResponse({"CaptainDismissGroupCheck": "success"})
        except Exception as e:
            return JsonResponse({"CaptainDismissGroupCheck": "failed"})


class CaptainGiveCaptain(View):
    def post(self, request):
        try:
            group_id = eval(request.body.decode()).get("group_id")
            token = eval(request.body.decode()).get("token")
            student_id = get_sid(token)
            target_id = eval(request.body.decode()).get("t_sid")

            user = UserProfile.objects.filter(student_id=target_id)
            if user.count() == 0:
                return JsonResponse({"CaptainGiveCaptainCheck": "fail"})
            else:
                for i in user:
                    target_id = i.id
            GroupOrg.objects.filter(group_name_id=group_id).update(captain_name_id=target_id)
            return JsonResponse({"CaptainGiveCaptainCheck": "success"})
        except Exception as e:
            return JsonResponse({"CaptainGiveCaptainCheck": "failed"})


class StudentGetAllGroupsInProject(View):
    def post(self, request):
        try:
            project_id = eval(request.body.decode()).get("project_id")
            token = eval(request.body.decode()).get("token")
            student_id = get_sid(token)
            groups = GroupOrg.objects.filter(project_id=project_id)
            project = Project.objects.filter(id=project_id)
            group = {}
            for i in project:
                group["group_size"] = i.group_size
                group["min_group_size"] = i.min_group_size
            for i in groups:
                group[i.id] = {}
                group[i.id]["group_name"] = i.group_name
                group[i.id]["member"] = i.member
                group[i.id]["captain_id"] = i.captain_name_id
                captain = UserProfile.objects.filter(student_id=i.captain_name_id)
                for j in captain:
                    group[i.id]["captain_name"] = j.student_id

            return JsonResponse({"Data": group, "StudentGetAllGroupsInProjectCheck": "success"})
        except Exception as e:
            return JsonResponse({"StudentGetAllGroupsInProjectCheck": "failed"})


class StudentGetAllStudentsInProject(View):
    def post(self, request):
        try:
            project_id = eval(request.body.decode()).get("project_id")
            token = eval(request.body.decode()).get("token")
            student_id = get_sid(token)
            groups = GroupOrg.objects.filter(project_id=project_id)
            project = Project.objects.filter(id=project_id)
            group = {}
            groupList = []
            for i in project:
                group["group_size"] = i.group_size
                group["min_group_size"] = i.min_group_size
                group["course_id"] = i.course_id
            for i in groups:
                group[i.id] = {}
                groupList.append(i.id)
                group[i.id]["group_name"] = i.group_name
                group[i.id]["member"] = i.member
            student = {}
            students = UserCourse.objects.filter(course_name_id=group["course_id"])
            for i in students:
                studentProfile = UserProfile.objects.filter(id=i.user_name_id)
                for j in studentProfile:
                    student[j.id] = {}
                    student[j.id]["username"] = j.student_id
                    student[j.id]["has_group"] = False
                    for k in groupList:
                        judge = UserGroup.objects.filter(group_name_id=k, user_name_id=j.id)
                        if judge.count() != 0:
                            student[j.id]["has_group"] = True
                            student[j.id]["group_id"] = k
                            student[j.id]["group_name"] = group[k]["group_name"]
                            student[j.id]["member"] = group[k]["member"]
                            break

            return JsonResponse({"Data": student, "StudentGetAllStudentsInProjectCheck": "success"})
        except Exception as e:
            return JsonResponse({"StudentGetAllStudentsInProjectCheck": "failed"})


class Image(View):
    # def post(self, request):
    #     print(request.body)
    #
    #     file_obj = request.FILES.get('image')
    #
    #     print("file_obj", file_obj.name)
    #
    #     BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    #
    #     file_path = os.path.join(BASE_DIR, 'static', 'head_images', file_obj.name)
    #     print("file_path", file_path)
    #     with open(file_path, 'wb+') as f:
    #         for chunk in file_obj.chunks():
    #             f.write(chunk)
    #
    #     message = {}
    #     message['code'] = 200
    #
    #     return JsonResponse(message)

    def post(self, request):
        try:
            # file = request.FILES.get('file')
            # print(type(file))
            # path = default_storage.save('tmp/'+str(request.FILES.get('file')), ContentFile(file.read()))  # 根据名字存图
            # return JsonResponse({
            #                          "image": file
            #                          })
            print(request.POST)
            arr = request.FILES.keys()
            print(arr)
            file_name = ''
            for k in arr:
                file_name = k

            sid = ''
            pswd = ''
            for k in request.POST:
                if str(k) == 'sid':
                    sid = str(request.POST[k])
                else:
                    pswd = str(request.POST[k])

            print(sid, pswd)

            if file_name != '':
                file = request.FILES.get(file_name)
                path = default_storage.save('tmp/' + file_name + ".jpg",
                                            ContentFile(file.read()))  # 根据名字存图(无类型)
                print(path)

            # 通过用户名和密码确认数据库中是否有和user对应的记录
            user = UserProfile.objects.filter(student_id=sid, password=pswd)
            # 如果能查询到相应记录
            if user.count() == 0:
                print('avatar fail')
                return JsonResponse({"ShowPersonalDataCheck": "ShowPersonalData failed!"})
            # 如果未能查询到用户
            else:
                print('avatar success')
                x = UserProfile.objects.get(student_id=sid, password=pswd)

                # TODO: Fix image.
                # file_path = x.image
                # file = open(file_path, "rb")

                return JsonResponse({"ShowPersonalDataCheck": "ShowPersonalData success!",
                                     # "realname": x.real_name,
                                     # "student_id": x.student_id,
                                     # "gender": x.gender,
                                     # "address": x.address,
                                     # "email": x.email,
                                     # "mobile": x.mobile,
                                     "image": None
                                     })

            # return JsonResponse({"ShowPersonalData": "success"})

        except Exception as e:
            print('avatar exception')
            return JsonResponse({"ShowPersonalData": "failed"})


class ChangeHeadImage(View):
    def post(self, request):
        try:
            print(request.POST)
            arr = request.FILES.keys()
            print(arr)
            file_name = ''
            for k in arr:
                file_name = k

            sid = ''
            pswd = ''
            path = " "

            for k in request.POST:
                if str(k) == 'sid':
                    sid = str(request.POST[k])
                else:
                    pswd = str(request.POST[k])

            print(sid, pswd)

            if file_name != '':
                file = request.FILES.get(file_name)
                path = default_storage.save('head_images/' + sid + "/" +
                                            time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime())
                                            + "/" + file_name + ".jpg",
                                            ContentFile(file.read()))  # 根据名字存图(无类型)
                print(path)

            # 通过用户名和密码确认数据库中是否有和user对应的记录
            user = UserProfile.objects.filter(student_id=sid, password=pswd)
            # 如果能查询到相应记录
            if user.count() == 0:
                print('avatar fail')
                return JsonResponse({"ChangeHeadImage": "failed"})
            # 如果未能查询到用户
            else:
                print('avatar success')
                UserProfile.objects.filter(student_id=sid, password=pswd).update(image=path)

                return JsonResponse({"ChangeHeadImage": "success"})

        except Exception as e:
            print('avatar exception')
            return JsonResponse({"ChangeHeadImage": "failed"})


class ShowHeadImage(View):
    # return path
    def post(self, request):
        try:
            token = eval(request.body.decode()).get("token")
            student_id = get_sid(token)

            head_image_path = ""

            # 通过用户名和密码确认数据库中是否有和user对应的记录
            query_set = UserProfile.objects.get(student_id=student_id)

            head_image_path = query_set.image
            return JsonResponse({"ShowHeadImage": head_image_path})

        except Exception as e:
            return JsonResponse({"ShowHeadImage": "failed"})


class TestAPI(View):
    def post(self, request):
        print(request.body)
        return JsonResponse({"message": "get it"})


class AddTag(View):
    # return path
    def post(self, request):
        """
        add tag
        :param token: token
                tag_target: id of operations_tag
        :return: UserTagID: id of operations_usertag
                Type: type of operations_tag
        """
        try:
            token = eval(request.body.decode()).get("token")
            student_id = get_sid(token)
            tag_id = eval(request.body.decode()).get("tag_target")
            # 通过用户名和密码确认数据库中是否有和user对应的记录
            user = UserProfile.objects.get(student_id=student_id)
            user_id = user.id

            tag = Tag.objects.get(id=tag_id)
            # 验证是否有重复的记录
            user_tag = UserTag.objects.filter(user_name_id=user_id, tag_id=tag_id)
            if user_tag.count() == 0:
                UserTag.objects.create(user_name_id=user_id, tag_id=tag_id, visibility=1)
                _user_tag = UserTag.objects.get(user_name_id=user_id, tag_id=tag_id)
                return JsonResponse({"AddTag": "success", "UserTagID": _user_tag.id, "Type": tag.type, "like": 0, "likes": 0})
            else:
                for i in user_tag:
                    if i.visibility == 0:
                        UserTag.objects.filter(user_name_id=user_id, tag_id=tag_id).update(
                            visibility=1)
                        _user_tag = UserTag.objects.get(user_name_id=user_id, tag_id=tag_id)
                        users_like = UserLikeTag.objects.filter(tag_id=i.id)
                        user_like = UserLikeTag.objects.filter(tag_id=i.id, user_name_id=user_id)
                        return JsonResponse({"AddTag": "success", "UserTagID": _user_tag.id, "Type": tag.type, "like": user_like.count(), "likes": users_like.count()})
            return JsonResponse({"AddTag": "failed"})
        except Exception as e:
            logger.debug('%s %s', self, e)
            return JsonResponse({"AddTag": "failed"})


class ShowTag(View):
    # return path
    def post(self, request):
        try:
            token = eval(request.body.decode()).get("token")
            student_id = get_sid(token)
            tag_id = eval(request.body.decode()).get("tag_id")

            user_id = 0

            # 通过用户名和密码确认数据库中是否有和user对应的记录
            query_set = UserProfile.objects.get(student_id=student_id)
            user_id = query_set.id

            query_set = Tag.objects.filter(id=tag_id)
            if query_set.count() == 0:
                return JsonResponse({"ShowTag": "failed"})
            else:
                for i in query_set:
                    tag_id = i.id

            UserTag.objects.filter(user_name_id=user_id, tag_id=tag_id).update(visibility=1)

            return JsonResponse({"ShowTag": "success"})

        except Exception as e:
            return JsonResponse({"ShowTag": "failed"})


class UnshowTag(View):
    # return path
    def post(self, request):
        try:
            token = eval(request.body.decode()).get("token")
            student_id = get_sid(token)
            tag_id = eval(request.body.decode()).get("tag_target")

            UserTag.objects.get(id=tag_id)
            UserTag.objects.filter(id=tag_id).update(visibility=0)

            return JsonResponse({"UnshowTag": "success"})

        except Exception as e:
            return JsonResponse({"UnshowTag": "failed"})


class GetTagVisibility(View):
    # return path
    def post(self, request):
        try:
            token = eval(request.body.decode()).get("token")
            student_id = get_sid(token)
            tag_id = eval(request.body.decode()).get("tag_id")

            user_id = 0

            # 通过用户名和密码确认数据库中是否有和user对应的记录
            query_set = UserProfile.objects.get(student_id=student_id)
            user_id = query_set.id

            query_set = Tag.objects.filter(id=tag_id)
            if query_set.count() == 0:
                return JsonResponse({"GetTagVisibility": "failed"})
            else:
                for i in query_set:
                    tag_id = i.id

            query_set = UserTag.objects.get(user_name_id=user_id, tag_id=tag_id)
            visibility = query_set.visibility

            return JsonResponse({"GetTagVisibility": visibility})

        except Exception as e:
            return JsonResponse({"GetTagVisibility": "failed"})


class StudentGetsAllTags(View):
    # return path
    def post(self, request):
        try:
            logger.debug('%s request.body %s', self, request.body)
            token = get_from_request(request, 'token')
            student_id = get_from_request(request, 'sid')
            t_id = get_from_request(request, 'sid_target')

            tags = []

            # 通过用户名和密码确认数据库中是否有和user对应的记录
            query_set = UserProfile.objects.get(student_id=t_id)
            user_id = query_set.id

            query_set = UserTag.objects.filter(user_name_id=user_id, visibility=1)
            if query_set.count() == 0:
                return JsonResponse({"StudentGetsAllTags": "no tag"})
            else:
                for i in query_set:
                    query_set2 = Tag.objects.get(id=i.tag_id)
                    query_set3 = UserLikeTag.objects.filter(tag_id=i.id)
                    query_set4 = UserLikeTag.objects.filter(user_name_id=user_id, tag_id=i.id)
                    if i.visibility == 1:
                        tags.append(
                            {"tag_id": i.id, "tag_name": query_set2.tag, "type": query_set2.type,
                             "likes": query_set3.count(), "IDofTag": query_set2.id,
                             "like": query_set4.count()})

            return JsonResponse({"Data": tags, "StudentGetsAllTags": "success"})

        except Exception as e:
            logger.exception('%s %s', self, e)
            return JsonResponse({"StudentGetsAllTags": "failed"})


class StudentGetsAllTagsCanAdd(View):
    def post(self, request):
        try:
            token = eval(request.body.decode()).get("token")
            student_id = get_sid(token)

            user_id = 0
            rev_tags = []
            tags = []

            query_set = UserProfile.objects.get(student_id=student_id)
            user_id = query_set.id
            query_set = UserTag.objects.filter(user_name_id=user_id, visibility=1)
            for i in query_set:
                rev_tags.append(i.tag_id)
            query_set = Tag.objects.all()
            for i in query_set:
                if i.id not in rev_tags:
                    tags.append({'tag_id': i.id, 'tag_name': i.tag})

            return JsonResponse({"Data": tags, "StudentGetsAllTagsCanAdd": "success"})

        except Exception as e:
            print(e)
            return JsonResponse({"StudentGetsAllTagsCanAdd": "failed"})


class StudentLikeTag(View):
    def post(self, request):
        try:
            print(datetime.datetime.now())
            token = eval(request.body.decode()).get("token")
            student_id = get_sid(token)
            t_id = eval(request.body.decode()).get("tag_target")

            query_set = UserProfile.objects.get(student_id=student_id)
            user_id = query_set.id
            query_set3 = UserLikeTag.objects.filter(user_name_id=user_id, tag_id=t_id)
            if query_set3.count() == 1:
                query_set3.delete()
                return JsonResponse({"StudentLikeTag": "no like"})
            else:
                UserLikeTag.objects.create(user_name_id=user_id, tag_id=t_id)
                return JsonResponse({"StudentLikeTag": "like"})

        except Exception as e:
            print(e)
            return JsonResponse({"StudentLikeTagCheck": "failed"})


class StudentGetValidGroupInProject(View):
    def post(self, request):
        try:

            project_id = eval(request.body.decode()).get("project_id")
            token = eval(request.body.decode()).get("token")
            student_id = get_sid(token)

            groups = GroupOrg.objects.filter(project_id=int(project_id))
            project = Project.objects.get(id=int(project_id))
            group = {}
            group["group_size"] = project.group_size
            group["min_group_size"] = project.min_group_size
            for i in groups:
                group[i.id] = {}
                group[i.id]["group_name"] = i.group_name
                group[i.id]["member"] = i.member
                group[i.id]["captain_id"] = i.captain_name_id
                captain = UserProfile.objects.get(student_id=i.captain_name_id)
                group[i.id]["captain_name"] = captain.student_id
                userGroup = UserGroup.objects.filter(group_name_id=i.id, user_name_id=student_id)
                if userGroup.count() == 1:
                    return JsonResponse(
                        {"Data": None, "StudentGetValidGroupInProjectCheck": "already has group"})
                if i.member == group["group_size"]:
                    group.pop(i.id)
            if len(group) == 0:
                return JsonResponse(
                    {"Data": None, "StudentGetValidGroupInProjectCheck": "no group to attend"})

            return JsonResponse({"Data": group, "StudentGetValidGroupInProjectCheck": "success"})
        except Exception as e:
            return JsonResponse({"StudentGetValidGroupInProjectCheck": "failed"})


class StudentGetProject(View):
    def post(self, request):
        try:

            # # TODO: Delete this.
            # sid = eval(request.body.decode()).get("sid")
            # pswd = eval(request.body.decode()).get("pswd")
            # course = eval(request.body.decode()).get("course")
            # project = eval(request.body.decode()).get("project")
            # if sid == '11810101' and pswd == '11810101' and course == 'CS303' and project == 'IMP':x
            #     data = {'description': 'This is a demo description',
            #             'inspectors': ['inspector1', 'inspector2'],
            #             'milestone': {'event1': 'datetime1', 'event2': 'datetime2'},
            #             'attachment': 'path to the attachment',
            #             'groupInfo': None}
            #     return JsonResponse({'projectDetail': data})

            project_id = eval(request.body.decode()).get("project_id")
            token = eval(request.body.decode()).get("token")
            student_id = get_sid(token)

            groups = GroupOrg.objects.filter(project_id=int(project_id))
            project = Project.objects.get(id=int(project_id))
            group = {}
            group["group_size"] = project.group_size
            group["min_group_size"] = project.min_group_size
            for i in groups:
                group[i.id] = {}
                group[i.id]["group_name"] = i.group_name
                group[i.id]["member"] = i.member
                group[i.id]["captain_id"] = i.captain_name_id
                captain = UserProfile.objects.get(student_id=i.captain_name_id)
                group[i.id]["captain_name"] = captain.student_id
                userGroup = UserGroup.objects.filter(group_name_id=i.id, user_name_id=student_id)
                if userGroup.count() == 1:
                    query_set = GroupOrg.objects.filter(id=i.id)

                    group_name = ""
                    group_detail = ""
                    project_name = ""
                    course_name = ""
                    captain_name = ""
                    captain_id = 0
                    project_id = 0
                    course_id = 0
                    members = []

                    for j in query_set:
                        group_name = j.group_name
                        group_detail = j.detail
                        captain_id = j.captain_name_id
                        project_id = j.project_id

                        query_set = Project.objects.filter(id=project_id)
                        for k in query_set:
                            project_name = k.name
                            course_id = k.course_id
                            query_set = Course.objects.filter(id=project_id)
                            for k in query_set:
                                course_name = k.name

                        query_set = UserProfile.objects.filter(id=captain_id)
                        for k in query_set:
                            captain_name = k.student_id

                        query_set = UserGroup.objects.filter(id=i.id)
                        for k in query_set:
                            user_id = k.user_name_id
                            query_set = UserProfile.objects.filter(id=user_id)
                            for k in query_set:
                                members.append(k.student_id)

                    return JsonResponse({"group_name": group_name,
                                         "group_introduction": group_detail,
                                         "project_id": project_id,
                                         "project_name": project_name,
                                         "course_id": course_id,
                                         "course_name": course_name,
                                         "captain_name": captain_name,
                                         "members": members,
                                         })
                if i.member == group["group_size"]:
                    group.pop(i.id)

            return JsonResponse({"Data": group, "StudentGetProjectCheck": "success"})
        except Exception as e:
            return JsonResponse({"StudentGetProjectCheck": "failed"})


class TeacherGetCourses(View):
    def post(self, request):
        try:
            token = eval(request.body.decode()).get("token")
            student_id = get_sid(token)

            query_set = UserProfile.objects.get(student_id=student_id, is_staff=1)
            user_id = query_set.id
            courses = {}
            course = Authority.objects.filter(user_id=user_id, type="teach")
            if course.count() == 0:
                return JsonResponse({"Data": None, "TeacherGetCoursesCheck": "no course"})
            for i in course:
                if i.end_time > datetime.datetime.now() > i.start_time:
                    name = Course.objects.get(id=i.course_id)
                    courses[name.id] = name.name
            if len(courses) == 0:
                return JsonResponse({"Data": None, "TeacherGetCoursesCheck": "no course"})
            return JsonResponse({"Data": courses, "TeacherGetCoursesCheck": "success"})
        except Exception as e:
            print(e)
            return JsonResponse({"TeacherGetCoursesCheck": "failed"})


class TeacherGetStudentsInCourse(View):
    def post(self, request):
        try:
            token = eval(request.body.decode()).get("token")
            student_id = get_sid(token)
            course_id = eval(request.body.decode()).get("course")

            query_set = UserProfile.objects.get(student_id=student_id, is_staff=1)
            user_id = query_set.id
            students = {}
            course = Authority.objects.get(user_id=user_id, type="teach", course_id=course_id)
            if course.end_time > datetime.datetime.now() > course.start_time:
                student = UserCourse.objects.filter(course_name_id=course_id)
                for j in student:
                    user = UserProfile.objects.filter(id=j.user_name_id)
                    for k in user:
                        students[k.student_id] = k.student_id
                return JsonResponse({"Data": students, "TeacherGetStudentsInCourse": "success"})
            else:
                return JsonResponse({"TeacherGetStudentsInCourse": "fail"})
        except Exception as e:
            print(e)
            return JsonResponse({"TeacherGetStudentsInCourseCheck": "failed"})


class TeacherCreateProject(View):
    def post(self, request):
        try:
            logger.debug('%s request.body %s', self, request.body)
            token = eval(request.body.decode()).get("token")
            student_id = get_sid(token)
            project_name = eval(request.body.decode()).get("newProjectName")
            introduction = eval(request.body.decode()).get("newProjectDescription")
            group_size = eval(request.body.decode()).get("groupingMaximum")
            min_group_size = eval(request.body.decode()).get("groupingMinimum")
            course_id = eval(request.body.decode()).get("newProjectCourse")
            ddl = eval(request.body.decode()).get("groupingDeadline")
            ddl = ddl // 1000
            key = eval(request.body.decode()).get("idx")
            group_ddl = datetime.datetime.fromtimestamp(ddl)

            query_set = UserProfile.objects.get(student_id=student_id, is_staff=1)
            user_id = query_set.id
            course = Authority.objects.get(user_id=user_id, type="teach", course_id=course_id)

            arr = request.FILES.keys()
            file_name = ''
            for k in arr:
                file_name = k

            if course.end_time > datetime.datetime.now() > course.start_time:
                project = Project.objects.filter(name=project_name, introduction=introduction,
                                                 group_size=group_size,
                                                 course_id=course_id, min_group_size=min_group_size,
                                                 group_ddl=group_ddl)
                project_id = 0
                if project.count() == 0:
                    Project.objects.create(name=project_name, introduction=introduction,
                                           group_size=group_size,
                                           course_id=course_id, min_group_size=min_group_size,
                                           group_ddl=group_ddl)
                else:
                    for j in project:
                        project_id = j.id
                keys = Key.objects.filter(key_word=key)
                if keys.count() == 0:
                    return JsonResponse({"TeacherCreateProject": "has no key"})
                array = base64.b64decode(key.encode("utf-8")).decode("utf-8").split(',')
                if float(array[-1]) + 3600 < time.time():
                    return JsonResponse({"TeacherCreateProject": "has no key"})
                if file_name != '':
                    file = request.FILES.get(file_name)
                    path = default_storage.save('file/' + project_name + "/" + file_name,
                                                ContentFile(file.read()))
                    ProjectFile.objects.create(file_path=path, project_id=project_id)

                return JsonResponse({"TeacherCreateProject": "success"})
            else:
                return JsonResponse({"TeacherCreateProject": "has no authority"})

        except Exception as e:
            logger.exception('%s %s', self, e)
            return JsonResponse({"TeacherCreateProjectCheck": "failed"})


class TeacherGetAuthInProject(View):
    def post(self, request):
        f"""
        user with "teach" authority can get all authority beside himself in the course of project
        :param token: token
                project_id: id of project_project
        :return: "Data": auths=  username:[type of authority]
        """
        try:
            token = eval(request.body.decode()).get("token")
            student_id = get_sid(token)
            project_id = eval(request.body.decode()).get("project_id")

            user = UserProfile.objects.get(student_id=student_id)
            user_id = user.id
            username = user.username
            project = Project.objects.get(id=project_id)
            course_id = project.course_id
            course = Authority.objects.get(user_id=user_id, type="teach", course_id=course_id)
            auths = {}
            if course.end_time > datetime.datetime.now() > course.start_time:
                auth = Authority.objects.filter(course_id=course_id)
                for i in auth:
                    auth_user = UserProfile.objects.get(id=i.user_id)
                    if auth_user.username == username:
                        continue
                    elif auth_user.username in auths.keys():
                        auths[auth_user.username].append(i.type)
                    else:
                        auths[auth_user.username] = [i.type]

            return JsonResponse({"Data": auths, "TeacherGetAuthInProject": "success"})

        except Exception as e:
            logger.debug('%s %s', self, e)
            return JsonResponse({"TeacherGetAuthInProject": "failed"})


class StudentPublishRequest(View):
    def post(self, request):
        try:
            token = eval(request.body.decode()).get("token")
            student_id = get_sid(token)
            type = 'request'
            information = eval(request.body.decode()).get("content")
            group_id = eval(request.body.decode()).get("group_id")
            project_id = eval(request.body.decode()).get("project_id")
            title = eval(request.body.decode()).get("title")

            query_set = UserProfile.objects.get(student_id=student_id)
            user_id = query_set.id
            floor = type + "," + str(group_id) + "," + title

            temp = ProjectComment.objects.filter(project_name_id=project_id, user_name_id=user_id)
            if temp.count() == 0:
                ProjectComment.objects.create(comments=information, floor=floor,
                                              project_name_id=project_id, user_name_id=user_id)
            else:
                ProjectComment.objects.filter(project_name_id=project_id, user_name_id=user_id).update(
                    comments=information, floor=floor)

            return JsonResponse({"StudentPublishRequest": "success"})

        except Exception as e:
            return JsonResponse({"StudentPublishRequest": "failed"})


class StudentPublishApply(View):
    def post(self, request):
        try:
            token = eval(request.body.decode()).get("token")
            student_id = get_sid(token)
            type = 'apply'
            information = eval(request.body.decode()).get("content")
            project_id = eval(request.body.decode()).get("project_id")
            title = eval(request.body.decode()).get("title")
            print(information, project_id, title)
            query_set = UserProfile.objects.get(student_id=student_id)
            user_id = query_set.id
            floor = type + ",Null," + title
            temp = ProjectComment.objects.filter(project_name_id=project_id, user_name_id=user_id)
            if temp.count() == 0:
                ProjectComment.objects.create(comments=information, floor=floor, project_name_id=project_id, user_name_id=user_id)
            else:
                ProjectComment.objects.filter(project_name_id=project_id, user_name_id=user_id).update(comments=information, floor=floor)
            print(project_id)
            return JsonResponse({"StudentPublishApply": "success"})

        except Exception as e:
            print('error', e)
            return JsonResponse({"StudentPublishApply": "failed"})


class StudentGetAllAd(View):
    def post(self, request):
        try:
            token = eval(request.body.decode()).get("token")
            student_id = get_sid(token)
            project_id = eval(request.body.decode()).get("project_id")

            query_set = ProjectComment.objects.filter(project_name_id=project_id)
            ad = []
            for i in query_set:
                str = i.floor.split(',')
                title = ""
                for j in range(2, len(str)):
                    title += str[j]
                query_set1 = UserProfile.objects.get(id=i.user_name_id)
                temp = {'id': i.id, "title": title, "content": i.comments, "type": str[0], "sid": query_set1.student_id, 'name': query_set1.real_name, 'titlee': title+'--'+query_set1.real_name}
                if str[1] == "Null":
                    temp["group_id"] = None
                else:
                    temp["group_id"] = int(str[1])
                ad.append(temp)
            print(project_id, ad)
            return JsonResponse({"Data": ad, "StudentGetAllAd": "success"})

        except Exception as e:
            print(e)
            return JsonResponse({"StudentGetAllAd": "failed"})


class SendMailToInvite(View):
    def post(self, request):
        try:
            token = eval(request.body.decode()).get("token")
            student_id = get_sid(token)
            tag_id = eval(request.body.decode()).get("t_sid")
            group_id = eval(request.body.decode()).get("group_id")

            query_set = UserProfile.objects.get(student_id=tag_id)
            email = query_set.email
            subject = '来自自强学堂的问候'
            text_content = '这是一封重要的邮件.'
            html_content = '''<p>这是一封<strong>重要的</strong>邮件.</p>'''
            msg = EmailMultiAlternatives(subject, text_content,
                                         student_id + '<11812710@mail.sustech.edu.cn>', [email])
            msg.attach_alternative(html_content, "text/html")
            msg.send()

            return JsonResponse({"SendMailToInvite": "success"})

        except Exception as e:
            return JsonResponse({"SendMailToInvite": "failed"})


class MailUrl(View):
    def get(self, request):
        # sender = request.GET.get('s')
        reciver = request.GET.get('r')
        # type = request.GET.get('t')
        # password = request.GET.get('c')
        # send_mail('Subject here', 'Here is the message.', 'me'+'<11812710@mail.sustech.edu.cn>',
        #           ['11811002@mail.sustech.edu.cn'], fail_silently=False)
        subject = '来自自强学堂的问候'
        text_content = '这是一封重要的邮件.'
        html_content = '''<p>这是一封<strong>重要的</strong>邮件.</p>'''
        msg = EmailMultiAlternatives(subject, text_content, 'me' + '<11812710@mail.sustech.edu.cn>',
                                     [reciver])
        msg.attach_alternative(html_content, "text/html")
        msg.send()  # http://127.0.0.1:8000/mailurl/?r=目标邮箱 测试用例
        return HttpResponse("success")


# class Test(View):
#     def post(self, request):
#         print(request)
#         print(request.POST)
#         # print(request.body)
#         student_id = "admin"
#         password = "123"
#         # get file
#         user = UserProfile.objects.filter(username=student_id, password=password)
#         if user.count() == 1:
#             return HttpResponse("yes")
#
#         return HttpResponse("no")
#
#     def get(self, request):
#         p1 = request.GET.get('p1')
#         p2 = request.GET.get('p2')
#         return HttpResponse("p1 = " + p1 + "; p2 = " + p2)


class SendKey(View):
    def post(self, request):
        try:
            token = eval(request.body.decode()).get("token")
            student_id = get_sid(token)
            course_id = eval(request.body.decode()).get("course")

            query_set = UserProfile.objects.get(student_id=student_id, is_staff=1)
            user_id = query_set.id
            course = Authority.objects.get(user_id=user_id, type="teach", course_id=course_id)
            string = str(student_id) + str(course_id) + "," + str(time.time())
            key = base64.b64encode(string.encode("utf-8")).decode("utf-8")
            Key.objects.create(key_word=key)
            return JsonResponse({"SendKey": key})

        except Exception as e:
            print(e)
            return JsonResponse({"SendKeyCheck": "failed"})


class TestFile(View):
    def post(self, request):
        try:
            print(request.POST)
            arr = request.FILES.keys()
            print(arr)
            file_name = ''
            for k in arr:
                file_name = k
            sid = ''
            pswd = ''
            for k in request.POST:
                if str(k) == 'sid':
                    sid = str(request.POST[k])
                else:
                    pswd = str(request.POST[k])
            print(sid, pswd)
            if file_name != '':
                file = request.FILES.get(file_name)
                path = default_storage.save('head_images/' + sid + "/" +
                                            time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime())
                                            + "/" + file_name,
                                            ContentFile(file.read()))  # 根据名字存图(无类型)
                print(path)
            return JsonResponse({"ChangeHeadImage": "success"})
        except Exception as e:
            print('avatar exception', e)
            return JsonResponse({"ChangeHeadImage": "failed"})

class TeacherGetSituationInProject(View):
    def post(self, request):
        f"""
        user with "teach" authority can get all authority beside himself in the course of project
        :param token: token
                project_id: id of project_project
        :return: "Data": auths=  username:[type of authority]
        """
        try:
            token = eval(request.body.decode()).get("token")
            student_id = get_sid(token)
            project_id = eval(request.body.decode()).get("project_id")
            print(project_id)
            user = UserProfile.objects.get(student_id=student_id)
            user_id = user.id
            project = Project.objects.get(id=project_id)
            course_id = project.course_id
            # course = Authority.objects.get(user_id=user_id, type="teach", course_id=course_id)
            groups = []
            # if course.end_time > datetime.datetime.now() > course.start_time:
            group = GroupOrg.objects.filter(project_id=project_id)
            for i in group:
                group_detail = {}
                group_detail["group_id"] = i.id
                group_detail["group_name"] = i.group_name
                captain = UserProfile.objects.get(id=i.captain_name_id)
                group_detail["captain_name"] = captain.username
                group_detail["captain_sid"] = captain.student_id
                group_detail["member_sid"] = [captain.username]
                group_detail["member_name"] = [captain.student_id]
                member = UserGroup.objects.filter(group_name_id=i.id)
                string = captain.username
                for j in member:
                    person = UserProfile.objects.get(id=j.user_name_id)
                    if person.student_id == captain.student_id:
                        continue
                    group_detail["member_sid"].append(person.student_id)
                    group_detail["member_name"].append(person.username)
                    string += " " + person.username
                group_detail["namelist"] = string
                if project.group_size > member.count():
                    group_detail["valid"] = True
                else:
                    group_detail["valid"] = False
                groups.append(group_detail)
            return JsonResponse({"Data": groups, "TeacherGetSituationInProject": "success"})

        except Exception as e:
            logger.debug('%s %s', self, e)
            return JsonResponse({"TeacherGetSituationInProject": "failed"})


class TeacherKickMember(View):
    def post(self, request):
        """
        Teacher kick student
        :param token:token
                group_id: id of student's group
                t_sid: sid of kicked student
        :return:
        """
        try:
            group_id = eval(request.body.decode()).get("group_id")
            token = eval(request.body.decode()).get("token")
            student_id = get_sid(token)
            target_id = eval(request.body.decode()).get("t_sid")
            user = UserProfile.objects.get(student_id=target_id)
            # TODO:等待权限判断，能否给course_id
            # auth = Authority.objects.get(user_id=student_id, type="teach", course_id=course_id)
            # if auth.end_time > datetime.datetime.now() > auth.start_time:
            group = GroupOrg.objects.get(group_name_id=group_id)
            GroupOrg.objects.filter(group_name_id=group_id).update(member=group.member-1)
            UserGroup.objects.delete(group_name_id=group_id, user_name_id=user.id)
            return JsonResponse({"TeacherKickMemberCheck": "success"})
        except Exception as e:
            logger.debug('%s %s', self, e)
            return JsonResponse({"TeacherKickMemberCheck": "failed"})
