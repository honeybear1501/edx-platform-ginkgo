from ratelimitbackend import admin
from verify_student.models import SoftwareSecurePhotoVerification
from verify_student.models import MidcourseReverificationWindow

admin.site.register(SoftwareSecurePhotoVerification)
admin.site.register(MidcourseReverificationWindow)