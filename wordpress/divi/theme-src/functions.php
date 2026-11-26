<?php
/**
 * BMPC Divi child theme.
 */
if ( ! defined( 'ABSPATH' ) ) { exit; }

define( 'BMPC_VER', '1.1.1' );
define( 'BMPC_DIR', get_stylesheet_directory() );
define( 'BMPC_URI', get_stylesheet_directory_uri() );

require_once BMPC_DIR . '/inc/menu-walker.php';
require_once BMPC_DIR . '/inc/setup.php';

/** Site data (pages, posts, schema) produced by build_theme.py. */
function bmpc_data() {
	static $data = null;
	if ( null === $data ) {
		$raw  = file_get_contents( BMPC_DIR . '/data/site.json' );
		$data = $raw ? json_decode( $raw, true ) : array();
	}
	return $data;
}

/** Styles and scripts. */
add_action( 'wp_enqueue_scripts', function () {
	wp_enqueue_style( 'divi-parent', get_template_directory_uri() . '/style.css', array(), null );
	wp_enqueue_style( 'bmpc-fonts', 'https://fonts.googleapis.com/css2?family=Anek+Bangla:wdth,wght@75..100,400..800&family=Galada&family=Hind+Siliguri:wght@400;500;600&display=swap', array(), null );
	$css = BMPC_DIR . '/assets/css/bmpc.css';
	wp_enqueue_style( 'bmpc', BMPC_URI . '/assets/css/bmpc.css', array( 'divi-parent', 'bmpc-fonts' ), BMPC_VER . '.' . filemtime( $css ) );
	wp_enqueue_script( 'bmpc-motion', BMPC_URI . '/assets/js/motion.js', array(), BMPC_VER . '.' . filemtime( BMPC_DIR . '/assets/js/motion.js' ), true );
	wp_enqueue_script( 'bmpc', BMPC_URI . '/assets/js/bmpc.js', array(), BMPC_VER . '.' . filemtime( BMPC_DIR . '/assets/js/bmpc.js' ), true );
}, 20 );

add_action( 'wp_head', function () {
	echo '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>' . "\n";
	echo '<meta name="theme-color" content="#073D2A">' . "\n";
}, 1 );

/** Body classes used to scope each page's styles. */
add_filter( 'body_class', function ( $classes ) {
	$classes[] = 'bmpc';
	if ( is_front_page() ) {
		$classes[] = 'bmpc-page-home';
	} elseif ( is_page() ) {
		$classes[] = 'bmpc-page-' . sanitize_html_class( get_post_field( 'post_name', get_queried_object_id() ) );
	}
	return $classes;
} );

/** Site icon fallback when none is set in Customizer. */
add_action( 'wp_head', function () {
	if ( has_site_icon() ) { return; }
	echo '<link rel="icon" href="' . esc_url( BMPC_URI . '/assets/img/icon-32.png' ) . '" sizes="32x32" type="image/png">' . "\n";
	echo '<link rel="apple-touch-icon" href="' . esc_url( BMPC_URI . '/assets/img/icon-180.png' ) . '">' . "\n";
}, 2 );

/** Person schema on the two message pages (Rank Math free doesn't create it). */
add_action( 'wp_head', function () {
	if ( ! is_page() ) { return; }
	$slug   = get_post_field( 'post_name', get_queried_object_id() );
	$people = bmpc_data()['people'] ?? array();
	if ( empty( $people[ $slug ] ) ) { return; }
	$person          = $people[ $slug ];
	$person['@context'] = 'https://schema.org';
	$person['url']   = get_permalink();
	$photo           = bmpc_media_url( $slug === 'chairman-message' ? 'chairman.jpg' : 'secretary.jpg' );
	$person['image'] = $photo;
	$person['worksFor'] = array( '@type' => 'NGO', 'name' => 'বাংলাদেশ মুক্তিযোদ্ধা প্রজন্ম কাউন্সিল', 'url' => home_url( '/' ) );
	echo '<script type="application/ld+json">' . wp_json_encode( $person, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES ) . '</script>' . "\n";
}, 30 );

/** Image URL: Media Library copy if imported, otherwise the theme file. */
function bmpc_media_url( $file ) {
	$map = get_option( 'bmpc_media', array() );
	if ( ! empty( $map[ $file ] ) ) {
		$url = wp_get_attachment_url( (int) $map[ $file ] );
		if ( $url ) { return $url; }
	}
	return BMPC_URI . '/assets/img/' . $file;
}

/** Bangla date, e.g. ৩০ অক্টোবর ২০২৬. */
function bmpc_bn_date( $timestamp = null ) {
	$timestamp = $timestamp ? $timestamp : get_post_time( 'U' );
	$months = array( 'জানুয়ারি', 'ফেব্রুয়ারি', 'মার্চ', 'এপ্রিল', 'মে', 'জুন', 'জুলাই', 'আগস্ট', 'সেপ্টেম্বর', 'অক্টোবর', 'নভেম্বর', 'ডিসেম্বর' );
	$d = wp_date( 'j', $timestamp ); $m = (int) wp_date( 'n', $timestamp ); $y = wp_date( 'Y', $timestamp );
	return bmpc_bn_num( $d ) . ' ' . $months[ $m - 1 ] . ' ' . bmpc_bn_num( $y );
}
function bmpc_bn_num( $s ) {
	return strtr( (string) $s, array( '0' => '০', '1' => '১', '2' => '২', '3' => '৩', '4' => '৪', '5' => '৫', '6' => '৬', '7' => '৭', '8' => '৮', '9' => '৯' ) );
}

/** URL of a page by slug, falling back to /slug/. */
function bmpc_page_url( $slug ) {
	$p = get_page_by_path( $slug );
	return $p ? get_permalink( $p ) : home_url( '/' . $slug . '/' );
}

/** [bmpc_latest_news] – newest post card for the homepage. */
add_shortcode( 'bmpc_latest_news', function () {
	$q = new WP_Query( array( 'posts_per_page' => 1, 'ignore_sticky_posts' => true, 'no_found_rows' => true ) );
	if ( ! $q->have_posts() ) { return ''; }
	ob_start();
	while ( $q->have_posts() ) {
		$q->the_post();
		$place   = get_post_meta( get_the_ID(), 'bmpc_place', true );
		$summary = get_post_meta( get_the_ID(), 'bmpc_summary', true );
		$summary = $summary ? $summary : wp_trim_words( get_the_excerpt(), 30, '…' );
		?>
		<a class="nstory" href="<?php the_permalink(); ?>">
			<?php if ( has_post_thumbnail() ) { the_post_thumbnail( 'large', array( 'loading' => 'lazy' ) ); } ?>
			<div><span class="ndate"><?php echo esc_html( bmpc_bn_date() . ( $place ? ' · ' . $place : '' ) ); ?></span>
			<h3><?php the_title(); ?></h3><p><?php echo esc_html( $summary ); ?></p></div>
		</a>
		<?php
	}
	wp_reset_postdata();
	return ob_get_clean();
} );

/** Social links (set in Appearance → BMPC Setup). */
function bmpc_social() {
	return wp_parse_args( get_option( 'bmpc_social', array() ), array( 'facebook' => '', 'x' => '', 'instagram' => '', 'youtube' => 'https://www.youtube.com/channel/UC3pXvRvIoVYgEGwdkNx3Gfw' ) );
}

/** Keep the WordPress admin bar from covering the sticky header. */
add_action( 'wp_head', function () {
	if ( is_admin_bar_showing() ) {
		echo '<style>.top{top:32px}@media(max-width:782px){.top{top:46px}}</style>';
	}
}, 40 );
