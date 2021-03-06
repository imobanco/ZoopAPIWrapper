from unittest.mock import patch, MagicMock

from tests.utils import SetTestCase
from zoop_wrapper.models.seller import Seller
from zoop_wrapper.exceptions import ValidationError
from tests.factories.seller import (
    SellerFactory,
    IndividualSellerFactory,
    BusinessSellerFactory,
)


class SellerTestCase(SetTestCase):
    def test_required_fields(self):
        self.assertEqual(set(), Seller.get_required_fields())

    def test_non_required_fields(self):
        self.assertIsSubSet(
            {
                "decline_on_fail_security_code",
                "decline_on_fail_zipcode",
                "is_mobile",
                "show_profile_online",
                "statement_descriptor",
                "terminal_code",
                "type",
                "merchant_code",
                "mcc",
            },
            Seller.get_non_required_fields(),
        )

    def test_individual_required_fields(self):
        self.assertIsSubSet(set(), Seller.get_individual_required_fields())

    def test_individual_non_required_fields(self):
        self.assertIsSubSet({"website"}, Seller.get_individual_non_required_fields())

    def test_business_required_fields(self):
        self.assertEqual(
            {
                "business_address",
                "business_email",
                "business_name",
                "business_opening_date",
                "business_phone",
                "ein",
            },
            Seller.get_business_required_fields(),
        )

    def test_business_non_required_fields(self):
        self.assertIsSubSet(
            {
                "business_website",
                "business_description",
                "business_facebook",
                "business_twitter",
                "owner",
            },
            Seller.get_business_non_required_fields(),
        )

    def test_get_all_fields_business(self):
        instance = BusinessSellerFactory()
        self.assertIsInstance(instance, Seller)

        self.assertIsSubSet(
            {
                "business_address",
                "business_description",
                "business_email",
                "business_facebook",
                "business_name",
                "business_opening_date",
                "business_phone",
                "business_twitter",
                "business_website",
                "owner",
            },
            instance.get_all_fields(),
        )

    def test_get_all_fields_individual(self):
        instance = IndividualSellerFactory()
        self.assertIsInstance(instance, Seller)

        self.assertIsSubSet({"website"}, instance.get_all_fields())

    def test_get_validation_fields_individual(self):
        instance = IndividualSellerFactory()
        self.assertIsInstance(instance, Seller)

        self.assertIsSubSet(set(), instance.get_validation_fields())

    def test_business_get_validation_fields(self):
        instance = BusinessSellerFactory()
        self.assertIsInstance(instance, Seller)

        self.assertIsSubSet(
            {
                "business_address",
                "business_email",
                "business_name",
                "business_opening_date",
                "business_phone",
            },
            instance.get_validation_fields(),
        )

    def test_create(self):
        self.assertRaises(ValidationError, SellerFactory)

    def test_create_individual(self):
        instance = IndividualSellerFactory()

        self.assertIsInstance(instance, Seller)

    def test_create_business(self):
        instance = BusinessSellerFactory()

        self.assertIsInstance(instance, Seller)

    @patch("zoop_wrapper.models.seller.Person.init_custom_fields")
    def test_init_custom_fields_individual(self, mocked_person_init):
        instance = MagicMock(
            INDIVIDUAL_TYPE="foo", get_type=MagicMock(return_value="foo")
        )

        Seller.init_custom_fields(instance)
        self.assertIsInstance(mocked_person_init, MagicMock)
        mocked_person_init.assert_called_once()

    @patch("zoop_wrapper.models.seller.Person.from_dict_or_instance")
    @patch("zoop_wrapper.models.seller.Address.from_dict_or_instance")
    def test_init_custom_fields_business(
        self, mocked_address_from_dict, mocked_person_from_dict
    ):
        instance = MagicMock(
            BUSINESS_TYPE="foo", get_type=MagicMock(return_value="foo")
        )

        Seller.init_custom_fields(instance)

        self.assertIsInstance(mocked_address_from_dict, MagicMock)
        self.assertIsInstance(mocked_person_from_dict, MagicMock)
        mocked_address_from_dict.assert_called_once()
        mocked_person_from_dict.assert_called_once()
