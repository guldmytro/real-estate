(function() {
    // intersection observer
    let options = {
        root: null,
        rootMargin: '0px',
        threshold: 0.2
    }

    let targets = document.querySelectorAll('.object-item');

    if (!targets.length) {
        return null;
    }

    let observer = new IntersectionObserver(intersectionCallback, options);
    targets.forEach(target => {
        observer.observe(target);
    });

    function intersectionCallback(entries, observer) {
        entries.map((entry) => {
            if (entry.isIntersecting) {
                try {
                    const link = entry.target.querySelector('.object-item__thumb');
                    fetch(link.getAttribute('href'), {method: 'GET'});
                } catch(e) {
                    console.warn(e);
                }
                observer.unobserve(entry.target);
            }
        });
    }
})();