import stripe
from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv

load_dotenv()

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")


class StripeApi:
    def __init__(self):
        self.api_key = stripe.api_key

    def create_payment_intent(self, amount, currency="usd"):
        """
        Creates a payment intent for the customer to initiate a payment process.
        :param amount: Amount to be charged (in cents).
        :param currency: Currency for the payment (default: USD).
        :return: PaymentIntent object.
        """
        try:
            payment_intent = stripe.PaymentIntent.create(
                amount=amount,
                currency=currency,
            )
            return payment_intent
        except stripe.error.StripeError as e:
            return {"error": str(e)}

    def create_customer(self, email, name=None):
        """
        Creates a new customer on Stripe.
        :param email: Customer's email.
        :param name: Customer's name (optional).
        :return: Customer object.
        """
        try:
            customer = stripe.Customer.create(
                email=email,
                name=name
            )
            return customer
        except stripe.error.StripeError as e:
            return {"error": str(e)}

    def list_customers(self, limit=10):
        """
        Lists customers on Stripe.
        :param limit: Number of customers to list (default: 10).
        :return: List of customer objects.
        """
        try:
            customers = stripe.Customer.list(limit=limit)
            return customers
        except stripe.error.StripeError as e:
            return {"error": str(e)}

    def create_charge(self, customer_id, amount, currency="usd", description=None):
        """
        Creates a charge for a specific customer.
        :param customer_id: The customer's Stripe ID.
        :param amount: The amount to charge (in cents).
        :param currency: The currency for the charge (default: USD).
        :param description: A description for the charge (optional).
        :return: Charge object.
        """
        try:
            charge = stripe.Charge.create(
                customer=customer_id,
                amount=amount,
                currency=currency,
                description=description,
            )
            return charge
        except stripe.error.StripeError as e:
            return {"error": str(e)}

    def retrieve_charge(self, charge_id):
        """
        Retrieves a specific charge by its ID.
        :param charge_id: The ID of the charge.
        :return: Charge object.
        """
        try:
            charge = stripe.Charge.retrieve(charge_id)
            return charge
        except stripe.error.StripeError as e:
            return {"error": str(e)}