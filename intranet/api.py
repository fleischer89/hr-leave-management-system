__author__ = 'Paul Fleischer'

from datetime import *
from intranet.models import *


def get_offering_chart_data(data, flag, dates, timestamps, member_id):
    summary = dict(total_amount=0, count=0, custodians=0, offerings=0)
    members = set()
    raw_data = None
    for d in range(len(dates)):
        amount = 0
        if member_id is not None:
            member = Member.objects.get(pk=member_id)
            raw_data = Offering.objects.filter(date=datetime(dates[d]['year'], dates[d]['month'], dates[d]['day']),
                                               custodian=member)
        else:
            raw_data = Offering.objects.filter(date=datetime(dates[d]['year'], dates[d]['month'], dates[d]['day']))

        if flag == "amount":
            for rd in raw_data:
                amount += rd.amount
            output = dict(date=dates[d], timestamp=timestamps[d], val=amount)
            data.append(output)
        elif flag == "number":
            for rd in range(len(raw_data)):
                amount += 1
            output = dict(date=dates[d], timestamp=timestamps[d], val=amount)
            data.append(output)

        # Get Summary Data
        for rd in raw_data:
            summary['total_amount'] += rd.amount
            members.add(rd.custodian)
            summary['count'] += 1

    summary['custodians'] += len(members)

    return data, summary


