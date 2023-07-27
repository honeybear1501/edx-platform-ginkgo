"""
This file contains AiAsideSummary class that take a `course_key` and return if:
    * the waffle flag is enabled in ai_aside
    * is the summary is enabled for a given xblock_id
    * change the settings for a given xblock_id
"""


from django.utils.functional import cached_property


class AiAsideSummary:
    """
    Configuration for the AI Aside summaries.
    """

    def __init__(self, course_key):
        self._course_key = course_key

    def __str__(self):
        """
        Return user-friendly string.
        """
        return f"AIAside summary configuration for {self.course_key} course"

    def __eq__(self, other):
        """
        Define equality based on course_key.
        """
        return isinstance(other, self.__class__) and self.course_key == other.course_key

    @cached_property
    def course_key(self):
        """
        Return the string representation of a CourseKey
        """
        return str(self._course_key)

    @cached_property
    def is_enabled(self):
        """
        Define if the waffle flag is enabled for the current course_key
        """
        try:
            from ai_aside.waffle import summaries_configuration_enabled
            return summaries_configuration_enabled(self._course_key)
        except ImportError:
            return False

    def is_summary_xblock_enabled(self, xblock_id=None):
        """
        Define if the summary configuration is enabled in ai_aside
        """
        try:
            from ai_aside.api.api import is_summary_enabled
            return is_summary_enabled(self.course_key, xblock_id)
        except ImportError:
            return False

    def set_xblock_settings(self, xblock_id, settings=None):
        """
        Define the settings for a given xblock_id in ai_aside
        """
        if settings is None:
            return None

        try:
            from ai_aside.api.api import set_unit_settings
            return set_unit_settings(self.course_key, xblock_id, settings)
        except ImportError:
            return None
