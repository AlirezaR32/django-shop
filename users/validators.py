from django.core.validators import RegexValidator

class PhoneNumberValidator(RegexValidator):
    regex = r"^09\d{9}$"
    code = "phone invalid"
    message = "phone invalid"

class PostalCodeValidator(RegexValidator):
    regex = r"^\d{10}$"
    code = "postal code invalid"
    message = "postal code invalid"

validate_phone_number = PhoneNumberValidator()
validate_postal_code = PostalCodeValidator()

