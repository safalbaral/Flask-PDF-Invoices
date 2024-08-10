import logging
from flask import render_template, flash

# Third party libraries imports
from weasyprint import HTML, CSS
from billing_system import bcrypt

# Inbuilt python modules import
from datetime import date
from base64 import b64encode

from weasyprint import HTML, CSS

# Import of various custom defined forms that are to be passed to the frontend
from billing_system.forms import ProcessCheckOutForm

# Imports from __init__.py
from billing_system import app

from io import BytesIO


@app.route('/', methods=('GET', 'POST'))
def process_check_out(filled_in_form=None):
    form = ProcessCheckOutForm()

    if filled_in_form is None:
        if form.validate_on_submit():
            generated_invoice = generate_invoice(form)
            print(f'Generated INCOIDE: {generated_invoice}')
            return render_template('billing/completed_check_out_process.html',
                            invoice=generated_invoice
                            )
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    flash(u"Error in the %s field - %s" % (
                        getattr(form, field).label.text,
                        error
                    ), 'warning')
            return render_template('billing/process_check_out.html',
                                form=form,
                                )
    else:
        print(f'FORM EDIT DETECTED!!!\n {filled_in_form.additional_items}')
        return render_template('billing/process_check_out.html',
                            form=filled_in_form,
                            )

def generate_invoice(form):
    VAT_PERCENT = 13
    SERVICE_CHARGE_PERCENT = 10
    CURRENT_DATE = date.today().strftime('%B %d, %Y')
    GUEST_NAME = form.guest_name.data
    INVOICE_ID = form.invoice_id.data
    DISCOUNT_PERCENT = form.discount_percent.data;

    TOTAL=tabulate_total_from_form(form)

    TOTAL_AFTER_DISCOUNT = apply_discount_to_total(TOTAL, DISCOUNT_PERCENT) 
    TOTAL_AFTER_SERVICE_CHARGE = apply_service_charge_to_total(TOTAL_AFTER_DISCOUNT, SERVICE_CHARGE_PERCENT)
    TOTAL_AFTER_VAT = apply_vat_to_total(TOTAL_AFTER_SERVICE_CHARGE, VAT_PERCENT)

    logger = logging.getLogger('weasyprint')
    logger.addHandler(logging.FileHandler('./weasyprint.log'))

    rendered_html=render_template('billing/invoice.html',
                                    GUEST_NAME = GUEST_NAME,
                                    INVOICE_ID = INVOICE_ID,
                                    VAT_PERCENT = VAT_PERCENT,
                                    SERVICE_CHARGE_PERCENT = SERVICE_CHARGE_PERCENT,
                                    DISCOUNT_PERCENT = DISCOUNT_PERCENT,
                                    TOTAL = TOTAL,
                                    TOTAL_AFTER_SERVICE_CHARGE = TOTAL_AFTER_SERVICE_CHARGE,
                                    TOTAL_AFTER_DISCOUNT = TOTAL_AFTER_DISCOUNT,
                                    TOTAL_AFTER_VAT = TOTAL_AFTER_VAT,
                                    CURRENT_DATE = CURRENT_DATE,
                                    form = form,
                                    )

    invoice_html=HTML(string = rendered_html)
    invoice_css=CSS(filename='./billing_system/static/invoice.css')

    invoice = invoice_html.write_pdf(stylesheets = [invoice_css])
    invoice = BytesIO(invoice).read()
    invoice = b64encode(invoice).decode('ascii')

    return invoice

def apply_discount_to_total(total, discount_percent):
    total_after_discount=total - ((discount_percent/100) * total)
    total_after_discount=round(total_after_discount, 2)

    print(f'TOTAL AFTER discount {total_after_discount}')

    return total_after_discount


def apply_vat_to_total(total, vat_percent):
    total_after_vat=(total + \
                        (vat_percent/100)*total)
    total_after_vat=round(total_after_vat, 2)

    print(f'TOTAL AFTER vat added {total_after_vat}')

    return total_after_vat

def apply_service_charge_to_total(total, service_charge_percent):
    total_after_service_charge=(total + \
                        (service_charge_percent/100)*total)
    total_after_service_charge=round(total_after_service_charge, 2)
    return total_after_service_charge

def tabulate_total_from_form(form):
    total=0;
    for item in form.additional_items:
        total += item.price.data * item.quantity.data

    print(f'TOTAL AFTER form added {total}')
    return total