# def get_sales_chart_data(data, flag, dates, timestamps, employee_id, product_id):
#     summary = dict(total_amount=0, count=0, employees=0, products=0)
#     employees = set()
#     products = set()
#     raw_data = None
#     for d in range(len(dates)):
#         amount = 0
#         if employee_id is not None and product_id is not None:
#             employee = Employee.objects.get(pk=employee_id)
#             product = Product.objects.get(pk=product_id)
#             raw_data = SalesRecord.objects.filter(date=datetime(dates[d]['year'], dates[d]['month'], dates[d]['day']),
#                                                   custodian=employee, product=product)
#         elif employee_id is not None:
#             employee = Employee.objects.get(pk=employee_id)
#             raw_data = SalesRecord.objects.filter(date=datetime(dates[d]['year'], dates[d]['month'], dates[d]['day']),
#                                                   custodian=employee)
#         elif product_id is not None:
#             product = Product.objects.get(pk=product_id)
#             raw_data = SalesRecord.objects.filter(date=datetime(dates[d]['year'], dates[d]['month'], dates[d]['day']),
#                                                   product=product)
#         else:
#             raw_data = SalesRecord.objects.filter(date=datetime(dates[d]['year'], dates[d]['month'], dates[d]['day']))
#
#         if flag == "amount":
#             for rd in raw_data:
#                 amount += rd.amount
#             output = dict(date=dates[d], timestamp=timestamps[d], val=amount)
#             data.append(output)
#         elif flag == "number":
#             for rd in range(len(raw_data)):
#                 amount += 1
#             output = dict(date=dates[d], timestamp=timestamps[d], val=amount)
#             data.append(output)
#
#         # Get Summary Data
#         for rd in raw_data:
#             summary['total_amount'] += rd.amount
#             employees.add(rd.custodian)
#             products.add(rd.product)
#             summary['count'] += 1
#
#     summary['employees'] += len(employees)
#     summary['products'] += len(products)
#
#     return data, summary
#
#
# def get_order_chart_data(data, flag, dates, timestamps, product_id):
#     summary = dict(total_amount=0, count=0, employees=0, products=0)
#     products = set()
#     raw_data = None
#     for d in range(len(dates)):
#         amount = 0
#         if product_id is not None:
#             product = Product.objects.get(pk=product_id)
#             raw_data = Order.objects.filter(dispatch_date=datetime(dates[d]['year'], dates[d]['month'],
#                                                                    dates[d]['day']), product=product)
#         else:
#             raw_data = Order.objects.filter(dispatch_date=datetime(dates[d]['year'], dates[d]['month'],
#                                                                    dates[d]['day']))
#
#         if flag == "amount":
#             for rd in raw_data:
#                 amount += rd.invoice.total_price
#             output = dict(date=dates[d], timestamp=timestamps[d], val=amount)
#             data.append(output)
#         elif flag == "number":
#             for rd in range(len(raw_data)):
#                 amount += 1
#             output = dict(date=dates[d], timestamp=timestamps[d], val=amount)
#             data.append(output)
#
#         # Get Summary Data
#         for rd in raw_data:
#             summary['total_amount'] += rd.invoice.total_price
#             products.add(rd.product)
#             summary['count'] += 1
#
#     summary['products'] += len(products)
#
#     return data, summary
#
#
# def get_invoice_chart_data(data, flag, dates, timestamps, product_id):
#     summary = dict(total_amount=0, count=0, employees=0, products=0)
#     employees = set()
#     products = set()
#     raw_data = None
#     for d in range(len(dates)):
#         amount = 0
#         if product_id is not None:
#             product = Product.objects.get(pk=product_id)
#             raw_data = Invoice.objects.filter(date=datetime(dates[d]['year'], dates[d]['month'], dates[d]['day']),
#                                               product=product)
#         else:
#             raw_data = Invoice.objects.filter(date=datetime(dates[d]['year'], dates[d]['month'], dates[d]['day']))
#
#         if flag == "total_price":
#             for rd in raw_data:
#                 amount += rd.total_price
#             output = dict(date=dates[d], timestamp=timestamps[d], val=amount)
#             data.append(output)
#         if flag == "discount":
#             for rd in raw_data:
#                 amount += rd.discount
#             output = dict(date=dates[d], timestamp=timestamps[d], val=amount)
#             data.append(output)
#         elif flag == "number":
#             for rd in range(len(raw_data)):
#                 amount += 1
#             output = dict(date=dates[d], timestamp=timestamps[d], val=amount)
#             data.append(output)
#
#         # Get Summary Data
#         for rd in raw_data:
#             summary['total_amount'] += rd.total_price
#             products.add(rd.product)
#             summary['count'] += 1
#
#     summary['products'] += len(products)
#
#     return data, summary
#
#
# def get_product_pricing_chart_data(data, flag, dates, timestamps, product_id):
#     summary = dict(total_amount=0, count=0, employees=0, products=0)
#     employees = set()
#     products = set()
#     raw_data = None
#     for d in range(len(dates)):
#         amount = 0
#         if product_id is not None:
#             product = Product.objects.get(pk=product_id)
#             raw_data = ProductPricingRecord.objects.filter(date=datetime(dates[d]['year'], dates[d]['month'],
#                                                                          dates[d]['day']),
#                                                            product=product)
#         else:
#             raw_data = ProductPricingRecord.objects.filter(date=datetime(dates[d]['year'], dates[d]['month'],
#                                                                          dates[d]['day']))
#
#         if flag == "open_market":
#             for rd in raw_data:
#                 amount += rd.open_market
#             output = dict(date=dates[d], timestamp=timestamps[d], val=amount)
#             data.append(output)
#         elif flag == "supermarket":
#             for rd in raw_data:
#                 amount += rd.supermarket
#             output = dict(date=dates[d], timestamp=timestamps[d], val=amount)
#             data.append(output)
#         elif flag == "pharmacy":
#             for rd in raw_data:
#                 amount += rd.pharmacy
#             output = dict(date=dates[d], timestamp=timestamps[d], val=amount)
#             data.append(output)
#         elif flag == "wholesalers":
#             for rd in raw_data:
#                 amount += rd.wholesalers
#             output = dict(date=dates[d], timestamp=timestamps[d], val=amount)
#             data.append(output)
#         elif flag == "distributors":
#             for rd in raw_data:
#                 amount += rd.distributors
#             output = dict(date=dates[d], timestamp=timestamps[d], val=amount)
#             data.append(output)
#         elif flag == "retail":
#             for rd in raw_data:
#                 amount += rd.retail
#             output = dict(date=dates[d], timestamp=timestamps[d], val=amount)
#             data.append(output)
#         elif flag == "number":
#             for rd in range(len(raw_data)):
#                 amount += 1
#             output = dict(date=dates[d], timestamp=timestamps[d], val=amount)
#             data.append(output)
#
#         # Get Summary Data
#         for rd in raw_data:
#             products.add(rd.product)
#             summary['count'] += 1
#
#     summary['products'] += len(products)
#
#     return data, summary
#
#
# def get_production_chart_data(data, flag, dates, timestamps, employee_id, product_id):
#     summary = dict(total_amount=0, count=0, employees=0, products=0)
#     employees = set()
#     products = set()
#     raw_data = None
#     for d in range(len(dates)):
#         amount = 0
#         if employee_id is not None and product_id is not None:
#             employee = Employee.objects.get(pk=employee_id)
#             product = Product.objects.get(pk=product_id)
#             raw_data = Production.objects.filter(date=datetime(dates[d]['year'], dates[d]['month'], dates[d]['day']),
#                                                  custodian=employee, product=product)
#         elif employee_id is not None:
#             employee = Employee.objects.get(pk=employee_id)
#             raw_data = Production.objects.filter(date=datetime(dates[d]['year'], dates[d]['month'], dates[d]['day']),
#                                                  custodian=employee)
#         elif product_id is not None:
#             product = Product.objects.get(pk=product_id)
#             raw_data = Production.objects.filter(date=datetime(dates[d]['year'], dates[d]['month'], dates[d]['day']),
#                                                  product=product)
#         else:
#             raw_data = Production.objects.filter(date=datetime(dates[d]['year'], dates[d]['month'], dates[d]['day']))
#
#         if flag == "quantity":
#             for rd in raw_data:
#                 amount += rd.quantity
#             output = dict(date=dates[d], timestamp=timestamps[d], val=amount)
#             data.append(output)
#         elif flag == "bottles_issued":
#             for rd in raw_data:
#                 amount += rd.bottles_issued
#             output = dict(date=dates[d], timestamp=timestamps[d], val=amount)
#             data.append(output)
#         elif flag == "bottles_rejected":
#             for rd in raw_data:
#                 amount += rd.bottles_rejected
#             output = dict(date=dates[d], timestamp=timestamps[d], val=amount)
#             data.append(output)
#         elif flag == "bottles_returned":
#             for rd in raw_data:
#                 amount += rd.bottles_returned
#             output = dict(date=dates[d], timestamp=timestamps[d], val=amount)
#             data.append(output)
#         elif flag == "labels_issued":
#             for rd in raw_data:
#                 amount += rd.labels_issued
#             output = dict(date=dates[d], timestamp=timestamps[d], val=amount)
#             data.append(output)
#         elif flag == "labels_rejected":
#             for rd in raw_data:
#                 amount += rd.labels_rejected
#             output = dict(date=dates[d], timestamp=timestamps[d], val=amount)
#             data.append(output)
#         elif flag == "labels_returned":
#             for rd in raw_data:
#                 amount += rd.labels_returned
#             output = dict(date=dates[d], timestamp=timestamps[d], val=amount)
#             data.append(output)
#         elif flag == "number":
#             for rd in range(len(raw_data)):
#                 amount += 1
#             output = dict(date=dates[d], timestamp=timestamps[d], val=amount)
#             data.append(output)
#
#         # Get Summary Data
#         for rd in raw_data:
#             summary['total_amount'] += rd.quantity
#             employees.add(rd.custodian)
#             products.add(rd.product)
#             summary['count'] += 1
#
#     summary['employees'] += len(employees)
#     summary['products'] += len(products)
#
#     return data, summary
#
#
# def get_accounting_chart_data(data, flag, dates, timestamps, employee_id):
#     summary = dict(total_amount=0, count=0, employees=0, products=0)
#     employees = set()
#     products = set()
#     raw_data = None
#     for d in range(len(dates)):
#         amount = 0
#         if employee_id is not None:
#             employee = Employee.objects.get(pk=employee_id)
#             raw_data = Accounting.objects.filter(date=datetime(dates[d]['year'], dates[d]['month'], dates[d]['day']),
#                                                  custodian=employee)
#         else:
#             raw_data = Accounting.objects.filter(date=datetime(dates[d]['year'], dates[d]['month'], dates[d]['day']))
#
#         if flag == "total_amount":
#             for rd in raw_data:
#                 amount += rd.total_amount
#             output = dict(date=dates[d], timestamp=timestamps[d], val=amount)
#             data.append(output)
#         elif flag == "credited_product_payment":
#             for rd in raw_data:
#                 amount += rd.credited_product_payment
#             output = dict(date=dates[d], timestamp=timestamps[d], val=amount)
#             data.append(output)
#         elif flag == "cash_inflow":
#             for rd in raw_data:
#                 amount += rd.cash_inflow
#             output = dict(date=dates[d], timestamp=timestamps[d], val=amount)
#             data.append(output)
#         elif flag == "production_expenses":
#             for rd in raw_data:
#                 amount += rd.production_expenses
#             output = dict(date=dates[d], timestamp=timestamps[d], val=amount)
#             data.append(output)
#         elif flag == "marketing_expenses":
#             for rd in raw_data:
#                 amount += rd.marketing_expenses
#             output = dict(date=dates[d], timestamp=timestamps[d], val=amount)
#             data.append(output)
#         elif flag == "sales_amount":
#             for rd in raw_data:
#                 amount += rd.sales_amount
#             output = dict(date=dates[d], timestamp=timestamps[d], val=amount)
#             data.append(output)
#         elif flag == "sales_number":
#             for rd in raw_data:
#                 amount += rd.sales_number
#             output = dict(date=dates[d], timestamp=timestamps[d], val=amount)
#             data.append(output)
#         elif flag == "number":
#             for rd in range(len(raw_data)):
#                 amount += 1
#             output = dict(date=dates[d], timestamp=timestamps[d], val=amount)
#             data.append(output)
#
#         # Get Summary Data
#         for rd in raw_data:
#             summary['total_amount'] += rd.total_amount
#             employees.add(rd.custodian)
#             summary['count'] += 1
#
#     summary['employees'] += len(employees)
#
#     return data, summary
#
#
# def get_receiving_chart_data(data, flag, dates, timestamps, employee_id, product_id):
#     summary = dict(total_amount=0, count=0, employees=0, products=0)
#     employees = set()
#     products = set()
#     raw_data = None
#     for d in range(len(dates)):
#         amount = 0
#         if employee_id is not None and product_id is not None:
#             employee = Employee.objects.get(pk=employee_id)
#             product = Product.objects.get(pk=product_id)
#             raw_data = WarehouseReceivingRecord.objects.filter(date=datetime(dates[d]['year'], dates[d]['month'],
#                                                                              dates[d]['day']),
#                                                                custodian=employee, product=product)
#         elif employee_id is not None:
#             employee = Employee.objects.get(pk=employee_id)
#             raw_data = WarehouseReceivingRecord.objects.filter(date=datetime(dates[d]['year'], dates[d]['month'],
#                                                                              dates[d]['day']), custodian=employee)
#         elif product_id is not None:
#             product = Product.objects.get(pk=product_id)
#             raw_data = WarehouseReceivingRecord.objects.filter(date=datetime(dates[d]['year'], dates[d]['month'],
#                                                                              dates[d]['day']), product=product)
#         else:
#             raw_data = WarehouseReceivingRecord.objects.filter(date=datetime(dates[d]['year'], dates[d]['month'],
#                                                                              dates[d]['day']))
#
#         if flag == "quantity":
#             for rd in raw_data:
#                 amount += rd.quantity
#             output = dict(date=dates[d], timestamp=timestamps[d], val=amount)
#             data.append(output)
#         elif flag == "number":
#             for rd in range(len(raw_data)):
#                 amount += 1
#             output = dict(date=dates[d], timestamp=timestamps[d], val=amount)
#             data.append(output)
#
#         # Get Summary Data
#         for rd in raw_data:
#             summary['total_amount'] += rd.quantity
#             employees.add(rd.custodian)
#             products.add(rd.product)
#             summary['count'] += 1
#
#     summary['employees'] += len(employees)
#     summary['products'] += len(products)
#
#     return data, summary
#
#
# def get_dispatch_chart_data(data, flag, dates, timestamps, employee_id, product_id):
#     summary = dict(total_amount=0, count=0, employees=0, products=0)
#     employees = set()
#     products = set()
#     raw_data = None
#     for d in range(len(dates)):
#         amount = 0
#         if employee_id is not None and product_id is not None:
#             employee = Employee.objects.get(pk=employee_id)
#             product = Product.objects.get(pk=product_id)
#             raw_data = WarehouseDispatchRecord.objects.filter(date=datetime(dates[d]['year'], dates[d]['month'],
#                                                                             dates[d]['day']),
#                                                               custodian=employee, product=product)
#         elif employee_id is not None:
#             employee = Employee.objects.get(pk=employee_id)
#             raw_data = WarehouseDispatchRecord.objects.filter(date=datetime(dates[d]['year'], dates[d]['month'],
#                                                                             dates[d]['day']), custodian=employee)
#         elif product_id is not None:
#             product = Product.objects.get(pk=product_id)
#             raw_data = WarehouseDispatchRecord.objects.filter(date=datetime(dates[d]['year'], dates[d]['month'],
#                                                                             dates[d]['day']), product=product)
#         else:
#             raw_data = WarehouseDispatchRecord.objects.filter(date=datetime(dates[d]['year'], dates[d]['month'],
#                                                                             dates[d]['day']))
#
#         if flag == "quantity":
#             for rd in raw_data:
#                 amount += rd.quantity
#             output = dict(date=dates[d], timestamp=timestamps[d], val=amount)
#             data.append(output)
#         elif flag == "number":
#             for rd in range(len(raw_data)):
#                 amount += 1
#             output = dict(date=dates[d], timestamp=timestamps[d], val=amount)
#             data.append(output)
#
#         # Get Summary Data
#         for rd in raw_data:
#             summary['total_amount'] += rd.quantity
#             employees.add(rd.custodian)
#             products.add(rd.product)
#             summary['count'] += 1
#
#     summary['employees'] += len(employees)
#     summary['products'] += len(products)
#
#     return data, summary
#
#
# def get_call_chart_data(data, flag, dates, timestamps, employee_id):
#     summary = dict(total_amount=0, count=0, employees=0, products=0)
#     employees = set()
#     products = set()
#     raw_data = None
#     for d in range(len(dates)):
#         amount = 0
#         if employee_id is not None:
#             employee = Employee.objects.get(pk=employee_id)
#             raw_data = CallRecord.objects.filter(date=datetime(dates[d]['year'], dates[d]['month'], dates[d]['day']),
#                                                  custodian=employee)
#         else:
#             raw_data = CallRecord.objects.filter(date=datetime(dates[d]['year'], dates[d]['month'], dates[d]['day']))
#
#         if flag == "number":
#             for rd in range(len(raw_data)):
#                 amount += 1
#             output = dict(date=dates[d], timestamp=timestamps[d], val=amount)
#             data.append(output)
#
#         # Get Summary Data
#         for rd in raw_data:
#             employees.add(rd.custodian)
#             summary['count'] += 1
#
#     summary['employees'] += len(employees)
#
#     return data, summary
#
#
# def get_enquiry_chart_data(data, flag, dates, timestamps):
#     for d in range(len(dates)):
#         amount = 0
#         raw_data = CallRecord.objects.filter(date=datetime(dates[d]['year'], dates[d]['month'], dates[d]['day']))
#
#         if flag == "number":
#             for rd in range(len(raw_data)):
#                 amount += 1
#             output = dict(date=dates[d], timestamp=timestamps[d], val=amount)
#             data.append(output)
#
#     return data
#
#
# def get_banking_chart_data(data, flag, dates, timestamps, trans_mode_id, trans_type_id, employee_id):
#     summary = dict(total_amount=0, count=0, employees=0, products=0)
#     employees = set()
#     raw_data = None
#     for d in range(len(dates)):
#         amount = 0
#         if (employee_id is not None) and (trans_mode_id is not None) and (trans_type_id is not None):
#             employee = Employee.objects.get(pk=employee_id)
#             trans_type = TransactionType.objects.get(pk=trans_type_id)
#             trans_mode = TransactionMode.objects.get(pk=trans_mode_id)
#             raw_data = BankingRecord.objects.filter(date=datetime(dates[d]['year'], dates[d]['month'], dates[d]['day']),
#                                                     custodian=employee, transaction_type=trans_type, mode=trans_mode)
#         elif (employee_id is not None) and (trans_mode_id is not None):
#             employee = Employee.objects.get(pk=employee_id)
#             trans_mode = TransactionMode.objects.get(pk=trans_mode_id)
#             raw_data = BankingRecord.objects.filter(date=datetime(dates[d]['year'], dates[d]['month'], dates[d]['day']),
#                                                     custodian=employee, mode=trans_mode)
#         elif (employee_id is not None) and (trans_type_id is not None):
#             employee = Employee.objects.get(pk=employee_id)
#             trans_type = TransactionType.objects.get(pk=trans_type_id)
#             raw_data = BankingRecord.objects.filter(date=datetime(dates[d]['year'], dates[d]['month'], dates[d]['day']),
#                                                     custodian=employee, transaction_type=trans_type)
#         elif (trans_type_id is not None) and (trans_mode_id is not None):
#             trans_type = TransactionType.objects.get(pk=trans_type_id)
#             trans_mode = TransactionMode.objects.get(pk=trans_mode_id)
#             raw_data = BankingRecord.objects.filter(date=datetime(dates[d]['year'], dates[d]['month'], dates[d]['day']),
#                                                     transaction_type=trans_type, mode=trans_mode)
#         elif trans_mode_id is not None:
#             trans_mode = TransactionMode.objects.get(pk=trans_mode_id)
#             raw_data = BankingRecord.objects.filter(date=datetime(dates[d]['year'], dates[d]['month'], dates[d]['day']),
#                                                     mode=trans_mode)
#         elif trans_type_id is not None:
#             trans_type = TransactionType.objects.get(pk=trans_type_id)
#             raw_data = BankingRecord.objects.filter(date=datetime(dates[d]['year'], dates[d]['month'], dates[d]['day']),
#                                                     transaction_type=trans_type)
#         elif employee_id is not None:
#             employee = Employee.objects.get(pk=employee_id)
#             raw_data = BankingRecord.objects.filter(date=datetime(dates[d]['year'], dates[d]['month'], dates[d]['day']),
#                                                     custodian=employee)
#         else:
#             raw_data = BankingRecord.objects.filter(date=datetime(dates[d]['year'], dates[d]['month'], dates[d]['day']))
#
#         if flag == "number":
#             for rd in range(len(raw_data)):
#                 amount += 1
#             output = dict(date=dates[d], timestamp=timestamps[d], val=amount)
#             data.append(output)
#         elif flag == "amount":
#             for rd in range(len(raw_data)):
#                 amount += rd.amount
#             output = dict(date=dates[d], timestamp=timestamps[d], val=amount)
#             data.append(output)
#
#         # Get Summary Data
#         for rd in raw_data:
#             summary['total_amount'] += rd.amount
#             employees.add(rd.custodian)
#             summary['count'] += 1
#
#     summary['employees'] += len(employees)
#
#     return data, summary
#
#
# def get_marketing_expense_chart_data(data, flag, dates, timestamps, employee_id):
#     summary = dict(total_amount=0, count=0, employees=0, products=0)
#     employees = set()
#     products = set()
#     raw_data = None
#     for d in range(len(dates)):
#         amount = 0
#         if employee_id is not None:
#             employee = Employee.objects.get(pk=employee_id)
#             raw_data = MarketingExpenseRecord.objects.filter(date=datetime(dates[d]['year'], dates[d]['month'],
#                                                                            dates[d]['day']), custodian=employee)
#         else:
#             raw_data = MarketingExpenseRecord.objects.filter(date=datetime(dates[d]['year'], dates[d]['month'],
#                                                                            dates[d]['day']))
#
#         if flag == "number":
#             for rd in range(len(raw_data)):
#                 amount += 1
#             output = dict(date=dates[d], timestamp=timestamps[d], val=amount)
#             data.append(output)
#         elif flag == "amount":
#             for rd in range(len(raw_data)):
#                 amount += rd.amount
#             output = dict(date=dates[d], timestamp=timestamps[d], val=amount)
#             data.append(output)
#
#         # Get Summary Data
#         for rd in raw_data:
#             summary['total_amount'] += rd.amount
#             employees.add(rd.custodian)
#             products.add(rd.product)
#             summary['count'] += 1
#
#     summary['employees'] += len(employees)
#     summary['products'] += len(products)
#
#     return data, summary
#
#
# def get_production_expense_chart_data(data, flag, dates, timestamps, employee_id):
#     summary = dict(total_amount=0, count=0, employees=0, products=0)
#     employees = set()
#     raw_data = None
#     for d in range(len(dates)):
#         amount = 0
#         if employee_id is not None:
#             employee = Employee.objects.get(pk=employee_id)
#             raw_data = ProductionExpense.objects.filter(date=datetime(dates[d]['year'], dates[d]['month'],
#                                                                       dates[d]['day']), custodian=employee)
#         else:
#             raw_data = ProductionExpense.objects.filter(date=datetime(dates[d]['year'], dates[d]['month'],
#                                                                       dates[d]['day']))
#
#         if flag == "number":
#             for rd in range(len(raw_data)):
#                 amount += 1
#             output = dict(date=dates[d], timestamp=timestamps[d], val=amount)
#             data.append(output)
#         elif flag == "amount":
#             for rd in range(len(raw_data)):
#                 amount += rd.amount
#             output = dict(date=dates[d], timestamp=timestamps[d], val=amount)
#             data.append(output)
#
#         # Get Summary Data
#         for rd in raw_data:
#             summary['total_amount'] += rd.amount
#             employees.add(rd.custodian)
#             summary['count'] += 1
#
#     summary['employees'] += len(employees)
#
#     return data, summary


