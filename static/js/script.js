document.addEventListener('DOMContentLoaded', () => {
    // Format and display the event date
    const eventDateElement = document.getElementById('eventDate');
    const eventDate = dayjs('2023-07-15').format('MMMM D, YYYY');
    eventDateElement.textContent = eventDate;

    // Form submission and validation
    const form = document.getElementById('registrationForm');
    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        const fullName = document.getElementById('fullName').value.trim();
        const email = document.getElementById('email').value.trim();

        // Validate form inputs
        if (!fullName || !email) {
            showMessage('Please fill in all fields.', 'error');
            return;
        }

        if (!validator.isEmail(email)) {
            showMessage('Please enter a valid email address.', 'error');
            return;
        }

        try {
            const response = await fetch('/register', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ fullName, email }),
            });

            const data = await response.json();

            if (data.success) {
                showMessage(data.message, 'success');
                form.reset();
            } else {
                showMessage(data.message, 'error');
            }
        } catch (error) {
            showMessage('An error occurred. Please try again later.', 'error');
        }
    });

    function showMessage(message, type) {
        const messageElement = document.createElement('div');
        messageElement.textContent = message;
        messageElement.className = type === 'success' ? 'success-message' : 'error-message';

        const existingMessage = form.nextElementSibling;
        if (existingMessage && (existingMessage.classList.contains('success-message') || existingMessage.classList.contains('error-message'))) {
            existingMessage.remove();
        }

        form.insertAdjacentElement('afterend', messageElement);

        setTimeout(() => {
            messageElement.remove();
        }, 5000);
    }
});
