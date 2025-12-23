document.addEventListener('click', function (e) {
    const btn = e.target.closest('.js-action')
    if (!btn) return

    const action = btn.dataset.action

    switch (action) {
        case 'like': {
            const likeBtn = btn
            const dislikeBtn = likeBtn.parentNode.querySelector('.js-dislike-btn')
            handleReaction(likeBtn, dislikeBtn, 'like')
            break
        }
        case 'dislike': {
            const dislikeBtn = btn
            const likeBtn = dislikeBtn.parentNode.querySelector('.js-like-btn')
            handleReaction(likeBtn, dislikeBtn, 'dislike')
            break
        }
        case 'verify': {
            handleVerify(btn)
            break
        }
        default: {
            console.log('default')
        }
    }
})

function handleReaction(likeBtn, dislikeBtn, reactionType) {
    const questionId = likeBtn.dataset.questionId

    fetch(`/question/${questionId}/${reactionType}`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrftoken,
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
        .then((response) => {
            if (response.redirected) {
                window.location.href = '/login'
            }
            return response.json()
        })
        .then((data) => {
            likeBtn.querySelector('.js-like-count').textContent = data.likes_count
            dislikeBtn.querySelector('.js-dislike-count').textContent = data.dislikes_count

            if (reactionType === 'like') {
                if (data.liked) {
                    likeBtn.classList.add('active')
                    dislikeBtn.classList.remove('active')
                } else {
                    likeBtn.classList.remove('active')
                }
            } else if (reactionType === 'dislike') {
                if (data.disliked) {
                    dislikeBtn.classList.add('active')
                    likeBtn.classList.remove('active')
                } else {
                    dislikeBtn.classList.remove('active')
                }
            }
        })
        .catch((err) => console.error(err))
}

function handleVerify(btn) {
    const answerId = btn.dataset.answerId
    const card = btn.closest('.answer-card')
    const badge = card.querySelector('.badge')

    fetch(`/answer/${answerId}/verify`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrftoken,
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
        .then((response) => {
            if (response.redirected) {
                window.location.href = '/login'
                return
            }
            return response.json()
        })
        .then((data) => {
            if (data.verified) {
                btn.classList.add('active')
                badge.classList.remove('d-none')
            } else {
                btn.classList.remove('active')
                badge.classList.add('d-none')
            }
        })
        .catch((err) => console.error(err))
}