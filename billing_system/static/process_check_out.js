document.addEventListener('DOMContentLoaded', (event) => {
    updateTotal()
    // On input event to the discount percentage field, it calculates and updates the total
    document.querySelector('#discount_percent').addEventListener('input', (event) => {
        updateTotal()
    })

    main_element = document.querySelector('main')
    main_element.classList.add('custom-card')

    // On input event to any of the input fields in the additional costs table, it calculates and updates the total
    document.querySelectorAll(`[id^="additional_items-"]`).forEach(item => {
        item.addEventListener('input', (event) => {
            updateTotal()
        })
    })

}
);

function updateTotal() {
    // var room_cost = document.querySelector('#room_cost').innerHTML
    // room_cost = parseInt(room_cost.replace(/^\w\w.\s/, ''))
    var totalling_table = document.querySelector('#totalling_table');
    // var total_amount = room_cost;
    var total_amount = 0;

    for (var i = 1; i < totalling_table.rows.length; i++) {
        var row = totalling_table.rows[i]
        var col = row.cells

        // children[0] is the input element inside of the td tag
        total_amount += col[2].children[0].value * col[3].children[0].value
    }

    var discount_percent = document.querySelector('#discount_percent').value

    total_amount = applyServiceChargeToTotal(total_amount)

    if (typeof (total_amount) !== 'number') {
        total_amount = 'Error: Discount percent has to be a number.'
    } else if (discount_percent > 100) {
        total_amount = 'Error: Discount cannot exceed 100%.'
    } else if (discount_percent < 0) {
        total_amount = 'Error: Discount cannot be less than 0%.'
    } else if (discount_percent !== '') {
        total_amount = applyDiscountToTotal(total_amount, discount_percent)
    }

    total_amount = applyVATToTotal(total_amount)
    // Line below makes sure that the total doesn't exceed two decimal places
    total_amount = total_amount.toFixed(2)

    var grand_total = document.querySelector('#grand_total')
    grand_total.innerHTML = `Rs.${total_amount}`
}

function applyServiceChargeToTotal(total) {
    const service_charge_percent = 10;
    total = total + ((service_charge_percent / 100) * total)
    return total
}

function applyVATToTotal(total) {
    const vat_percent = 13;
    total = total + ((vat_percent / 100) * total)
    return total
}

function applyDiscountToTotal(total, discount_percent) {
    total = total - ((discount_percent / 100) * total)
    return total
}

function updateTotalWithMessage(message) {
    var grand_total = document.querySelector('#grand_total')
    grand_total.innerHTML = message
}