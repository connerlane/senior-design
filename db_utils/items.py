#!/usr/bin/env python
import sqlite3

from bottle import FormsDict

from db_utils import Table, SQLiteDatabase


class Product(Table):
    """A Product table of an item database."""

    table_name = 'Product'
    primary_key = 'id'

    def get_by_name(self, name):
        """Fetch a Product row by its 'name' field.

        :param: the name of the product to find
        :type name: str
        :return: a row of the found product
        :rtype: sqlite3.Row
        """
        return self.get(name, key='name')


class Order(Table):
    """An Order table of an item database."""

    table_name = '"Order"'
    primary_key = 'id'

    def update_total(self, order_id, total):
        """Update 'total' field of table.

        :param order_id: primary key of table
        :param total: the new value for 'total'
        :type order_id: int
        :tye total: float
        """
        self.update(('total', total), order_id)


class OrderLine(Table):
    """An OrderLine table of an item database."""

    table_name = 'OrderLine'
    primary_key = 'id'


class ItemDatabase(SQLiteDatabase):
    """Controller for SQLite item databases."""

    def _create_orderline_row(self, form, order_id):
        """Helper method to create OrderLine row from item form.

        :param form: POST request form to pull data from
        :param order_id: primary key of Order row
        :type form: FormsDict
        :type order_id: int
        :return: new OrderLine row in regular dict form
        :rtype: dict
        """
        product = Product(self)
        product_row = product.get_by_name(form['name'])

        if product_row is None:
            raise sqlite3.DatabaseError("Product not found.")

        cost = int(form['quantity']) * product_row['price']
        return {'order_id': order_id,
                'product_id': product_row['id'],
                'price': product_row['price'],
                'quantity': int(form['quantity']),
                'cost': cost}

    def _update_order_total(self, cost, order_id):
        """Helper method to update the 'total' field of an Order table.

        :param order_id: primary key of Order row
        :param cost: cost field of OrderLine row
        :type order_id: int
        :type cost: float
        """
        order = Order(self)
        order_row = order.get(order_id)
        total = order_row['total'] + cost
        order.update_total(order_id, total)

    def add_by_form(self, form, order_id):
        """Add a row using data from a POST request form.

        :param order_id: primary key of Order row
        :param form: POST request form to pull data from
        :type order_id: int
        :type form: FormsDict
        :return: whether the item was added successfully
        :rtype: bool
        """
        try:
            orderline_row = self._create_orderline_row(form, order_id)
        except sqlite3.DatabaseError:
            return False
        self._update_order_total(orderline_row['cost'], order_id)
        orderline = OrderLine(self)
        orderline.add(orderline_row)
        return True

    def receipt(self, order_id):
        """Fetches a receipt of a given order.

        A receipt is formed by displaying all the OrderLine rows that pertain
        to a given Order.

        :param order_id: primary key of Order row
        :type order_id: int
        :return: the OrderLine rows that match the order_id
        :rtype: List[sqlite3.Row]
        """
        query = ('SELECT Product.name, OrderLine.quantity, OrderLine.price,'
                 '    OrderLine.cost '
                 'FROM OrderLine '
                 'JOIN Product ON Product.id = OrderLine.product_id '
                 'WHERE order_id = ? ORDER BY OrderLine.id')
        return self.fetchall(query, (order_id,))

    def report(self):
        """Fetches a report that contains all items sold.

        :return: rows describing info about items sold
        :rtype: List[sqlite3.Row]
        """
        query = ('SELECT Product.name AS name, sum(OrderLine.quantity) as sold,'
                 '     sum(OrderLine.cost) AS revenue '
                 'FROM OrderLine '
                 'JOIN Product ON Product.id = OrderLine.product_id '
                 'GROUP BY Product.name '
                 'ORDER BY Product.id DESC')
        return self.fetchall(query)

    def total_revenue(self):
        """Fetches the total revenue of all items sold.

        :return: total item revenue
        :rtype: float
        """
        query = 'SELECT sum(OrderLine.cost) AS total FROM OrderLine'
        result = self.fetchone(query)
        return result['total']
