<?php
/** Menu markup for the BMPC header: desktop dropdowns and a flat mobile list. */
if ( ! defined( 'ABSPATH' ) ) { exit; }

/** Fallback menu when no menu is assigned to the Primary Menu location yet. */
function bmpc_fallback_menu() {
	$items = array(
		home_url( '/' )                          => 'হোম',
		bmpc_page_url( 'about' )                 => 'আমাদের সম্পর্কে',
		bmpc_page_url( 'manifesto' )             => 'ঘোষণাপত্র',
		bmpc_page_url( 'objectives' )            => 'লক্ষ্য ও উদ্দেশ্য',
		bmpc_page_url( 'chairman-message' )      => 'চেয়ারম্যানের বাণী',
		bmpc_page_url( 'news' )                  => 'সর্বশেষ সংবাদ',
	);
	echo '<ul class="bmpc-menu">';
	foreach ( $items as $url => $label ) {
		echo '<li class="menu-item"><a href="' . esc_url( $url ) . '">' . esc_html( $label ) . '</a></li>';
	}
	echo '</ul>';
}

/** Mark the open dropdown parent for keyboard and screen-reader users. */
add_filter( 'nav_menu_link_attributes', function ( $atts, $item, $args ) {
	if ( isset( $args->theme_location ) && 'primary-menu' === $args->theme_location && in_array( 'menu-item-has-children', (array) $item->classes, true ) ) {
		$atts['aria-haspopup'] = 'true';
	}
	if ( in_array( 'current-menu-item', (array) $item->classes, true ) ) {
		$atts['aria-current'] = 'page';
	}
	return $atts;
}, 10, 3 );
