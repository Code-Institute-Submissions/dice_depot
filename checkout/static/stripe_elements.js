let stripePublicKey = $("#id_stripe_public_key").text().slice(1, -1);
let clientSecret = $("#id_client_secret").text().slice(1, -1);
let stripe = Stripe(stripePublicKey);
let elements = stripe.elements();
let card = elements.create('card');
card.mount('#card-element');

// Event listener for card errors

card.addEventListener('change', function(event) {
    let paymentError = document.getElementById('payment-failed');
    if (event.error) {
        let html =`
            <span class="icon" role="alert">
                <i class="fas fa-times"></i>
            </span>
            <span>${event.error.message}</span>
        `
        $(paymentError).html(html);
    } else {
        paymentError.textContent = '';
    }
});

// Handle realtime validation errors on the card element
card.addEventListener('change', function (event) {
    let errorDiv = document.getElementById('card-errors');
    if (event.error) {
        let html = `
            <span class="icon" role="alert">
                <i class="fas fa-times"></i>
            </span>
            <span>${event.error.message}</span>
        `;
        $(errorDiv).html(html);
    } else {
        errorDiv.textContent = '';
    }
});

// Stripe Form Submit
let form = document.getElementById('payment-form');

form.addEventListener('submit', function(ev) {
ev.preventDefault();
    card.update({ 'disabled': true});
    $('#submit-button').attr('disabled', true);
    stripe.confirmCardPayment(clientSecret, {
        payment_method: {
            card: card,
        }
    }).then(function(result) {
        if (result.error) {
            let errorDiv = document.getElementById('card-errors');
            var html = `
            <span class="icon" role="alert">
                <i class="fas fa-times"></i>
            </span>
            <span>${result.error.message}</span>
        `;
        $(errorDiv).html(html);
        card.update({ 'disabled': false});
        $('#submit-button').attr('disabled', true);
        } else {
            if (result.paymentIntent.status === 'succeeded') {
                form.submit();
            }
        }
    };