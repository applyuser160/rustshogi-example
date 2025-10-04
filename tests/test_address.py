from rustshogi import Address


class TestAddress:
    def test_address_init(self):
        # Act
        address = Address(column=2, row=5)

        # Assert
        assert address.column == 2
        assert address.row == 5
        assert address.to_int() == 57
        assert address.__repr__() == "Address(column=2, row=5)"
        assert address.__str__() == "Address(column=2, row=5)"
