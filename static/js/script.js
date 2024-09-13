document.addEventListener('DOMContentLoaded', () => {
    // 이벤트 날짜 포맷 및 표시
    const eventDateElement = document.getElementById('eventDate');
    const eventDate = dayjs('2024-09-30');
    eventDateElement.textContent = eventDate.format('YYYY년 M월 D일');

    // 카운트다운 타이머
    const countdownElement = document.getElementById('countdown');
    
    function updateCountdown() {
        const now = dayjs();
        const duration = eventDate.diff(now);
        
        if (duration > 0) {
            const days = Math.floor(duration / (1000 * 60 * 60 * 24));
            const hours = Math.floor((duration % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
            const minutes = Math.floor((duration % (1000 * 60 * 60)) / (1000 * 60));
            const seconds = Math.floor((duration % (1000 * 60)) / 1000);
            
            countdownElement.textContent = `${days}일 ${hours}시간 ${minutes}분 ${seconds}초`;
        } else {
            countdownElement.textContent = "이벤트가 시작되었습니다!";
        }
    }

    // 1초마다 카운트다운 업데이트
    updateCountdown();
    setInterval(updateCountdown, 1000);

    // 소셜 미디어 공유 기능
    const twitterShareBtn = document.getElementById('twitter-share');
    const facebookShareBtn = document.getElementById('facebook-share');
    const linkedinShareBtn = document.getElementById('linkedin-share');

    const eventTitle = "테크 혁신가 모임";
    const eventUrl = window.location.href;

    twitterShareBtn.href = `https://twitter.com/intent/tweet?text=${encodeURIComponent(eventTitle)}&url=${encodeURIComponent(eventUrl)}`;
    facebookShareBtn.href = `https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent(eventUrl)}`;
    linkedinShareBtn.href = `https://www.linkedin.com/shareArticle?mini=true&url=${encodeURIComponent(eventUrl)}&title=${encodeURIComponent(eventTitle)}`;

    // 폼 제출 및 유효성 검사
    const form = document.getElementById('registrationForm');
    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        const fullName = document.getElementById('fullName').value.trim();
        const email = document.getElementById('email').value.trim();

        // 입력 유효성 검사
        if (!fullName || !email) {
            showMessage('모든 필드를 입력해주세요.', 'error');
            return;
        }

        if (!validator.isEmail(email)) {
            showMessage('유효한 이메일 주소를 입력해주세요.', 'error');
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
            showMessage('오류가 발생했습니다. 나중에 다시 시도해주세요.', 'error');
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
