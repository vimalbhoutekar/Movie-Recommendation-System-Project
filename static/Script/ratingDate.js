function formatRating(rating) {
    return parseFloat(rating).toFixed(1);
}

document.addEventListener('DOMContentLoaded', function() {
    const ratingElements = document.querySelectorAll('.rating span:last-child');
    ratingElements.forEach(function(element) {
        const ratingText = element.textContent;
        const rating = parseFloat(ratingText);
        if (!isNaN(rating)) {
            element.textContent = formatRating(rating) + '/10';
        }
    });
});

function formatDate(dateString) {
    const options = { day: 'numeric', month: 'long', year: 'numeric' };
    return new Date(dateString).toLocaleDateString('en-US', options);
}

document.addEventListener('DOMContentLoaded', function() {
    const releaseDates = document.querySelectorAll('.release-date');
    releaseDates.forEach(function(element) {
        const originalDate = element.getAttribute('data-date');
        element.textContent = formatDate(originalDate);
    });
});
