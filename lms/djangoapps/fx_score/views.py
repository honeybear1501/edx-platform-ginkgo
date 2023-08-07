"""
Instructor Dashboard Views
"""


import datetime
import logging
import uuid
from functools import reduce
from unittest.mock import patch

import pytz
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseServerError
from django.urls import reverse
from django.utils.html import escape
from django.utils.translation import gettext as _
from django.utils.translation import gettext_noop
from django.views.decorators.cache import cache_control
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_POST
from edx_proctoring.api import does_backend_support_onboarding
from edx_when.api import is_enabled_for_course
from opaque_keys import InvalidKeyError
from opaque_keys.edx.keys import CourseKey
from xblock.field_data import DictFieldData
from xblock.fields import ScopeIds

from common.djangoapps.course_modes.models import CourseMode, CourseModesArchive
from common.djangoapps.edxmako.shortcuts import render_to_response
from common.djangoapps.student.models import CourseEnrollment
from common.djangoapps.student.roles import (
    CourseFinanceAdminRole,
    CourseInstructorRole,
    CourseSalesAdminRole,
    CourseStaffRole
)
from common.djangoapps.util.json_request import JsonResponse
from lms.djangoapps.bulk_email.api import is_bulk_email_feature_enabled
from lms.djangoapps.certificates import api as certs_api
from lms.djangoapps.certificates.data import CertificateStatuses
from lms.djangoapps.certificates.models import (
    CertificateGenerationConfiguration,
    CertificateGenerationHistory,
    CertificateInvalidation,
    GeneratedCertificate
)
from lms.djangoapps.courseware.access import has_access
from lms.djangoapps.courseware.courses import get_studio_url
from lms.djangoapps.courseware.module_render import get_module_by_usage_id
from lms.djangoapps.discussion.django_comment_client.utils import available_division_schemes, has_forum_access
from lms.djangoapps.grades.api import is_writable_gradebook_enabled
from openedx.core.djangoapps.course_groups.cohorts import DEFAULT_COHORT_NAME, get_course_cohorts, is_course_cohorted
from openedx.core.djangoapps.discussions.config.waffle_utils import legacy_discussion_experience_enabled
from openedx.core.djangoapps.django_comment_common.models import FORUM_ROLE_ADMINISTRATOR, CourseDiscussionSettings
from openedx.core.djangoapps.site_configuration import helpers as configuration_helpers
from openedx.core.djangoapps.verified_track_content.models import VerifiedTrackCohortedCourse
from openedx.core.djangolib.markup import HTML, Text
from openedx.core.lib.courses import get_course_by_id
from openedx.core.lib.url_utils import quote_slashes
from openedx.core.lib.xblock_utils import wrap_xblock
from xmodule.html_module import HtmlBlock
from xmodule.modulestore.django import modulestore
from xmodule.tabs import CourseTab

log = logging.getLogger(__name__)

class ScoreDashboardTab(CourseTab):
    """
    Defines the Score Dashboard view type that is shown as a course tab.
    """
    type='score'
    title = gettext_noop('Score')
    view_name = "score_dashboard"
    is_dynamic = True

    @classmethod
    def is_enabled(cls, course, user=None):
        return True;

@ensure_csrf_cookie
@cache_control(no_cache=True, no_store=True, must_revalidate=True)
def score_dashboard(request, course_id):  # lint-amnesty, pylint: disable=too-many-statements
    """ Display the instructor dashboard for a course. """
    try:
        course_key = CourseKey.from_string(course_id)
    except InvalidKeyError:
        log.error("Unable to find course with course key %s while loading the Instructor Dashboard.", course_id)
        return HttpResponseServerError()

    course = get_course_by_id(course_key, depth=0)

    context = {
        'course': course
    }

    return render_to_response('fx_score/score_dashboard.html', context)