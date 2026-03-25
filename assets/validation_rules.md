# Form Validation Rules

## Name Field (id="name")
- REQUIRED: Cannot be empty or whitespace only.
- Error message: "Name is required."
- Error element id: "name-error"
- Must show error in red text when empty on form submission.

## Email Field (id="email")
- REQUIRED: Cannot be empty.
- FORMAT: Must match standard email format (user@domain.com).
- Error message: "Please enter a valid email address."
- Error element id: "email-error"
- Must reject: "notanemail", "missing@", "@nodomain"
- Must accept: "user@example.com", "test.name+tag@domain.co"

## Address Field (id="address")
- REQUIRED: Cannot be empty or whitespace only.
- Error message: "Address is required."
- Error element id: "address-error"

## Validation Trigger
- Validation runs when "Pay Now" button is clicked.
- All errors shown simultaneously (not one at a time).
- Errors must be hidden when the user fixes the field and resubmits.

## Cart Validation
- Cart does not need to have items for the form to be submitted.
- Quantity input must accept only positive integers (min=1).
