# Product Specifications - E-Shop Checkout

## Discount Codes
- The discount code `SAVE15` applies a 15% discount to the cart total.
- Discount codes are case-insensitive (SAVE15 = save15).
- Only one discount code can be applied per order.
- If an invalid code is entered, the system must show an error message.
- Discount is applied BEFORE shipping costs are added.

## Shipping Options
- Standard Shipping: Free of charge. Estimated 5-7 business days.
- Express Shipping: Costs $10.00. Estimated 1-2 business days.
- Shipping method must be selected before payment.

## Products Available
1. Wireless Headphones - $49.99
2. Laptop Stand - $29.99
3. USB-C Hub - $39.99

## Cart Behavior
- Users can add multiple quantities of the same item.
- Quantity can be updated from the cart summary section.
- Total price updates dynamically as quantity or shipping changes.

## Payment
- Supported methods: Credit Card, PayPal
- Clicking "Pay Now" validates the form first.
- On success, display "Payment Successful!" message.
- The form disappears after successful payment.
