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
        Define equality based on course_id.
        """
        return isinstance(other, self.__class__) and self.course_key == other.course_key

    @cached_property
    def course_key(self):
        return str(self._course_key)

    @cached_property
    def is_enabled(self):
        try:
            from ai_aside.waffle import summaries_configuration_enabled
            return summaries_configuration_enabled(self._course_key)
        except ImportError:
            return False

    def is_summary_xblock_enabled(self, xblock_id=None):
        try:
            from ai_aside.api.api import is_summary_enabled
            return is_summary_enabled(self.course_key, xblock_id)
        except ImportError:
            return False

    def set_xblock_settings(self, xblock_id, settings=None):
        if settings is None:
            return None

        try:
            from ai_aside.api.api import set_unit_settings
            return set_unit_settings(self.course_key, xblock_id, settings)
        except ImportError:
            return None
