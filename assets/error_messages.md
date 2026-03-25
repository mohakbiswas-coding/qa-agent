# Error Messages Reference

## Form Errors (shown inline in red)
| Field   | Element ID    | Error Message                              |
|---------|---------------|--------------------------------------------|
| Name    | name-error    | "Name is required."                        |
| Email   | email-error   | "Please enter a valid email address."      |
| Address | address-error | "Address is required."                     |

## Discount Code Errors
| Condition     | Element ID       | Message                    | Color |
|---------------|------------------|----------------------------|-------|
| Invalid code  | discount-error   | "❌ Invalid discount code." | red   |
| Valid code    | discount-msg     | "✅ Discount applied: 15% off!" | green |

## Payment Success
| Condition       | Element ID        | Message                                        |
|-----------------|-------------------|------------------------------------------------|
| Payment success | success-message   | "✅ Payment Successful! Thank you for your order." |

## General Rules
- Never show success and error messages simultaneously for the same field.
- Error elements use CSS class "error" and become visible with class "visible".
- The success-message div is hidden by default (display: none) and shown after valid payment.
