function getCookie(name) {
	let matches = document.cookie.match(new RegExp(
	  "(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)"
	));
	return matches ? decodeURIComponent(matches[1]) : undefined;
}

function setCookie(name, value) {
    options = {
      	path: '/',
      	secure: false,
		'max-age': 2678400
    };
  
    if (options.expires instanceof Date) {
      	options.expires = options.expires.toUTCString();
    }
  
    let updatedCookie = encodeURIComponent(name) + "=" + value;
  
    for (let optionKey in options) {
		updatedCookie += "; " + optionKey;
		let optionValue = options[optionKey];
		if (optionValue !== true) {
				updatedCookie += "=" + optionValue;
		}
    }
    document.cookie = updatedCookie;
}

$('.add-to-wishlist').on('click', function() {
	const $this = $(this);
	$this.attr('disabled', true);
	const id = $this.attr('data-id');
	if (!id) return false;
	
	const wishlist = getCookie('wishlist') || false;
	if (!wishlist) {
		setCookie('wishlist', id);
		$this.addClass('added');
	}
	if (wishlist) {
		let wishlistArray = wishlist.split(',');
		if (wishlistArray.includes(id)) {
			wishlistArray = wishlistArray.filter(pk => pk != id);
			$this.removeClass('added');
		} else {
			wishlistArray.push(id);
			$this.addClass('added');
		}
		setCookie('wishlist', wishlistArray.join(','));
	}
	$this.attr('disabled', false);
});


$('.show-more-attributes__btn').on('click', function() {
	$(this).closest('tr').remove();
	$('.show-more-attributes ~ tr').animate({ height: 'toggle' }, 0, function() {
        $(this).css('display', 'table-row');
    });
});
