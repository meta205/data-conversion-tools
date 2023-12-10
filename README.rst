data-conversion-tools
=====================

.. code-block:: shell-session

   $ pip freeze > requirements.txt

.. code-block:: shell-session

   $ pip install -r requirements.txt

.. code-block:: shell-session

   $ python main.py select 'orders[row_id, order_priority, customer_name, ship_mode, order_date, quantity_ordered_new]' --path ./sample/SuperStoreUS-2015.xls
        row_id order_priority      customer_name       ship_mode order_date  quantity_ordered_new
   0     20847           High      Bonnie Potter     Express Air 2015-01-07                   4.0
   1     20228  Not Specified     Ronnie Proctor  Delivery Truck 2015-06-13                  12.0
   2     21776       Critical      Marcus Dunlap     Regular Air 2015-02-15                  22.0
   3     24844         Medium  Gwendolyn F Tyson     Regular Air 2015-05-12                  16.0
   4     24846         Medium  Gwendolyn F Tyson     Regular Air 2015-05-12                   7.0
   ...     ...            ...                ...             ...        ...                   ...
   1947  19842           High        Andrea Shaw     Regular Air 2015-03-11                  18.0
   1948  19843           High        Andrea Shaw     Regular Air 2015-03-11                  22.0
   1949  26208  Not Specified        Marvin Reid     Regular Air 2015-03-29                   5.0
   1950  24911         Medium      Florence Gold     Express Air 2015-04-04                  15.0
   1951  25914           High      Tammy Buckley     Express Air 2015-02-08                   5.0

   [1952 rows x 6 columns]

.. code-block:: shell-session

   $ python main.py newfile --path ./sample/SuperStoreUS-2015.xls
